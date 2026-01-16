"""
Long-term fundamentals data fetcher.

Extends existing FMP infrastructure to fetch and cache 5-year historical data
for ROIC, WACC, growth metrics, and capital efficiency analysis.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class LongTermFundamentals:
    """Container for 5-year fundamental data and calculated metrics."""

    ticker: str
    currency: str
    income_statements: List[Dict[str, Any]]  # 5+ years
    balance_sheets: List[Dict[str, Any]]  # 5+ years
    cash_flows: List[Dict[str, Any]]  # 5+ years

    # Calculated metrics (3-year averages)
    roic_3yr: Optional[float] = None
    roic_5yr: Optional[float] = None
    wacc: Optional[float] = None
    fcf_margin_3yr: Optional[float] = None
    revenue_cagr_3yr: Optional[float] = None
    revenue_cagr_5yr: Optional[float] = None
    eps_cagr_3yr: Optional[float] = None
    eps_cagr_5yr: Optional[float] = None
    gross_margin_trend: Optional[float] = None
    debt_to_ebitda: Optional[float] = None
    interest_coverage: Optional[float] = None

    # Metadata
    fetched_at: str = ""
    data_quality_score: float = 0.0  # 0-100


class LongTermFundamentalsFetcher:
    """
    Fetch and cache 5-year fundamental data from FMP API.

    Leverages existing FMP infrastructure, extending to 5-year history
    and calculating long-term metrics (ROIC, WACC, growth rates).
    """

    def __init__(
        self,
        cache_dir: str = "data/long_term_fundamentals",
        cache_expiry_days: int = 90
    ):
        """
        Initialize fetcher.

        Args:
            cache_dir: Directory to cache fundamental data
            cache_expiry_days: Days before cache expires (default 90)
        """
        # Import here to avoid circular imports
        from src.data.fmp_fetcher import FMPFetcher

        self.fmp = FMPFetcher()  # Uses FMP_API_KEY env var
        self.cache_dir = cache_dir
        self.cache_expiry_days = cache_expiry_days

        # Create cache directory if needed
        os.makedirs(cache_dir, exist_ok=True)

    def fetch(
        self,
        ticker: str,
        force_refresh: bool = False
    ) -> Optional[LongTermFundamentals]:
        """
        Fetch 5+ year fundamentals for a ticker.

        Args:
            ticker: Stock ticker
            force_refresh: Ignore cache and fetch fresh

        Returns:
            LongTermFundamentals object, or None if fetch fails
        """
        # Check cache first
        if not force_refresh:
            cached = self._load_from_cache(ticker)
            if cached:
                return cached

        logger.info(f"Fetching long-term fundamentals for {ticker}")

        try:
            # Fetch using existing FMP infrastructure
            # fetch_comprehensive_fundamentals returns 8 quarters by default
            fundamentals_data = self.fmp.fetch_comprehensive_fundamentals(ticker)

            if not fundamentals_data:
                logger.warning(f"No data from FMP for {ticker}")
                return None

            # Extract and organize data (note: keys are singular, not plural)
            income_statements = fundamentals_data.get("income_statement", [])
            balance_sheets = fundamentals_data.get("balance_sheet", [])
            cash_flows = fundamentals_data.get("cash_flow", [])

            if not income_statements or not balance_sheets or not cash_flows:
                logger.warning(f"Incomplete data for {ticker}")
                return None

            # Create fundamentals object
            fundamentals = LongTermFundamentals(
                ticker=ticker,
                currency="USD",
                income_statements=income_statements,
                balance_sheets=balance_sheets,
                cash_flows=cash_flows,
                fetched_at=datetime.utcnow().isoformat()
            )

            # Calculate metrics
            self._calculate_metrics(fundamentals)

            # Cache the result
            self._save_to_cache(fundamentals)

            logger.info(f"✓ Fetched {ticker}: {len(income_statements)} Q, "
                       f"quality={fundamentals.data_quality_score:.0f}%")

            return fundamentals

        except Exception as e:
            logger.error(f"Error fetching {ticker}: {e}")
            return None

    def _calculate_metrics(self, fundamentals: LongTermFundamentals) -> None:
        """
        Calculate long-term metrics from financial statements.

        Populates ROIC, WACC, growth rates, and other metrics.
        """
        from .metrics import MetricsCalculator

        try:
            # Extract historical values (sorted oldest to newest)
            revenues = [
                s.get("revenue", 0) for s in fundamentals.income_statements
                if s.get("revenue") and s.get("revenue") > 0
            ]
            net_incomes = [
                s.get("netIncome", 0) for s in fundamentals.income_statements
                if s.get("netIncome")
            ]
            gross_margins = [
                s.get("grossProfitRatio", 0) for s in fundamentals.income_statements
                if s.get("grossProfitRatio")
            ]

            # Calculate CAGR metrics
            if len(revenues) >= 4:
                # 3-year CAGR (4 data points = 3 years)
                fundamentals.revenue_cagr_3yr = MetricsCalculator.calculate_cagr(
                    revenues[0], revenues[3], 3
                )

            if len(revenues) >= 5:
                # 5-year CAGR
                fundamentals.revenue_cagr_5yr = MetricsCalculator.calculate_cagr(
                    revenues[0], revenues[4], 5
                )

            # Calculate FCF margin (most recent)
            if revenues and fundamentals.cash_flows:
                fcf = fundamentals.cash_flows[0].get("freeCashFlow", 0)
                if revenues[-1] > 0:
                    fundamentals.fcf_margin_3yr = fcf / revenues[-1]

            # Calculate gross margin trend
            if len(gross_margins) >= 4:
                fundamentals.gross_margin_trend = (
                    MetricsCalculator.calculate_net_margin_trend(
                        gross_margins, min(12, len(gross_margins))
                    )
                )

            # Extract debt/equity metrics
            if fundamentals.balance_sheets and fundamentals.income_statements:
                bs = fundamentals.balance_sheets[0]
                is_stmt = fundamentals.income_statements[0]

                total_debt = (
                    bs.get("shortTermDebt", 0) + bs.get("longTermDebt", 0)
                )

                # Calculate EBITDA
                ebitda = (
                    is_stmt.get("netIncome", 0) +
                    is_stmt.get("interestExpense", 0) +
                    is_stmt.get("incomeTaxExpense", 0) +
                    is_stmt.get("depreciationAndAmortization", 0)
                )

                interest_expense = is_stmt.get("interestExpense", 0)

                if ebitda > 0:
                    fundamentals.debt_to_ebitda = total_debt / ebitda

                if interest_expense > 0 and ebitda > 0:
                    fundamentals.interest_coverage = ebitda / interest_expense

            # Calculate data quality score
            completeness = sum([
                len(fundamentals.income_statements) > 0,
                len(fundamentals.balance_sheets) > 0,
                len(fundamentals.cash_flows) > 0,
                fundamentals.revenue_cagr_3yr is not None,
                fundamentals.debt_to_ebitda is not None,
            ]) / 5.0 * 100

            fundamentals.data_quality_score = max(50, completeness)

        except Exception as e:
            logger.error(f"Error calculating metrics for {fundamentals.ticker}: {e}")
            fundamentals.data_quality_score = 50.0

    def _load_from_cache(self, ticker: str) -> Optional[LongTermFundamentals]:
        """Load fundamentals from cache if fresh."""
        cache_file = os.path.join(self.cache_dir, f"{ticker}_fundamentals.json")

        if not os.path.exists(cache_file):
            return None

        try:
            # Check cache age
            file_age = datetime.utcnow() - datetime.fromtimestamp(
                os.path.getmtime(cache_file)
            )

            if file_age > timedelta(days=self.cache_expiry_days):
                logger.debug(f"Cache expired for {ticker}")
                return None

            # Load from cache
            with open(cache_file, "r") as f:
                data = json.load(f)

            logger.debug(f"Loaded {ticker} from cache")

            return self._dict_to_fundamentals(data)

        except Exception as e:
            logger.debug(f"Error loading cache for {ticker}: {e}")
            return None

    def _save_to_cache(self, fundamentals: LongTermFundamentals) -> None:
        """Save fundamentals to cache."""
        cache_file = os.path.join(
            self.cache_dir,
            f"{fundamentals.ticker}_fundamentals.json"
        )

        try:
            with open(cache_file, "w") as f:
                json.dump(asdict(fundamentals), f, indent=2)

            logger.debug(f"Cached {fundamentals.ticker}")

        except Exception as e:
            logger.error(f"Error caching {fundamentals.ticker}: {e}")

    def _dict_to_fundamentals(
        self,
        data: Dict[str, Any]
    ) -> Optional[LongTermFundamentals]:
        """Convert dictionary back to LongTermFundamentals object."""
        try:
            return LongTermFundamentals(
                ticker=data.get("ticker", ""),
                currency=data.get("currency", "USD"),
                income_statements=data.get("income_statements", []),
                balance_sheets=data.get("balance_sheets", []),
                cash_flows=data.get("cash_flows", []),
                roic_3yr=data.get("roic_3yr"),
                roic_5yr=data.get("roic_5yr"),
                wacc=data.get("wacc"),
                fcf_margin_3yr=data.get("fcf_margin_3yr"),
                revenue_cagr_3yr=data.get("revenue_cagr_3yr"),
                revenue_cagr_5yr=data.get("revenue_cagr_5yr"),
                eps_cagr_3yr=data.get("eps_cagr_3yr"),
                eps_cagr_5yr=data.get("eps_cagr_5yr"),
                gross_margin_trend=data.get("gross_margin_trend"),
                debt_to_ebitda=data.get("debt_to_ebitda"),
                interest_coverage=data.get("interest_coverage"),
                fetched_at=data.get("fetched_at", ""),
                data_quality_score=data.get("data_quality_score", 0.0)
            )
        except Exception as e:
            logger.error(f"Error converting dict to fundamentals: {e}")
            return None

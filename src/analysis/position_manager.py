#!/usr/bin/env python3
"""Position management and stop loss recommendations.

Analyzes current Robinhood positions and recommends:
- When to move stop loss up (trail stops)
- New stop loss levels with rationale
- When to take partial profits
- Exit target adjustments

Only provides recommendations for SHORT-TERM positions (held <1 year).
Long-term positions (held 1+ years) are excluded to preserve favorable tax treatment.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

from src.screening.phase_classifier import classify_phase
from src.screening.signal_engine import calculate_stop_loss

logger = logging.getLogger(__name__)


class PositionManager:
    """Analyze positions and recommend stop loss adjustments."""

    def __init__(self):
        """Initialize position manager."""
        pass

    def analyze_position(
        self,
        ticker: str,
        entry_price: float,
        current_price: float,
        entry_date: Optional[datetime] = None
    ) -> Dict:
        """Analyze a single position and recommend stop management.

        Args:
            ticker: Stock symbol
            entry_price: Your average entry price
            current_price: Current market price
            entry_date: When you entered (optional, for tax treatment check)

        Returns:
            Dict with recommendations:
            - should_adjust_stop: bool
            - recommended_stop: float (new stop level)
            - current_gain_pct: float
            - rationale: str (why adjust)
            - action: str (trail_to_breakeven, trail_to_profit, take_partial, hold)
            - tax_treatment: str (short_term or long_term)
        """
        result = {
            'ticker': ticker,
            'entry_price': entry_price,
            'current_price': current_price,
            'should_adjust_stop': False,
            'recommended_stop': None,
            'current_gain_pct': 0,
            'rationale': '',
            'action': 'hold',
            'tax_treatment': 'unknown',
            'warnings': []
        }

        # Calculate current gain
        gain_pct = ((current_price - entry_price) / entry_price) * 100
        result['current_gain_pct'] = round(gain_pct, 2)

        # Check tax treatment
        if entry_date:
            days_held = (datetime.now() - entry_date).days
            if days_held >= 365:
                result['tax_treatment'] = 'long_term'
                result['rationale'] = f"LONG-TERM HOLD ({days_held} days) - Preserve long-term capital gains tax rate. No stop adjustment recommended."
                return result
            else:
                result['tax_treatment'] = 'short_term'
                result['days_held'] = days_held

        # Fetch price data and analyze
        try:
            stock = yf.Ticker(ticker)
            price_data = stock.history(period='1y', interval='1d')

            if price_data.empty or len(price_data) < 50:
                result['warnings'].append('Insufficient price data for analysis')
                return result

            # Calculate phase and technical levels
            phase_info = classify_phase(price_data, current_price)
            phase = phase_info['phase']

            sma_50 = phase_info.get('sma_50', 0)
            sma_200 = phase_info.get('sma_200', 0)

            # Recent swing low (last 10 days)
            recent_low = price_data['Low'].iloc[-10:].min()

            result['phase'] = phase
            result['sma_50'] = round(sma_50, 2)
            result['recent_low'] = round(recent_low, 2)

            # STOP LOSS ADJUSTMENT LOGIC
            # Based on gain and technical structure

            if gain_pct < 5:
                # Small gain - don't adjust yet
                result['action'] = 'hold'
                result['rationale'] = f"Position up {gain_pct:.1f}% - hold initial stop. Wait for 5-10% gain before adjusting."

            elif gain_pct >= 5 and gain_pct < 10:
                # 5-10% gain - Move to breakeven
                result['should_adjust_stop'] = True
                result['action'] = 'trail_to_breakeven'

                # Stop just below breakeven (entry - 0.5%)
                result['recommended_stop'] = round(entry_price * 0.995, 2)

                result['rationale'] = (
                    f"Position up {gain_pct:.1f}% - TRAIL TO BREAKEVEN.\n"
                    f"  Move stop to ${result['recommended_stop']:.2f} (just below entry).\n"
                    f"  Locks in risk-free position. If it pulls back, you exit at breakeven."
                )

            elif gain_pct >= 10 and gain_pct < 20:
                # 10-20% gain - Trail to +5% profit or 50 SMA
                result['should_adjust_stop'] = True
                result['action'] = 'trail_to_profit'

                # Option 1: Trail to +5% locked profit
                profit_stop = entry_price * 1.05

                # Option 2: Trail to 50 SMA (if above and close)
                if sma_50 > 0 and sma_50 < current_price:
                    sma_stop = sma_50 * 0.99  # Just below 50 SMA

                    # Use whichever is higher
                    if sma_stop > profit_stop:
                        result['recommended_stop'] = round(sma_stop, 2)
                        result['rationale'] = (
                            f"Position up {gain_pct:.1f}% - TRAIL STOP TO 50 SMA.\n"
                            f"  Move stop to ${result['recommended_stop']:.2f} (1% below 50 SMA at ${sma_50:.2f}).\n"
                            f"  Locks in ~{((result['recommended_stop']/entry_price - 1)*100):.1f}% profit minimum.\n"
                            f"  Let winner run while protecting gains."
                        )
                    else:
                        result['recommended_stop'] = round(profit_stop, 2)
                        result['rationale'] = (
                            f"Position up {gain_pct:.1f}% - TRAIL STOP TO PROFIT.\n"
                            f"  Move stop to ${result['recommended_stop']:.2f} (locks in +5% gain).\n"
                            f"  50 SMA too far below (${sma_50:.2f}). Use profit-based stop instead."
                        )
                else:
                    result['recommended_stop'] = round(profit_stop, 2)
                    result['rationale'] = (
                        f"Position up {gain_pct:.1f}% - TRAIL STOP TO PROFIT.\n"
                        f"  Move stop to ${result['recommended_stop']:.2f} (locks in +5% gain minimum).\n"
                        f"  Let position run while protecting profit floor."
                    )

            elif gain_pct >= 20 and gain_pct < 30:
                # 20-30% gain - Consider partial exit + trail remainder
                result['should_adjust_stop'] = True
                result['action'] = 'take_partial_and_trail'

                # Trail to +10% profit or 50 SMA, whichever higher
                profit_stop = entry_price * 1.10

                if sma_50 > 0 and sma_50 < current_price:
                    sma_stop = sma_50 * 0.99
                    result['recommended_stop'] = round(max(profit_stop, sma_stop), 2)
                else:
                    result['recommended_stop'] = round(profit_stop, 2)

                result['rationale'] = (
                    f"Position up {gain_pct:.1f}% - STRONG WINNER!\n"
                    f"  CONSIDER: Sell 25-30% here at ${current_price:.2f} to lock in gains.\n"
                    f"  TRAIL remaining 70-75% with stop at ${result['recommended_stop']:.2f}.\n"
                    f"  This locks in minimum +10% on full position while letting runners go.\n"
                    f"  Phase: {phase} | 50 SMA: ${sma_50:.2f}"
                )

            elif gain_pct >= 30:
                # 30%+ gain - Major winner, aggressive trailing
                result['should_adjust_stop'] = True
                result['action'] = 'take_partial_and_trail_tight'

                # Trail very tight - either 50 SMA or +15% profit minimum
                profit_stop = entry_price * 1.15

                if sma_50 > 0 and sma_50 < current_price:
                    sma_stop = sma_50 * 0.995  # Very tight (0.5% below 50 SMA)
                    result['recommended_stop'] = round(max(profit_stop, sma_stop), 2)
                else:
                    result['recommended_stop'] = round(profit_stop, 2)

                # Check if entering Phase 3 (distribution)
                phase_warning = ""
                if phase == 3:
                    phase_warning = "\n  ⚠️ WARNING: Stock entering Phase 3 (distribution). Consider heavier exit."

                result['rationale'] = (
                    f"Position up {gain_pct:.1f}% - MAJOR WINNER! 🎯\n"
                    f"  STRONGLY CONSIDER: Sell 50% here at ${current_price:.2f} to secure profits.\n"
                    f"  TRAIL remaining 50% TIGHT with stop at ${result['recommended_stop']:.2f}.\n"
                    f"  Lock in minimum +15% on full position while giving last piece room.\n"
                    f"  Phase: {phase} | 50 SMA: ${sma_50:.2f}"
                    f"{phase_warning}"
                )

            # Additional checks
            if phase == 3 or phase == 4:
                result['warnings'].append(
                    f'⚠️ Stock in Phase {phase} (distribution/decline). Consider tighter stops or exit.'
                )

            if current_price < sma_50 and sma_50 > 0:
                result['warnings'].append(
                    f'⚠️ Price broke below 50 SMA (${sma_50:.2f}). Trend weakening - review position.'
                )

        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {e}")
            result['warnings'].append(f'Analysis error: {str(e)}')

        return result

    def analyze_portfolio(
        self,
        positions: List[Dict],
        entry_dates: Optional[Dict[str, datetime]] = None
    ) -> Dict:
        """Analyze all positions and generate comprehensive report.

        Args:
            positions: List of position dicts from RobinhoodPositionFetcher
            entry_dates: Optional dict of {ticker: entry_date} for tax treatment

        Returns:
            Dict with:
            - position_analyses: List of individual position analyses
            - summary: Portfolio-level stats
            - urgent_actions: List of positions needing immediate attention
        """
        if not positions:
            return {
                'position_analyses': [],
                'summary': {'total_positions': 0},
                'urgent_actions': []
            }

        entry_dates = entry_dates or {}
        analyses = []

        for pos in positions:
            ticker = pos['ticker']
            entry_date = entry_dates.get(ticker)

            analysis = self.analyze_position(
                ticker=ticker,
                entry_price=pos['average_buy_price'],
                current_price=pos['current_price'],
                entry_date=entry_date
            )

            analysis['quantity'] = pos['quantity']
            analyses.append(analysis)

        # Generate summary
        total_positions = len(analyses)
        positions_to_adjust = sum(1 for a in analyses if a['should_adjust_stop'])
        short_term_positions = sum(
            1 for a in analyses if a['tax_treatment'] == 'short_term'
        )
        long_term_positions = sum(
            1 for a in analyses if a['tax_treatment'] == 'long_term'
        )

        avg_gain = sum(a['current_gain_pct'] for a in analyses) / total_positions if total_positions > 0 else 0

        summary = {
            'total_positions': total_positions,
            'positions_need_adjustment': positions_to_adjust,
            'short_term_positions': short_term_positions,
            'long_term_positions': long_term_positions,
            'average_gain_pct': round(avg_gain, 2)
        }

        # Urgent actions (Phase 3/4 warnings, big winners, breakdowns)
        urgent = []
        for analysis in analyses:
            if analysis['warnings']:
                urgent.append({
                    'ticker': analysis['ticker'],
                    'reason': analysis['warnings'],
                    'current_gain': analysis['current_gain_pct']
                })
            elif analysis.get('action') in ['take_partial_and_trail', 'take_partial_and_trail_tight']:
                urgent.append({
                    'ticker': analysis['ticker'],
                    'reason': 'Big winner - consider taking partial profits',
                    'current_gain': analysis['current_gain_pct']
                })

        return {
            'position_analyses': analyses,
            'summary': summary,
            'urgent_actions': urgent,
            'timestamp': datetime.now()
        }

    def format_portfolio_report(self, analysis_result: Dict) -> str:
        """Format portfolio analysis as readable report.

        Args:
            analysis_result: Output from analyze_portfolio()

        Returns:
            Formatted string report
        """
        lines = []
        lines.append("="*80)
        lines.append("POSITION MANAGEMENT REPORT - STOP LOSS RECOMMENDATIONS")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("="*80)
        lines.append("")

        summary = analysis_result['summary']
        lines.append("PORTFOLIO SUMMARY")
        lines.append("-"*80)
        lines.append(f"Total Positions: {summary['total_positions']}")
        lines.append(f"Need Stop Adjustment: {summary['positions_need_adjustment']}")
        lines.append(f"Short-term (<1 year): {summary['short_term_positions']}")
        lines.append(f"Long-term (1+ years): {summary['long_term_positions']}")
        lines.append(f"Average Gain: {summary['average_gain_pct']:+.2f}%")
        lines.append("")

        # Urgent actions
        if analysis_result['urgent_actions']:
            lines.append("⚠️  URGENT ACTIONS NEEDED")
            lines.append("-"*80)
            for urgent in analysis_result['urgent_actions']:
                lines.append(f"\n{urgent['ticker']} ({urgent['current_gain']:+.1f}%)")
                if isinstance(urgent['reason'], list):
                    for reason in urgent['reason']:
                        lines.append(f"  • {reason}")
                else:
                    lines.append(f"  • {urgent['reason']}")
            lines.append("\n" + "="*80 + "\n")

        # Individual position analyses
        lines.append("POSITION-BY-POSITION ANALYSIS")
        lines.append("="*80)

        for i, analysis in enumerate(analysis_result['position_analyses'], 1):
            lines.append(f"\n{'#'*80}")
            lines.append(f"POSITION #{i}: {analysis['ticker']}")
            lines.append(f"{'#'*80}")

            lines.append(f"Entry: ${analysis['entry_price']:.2f} | Current: ${analysis['current_price']:.2f} | Gain: {analysis['current_gain_pct']:+.2f}%")

            if analysis['tax_treatment'] != 'unknown':
                lines.append(f"Tax Treatment: {analysis['tax_treatment'].upper()}")
                if 'days_held' in analysis:
                    lines.append(f"Days Held: {analysis['days_held']}")

            lines.append("")
            lines.append(f"ACTION: {analysis['action'].replace('_', ' ').upper()}")
            lines.append("")

            if analysis['should_adjust_stop']:
                lines.append(f"✓ RECOMMENDED STOP LOSS: ${analysis['recommended_stop']:.2f}")
                lines.append("")

            lines.append("RATIONALE:")
            lines.append(analysis['rationale'])

            if analysis.get('phase'):
                lines.append(f"\nTechnical: Phase {analysis['phase']}", end="")
                if analysis.get('sma_50'):
                    lines.append(f" | 50 SMA: ${analysis['sma_50']:.2f}")
                else:
                    lines.append("")

            if analysis['warnings']:
                lines.append("\nWARNINGS:")
                for warning in analysis['warnings']:
                    lines.append(f"  {warning}")

            lines.append("")

        lines.append("="*80)
        lines.append("END OF REPORT")
        lines.append("="*80)

        return "\n".join(lines)


def main():
    """Example usage."""
    # Example positions
    positions = [
        {'ticker': 'AAPL', 'quantity': 50, 'average_buy_price': 175.50, 'current_price': 182.30},
        {'ticker': 'MSFT', 'quantity': 25, 'average_buy_price': 380.00, 'current_price': 385.50},
        {'ticker': 'NVDA', 'quantity': 30, 'average_buy_price': 495.00, 'current_price': 545.00},
    ]

    # Example entry dates (for tax treatment)
    entry_dates = {
        'AAPL': datetime.now() - timedelta(days=45),  # 45 days ago (short-term)
        'MSFT': datetime.now() - timedelta(days=400),  # 400 days ago (long-term)
        'NVDA': datetime.now() - timedelta(days=20),   # 20 days ago (short-term)
    }

    manager = PositionManager()
    result = manager.analyze_portfolio(positions, entry_dates)

    print(manager.format_portfolio_report(result))


if __name__ == '__main__':
    main()

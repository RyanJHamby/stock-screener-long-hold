# Stock Screener Data Module

A production-ready data fetching and storage module for identifying undervalued stocks near support levels. This module provides robust interfaces for retrieving stock data from Yahoo Finance and persisting it to a PostgreSQL or SQLite database.

## Features

- **Data Fetching**: Retrieve stock fundamentals and 5 years of price history from Yahoo Finance
- **Intelligent Caching**: Local pickle-based caching with configurable expiry (default: 24 hours)
- **Error Handling**: Automatic retry logic with exponential backoff for network failures
- **Database Storage**: SQLAlchemy-based storage with PostgreSQL or SQLite support
- **Value Screening**: Built-in queries to find undervalued stocks by P/E, P/B ratios
- **Type Safety**: Comprehensive type hints throughout the codebase
- **Production Ready**: Connection pooling, logging, and proper error handling

## Project Structure

```
stock-screener/
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── fetcher.py       # Yahoo Finance data fetching with caching
│   │   └── storage.py       # PostgreSQL/SQLite storage layer
├── tests/
│   ├── __init__.py
│   └── test_fetcher.py      # Comprehensive test suite
├── requirements.txt         # Python dependencies
├── .env.example            # Environment configuration template
└── README.md               # This file
```

## Installation

### 1. Clone and Setup

```bash
cd stock-screener
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

For **local development** (easiest):
```bash
DATABASE_URL=sqlite:///./stock_screener.db
```

For **production** with PostgreSQL:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/stock_screener
```

### 3. PostgreSQL Setup (Optional)

If using PostgreSQL:

```bash
# Install PostgreSQL (macOS)
brew install postgresql
brew services start postgresql

# Create database
createdb stock_screener

# Or using psql
psql postgres
CREATE DATABASE stock_screener;
\q
```

## Usage Examples

### Basic Data Fetching

```python
from src.data import YahooFinanceFetcher

# Initialize fetcher
fetcher = YahooFinanceFetcher(cache_dir="./data/cache")

# Fetch fundamentals for a single stock
fundamentals = fetcher.fetch_fundamentals("AAPL")
print(f"P/E Ratio: {fundamentals['pe_ratio']}")
print(f"P/B Ratio: {fundamentals['pb_ratio']}")
print(f"Current Price: {fundamentals['current_price']}")

# Fetch 5 years of price history
prices = fetcher.fetch_price_history("AAPL", period="5y")
print(prices.head())
print(f"Total records: {len(prices)}")

# Fetch data for multiple stocks
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
fundamentals_df, prices_df = fetcher.fetch_multiple(tickers)
print(f"Fetched data for {len(fundamentals_df)} stocks")
print(fundamentals_df[['ticker', 'pe_ratio', 'pb_ratio', 'current_price']])

# Clear cache for specific ticker or all
fetcher.clear_cache("AAPL")  # Clear AAPL cache only
fetcher.clear_cache()        # Clear all cache
```

### Database Storage

```python
from src.data import StockDatabase, YahooFinanceFetcher

# Initialize database (creates tables automatically)
db = StockDatabase()  # Uses DATABASE_URL from .env

# Fetch and save data
fetcher = YahooFinanceFetcher()

# Save fundamentals
fundamentals = fetcher.fetch_fundamentals("AAPL")
db.save_stock_fundamentals("AAPL", fundamentals)

# Save price history
prices = fetcher.fetch_price_history("AAPL", period="5y")
db.save_price_history("AAPL", prices)

# Retrieve data from database
latest = db.get_latest_fundamentals("AAPL")
print(f"Latest P/E: {latest['pe_ratio']}")

history = db.get_price_history("AAPL", "2023-01-01", "2024-01-01")
print(f"Retrieved {len(history)} price records")

# Find undervalued stocks
cheap_stocks = db.query_cheap_stocks(pe_max=15, pb_max=1.5)
print(f"Found {len(cheap_stocks)} undervalued stocks: {cheap_stocks}")

# Get all tickers in database
all_tickers = db.get_all_tickers()
print(f"Database contains {len(all_tickers)} stocks")
```

### Complete Workflow Example

```python
from src.data import YahooFinanceFetcher, StockDatabase

# Initialize
fetcher = YahooFinanceFetcher(cache_dir="./data/cache")
db = StockDatabase()

# Define stock universe
sp500_sample = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "V", "JNJ"]

# Fetch and store data
print("Fetching data for S&P 500 sample...")
for ticker in sp500_sample:
    print(f"Processing {ticker}...")

    # Fetch fundamentals
    fundamentals = fetcher.fetch_fundamentals(ticker)
    if fundamentals:
        db.save_stock_fundamentals(ticker, fundamentals)

    # Fetch price history
    prices = fetcher.fetch_price_history(ticker, period="5y")
    if not prices.empty:
        db.save_price_history(ticker, prices)

# Screen for value stocks
print("\nScreening for undervalued stocks...")
value_stocks = db.query_cheap_stocks(pe_max=20, pb_max=3.0, min_market_cap=10_000_000_000)
print(f"Found {len(value_stocks)} value stocks: {value_stocks}")

# Analyze each value stock
for ticker in value_stocks:
    data = db.get_latest_fundamentals(ticker)
    print(f"\n{ticker} - {data['name']}")
    print(f"  P/E: {data['pe_ratio']:.2f}, P/B: {data['pb_ratio']:.2f}")
    print(f"  Price: ${data['current_price']:.2f}")
    print(f"  52W Range: ${data['week_52_low']:.2f} - ${data['week_52_high']:.2f}")
```

## API Reference

### YahooFinanceFetcher

#### Methods

- `fetch_fundamentals(ticker: str) -> Dict[str, any]`
  - Fetches fundamental data for a stock
  - Returns: Dict with P/E, P/B, debt-to-equity, FCF, price data
  - Cached for 24 hours by default

- `fetch_price_history(ticker: str, period: str = "5y") -> pd.DataFrame`
  - Fetches historical OHLCV data
  - Period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
  - Returns: DataFrame with Date, Open, High, Low, Close, Volume

- `fetch_multiple(tickers: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]`
  - Fetches data for multiple stocks
  - Returns: (fundamentals_df, prices_df)

- `clear_cache(ticker: Optional[str] = None) -> None`
  - Clears cached data for ticker or all if None

### StockDatabase

#### Methods

- `save_stock_fundamentals(ticker: str, data: Dict[str, any]) -> None`
  - Saves fundamental data to database
  - Creates/updates stock entry automatically

- `save_price_history(ticker: str, df: pd.DataFrame) -> None`
  - Bulk inserts price history data
  - Handles duplicates gracefully

- `get_latest_fundamentals(ticker: str) -> Dict[str, any]`
  - Retrieves most recent fundamental data
  - Returns: Dict with all fundamental metrics

- `get_price_history(ticker: str, start_date: str, end_date: str) -> pd.DataFrame`
  - Retrieves price data for date range
  - Date format: 'YYYY-MM-DD'
  - Returns: DataFrame with OHLCV data

- `query_cheap_stocks(pe_max: float, pb_max: float, min_market_cap: Optional[float]) -> List[str]`
  - Queries undervalued stocks by criteria
  - Returns: List of ticker symbols

- `get_all_tickers() -> List[str]`
  - Returns list of all tickers in database

## Database Schema

### Tables

**stocks**
- `id`: Primary key
- `ticker`: Unique stock symbol (indexed)
- `name`: Company name
- `sector`: Industry sector
- `last_updated`: Last update timestamp

**fundamentals**
- `id`: Primary key
- `stock_id`: Foreign key to stocks
- `date`: Data date (indexed)
- `pe_ratio`, `pb_ratio`, `debt_equity`, `fcf_yield`
- `market_cap`, `current_price`, `week_52_high`, `week_52_low`
- `trailing_eps`, `forward_eps`, `dividend_yield`

**price_history**
- `id`: Primary key
- `stock_id`: Foreign key to stocks
- `date`: Trading date (indexed, unique with stock_id)
- `open`, `high`, `low`, `close`, `volume`

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/data tests/

# Run specific test file
pytest tests/test_fetcher.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_fetcher.py::test_fetch_fundamentals_success
```

## Error Handling

The module includes comprehensive error handling:

- **Network Failures**: Automatic retry with 3 attempts and 2-second delays
- **Invalid Tickers**: Graceful handling with logging
- **Missing Data**: Returns None/empty for missing fields with warnings
- **Database Errors**: Transaction rollback with detailed error messages
- **Cache Issues**: Fallback to API if cache fails

## Configuration

Environment variables (set in `.env`):

- `DATABASE_URL`: Database connection string
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `CACHE_DIR`: Cache directory path (default: ./data/cache)
- `CACHE_EXPIRY_HOURS`: Cache expiry time (default: 24)

## Performance Tips

1. **Use Caching**: Let the cache work - subsequent calls are instant
2. **Batch Operations**: Use `fetch_multiple()` for multiple stocks
3. **Database Pooling**: PostgreSQL with connection pooling for production
4. **Bulk Inserts**: `save_price_history()` uses bulk operations
5. **Index Queries**: Database is indexed on ticker and date columns

## Logging

All operations are logged with timestamps:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

Log levels:
- `INFO`: Successful operations, cache hits/misses
- `WARNING`: Missing data, cache failures
- `ERROR`: API failures, database errors

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'yfinance'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "Could not connect to PostgreSQL"
**Solution**: Use SQLite for local testing: `DATABASE_URL=sqlite:///./stock_screener.db`

### Issue: "No data returned for ticker"
**Solution**: Ticker may be invalid or delisted. Check ticker symbol on Yahoo Finance.

### Issue: "Cache directory permission denied"
**Solution**: Ensure write permissions: `chmod 755 ./data/cache`

## Contributing

To extend this module:

1. Add new methods to `YahooFinanceFetcher` for additional data sources
2. Add new tables to `storage.py` for different data types
3. Add new query methods to `StockDatabase` for screening criteria
4. Write tests for all new functionality

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the test files for usage examples
3. Check Yahoo Finance API documentation: https://pypi.org/project/yfinance/

## Roadmap

Future enhancements:
- [ ] Support for multiple data sources (Alpha Vantage, IEX Cloud)
- [ ] Technical indicators calculation (RSI, MACD, Bollinger Bands)
- [ ] Support level detection algorithms
- [ ] Real-time data streaming
- [ ] Async data fetching for improved performance
- [ ] Web dashboard for visualization

## Screening Module

The screening module combines fundamental value analysis with technical support analysis to identify high-probability buying opportunities.

### Features

- **Value Scoring**: Evaluates P/E ratio, P/B ratio, FCF yield, and debt levels
- **Support Detection**: Identifies support levels from swing lows, moving averages, and historical lows
- **Technical Indicators**: RSI, SMA, EMA, MACD, Bollinger Bands, volume analysis
- **Combined Scoring**: Weights value (70%) and technical (30%) factors for buy signal

### Quick Start

```python
from src.data import StockDatabase
from src.screening import screen_candidates

# Initialize database
db = StockDatabase()

# Screen candidates
tickers = ["AAPL", "MSFT", "GOOGL", "JPM", "WMT"]
results = screen_candidates(db, tickers)

# View results
print(results[['ticker', 'buy_signal', 'value_score', 'support_score']])

# Top candidate
top_pick = results.iloc[0]
print(f"Top pick: {top_pick['ticker']} (Buy Signal: {top_pick['buy_signal']:.1f})")
```

### API Reference

#### Value Scoring

```python
from src.screening import calculate_value_score

fundamentals = {
    'pe_ratio': 15.0,
    'pb_ratio': 2.0,
    'fcf_yield': 5.0,
    'debt_equity': 50.0
}
score = calculate_value_score(fundamentals)
# Returns: 0-100 score (higher is better)
```

**Scoring Criteria:**
- P/E < 15: Maximum points
- P/B < 1.5: Maximum points  
- FCF yield > 5%: Maximum points
- Debt/Equity < 50%: Bonus points

#### Support Detection

```python
from src.screening import detect_support_levels

# Requires DataFrame with Date, Close, High, Low columns
support_levels = detect_support_levels(price_df)
# Returns: [95.50, 98.20, 100.00, 105.30] (sorted list)
```

Detects support from:
- Swing lows (30-day window)
- 50-day and 200-day moving averages
- Recent significant lows (90 days)
- 52-week low

#### Support Scoring

```python
from src.screening import calculate_support_score

score = calculate_support_score(
    current_price=100.0,
    support_levels=[95, 98, 105],
    rsi=35,  # Oversold
    volume_spike=True
)
# Returns: 0-100 score
```

**Scoring Factors:**
- Distance from support (40 points max)
- RSI oversold condition (30 points max)
- Volume spike (20 points)
- Multiple support confluence (10 points)

#### Technical Indicators

```python
from src.screening.indicators import (
    calculate_rsi,
    calculate_sma,
    calculate_ema,
    calculate_macd,
    calculate_bollinger_bands,
    detect_volume_spike,
    find_swing_lows
)

# RSI (14-period default)
rsi = calculate_rsi(prices, period=14)

# Moving averages
sma_50 = calculate_sma(prices, period=50)
ema_200 = calculate_ema(prices, period=200)

# MACD
macd, signal, histogram = calculate_macd(prices)

# Bollinger Bands
middle, upper, lower = calculate_bollinger_bands(prices, period=20)

# Volume analysis
is_spike = detect_volume_spike(volumes, current_volume, threshold=1.5)

# Swing lows
lows = find_swing_lows(prices, window=30)
```

### Running the Demo

```bash
# Full screening demonstration
python screening_demo.py
```

The demo will:
1. Fetch data for 8 sample stocks (AAPL, MSFT, JPM, etc.)
2. Run screening algorithm
3. Display ranked results with buy signals
4. Show detailed analysis of top candidate

### Understanding Buy Signals

Buy signals range from 0-100:

- **80-100**: 🔥 STRONG BUY - Excellent value at strong support
- **65-79**: ✅ BUY - Good value with favorable technicals
- **50-64**: ⚡ CONSIDER - Decent setup, monitor for entry
- **0-49**: ⏸️ WATCH - Wait for better opportunity

### Customizing the Screener

#### Adjust Weights

```python
# More value-focused (80% value, 20% technical)
results = screen_candidates(db, tickers, value_weight=0.8, support_weight=0.2)

# More technical-focused (50/50 split)
results = screen_candidates(db, tickers, value_weight=0.5, support_weight=0.5)
```

#### Filter Results

```python
# Only strong buy signals
strong_buys = results[results['buy_signal'] >= 80]

# Oversold stocks only
oversold = results[results['rsi'] < 40]

# Value stocks at support
value_at_support = results[
    (results['value_score'] >= 70) & 
    (results['support_score'] >= 60)
]
```

### Example Output

```
TOP CANDIDATES (sorted by Buy Signal)

#1: AAPL - Apple Inc.
  Sector: Technology
  Current Price: $175.50
  Nearest Support: $172.30 (+1.9%)

  Scores:
    Buy Signal:     85.3/100 ★★★★
    Value Score:    78.5/100 ■■■■
    Support Score:  82.1/100 ▲▲▲▲

  Fundamentals:
    P/E Ratio:      28.50
    P/B Ratio:      45.30

  Technicals:
    RSI:            35.2 (Oversold)

  Signal: 🔥 STRONG BUY
```

### Performance Tips

1. **Batch Screening**: Screen multiple stocks at once for efficiency
2. **Use Cached Data**: Subsequent runs are instant with cached data
3. **Filter Tickers**: Pre-filter by sector/market cap before screening
4. **Adjust Thresholds**: Customize min_data_days based on your needs

### Common Use Cases

#### Find Value Stocks

```python
# Screen S&P 500 value stocks
sp500_tickers = [...] # List of S&P 500 tickers
results = screen_candidates(db, sp500_tickers, value_weight=0.8)
value_stocks = results[results['pe_ratio'] < 20]
```

#### Find Oversold Stocks at Support

```python
# Focus on technical setup
results = screen_candidates(db, tickers, support_weight=0.6)
oversold_support = results[
    (results['rsi'] < 40) & 
    (results['support_score'] > 70)
]
```

#### Sector Rotation Strategy

```python
# Screen by sector
tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'META']
finance_stocks = ['JPM', 'BAC', 'GS', 'MS']

tech_results = screen_candidates(db, tech_stocks)
finance_results = screen_candidates(db, finance_stocks)

# Compare sectors
print(f"Tech avg signal: {tech_results['buy_signal'].mean():.1f}")
print(f"Finance avg signal: {finance_results['buy_signal'].mean():.1f}")
```

### Testing

```bash
# Run all screening tests
pytest tests/test_screener.py -v

# Run specific test category
pytest tests/test_screener.py::TestValueScoring -v
pytest tests/test_screener.py::TestTechnicalIndicators -v
```

### Algorithm Details

#### Value Score Calculation

The value score is calculated from four components:

1. **P/E Ratio (40 points)**
   - ≤15: 40 points
   - 15-30: 20-40 points (linear scale)
   - 30-50: 0-20 points (linear scale)
   - >50: 0 points

2. **P/B Ratio (30 points)**
   - ≤1.5: 30 points
   - 1.5-3.0: 10-30 points (linear scale)
   - 3.0-5.0: 0-10 points (linear scale)
   - >5.0: 0 points

3. **FCF Yield (20 points)**
   - ≥5%: 20 points
   - 0-5%: 0-20 points (linear scale)
   - <0%: 0 points

4. **Debt/Equity (10 points bonus)**
   - ≤50%: 10 points
   - 50-100%: 5-10 points (linear scale)
   - >100%: 0-5 points (linear scale)

#### Support Score Calculation

The support score combines multiple technical factors:

1. **Distance from Support (40 points)**
   - Within 1%: 40 points
   - 1-3%: 25-40 points
   - 3-5%: 15-25 points
   - 5-10%: 0-15 points
   - >10%: 0 points

2. **RSI Level (30 points)**
   - ≤30: 30 points (deeply oversold)
   - 30-40: 20-30 points (oversold)
   - 40-50: 10-20 points (neutral)
   - 50-70: 0-10 points
   - >70: -10 points (overbought penalty)

3. **Volume Spike (20 points)**
   - Volume >150% of average: +20 points

4. **Support Confluence (10 points bonus)**
   - Multiple support levels within 3% of price: +10 points


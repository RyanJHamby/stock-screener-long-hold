# Long-Term Compounder Scoring Methodology

## Complete Scoring Formula (0-110+ points)

The long-term compounder system identifies elite 5-10 year wealth builders through rigorous, deterministic scoring:

```
Total Score = Fundamental Dominance (60) + RS Persistence (25) + Trend Durability (15) + Moat Bonus (0-10)
Range: 0-110+ points
Interpretation: 80+ = Elite, 70-79 = Quality, 50-69 = Decent, <50 = Below threshold
```

---

## Component 1: Fundamental Dominance (60 points)

### A. Growth Quality (20 points)

**Purpose:** Measure sustainable top-line and earnings growth over 3-5 year periods.

| Metric | Formula | Points | Range |
|--------|---------|--------|-------|
| Revenue CAGR (3Y) | (Current Revenue / Revenue 3 Years Ago) ^ (1/3) - 1 | 0-8 | 0% = 0, 15%+ = 8 |
| Revenue CAGR (5Y) | (Current Revenue / Revenue 5 Years Ago) ^ (1/5) - 1 | 0-7 | 0% = 0, 15%+ = 7 |
| EPS CAGR (3Y) | (Current EPS / EPS 3 Years Ago) ^ (1/3) - 1 | 0-5 | 0% = 0, 20%+ = 5 |

**Scoring Approach:** Linear scaling between min and max thresholds.

**Example: Apple (AAPL)**
```
Revenue CAGR (3Y): 9.2%     → 9.2/15 * 8 = 4.9 pts (trending toward 15%)
Revenue CAGR (5Y): 8.1%     → 8.1/15 * 7 = 3.8 pts
EPS CAGR (3Y):    12.8%     → 12.8/20 * 5 = 3.2 pts
Subtotal:                              11.9 pts / 20
```

**What This Measures:**
- Consistency of growth over multiple economic cycles
- Revenue quality (top-line health)
- Earnings expansion (operational leverage)

**Why It Matters:**
- Companies with 10%+ CAGR compound wealth dramatically over decades
- Eliminates one-hit wonders and cyclicals
- Shows business resilience through different market conditions

---

### B. Capital Efficiency (20 points)

**Purpose:** Measure how effectively management deploys capital to generate returns.

| Metric | Formula | Points | Range |
|--------|---------|--------|-------|
| ROIC | NOPAT / Invested Capital | 0-10 | 10% = 0, 25%+ = 10 |
| ROIC-WACC Spread | ROIC - WACC | 0-5 | 0% = 0, 15%+ = 5 |
| FCF Margin | Free Cash Flow / Revenue | 0-5 | 0% = 0, 20%+ = 5 |

**Scoring Approach:** Linear scaling, with higher ROIC and wider spread = higher score.

**Example: Microsoft (MSFT)**
```
ROIC:              38%    → 38-10 / (25-10) * 10 = 18.7 pts (capped at 10)
ROIC-WACC Spread:  30%    → min(30/15, 1) * 5 = 5.0 pts
FCF Margin:        27%    → min(27/20, 1) * 5 = 5.0 pts
Subtotal:                                    10.0 + 5.0 + 5.0 = 20 pts / 20
```

**What This Measures:**
- Competitive moat strength (can earn above cost of capital?)
- Management quality (capital allocation skills)
- Cash generation ability (sustainability)

**Why It Matters:**
- ROIC > WACC = creating shareholder value
- ROIC > 20% = genuine competitive advantage
- FCF > net income = quality of earnings (not accounting tricks)

---

### C. Reinvestment Quality (10 points)

**Purpose:** Assess quality of capital reinvestment in growth.

| Metric | Formula | Points | Interpretation |
|--------|---------|--------|-----------------|
| R&D to Sales (Tech/Pharma) | R&D / Revenue | 0-5 | Validate innovation investment |
| Capex to Sales (Manufacturing) | Capex / Revenue | 0-5 | Validate production capability |

**Scoring Approach:** Context-dependent on industry.

**Example: NVIDIA (NVDA)**
```
R&D Ratio:  27% of revenue    → High investment in future (AI, architecture)
            → 5.0 pts (validates continued leadership)
Capex:      Lower (fabless model) → 0-2 pts (outsources to TSMC)
Subtotal:                            ~5 pts / 10
```

**What This Measures:**
- Whether company reinvests in staying competitive
- Industry-appropriate capital intensity
- Innovation pipeline strength

---

### D. Balance Sheet Strength (10 points)

**Purpose:** Ensure financial health and downside protection.

| Metric | Formula | Points | Range |
|--------|---------|--------|-------|
| Net Debt / EBITDA | (Total Debt - Cash) / EBITDA | 0-5 | 3.0x = 0, <1.0x = 5 |
| Interest Coverage | EBIT / Interest Expense | 0-3 | 3x = 0, 10x+ = 3 |
| Cash to Debt | Cash / Total Debt | 0-2 | 0.2x = 0, 1.0x+ = 2 |

**Scoring Approach:** Lower leverage = higher score.

**Example: Apple (AAPL)**
```
Net Debt / EBITDA:  -0.8x (net cash)  → max(5) = 5.0 pts
Interest Coverage:  12x              → min(12/10, 1) * 3 = 3.0 pts
Cash to Debt:       0.95x            → 0.95/1 * 2 = 1.9 pts
Subtotal:                                 9.9 pts / 10
```

**What This Measures:**
- Ability to survive downturns without equity dilution
- Financial flexibility for M&A or buybacks
- Bankruptcy risk mitigation

**Fundamental Dominance Total: 60 points maximum**

---

## Component 2: Long-Horizon Relative Strength Persistence (25 points)

### Purpose: Multi-year outperformance vs SPY benchmark.

**Why 1Y/3Y/5Y?** Different market cycles:
- 1Y = Recent momentum (still valid?)
- 3Y = Mid-cycle performance (can it repeat?)
- 5Y = Full cycle test (does it work in all conditions?)

| Period | Points | Threshold (Outperformance) |
|--------|--------|---------------------------|
| 1-Year Return | 0-8 | -10% = 0, +20% = 8 |
| 3-Year Annual | 0-10 | -5% = 0, +15% = 10 |
| 5-Year Annual | 0-7 | -3% = 0, +12% = 7 |

### Volatility Adjustment (-5 to 0 points)

**Penalty for excessive drawdown:**
- If stock max drawdown > SPY max drawdown by 20%+: Apply penalty
- Protects against over-concentrated risk

**Example: NVIDIA (NVDA)**
```
1Y Return:    +35% vs SPY +10%  → Outperformance +25%  → 8.0 pts (capped)
3Y Annual:    +22% vs SPY +8%   → Outperformance +14%  → 9.3 pts
5Y Annual:    +28% vs SPY +10%  → Outperformance +18%  → 7.0 pts (capped)
Drawdown:     -40% vs SPY -15%  → Excess -25%          → -3.0 pts penalty
Subtotal:                                   8.0 + 9.3 + 7.0 - 3.0 = 21.3 / 25
```

**What This Measures:**
- Multi-year winning streak (not one-quarter luck)
- Relative strength persistence (beating the market)
- Risk-adjusted returns (doesn't penalize growth volatility)

---

## Component 3: Structural Trend Durability (15 points)

### Purpose: Confirm long-term uptrend is intact and durable.

| Metric | Formula | Points | Interpretation |
|--------|---------|--------|-----------------|
| Price > 40W MA | Distance above 40-week moving average | 0-5 | 0% = 0, 20%+ = 5 |
| 40W MA Slope | Slope of 40-week MA (annualized %) | 0-5 | 0% = 0, 15%+ = 5 |
| Months in Uptrend | Consecutive months with higher lows | 0-5 | 12 = 0, 36+ = 5 |

### Moving Average Interpretation

**40-Week MA (280-day average):**
- Filters out daily/weekly noise
- Represents institutional positioning
- Crossing above = regime change signal

**Scoring Example: Microsoft (MSFT)**
```
Price vs 40W MA:    $370 vs $350 MA  → 5.7% above    → 1.4 pts
40W MA Slope:       +12% annualized   → 12/15 * 5     → 4.0 pts
Months Uptrend:     28 consecutive    → 28/36 * 5     → 3.9 pts
Subtotal:                                   1.4 + 4.0 + 3.9 = 9.3 / 15
```

**What This Measures:**
- Uptrend stability (price respecting long-term MA)
- Trend strength (slope of MA)
- Trend consistency (how long sustained?)

---

## Component 4: Moat Bonus (0-10 points)

### Purpose: Quantify business moat using measurable proxies.

#### A. Pricing Power (0-3 points)

**Proxy:** Gross margin stability + expansion

```python
Gross Margin Stability = 3 - (std_dev_of_3yr_margins / 2%)
Gross Margin Expansion = (Current GM - 3Y Ago GM) / 100 bps
Score = Stability + Expansion * 2
```

**Example: Apple**
```
Gross Margins: 42%, 43%, 44%, 42% (3 years)
Std Dev: 0.8%               → Stable = 2.6 pts
Expansion: +1.5% = 150 bps  → 0.3 pts
Subtotal:                      3.0 pts / 3
```

#### B. Customer Lock-In (0-3 points)

**Proxy:** Revenue volatility + subscription %

```python
Revenue Volatility = 3 - (YoY revenue std_dev / 5%)
Subscription Revenue = (Recurring / Total) * 2
Score = Volatility + Subscription
```

**Example: Microsoft (cloud/subscriptions)**
```
Revenue Growth Consistency: Low volatility  → 2.5 pts
Subscription %: 60% of revenue             → 1.2 pts
Subtotal:                                      3.7 pts / 3 (capped)
```

#### C. Platform Effects (0-3 points)

**Proxy:** Revenue per employee growth + operating leverage

```python
Revenue per Employee Growth = 3Y CAGR of (Revenue / Headcount)
Operating Leverage = (Revenue Growth % - Opex Growth %) / 2
Score = 2 * (RPEG / 5%) + OL (capped at 3)
```

**Example: Meta**
```
Revenue/Employee CAGR: 8%        → 2.5 pts
Operating Leverage: Negative      → 0 pts (cost cutting phase)
Subtotal:                            2.5 pts / 3
```

#### D. Operating Leverage (0-2 points)

**Proxy:** Margin expansion from incremental revenue

```python
Operating Leverage = (Operating Income Growth % / Revenue Growth %) * 2
Score = min(Operating Leverage, 2)
```

**Example: Visa**
```
Revenue Growth: 10%
Operating Income Growth: 18%
Operating Leverage: (18/10) * 2 = 3.6 (capped at 2)
Score: 2.0 pts / 2
```

---

## Scoring Examples

### Example 1: Apple (AAPL) - Elite Compounder

```
FUNDAMENTAL DOMINANCE (60):
  Growth Quality:        11.9/20    (9.2% rev, 12.8% eps)
  Capital Efficiency:    20.0/20    (38% ROIC, 30% spread, 27% FCF)
  Reinvestment:           6.0/10    (5% R&D, solid capex)
  Balance Sheet:          9.9/10    (-0.8x debt, 12x coverage)
  Subtotal:             47.8 points

RS PERSISTENCE (25):
  1Y Return:              8.0/8     (+25% vs SPY)
  3Y Annual:              9.0/10    (+12% vs SPY)
  5Y Annual:              7.0/7     (+14% vs SPY)
  Volatility:             -3.0      (excessive drawdown penalty)
  Subtotal:             21.0 points

TREND DURABILITY (15):
  Price > 40W MA:         3.5/5     (7% above)
  40W MA Slope:           4.5/5     (+12% slope)
  Months Uptrend:         4.0/5     (30 months)
  Subtotal:             12.0 points

MOAT BONUS:
  Pricing Power:          3.0/3     (stable 40-44% margins)
  Lock-In:                2.5/3     (high ecosystem stickiness)
  Platform:               2.0/3     (high revenue/employee)
  Operating Leverage:     1.5/2     (margin expansion)
  Subtotal:              9.0 points

TOTAL SCORE: 47.8 + 21.0 + 12.0 + 9.0 = 89.8 / 110

INTERPRETATION:
✅ STRUCTURAL_GROWTH (Regime)
🏆 ELITE COMPOUNDER
Target Allocation: 4-5% of portfolio (core position)
```

### Example 2: Visa (V) - Quality Compounder

```
FUNDAMENTAL DOMINANCE (60):
  Growth Quality:        15.0/20    (13% rev CAGR, 16% eps)
  Capital Efficiency:    18.0/20    (45% ROIC, 37% spread, 50% FCF)
  Reinvestment:           4.0/10    (network model, low capex)
  Balance Sheet:          8.0/10    (1.2x debt, 9x coverage)
  Subtotal:             45.0 points

RS PERSISTENCE (25):
  1Y Return:              6.5/8     (+18% vs SPY)
  3Y Annual:              8.5/10    (+11% vs SPY)
  5Y Annual:              6.0/7     (+10% vs SPY)
  Volatility:             -1.0      (minor penalty)
  Subtotal:             20.0 points

TREND DURABILITY (15):
  Price > 40W MA:         4.0/5     (10% above)
  40W MA Slope:           4.0/5     (+10% slope)
  Months Uptrend:         4.5/5     (35 months)
  Subtotal:             12.5 points

MOAT BONUS:
  Pricing Power:          2.5/3     (40-42% margins, flat)
  Lock-In:                3.0/3     (high switching costs)
  Platform:               3.0/3     (network effects)
  Operating Leverage:     2.0/2     (strong margin expansion)
  Subtotal:             10.5 points (capped at 10)

TOTAL SCORE: 45.0 + 20.0 + 12.5 + 10.0 = 87.5 / 110

INTERPRETATION:
✅ STRUCTURAL_GROWTH (Regime)
🏆 ELITE COMPOUNDER (slight dip from AAPL due to lower growth)
Target Allocation: 3.5-4.5% of portfolio (core position)
```

### Example 3: Netflix (NFLX) - Mature Hold

```
FUNDAMENTAL DOMINANCE (60):
  Growth Quality:         6.0/20    (4% rev CAGR - decelerating)
  Capital Efficiency:    12.0/20    (22% ROIC, 14% spread, 30% FCF)
  Reinvestment:           3.0/10    (moderate content spend)
  Balance Sheet:          7.0/10    (1.8x debt, 6x coverage)
  Subtotal:             28.0 points

RS PERSISTENCE (25):
  1Y Return:              3.0/8     (-5% vs SPY - underperforming)
  3Y Annual:              5.0/10    (+2% vs SPY)
  5Y Annual:              4.0/7     (+5% vs SPY)
  Volatility:             -2.0      (higher volatility)
  Subtotal:             10.0 points

TREND DURABILITY (15):
  Price > 40W MA:         2.0/5     (3% above - weak)
  40W MA Slope:           2.0/5     (+3% slope - flattening)
  Months Uptrend:         3.0/5     (18 months - recent, not sustained)
  Subtotal:              7.0 points

MOAT BONUS:
  Pricing Power:          1.0/3     (margins under pressure)
  Lock-In:                2.0/3     (moderate churn risk)
  Platform:               1.5/3     (mature subscriber base)
  Operating Leverage:     0.5/2     (margin compression)
  Subtotal:              5.0 points

TOTAL SCORE: 28.0 + 10.0 + 7.0 + 5.0 = 50.0 / 110

INTERPRETATION:
⏸️ MATURE_HOLD (Regime)
⚠️ BELOW THRESHOLD - Not suitable for long-term compounder portfolio
Growth has decelerated, technical indicators weakening
Consider: Exit or reduce position
```

---

## Scoring Thresholds & Interpretation

| Score Range | Category | Regime | Action |
|-------------|----------|--------|--------|
| 85-110+ | Elite Compounder | Structural Growth ✅ | Core position (3-5%) |
| 75-84 | High Quality | Structural Growth ✅ | Core position (2.5-4%) |
| 70-74 | Quality | Structural Growth ✅ | Satellite position (1.5-3%) |
| 50-69 | Decent Business | Mature Hold ⏸️ | Hold existing only |
| <50 | Below Threshold | Capital Destruction ❌ | Do not hold |

---

## Data Requirements

For accurate scoring, you need:

**Historical Fundamentals (5 years):**
- Revenue (quarterly + annual)
- Net income / EPS
- Operating income (NOPAT)
- Free cash flow
- Total debt & cash
- Interest expense
- R&D & Capex (item level)

**Historical Price Data (5+ years):**
- Daily closing prices
- 40-week moving average
- 1Y/3Y/5Y total returns
- Maximum drawdown
- SPY comparison data

**Current Period:**
- Shares outstanding (for per-share metrics)
- Cash flow statement (FCF calculation)
- Balance sheet (debt, cash, equity)

---

## Implementation Notes

### Scoring Stability

The scoring formula is **deterministic** - same inputs always produce same outputs. No random variation or subjective judgment.

### Updates & Refresh

Scores are recalculated quarterly (Jan 15, Apr 15, Jul 15, Oct 15) when:
- New quarterly earnings released
- Annual reports available
- New 1Y/3Y/5Y price data complete

### Invalidation Triggers

For each position, track these violations:

**Stock-Specific:**
- ROIC < WACC (capital destruction)
- Revenue declining 2+ consecutive quarters
- Gross margin compression > 200 bps
- Debt/EBITDA > 4.0x
- Price < 40W MA for 3+ months (trend broken)
- 3Y and 5Y RS both turn negative

**Portfolio-Level:**
- Position > 10% → Trim to max 10%
- Sector > 30% → Rebalance proportionally
- Quality score drops >20 pts → Reduce or exit

---

## Summary

The compounder scoring methodology combines:
- **Fundamental strength** (60%): Can company sustain growth?
- **Multi-year outperformance** (25%): Does it beat the market?
- **Trend durability** (15%): Is the uptrend intact?
- **Business moat** (bonus): Can it stay competitive?

This creates a **deterministic, reproducible system** for identifying elite 5-10 year wealth builders from a universe of thousands of candidates.

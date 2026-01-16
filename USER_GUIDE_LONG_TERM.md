# User Guide: Long-Term Compounder System

## Getting Started (5 minutes)

### What You'll Get

Every quarter (Jan 15, Apr 15, Jul 15, Oct 15), you'll receive:

1. **Allocation Model (CSV)** - Top 25 stocks + 10 ETFs ranked by quality score
2. **Ownership Report (TXT)** - Investment thesis + portfolio statistics
3. **Rebalance Actions** - Specific buy/sell/hold recommendations
4. **Git History** - Quarterly reports tracked in version control

### Installation & Setup (First Time)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/stock-screener-long-hold.git
cd stock-screener-long-hold

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set FMP API key (for local testing)
export FMP_API_KEY=your_api_key_here

# 4. Create reports directory
mkdir -p data/quarterly_reports
```

### First Quarterly Report (Manual Trigger)

```bash
# Test mode (10 stocks, ~10 seconds)
python run_quarterly_compounder_scan.py --test-mode

# Full scan (500 stocks, ~20 minutes)
python run_quarterly_compounder_scan.py

# View results
cat data/quarterly_reports/allocation_model_*.csv
```

---

## Understanding Your Quarterly Report

### Section 1: Portfolio Summary

```
Total Stocks: 25
Total ETFs: 10
Total Positions: 35
Portfolio Score: 78.2/100
Concentration (Herfindahl): 0.032
Rebalance Cadence: Annual
```

**What This Means:**
- **35 total positions** - Diversified, not concentrated
- **78.2/100 score** - Portfolio quality metric (higher = better)
- **0.032 concentration** - Low concentration (0 = perfect diversification, 1 = one stock)
- **Annual rebalance** - Review once per year minimum

### Section 2: Top 5 Conviction Positions

```
1. AAPL    → 3.97% (Stock)
2. SOXX    → 3.96% (ETF)
3. MSFT    → 3.87% (Stock)
4. GOOGL   → 3.82% (Stock)
5. SMH     → 3.82% (ETF)
```

**Interpretation:**
- Highest allocation goes to highest-quality assets
- No single position exceeds 10% (concentration rule)
- Mix of stocks and ETFs provides diversification
- These 5 positions = ~19% of portfolio

**Action Items:**
- Review theses for top 5 regularly (quarterly minimum)
- Monitor invalidation triggers (market changes?)
- Consider if you're comfortable with concentration in these names

### Section 3: Sector Allocation

```
Technology:     26%
Healthcare:     11%
Consumer:       10%
Financials:     10%
Defense:         7%
Energy:          6%
Materials:       4%
```

**Interpretation:**
- No sector exceeds 30% (concentration rule)
- Technology represents growth (correct for 5-10 year horizon)
- Healthcare, Consumer provide stability/diversification
- Aligned with long-term structural trends

**Historical Comparison:**
- Track sector shifts quarter-to-quarter
- Large shifts indicate scoring changes or new market leaders
- Can reveal unintended drift toward single sector

### Section 4: Theme Allocation (ETFs)

```
AI & Cloud:          7.78%
Defense:             6.97%
Healthcare:          6.85%
Energy Transition:   6.39%
Cybersecurity:       3.24%
```

**Interpretation:**
- Represents exposure to 5 strategic themes
- Avoids single-security risk of direct stock picking
- Each theme has 2 qualified ETF options (concentrate or diversify)

**Action Items:**
- Decide if you want all 5 themes or prefer to focus
- Consider core/satellite: Keep all 5 or reduce to top 3?
- Monitor ETF holdings for theme drift

### Section 5: Core vs Satellite Split

```
Core (60%):      14 positions (highest conviction)
Satellite (40%): 15 positions (tactical bets)
```

**Interpretation:**
- **Core positions** - Top 50% by quality score, highest conviction
  - Should be 60% of portfolio by allocation
  - Hold for 5+ years
  - Monitor quarterly but don't trade frequently

- **Satellite positions** - Bottom 50% by quality score, tactical
  - Should be 40% of portfolio by allocation
  - Can be trimmed if position down 10%+
  - More flexible allocation rules

**Action Items:**
- Focus monitoring on core positions
- Be willing to add to core positions if opportunity arises
- Trim satellites if they underperform peers

---

## Allocation CSV: Detailed Breakdown

### Column Definitions

| Column | Meaning | Example |
|--------|---------|---------|
| **Rank** | Position in portfolio by allocation | 1, 2, 3... |
| **Ticker** | Stock or ETF symbol | AAPL, SOXX |
| **Type** | Stock or ETF | Stock, ETF |
| **Score** | Quality score (0-110) | 87.5 |
| **Allocation (%)** | Target allocation % | 3.97% |
| **Sector/Theme** | Industry or investment theme | Technology, AI & Cloud |
| **Regime/Bucket** | Core or Satellite | Core, Satellite |
| **Position Size ($1M)** | Dollar amount per $1M portfolio | $39,697 |

### How to Use the CSV

**For portfolio managers:**
```
# Extract allocations for your portfolio tool
awk -F',' '{print $2, $5}' allocation_model_YYYY_QQ.csv | tail -n +2
# Output: AAPL 3.97%, SOXX 3.96%, etc.
```

**For financial planning:**
```
# Total allocation for verification (should be 100%)
awk -F',' '{sum += $5} END {print sum}' allocation_model_YYYY_QQ.csv
```

**For sector analysis:**
```
# Group by sector
awk -F',' '{print $6, $5}' allocation_model_YYYY_QQ.csv | sort | uniq
```

---

## Rebalance Actions: What to Do

### Buy Recommendations

```
BUY (3 positions):
  LMT   → +2.13% (current 1.29%, target 3.42%)
  RTX   → +2.21% (current 1.14%, target 3.35%)
  AXP   → +2.25% (current 0.94%, target 3.20%)
```

**Interpretation:**
- These positions have drifted below target allocation
- Buy small amounts to bring back to target
- Action required only if drift > 2% threshold

**How to Execute:**
1. Don't panic buy - these are long-term positions
2. Spread purchases over several weeks if possible
3. Or buy all at once if you have new capital
4. Update your records (target allocation now = current)

### Sell Recommendations

```
SELL (0 positions):
  None - portfolio at target allocations
```

**Interpretation:**
- No positions have drifted above target by >2%
- No rebalancing sales needed this quarter
- Efficient portfolio (minimal drift)

**When Sells Appear:**
- Position has grown significantly (success!)
- Drift > 2% from target
- Trim to target allocation only
- Don't sell entire position (staying for 5-10 years)

### Hold Recommendations

```
HOLD (26 positions):
  MA   → drift 1.84% (current 1.72%, target 3.56%)
  AAPL → drift 1.83% (current 5.80%, target 3.97%)
  ...
```

**Interpretation:**
- These positions within ±2% of target
- No action needed - let them drift
- Reduces unnecessary trading
- Minimizes tax consequences

**When to Review:**
- If position hits +2.5% drift, consider trim
- If position hits -2.5% drift, consider small add
- At annual rebalance (year-end) reset all positions

---

## Thesis Invalidation Triggers

The system tracks 9 stock-specific and 5 ETF-specific exit triggers.

### Stock Invalidation Triggers (By Severity)

| Trigger | Category | Action | Threshold |
|---------|----------|--------|-----------|
| ROIC < WACC | Fundamental | 🔴 Critical Exit | Negative spread |
| Revenue Decline 2+ Q | Fundamental | 🔴 Critical Exit | 2 consecutive |
| Margin Compression >200bps | Fundamental | 🟠 Reduce 50% | 2% gross margin drop |
| Debt/EBITDA >4.0x | Fundamental | 🔴 Critical Exit | >4.0x leverage |
| Price <40W MA 3+ months | Technical | 🔴 Critical Exit | 3 months below |
| 3Y RS Turns Negative | Technical | 🟠 Reduce 50% | Multiple year underperformance |
| 5Y RS Turns Negative | Technical | 🔴 Critical Exit | Long-term underperformance |
| Score Drops >20 pts | Quality | 🟡 Monitor | >20 point decline |
| 12-Month Holding Patience | Time-based | 🟡 Monitor | <12 months old |

### Example: Tracking Apple (AAPL)

**Current Status:**
- ROIC: 42% > WACC 8% ✅
- 3Y Revenue Growth: +9.2% ✅
- Gross Margin: 43% (stable) ✅
- Debt/EBITDA: -0.8x (net cash) ✅
- Price vs 40W MA: +7% ✅
- 3Y RS: +52% vs SPY ✅
- 5Y RS: +112% vs SPY ✅

**Conclusion:** All triggers green. Hold position.

**If ROIC Dropped Below WACC:**
- Trigger: 🔴 Critical Exit
- Action: Sell entire position within 30 days
- Rationale: No longer creating shareholder value

**If Gross Margin Dropped 250 bps:**
- Trigger: 🟠 Reduce 50%
- Action: Sell 50% of position within 60 days
- Rationale: Pricing power weakening, monitor for further deterioration

---

## Common Questions & Answers

### Q: What if I don't have money to buy recommended positions?

**A:** No problem. The allocation assumes equal capital deployment, but:
- Hold what you have (don't sell positions to make room)
- When you get new capital, allocate per target weights
- Over time, portfolio will converge to recommendation
- Consider holding more of highest conviction (top 5)

### Q: Can I hold positions not on this list?

**A:** Yes, but understand the trade-offs:
- Added positions consume allocation % from list
- Reduces diversification/increases concentration
- May underperform (list is optimized)
- **Recommendation:** Keep 90%+ in list, 10% max "personal picks"

### Q: How often should I rebalance?

**A:** This system uses **annual rebalancing**:
- Review quarterly (this report)
- Rebalance only if drift > 2%
- Full rebalance once per year (year-end or Jan 15)
- Minimizes trading costs + taxes

### Q: What if I want to hold a position for 10+ years?

**A:** Perfect! This system is designed for 5-10+ year holds:
- Don't sell on short-term price movements
- Use annual rebalance to adjust drifts
- Monitor quarterly for invalidation triggers
- Most positions should be held 5-10+ years

### Q: Can I concentrate in my highest-conviction positions?

**A:** Moderately yes, but with caution:
- Portfolio rule: Max 10% per stock (hard limit)
- Core/satellite split allows higher convictions
- Over-concentration = over-risk
- **Better approach:** Keep core 5 at 4-5% each, let others be smaller

### Q: What if all my positions are down 20%?

**A:** Normal market cycle. Check:
- Did fundamentals change? (Check invalidation triggers)
- Is market (SPY) also down 20%? (If yes, normal)
- Are your positions still in uptrend > 40W MA?
- Any thesis invalidation triggers hit?

If no triggers hit: **Do nothing**. Long-term holds experience drawdowns.

---

## Integration with Your Trading

### Can I use this for swing trading?

**A:** Not designed for it, but compatible:
- System identifies 5-10 year compounders
- Can enter short-term trades from this list
- Higher quality companies = less downside risk
- **Recommendation:** Use daily momentum system for swings, hold core for decades

### Can I hold both short-term and long-term positions?

**A:** Yes! This is the dual-system philosophy:
- Short-term: Trade Minervini setups on swing time frame
- Long-term: Hold this compounder portfolio for 5-10 years
- **Ideal use:** Use compounder list as "swing trade universe" filter

---

## Monitoring Cadence

### Daily (2 minutes)
- Check market news for your top 5 positions
- Any major earnings surprises or management changes?
- Nothing to do, just stay informed

### Weekly (5 minutes)
- Review price moves of top 5 positions
- Any position > 10% off target? Plan rebalance
- Update personal notes on thesis validation

### Monthly (10 minutes)
- Analyze sector rotation trends
- Are new themes emerging? (Check ETF holdings)
- Any positions hitting invalidation triggers?

### Quarterly (30 minutes)
- **Read quarterly report in full**
- Compare to previous quarter (allocations changed? Why?)
- Review top 5 conviction theses
- Plan rebalancing (buy/sell if >2% drift)
- Update portfolio management system

### Annually (1-2 hours)
- Full rebalance - reset all positions to target allocation
- Review and update thesis notes for each position
- Evaluate overall portfolio performance vs SPY
- Plan for next year's holdings

---

## Performance Tracking

### Track These Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Total Return | (Current Value - Initial Value) / Initial | SPY + 3-5% |
| Volatility | Standard deviation of monthly returns | < 1.2x SPY |
| Drawdown | Max peak-to-trough decline | < 1.5x SPY |
| Sharpe Ratio | (Return - Risk-free) / Volatility | > 0.8 |
| Turnover | (Sum of sells) / Average portfolio value | < 20% annually |

### Compare Against Benchmarks

- **SPY** (S&P 500) - Total market return
- **QQQ** (Nasdaq-100) - Growth-heavy comparison
- **SPLG** (SPY aggregate) - Equal-weight S&P

**Goal:** Beat SPY by 3-5% annually with similar or lower volatility.

---

## Troubleshooting

### "This position is down 30%. Should I sell?"

**Steps:**
1. Check invalidation triggers (hit any red flags?)
2. Has the fundamental thesis changed?
3. Is SPY also down? (If yes, normal market)
4. Is price still above 40W MA? (If yes, trend intact)

If no triggers hit: **Hold and add if possible**. Market downturns are opportunities.

### "Portfolio allocation doesn't match recommendation."

**Causes:**
- New positions added (diluted allocation %)
- Dividend reinvestment (changed weights)
- Market gains/losses (prices moved, % changed)
- Data import error

**Fix:**
- Verify positions match list
- Check total allocation = 100%
- Rebalance if single position > 10%

### "I'm holding different stocks than recommendation."

**Options:**
- **Transition period** (1-2 quarters): Gradually sell old, buy new
- **Keep both** (if high conviction): Accept concentration
- **Immediate switch** (if poor fundamentals): Sell old, buy new now

---

## Advanced: Manual Portfolio Construction

If you want to modify the allocation:

### Adjusting Position Sizes

```
# Formula: Adjusted Allocation = (Base Score / Total Scores) * Available Capital
# Example: Position with score 87.5

Base allocation (87.5 / 2,000 total) * $1,000,000 = ~$43,750 (4.4%)

# Want only 3% instead? → $30,000 per position
# Want 5% instead? → $50,000 per position
```

### Sector-Specific Rebalancing

If one sector drifts >30%:
1. Calculate sector total allocation
2. Proportionally reduce largest positions
3. Maintain rank order (highest scores largest)
4. Verify no single position exceeds 10%

### Concentration Tiers

```
Tier 1 (Highest Conviction): 5-6% each
  └─ Top 5 scores: AAPL, MSFT, GOOGL, NVDA, UNH

Tier 2 (Core Holdings): 3-4% each
  └─ Scores 75-85: 10-15 positions

Tier 3 (Satellite): 1-3% each
  └─ Scores 60-74: Remaining positions
```

---

## Summary

The long-term compounder system provides:

✅ **Quarterly identification** of top 25 stocks + 10 ETFs
✅ **Objective scoring** (deterministic, transparent)
✅ **Portfolio optimization** (concentration rules, diversification)
✅ **Clear exit triggers** (invalidation framework)
✅ **Minimal rebalancing** (annual, tax-efficient)
✅ **5-10 year focus** (long-term wealth building)

Your job: Read the quarterly report, understand the thesis, monitor invalidation triggers, and rebalance annually.

The system does the heavy lifting of stock analysis and portfolio construction.

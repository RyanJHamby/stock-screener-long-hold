# Phase 6: GitHub Actions Automation

## Overview

Phase 6 implements **quarterly automated scanning** for the long-term compounder system using GitHub Actions.

**Schedule:** Jan 15, Apr 15, Jul 15, Oct 15 (quarterly reviews)
**Runtime:** ~20-30 minutes per scan
**Outputs:** Quarterly ownership reports + allocation CSVs

---

## Architecture

### Main Entry Point: `run_quarterly_compounder_scan.py`

**Orchestrates the complete pipeline:**

```
Step 1: Stock Universe
  └─ Fetch top 500 stocks by market cap

Step 2: Score Stocks
  └─ CompounderEngine (60/25/15 formula)
  └─ 500 stocks × ~100ms each = ~50 seconds

Step 3: Select Top Stocks
  └─ Top 25 by score

Step 4: Score ETFs
  └─ ETFEngine (30/40/20/10 formula)
  └─ 10-15 ETFs × ~50ms each = ~1 second

Step 5: Select Top ETFs
  └─ Top 10 by score

Step 6: Build Portfolio
  └─ PortfolioConstructor with concentration rules
  └─ Constraint validation

Step 7: Generate Reports
  └─ Ownership report (TXT)
  └─ Allocation CSV
  └─ Rebalance actions
  └─ Invalidation tracking
```

### GitHub Actions Workflow: `.github/workflows/quarterly_compounder_scan.yml`

**Automated trigger on schedule or manual dispatch:**

```yaml
name: Quarterly Compounder Scan

on:
  schedule:
    - cron: '0 9 15 1 *'   # January 15
    - cron: '0 9 15 4 *'   # April 15
    - cron: '0 9 15 7 *'   # July 15
    - cron: '0 9 15 10 *'  # October 15

  workflow_dispatch:  # Allow manual trigger
```

---

## Usage

### Manual Trigger (GitHub Web UI)

1. Go to: **Actions** → **Quarterly Compounder Scan**
2. Click: **Run workflow** → **Run workflow**
3. Monitor execution in real-time

### Manual Trigger (Command Line)

```bash
# Via GitHub CLI
gh workflow run quarterly_compounder_scan.yml

# Or manually run locally
python run_quarterly_compounder_scan.py
```

### Local Testing

```bash
# Test mode (10 stocks)
python run_quarterly_compounder_scan.py --test-mode

# Limit universe (50 stocks)
python run_quarterly_compounder_scan.py --limit 50

# Full production scan (500 stocks)
python run_quarterly_compounder_scan.py

# With custom logging and output
python run_quarterly_compounder_scan.py \
  --log-level DEBUG \
  --output-dir data/quarterly_reports
```

---

## Workflow Steps

### 1. Environment Setup

```yaml
- Set up Python 3.10
- Install dependencies (pandas, numpy, yfinance, etc.)
- Configure git for commits
```

### 2. Run Quarterly Scan

```yaml
runs: python run_quarterly_compounder_scan.py
timeout: 30 minutes
env: FMP_API_KEY (from secrets)
```

**What happens:**
- Fetches fundamental data for top 500 stocks (via FMP API)
- Fetches price data for all assets (via yfinance)
- Scores each stock with compounder engine
- Scores thematic ETFs
- Builds optimal portfolio
- Generates quarterly reports

### 3. Commit Reports to Git

```yaml
- Adds: data/quarterly_reports/allocation_model_*.csv
- Adds: data/quarterly_reports/ownership_report_*.txt
- Commits with message showing Q/year
- Pushes to repository
```

**Example commit message:**
```
chore: Quarterly compounder scan results Q1 2026

- Scored top 500 stocks with compounder engine
- Identified top 25 individual compounders
- Scored and selected top 10 thematic ETFs
- Built optimal portfolio with concentration rules
- Generated quarterly ownership reports
- Calculated rebalance actions

Automated by GitHub Actions quarterly_compounder_scan workflow.
```

### 4. Generate Artifacts

```yaml
- Uploads reports to workflow artifacts
- Retention: 90 days
- Available for download from Actions page
```

### 5. Error Handling

```yaml
On failure:
  - Creates GitHub issue with error details
  - Attaches workflow run link
  - Tags with 'scan-failure' label
  - Uploads partial artifacts for debugging
```

---

## Configuration

### Secrets (Required)

**Set in GitHub repository settings:**

```
FMP_API_KEY = <your_fmp_api_key>
```

**Steps to add:**
1. Go to: **Settings** → **Secrets and variables** → **Actions**
2. Click: **New repository secret**
3. Name: `FMP_API_KEY`
4. Value: Your FMP API key
5. Save

### Schedule (Customizable)

**To change quarterly schedule, edit workflow file:**

```yaml
on:
  schedule:
    - cron: '0 9 15 1 *'   # Jan 15 at 9 AM UTC
```

**Cron format:** `minute hour day month day_of_week`

**Common examples:**
- `'0 9 15 * *'` → Every 15th day at 9 AM UTC
- `'0 14 15 1,4,7,10 *'` → Quarterly at 2 PM UTC
- `'0 0 1 * *'` → First of every month at midnight UTC

---

## Outputs

### Generated Files

**Location:** `data/quarterly_reports/`

```
allocation_model_2026_Q1.csv
  ├─ Rank, Ticker, Type, Score
  ├─ Allocation %, Sector/Theme
  ├─ Regime/Bucket, Position Size ($1M)
  └─ 25-35 rows (stocks + ETFs)

ownership_report_2026_Q1.txt
  ├─ Portfolio Summary
  ├─ Top 5 Conviction Positions
  ├─ Sector Allocation
  ├─ Theme Allocation (ETFs)
  └─ Core vs Satellite Split
```

### Git History

```bash
# View all scans
git log --grep="Quarterly compounder scan"

# See what changed each quarter
git diff HEAD~1 data/quarterly_reports/

# Track allocation evolution
git log -p data/quarterly_reports/allocation_model_*.csv
```

---

## Monitoring

### GitHub Actions Dashboard

**View all quarterly scans:**
1. Go to: **Actions** tab
2. Click: **Quarterly Compounder Scan**
3. See workflow runs with status (✅ success / ❌ failure)
4. Click run to see detailed logs

### Workflow Artifacts

**Download reports after completion:**
1. Click on workflow run
2. Scroll to **Artifacts** section
3. Download `quarterly-reports` zip file
4. Contains all generated reports

### Email Notifications

**GitHub automatically notifies on:**
- Workflow failure (if enabled in settings)
- Issues created for scan failures
- Workflow completion (if subscribed)

---

## Troubleshooting

### Workflow Times Out

**Symptoms:** "Workflow exceeded maximum execution time"

**Solutions:**
- Reduce stock universe (`--limit 250`)
- Run in smaller batches
- Optimize data fetching with caching

### FMP API Key Not Found

**Symptoms:** "API Error: 401 Unauthorized"

**Solutions:**
1. Verify secret is set: Settings → Secrets → FMP_API_KEY
2. Verify key is valid (test locally)
3. Check for spaces or special characters in key

### Reports Not Committed to Git

**Symptoms:** "No changes to commit"

**Solutions:**
- Verify git configuration (user.email, user.name)
- Check write permissions on repository
- Review git error logs in workflow

### Out of Memory During Scoring

**Symptoms:** "Process killed (out of memory)"

**Solutions:**
- Reduce stock universe
- Increase runner resources (GitHub Pro)
- Optimize data structures

---

## Integration with Existing System

### Dual-Purpose Architecture

The quarterly compounder scan **coexists** with the existing short-term momentum system:

```
src/
├── screening/          # SHORT-TERM (existing)
│   ├── momentum_engine.py
│   ├── vcp_detector.py
│   └── entry_signals.py
│
└── long_term/          # LONG-TERM (Phase 4-6)
    ├── compounder_engine.py
    ├── etf_engine.py
    ├── portfolio_constructor.py
    └── report_generator.py
```

**Both systems:**
- Share data infrastructure (metrics, caching, FMP API)
- Use separate scoring philosophies
- Target different time horizons
- Can run independently or together

### Quarterly Review Process

**Typical workflow:**

1. **GitHub Actions triggers** quarterly scan (Jan 15, Apr 15, Jul 15, Oct 15)
2. **Top 25 stocks + 10 ETFs** identified and ranked
3. **Ownership report** generated with investment thesis
4. **CSV allocation** created for portfolio managers
5. **Invalidation triggers** tracked for next quarter
6. **Reports committed** to git for history tracking

---

## Example Outputs

### Allocation CSV (Sample)

```csv
Rank,Ticker,Type,Score,Allocation (%),Sector/Theme,Regime/Bucket,Position Size ($1M portfolio)
1,AAPL,Stock,87.5,3.97,Technology,Core,"$39,697"
2,SOXX,ETF,87.3,3.96,AI & Cloud,Core,"$39,606"
3,MSFT,Stock,85.2,3.87,Technology,Core,"$38,653"
...
25,TAN,ETF,68.5,2.15,Energy Transition,Satellite,"$21,500"
```

### Ownership Report (Sample)

```
================================================================================
LONG-TERM COMPOUNDER REPORT - Q1 2026
Generated: 2026-01-16
Investment Horizon: 5-10 Years
================================================================================

PORTFOLIO SUMMARY
Total Stocks: 25
Total ETFs: 10
Total Positions: 35
Portfolio Score: 78.2/100
Concentration (Herfindahl): 0.032
Rebalance Cadence: Annual

TOP 5 CONVICTION POSITIONS
1. AAPL   →  3.97% (Stock)
2. SOXX   →  3.96% (ETF)
3. MSFT   →  3.87% (Stock)
4. GOOGL  →  3.82% (Stock)
5. SMH    →  3.82% (ETF)
```

---

## Next Steps (Phase 7)

After Phase 6 automation is running:

1. **Update README** with new quarterly scan documentation
2. **Create example outputs** showing quarterly evolution
3. **Document methodology** with detailed scoring breakdowns
4. **Build user guide** for interpreting reports

---

## Summary

**Phase 6 enables:**
- ✅ Automated quarterly identification of long-term compounders
- ✅ Reproducible, deterministic scoring
- ✅ Git-based history tracking
- ✅ Easy manual trigger via GitHub UI
- ✅ Error notifications and artifacts
- ✅ Production-grade reliability

**Workflow runs quarterly** (Jan 15, Apr 15, Jul 15, Oct 15) with results committed to git for permanent tracking.

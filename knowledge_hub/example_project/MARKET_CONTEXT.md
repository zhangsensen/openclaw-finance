# Market Context — Example Project

> Every agent MUST read this file before starting work on this project.

## Project Overview
- **Name**: Example Stock Analysis
- **Market**: US Equities
- **Universe**: S&P 500 constituents
- **Date Range**: 2023-01-01 to 2025-12-31

## Data Sources
- **Price Data**: Daily OHLCV from your preferred provider
- **Fundamentals**: Quarterly earnings (if applicable)
- **Format**: Parquet files in `data/` directory

## Rules
1. Use only the data sources listed above
2. All dates must be in UTC
3. Include dividends and splits adjustments
4. Account for delisted stocks (no survivorship bias)

## Output Location
- Engineer data → `data/`
- Skeptic reports → `attribution/`
- Visualizer charts → `visuals/`
- Coordinator summaries → `integration/`

"""
Example: Stock Analysis Pipeline
This script demonstrates the data loading and analysis pattern
that the Engineer agent would execute.

Usage:
    python run_analysis.py --stock AAPL --start 2023-01-01 --end 2025-12-31
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Install dependencies: pip install pandas numpy")
    raise


def load_stock_data(filepath: str) -> pd.DataFrame:
    """Load stock data from parquet file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")

    df = pd.read_parquet(filepath)
    print(f"Loaded {len(df)} rows from {filepath}")
    return df


def validate_data(df: pd.DataFrame, stock: str) -> dict:
    """Validate data quality — the Skeptic agent would review this."""
    checks = {
        "stock": stock,
        "rows": len(df),
        "date_range": {
            "start": str(df["date"].min()) if "date" in df.columns else "unknown",
            "end": str(df["date"].max()) if "date" in df.columns else "unknown",
        },
        "null_counts": df.isnull().sum().to_dict(),
        "has_nulls": bool(df.isnull().any().any()),
        "columns": list(df.columns),
        "validated_at": datetime.now().isoformat(),
    }
    return checks


def calculate_metrics(df: pd.DataFrame) -> dict:
    """Calculate basic financial metrics."""
    if "close" not in df.columns:
        raise ValueError("DataFrame must have a 'close' column")

    close = df["close"]
    returns = close.pct_change().dropna()

    metrics = {
        "total_return": float((close.iloc[-1] / close.iloc[0]) - 1),
        "annualized_return": float(
            ((close.iloc[-1] / close.iloc[0]) ** (252 / len(close))) - 1
        ),
        "volatility": float(returns.std() * np.sqrt(252)),
        "sharpe_ratio": float(
            (returns.mean() * 252) / (returns.std() * np.sqrt(252))
        )
        if returns.std() > 0
        else 0.0,
        "max_drawdown": float(
            ((close / close.cummax()) - 1).min()
        ),
        "total_trading_days": len(close),
        "calculated_at": datetime.now().isoformat(),
    }
    return metrics


def generate_report(stock: str, validation: dict, metrics: dict) -> str:
    """Generate a markdown report — the Coordinator would integrate this."""
    report = f"""# {stock} Analysis Report

## Data Quality (Skeptic Validation)
- Rows: {validation['rows']}
- Date Range: {validation['date_range']['start']} to {validation['date_range']['end']}
- Has Nulls: {validation['has_nulls']}
- Validated: {validation['validated_at']}

## Key Metrics (Engineer Output)
| Metric | Value |
|--------|-------|
| Total Return | {metrics['total_return']:.2%} |
| Annualized Return | {metrics['annualized_return']:.2%} |
| Volatility | {metrics['volatility']:.2%} |
| Sharpe Ratio | {metrics['sharpe_ratio']:.2f} |
| Max Drawdown | {metrics['max_drawdown']:.2%} |
| Trading Days | {metrics['total_trading_days']} |

## Bias Checklist
- [ ] Survivorship bias: Are delisted stocks in the universe?
- [ ] Look-ahead bias: Does analysis use only past data?
- [ ] Selection bias: Why this stock and not others?
- [ ] Transaction costs: Slippage and commissions accounted for?

---
Generated: {datetime.now().isoformat()}
"""
    return report


def main():
    parser = argparse.ArgumentParser(description="Stock Analysis Pipeline")
    parser.add_argument("--stock", required=True, help="Stock ticker (e.g., AAPL)")
    parser.add_argument("--start", default="2023-01-01", help="Start date")
    parser.add_argument("--end", default="2025-12-31", help="End date")
    parser.add_argument("--data-dir", default="data", help="Data directory")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data_file = Path(args.data_dir) / f"{args.stock}.parquet"

    # Step 1: Load data (Engineer)
    print(f"\n[Engineer] Loading {args.stock} data...")
    try:
        df = load_stock_data(str(data_file))
    except FileNotFoundError:
        print(f"\n[Demo Mode] No data file found at {data_file}")
        print("In production, the Engineer agent would load real market data.")
        print("Creating sample structure for demonstration...\n")

        # Create sample data for demo purposes
        dates = pd.date_range(args.start, args.end, freq="B")
        np.random.seed(42)
        price = 150 * np.cumprod(1 + np.random.normal(0.0003, 0.015, len(dates)))
        df = pd.DataFrame(
            {
                "date": dates,
                "open": price * (1 + np.random.normal(0, 0.005, len(dates))),
                "high": price * (1 + abs(np.random.normal(0, 0.01, len(dates)))),
                "low": price * (1 - abs(np.random.normal(0, 0.01, len(dates)))),
                "close": price,
                "volume": np.random.randint(10_000_000, 100_000_000, len(dates)),
            }
        )

    # Step 2: Validate data (Skeptic)
    print(f"[Skeptic] Validating data quality...")
    validation = validate_data(df, args.stock)
    validation_path = output_dir / f"S01_{args.stock}_validation.json"
    with open(validation_path, "w") as f:
        json.dump(validation, f, indent=2, default=str)
    print(f"  → Saved: {validation_path}")

    # Step 3: Calculate metrics (Engineer)
    print(f"[Engineer] Calculating metrics...")
    metrics = calculate_metrics(df)
    metrics_path = output_dir / f"E01_{args.stock}_metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"  → Saved: {metrics_path}")

    # Step 4: Generate report (Coordinator integration)
    print(f"[Coordinator] Generating report...")
    report = generate_report(args.stock, validation, metrics)
    report_path = output_dir / f"I01_{args.stock}_report.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"  → Saved: {report_path}")

    print(f"\nAnalysis complete! Results in {output_dir}/")


if __name__ == "__main__":
    main()

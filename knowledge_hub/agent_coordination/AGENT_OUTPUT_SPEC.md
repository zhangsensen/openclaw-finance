# Agent Output Specification v1.0

> Single source of truth for how agents deliver work products.

## Core Rule
**All products must be delivered through files, never text-only messages.**

## Output Directory Structure

```
knowledge_hub/{project}/
├── data/           # Engineer outputs (JSON, CSV, Parquet)
├── attribution/    # Skeptic validation reports
├── visuals/        # Visualizer charts and reports
└── integration/    # Coordinator summaries
```

## File Naming Convention

Format: `{prefix}_{description}.{ext}`

| Agent | Prefix | Example |
|-------|--------|---------|
| Engineer | `E` + number | `E01_price_data.parquet` |
| Skeptic | `S` + number | `S01_bias_check.md` |
| Visualizer | `V` + number | `V01_price_trend.png` |
| Coordinator | `I` + number | `I01_analysis_summary.md` |

## Return Message Format

Every agent must include in their completion message:

```
## Task Complete
- **Task ID**: [spawned task reference]
- **Time**: [completion timestamp]
- **Output**: [absolute file path]
- **Summary**: [1-2 sentence result]
- **Verification**: [how the output was validated]
```

## Data Format Standards

| Type | Format | Use Case |
|------|--------|----------|
| Time series | Parquet | Price data, indicators |
| Metadata | JSON | Config, state, parameters |
| Tabular | CSV | Human-readable exports |
| Reports | Markdown | Analysis, validation |
| Charts | PNG (300 DPI) | Static visualizations |
| Interactive | HTML | Plotly dashboards |

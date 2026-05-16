# Day 42 — Outlier Detection
**84-Day Python & Excel Roadmap | Phase 3: Data Cleaning & Processing**
**Date:** May 16, 2026 | **Author:** Bhanu Pratap Singh

---

## What This Does
Detects anomalous/unusual values in financial datasets using three industry-standard methods.

## Files
| File | Purpose |
|---|---|
| `Day42_Outlier_Detection_Practice.xlsx` | Input: 3 sheets with planted outliers |
| `day42_outlier_detection.py` | Main script: 5 detection concepts |
| `Day42_Outlier_Results.xlsx` | Output: All sheets with outlier flags |

## Methods Implemented

| Method | When to Use | Key Formula |
|---|---|---|
| Z-Score | Normal distributions | `Z = (x − μ) / σ` |
| IQR | Skewed / robust | `fence = Q1−1.5×IQR to Q3+1.5×IQR` |
| Business Logic | Domain knowledge | Custom thresholds |
| Combined | High-confidence detection | Flagged by 2+ methods |
| Groupwise | Within-group comparison | `.transform()` for dept/sector Z-scores |

## Key pandas Functions Used
- `Series.mean()`, `Series.std()` — statistical moments
- `Series.quantile(0.25 / 0.75)` — IQR boundaries
- `Series.abs()` — absolute Z-score comparison
- `GroupBy.transform()` — group-level stats aligned to original index
- `pd.ExcelWriter` — multi-sheet export

## Portfolio Connection
→ Used in **Financial Dashboard (Day 78)** for data quality layer before charting.
→ Used in **Expense Tracker (Day 80)** to flag suspicious submissions automatically.

## Skills Demonstrated
- Statistical outlier detection (Z-Score, IQR)
- Business-rule validation
- Multi-method combined flagging
- Groupwise analysis with `.transform()`
- Clean multi-sheet Excel export

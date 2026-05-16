"""
Day 42: Outlier Detection
Techniques: Z-Score, IQR, Business Logic, Groupwise Detection
Dataset: Employee Expenses, Stock Returns, Salary Data
"""

import pandas as pd
import numpy as np

# ─── LOAD DATA ─────────────────────────────────────────────────────────────────
FILE = "Day42_Outlier_Detection_Practice.xlsx"

expenses = pd.read_excel(FILE, sheet_name="Employee_Expenses")
stocks   = pd.read_excel(FILE, sheet_name="Stock_Returns")
salary   = pd.read_excel(FILE, sheet_name="Salary_Data")

print("=" * 60)
print("DAY 42: OUTLIER DETECTION")
print("=" * 60)

# ══════════════════════════════════════════════════════════════════════
# CONCEPT 1: Z-SCORE METHOD
# Formula: Z = (value - mean) / standard_deviation
# Rule   : |Z| > 3  →  outlier  (3 std deviations from the mean)
# Best for: Normally distributed data
# ══════════════════════════════════════════════════════════════════════

print("\n── CONCEPT 1: Z-SCORE (Employee Expenses) ──")

col  = "Amount_INR"
mean = expenses[col].mean()
std  = expenses[col].std()

expenses["Z_Score"]  = (expenses[col] - mean) / std
expenses["Z_Outlier"] = expenses["Z_Score"].abs() > 3

z_out = expenses[expenses["Z_Outlier"]]
print(f"  Mean   : ₹{mean:,.0f}")
print(f"  Std Dev: ₹{std:,.0f}")
print(f"\n  Outliers (|Z| > 3):")
print(z_out[["Emp_ID", "Employee_Name", "Amount_INR", "Z_Score"]].to_string(index=False))


# ══════════════════════════════════════════════════════════════════════
# CONCEPT 2: IQR METHOD
# Q1 = 25th percentile  |  Q3 = 75th percentile
# IQR = Q3 − Q1
# Lower Fence = Q1 − 1.5 × IQR
# Upper Fence = Q3 + 1.5 × IQR
# Values outside fences = outliers
# Best for: Skewed data — robust, no assumption of normal distribution
# ══════════════════════════════════════════════════════════════════════

print("\n── CONCEPT 2: IQR METHOD (Stock Returns) ──")

ret = "Daily_Return_%"
Q1  = stocks[ret].quantile(0.25)
Q3  = stocks[ret].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

stocks["IQR_Outlier"] = (stocks[ret] < lower) | (stocks[ret] > upper)

iqr_out = stocks[stocks["IQR_Outlier"]]
print(f"  Q1={Q1:.2f}%  Q3={Q3:.2f}%  IQR={IQR:.2f}")
print(f"  Fences: [{lower:.2f}%, {upper:.2f}%]")
print(f"\n  Outliers (outside fences):")
print(iqr_out[["Stock", "Date", "Daily_Return_%"]].to_string(index=False))


# ══════════════════════════════════════════════════════════════════════
# CONCEPT 3: BUSINESS LOGIC THRESHOLDS
# Rules defined by domain knowledge, not statistics.
# Examples for finance:
#   Expense > ₹50,000  → needs manager approval / likely fraud
#   Expense < 0        → invalid (negative expense is impossible)
#   Salary > 100 LPA   → review — possible data entry error
#   Stock return > 20% in a single day → flag for audit
# ══════════════════════════════════════════════════════════════════════

print("\n── CONCEPT 3: BUSINESS LOGIC (Salary Data) ──")

salary["BL_High"] = salary["Salary_LPA"] > 100
salary["BL_Low"]  = salary["Salary_LPA"] < 1
salary["BL_Outlier"] = salary["BL_High"] | salary["BL_Low"]

bl_out = salary[salary["BL_Outlier"]]
print("  Rules: Salary > 100 LPA  OR  Salary < 1 LPA")
print(f"\n  Outliers:")
print(bl_out[["Emp_ID", "Role", "Salary_LPA", "BL_High", "BL_Low"]].to_string(index=False))


# ══════════════════════════════════════════════════════════════════════
# CONCEPT 4: COMBINING ALL METHODS
# Best practice: flag rows caught by 2+ methods → high confidence
# ══════════════════════════════════════════════════════════════════════

print("\n── CONCEPT 4: COMBINED DETECTION (Expenses) ──")

Q1e  = expenses[col].quantile(0.25)
Q3e  = expenses[col].quantile(0.75)
IQRe = Q3e - Q1e

expenses["IQR_Outlier"] = (
    (expenses[col] < Q1e - 1.5 * IQRe) |
    (expenses[col] > Q3e + 1.5 * IQRe)
)
expenses["BL_Outlier"] = (expenses[col] > 50000) | (expenses[col] < 0)

# Count methods that flagged each row
expenses["Flags"] = (
    expenses["Z_Outlier"].astype(int)  +
    expenses["IQR_Outlier"].astype(int) +
    expenses["BL_Outlier"].astype(int)
)

combined = expenses[expenses["Flags"] >= 2]
print("  Rows flagged by 2+ methods (high confidence):")
print(combined[["Emp_ID", "Employee_Name", "Amount_INR", "Flags"]].to_string(index=False))


# ══════════════════════════════════════════════════════════════════════
# CONCEPT 5: GROUPWISE OUTLIER DETECTION using .transform()
# Don't compare all rows globally.
# Compare each row against its own group (dept, sector, etc.)
# Use .transform() — it returns a Series aligned with the original df
# This preserves all columns (unlike groupby+apply which can drop keys)
# ══════════════════════════════════════════════════════════════════════

print("\n── CONCEPT 5: GROUPWISE Z-SCORE via .transform() ──")

dept_mean = expenses.groupby("Department")[col].transform("mean")
dept_std  = expenses.groupby("Department")[col].transform("std")

expenses["Dept_Z"]  = (expenses[col] - dept_mean) / dept_std
expenses["Dept_Out"] = expenses["Dept_Z"].abs() > 2   # tighter threshold within groups

dept_out = expenses[expenses["Dept_Out"]]
print("  Z > 2 within each department:")
print(dept_out[["Emp_ID", "Department", "Amount_INR", "Dept_Z"]].to_string(index=False))


# ─── EXPORT ───────────────────────────────────────────────────────────────────
print("\n── EXPORTING RESULTS ──")

with pd.ExcelWriter("Day42_Outlier_Results.xlsx", engine="openpyxl") as writer:
    expenses.to_excel(writer, sheet_name="Expense_Flags", index=False)
    stocks.to_excel(  writer, sheet_name="Stock_Flags",   index=False)
    salary.to_excel(  writer, sheet_name="Salary_Flags",  index=False)

print("  Saved → Day42_Outlier_Results.xlsx")
print("\n[Day 42 Complete]")

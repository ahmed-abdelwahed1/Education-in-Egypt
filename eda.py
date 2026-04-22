"""
=======================================================================
  Data Analysis Course Project — Exploratory Data Analysis (EDA)
  Dataset : Education in Egypt
  Source  : https://www.kaggle.com/datasets/mohamedalabasy/education-in-egypt
  Student : Ahmed Shehata Said Abdelwahed  |  3rd Year
=======================================================================

  Description
  -----------
  This script performs a full exploratory data analysis on a dataset of
  50,000 Egyptian students across three education systems (Thanweya,
  IGCSE, IB).  It covers:

    Step 1  — Loading & initial inspection
    Step 2  — Descriptive statistics
    Step 3  — Feature engineering (average grade per student)
    Step 4  — Education-type distribution        (donut chart)
    Step 5  — Student-age distribution            (bar chart)
    Step 6  — Average grade by demographic group  (2x2 bar chart)
    Step 7  — Per-subject average grades           (bar chart)
    Step 8  — Overall grade distribution          (histogram)
    Step 9  — Inter-subject correlation           (heatmap)
    Step 10 — Key findings summary

  Libraries Used
  --------------
  - pandas   : data loading, manipulation, aggregation
  - numpy    : numerical computations, array operations
  - matplotlib : all chart creation (bar, pie, histogram)
  - seaborn  : correlation heatmap styling

  How to Run
  ----------
    pip install -r requirements.txt
    python eda.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend (no GUI window)
import matplotlib.pyplot as plt
import seaborn as sns

# ─── Configuration ──────────────────────────────────────────────────────
DATA_PATH   = os.path.join("data", "dataset.csv")
PLOTS_DIR   = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

HEADER = """
================================================================
   Data Analysis Course — Exploratory Data Analysis Project
   Student: Ahmed Shehata Said Abdelwahed  |  3rd Year
   Dataset: Education in Egypt (Kaggle)
================================================================
"""


# =====================================================================
#  STEP 1 — Load & Inspect the Dataset
# =====================================================================
print(HEADER)
print("=" * 64)
print("  STEP 1: Loading & Inspecting the Dataset")
print("=" * 64)

df = pd.read_csv(DATA_PATH)

print(f"\n  Shape : {df.shape[0]:,} rows  x  {df.shape[1]} columns")
print(f"\n  First 5 rows:")
print(df.head().to_string(index=True))
print(f"\n  Data types:")
print(df.dtypes.to_string())
print(f"\n  Missing values per column:")
print(df.isnull().sum().to_string())


# =====================================================================
#  STEP 2 — Descriptive Statistics
# =====================================================================
print("\n\n" + "=" * 64)
print("  STEP 2: Descriptive Statistics")
print("=" * 64)

print("\n  Numerical summary (describe):")
print(df.describe().to_string())

print("\n  Education Type distribution:")
print(df["Education Type"].value_counts().to_string())

print("\n  Father Degree distribution (including NaN):")
print(df["Father Degree"].value_counts(dropna=False).to_string())

print("\n  Mother Degree distribution (including NaN):")
print(df["Mother Degree"].value_counts(dropna=False).to_string())

print("\n  Student Year distribution:")
print(df["Student year"].value_counts().to_string())

print("\n  Student Age distribution:")
print(df["Student Age"].value_counts().sort_index().to_string())


# =====================================================================
#  STEP 3 — Feature Engineering: Average Grade per Student
# =====================================================================
print("\n\n" + "=" * 64)
print("  STEP 3: Computing Average Grade per Student")
print("=" * 64)

subject_cols = [f"Subject_{i}" for i in range(1, 11)]
df["avg_grade"] = df[subject_cols].mean(axis=1)

print(f"\n  New column 'avg_grade' created.")
print(f"  avg_grade statistics:")
print(f"    Mean   : {df['avg_grade'].mean():.2f}%")
print(f"    Median : {df['avg_grade'].median():.2f}%")
print(f"    Std    : {df['avg_grade'].std():.2f}%")
print(f"    Min    : {df['avg_grade'].min():.2f}%")
print(f"    Max    : {df['avg_grade'].max():.2f}%")


# =====================================================================
#  STEP 4 — Plot 1: Education Type Distribution (Donut Chart)
# =====================================================================
print("\n\n" + "=" * 64)
print("  STEP 4: Plotting Education Type Distribution")
print("=" * 64)

edu_counts = df["Education Type"].value_counts()

fig, ax = plt.subplots(figsize=(7, 5))
colors_edu = ["#378ADD", "#1D9E75", "#D85A30"]
wedges, texts, autotexts = ax.pie(
    edu_counts,
    labels=edu_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors_edu,
    wedgeprops=dict(width=0.5, edgecolor="white", linewidth=2),
    textprops=dict(fontsize=11),
)
for t in autotexts:
    t.set_fontweight("bold")
ax.set_title("Education Type Distribution", fontsize=13, fontweight="bold", pad=15)
plt.tight_layout()
path = os.path.join(PLOTS_DIR, "plot_edu_type.png")
plt.savefig(path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  -> Saved: {path}")


# =====================================================================
#  STEP 5 — Plot 2: Student Age Distribution (Bar Chart)
# =====================================================================
print("\n\n" + "=" * 64)
print("  STEP 5: Plotting Student Age Distribution")
print("=" * 64)

age_counts = df["Student Age"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(
    age_counts.index.astype(str), age_counts.values,
    color="#378ADD", edgecolor="white", linewidth=1.2,
)
# Add count labels on top of each bar
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
        f"{int(bar.get_height()):,}", ha="center", va="bottom",
        fontsize=10, fontweight="bold",
    )
ax.set_xlabel("Age", fontsize=11)
ax.set_ylabel("Number of Students", fontsize=11)
ax.set_title("Student Age Distribution", fontsize=13, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
path = os.path.join(PLOTS_DIR, "plot_age_dist.png")
plt.savefig(path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  -> Saved: {path}")


# =====================================================================
#  STEP 6 — Plot 3: Average Grade by Category (2x2 Grouped Bar Chart)
# =====================================================================
print("\n\n" + "=" * 64)
print("  STEP 6: Plotting Average Grade by Demographic Category")
print("=" * 64)

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
categories = [
    ("Education Type", axes[0, 0], "#378ADD"),
    ("Student year",   axes[0, 1], "#1D9E75"),
    ("Father Degree",  axes[1, 0], "#D85A30"),
    ("Mother Degree",  axes[1, 1], "#BA7517"),
]

for col, ax, color in categories:
    grp = df.groupby(col)["avg_grade"].mean().sort_values(ascending=False)
    bars = ax.barh(grp.index, grp.values, color=color, edgecolor="white", height=0.6)
    ax.set_xlim(74.4, 74.9)
    ax.set_xlabel("Average Grade (%)", fontsize=10)
    ax.set_title(f"Average Grade by {col}", fontsize=11, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # Add value labels
    for bar in bars:
        ax.text(
            bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width():.2f}%", va="center", fontsize=9,
        )

fig.suptitle(
    "Average Grade by Demographic Category",
    fontsize=14, fontweight="bold", y=1.02,
)
plt.tight_layout()
path = os.path.join(PLOTS_DIR, "plot_avg_by_category.png")
plt.savefig(path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  -> Saved: {path}")


# =====================================================================
#  STEP 7 — Plot 4: Per-Subject Average Grades (Bar Chart)
# =====================================================================
print("\n\n" + "=" * 64)
print("  STEP 7: Plotting Per-Subject Average Grades")
print("=" * 64)

subj_means = df[subject_cols].mean().sort_values()

fig, ax = plt.subplots(figsize=(10, 5))
colors_subj = plt.cm.tab10.colors[: len(subj_means)]
bars = ax.bar(subj_means.index, subj_means.values, color=colors_subj, edgecolor="white")
ax.set_ylim(74.0, 75.2)
ax.set_ylabel("Mean Grade (%)", fontsize=11)
ax.set_title("Average Grade per Subject", fontsize=13, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
# Add labels on top
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
        f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=9,
    )
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
path = os.path.join(PLOTS_DIR, "plot_subject_avgs.png")
plt.savefig(path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  -> Saved: {path}")


# =====================================================================
#  STEP 8 — Plot 5: Overall Grade Distribution (Histogram)
# =====================================================================
print("\n\n" + "=" * 64)
print("  STEP 8: Plotting Overall Grade Distribution")
print("=" * 64)

all_grades = df[subject_cols].values.flatten()

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(
    all_grades, bins=20, color="#378ADD",
    edgecolor="white", linewidth=0.8, alpha=0.9,
)
ax.axvline(
    np.mean(all_grades), color="#D85A30", linestyle="--", linewidth=2,
    label=f"Mean = {np.mean(all_grades):.1f}%",
)
ax.set_xlabel("Grade (%)", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.set_title("Overall Grade Distribution (All Subjects Combined)", fontsize=13, fontweight="bold")
ax.legend(fontsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
path = os.path.join(PLOTS_DIR, "plot_grade_dist.png")
plt.savefig(path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  -> Saved: {path}")


# =====================================================================
#  STEP 9 — Plot 6: Inter-Subject Correlation Heatmap
# =====================================================================
print("\n\n" + "=" * 64)
print("  STEP 9: Plotting Inter-Subject Correlation Heatmap")
print("=" * 64)

corr = df[subject_cols].corr()

fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(
    corr, annot=True, fmt=".2f", cmap="coolwarm",
    center=0, linewidths=0.5, ax=ax,
    square=True, cbar_kws={"shrink": 0.8},
)
ax.set_title(
    "Inter-Subject Correlation Matrix",
    fontsize=13, fontweight="bold", pad=15,
)
plt.tight_layout()
path = os.path.join(PLOTS_DIR, "plot_corr_heatmap.png")
plt.savefig(path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  -> Saved: {path}")


# =====================================================================
#  STEP 10 — Key Findings Summary
# =====================================================================
print("\n\n" + "=" * 64)
print("  STEP 10: Key Findings Summary")
print("=" * 64)

print(f"""
  Total students       : {len(df):,}
  Overall mean grade   : {df[subject_cols].mean().mean():.2f}%
  Overall std grade    : {df[subject_cols].std().mean():.2f}%
  Grade range          : {df[subject_cols].min().min():.0f}% - {df[subject_cols].max().max():.0f}%

  Missing Data:
    Father Degree      : {df['Father Degree'].isnull().sum():,} ({df['Father Degree'].isnull().mean()*100:.1f}%)
    Mother Degree      : {df['Mother Degree'].isnull().sum():,} ({df['Mother Degree'].isnull().mean()*100:.1f}%)

  Average Grade by Education Type:
{df.groupby('Education Type')['avg_grade'].mean().to_string()}

  Average Grade by Father Degree:
{df.groupby('Father Degree')['avg_grade'].mean().sort_values(ascending=False).to_string()}

  Average Grade by Mother Degree:
{df.groupby('Mother Degree')['avg_grade'].mean().sort_values(ascending=False).to_string()}
""")

off_diag = corr.where(~np.eye(len(corr), dtype=bool)).abs().max().max()
print(f"  Max inter-subject correlation (off-diagonal): {off_diag:.4f}")

print("\n" + "=" * 64)
print("  All 6 plots saved to the 'plots/' directory.")
print("  EDA complete.")
print("=" * 64)

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / 'data' / "survey_responses_cleaned.csv"

data = pd.read_csv(DATA_PATH)

# Q3.1

print('='*50,"Q3.1",'='*50)
layout_count = data['desired_layout'].value_counts().sort_values(ascending=False)
layout_pct = data['desired_layout'].value_counts(normalize=True).sort_values(ascending=False)

print(layout_count)
print(layout_pct)

# Q3.2

print('='*50,"Q3.2",'='*50)
exp_mean = data['exp_score'].mean()
exp_median = data['exp_score'].median()
ui_ux_mean = data['ui_ux_score'].mean()
ui_ux_median = data['ui_ux_score'].median()

print("exp_score")
print("Mean:", exp_mean)
print("Median:", exp_median)
print("ui_ux_score")
print("Mean:", ui_ux_mean)
print("Median:", ui_ux_median)
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / 'data' / "survey_responses_cleaned.csv"

data = pd.read_csv(DATA_PATH)

# Q1.1

print('='*50,"Q1.1",'='*50)
role_count = data.groupby("current_role").size().sort_values(ascending=False)
role_pct = data["current_role"].value_counts(normalize=True).sort_values(ascending=False)

print(role_count)
print(role_pct)

# Q1.2

print('='*50,"Q1.2",'='*50)
data["primary_goal"] = data["primary_goal"].str.split(r",\s*(?![^()]*\))")
goal_exploded = data.explode(column="primary_goal", ignore_index=True)
goal_exploded['primary_goal'] = goal_exploded['primary_goal'].str.strip()

goal_num = goal_exploded.groupby('primary_goal').size().sort_values(ascending=False)
goal_pct = goal_num / goal_exploded.shape[0]
goal_pct_by_role = goal_exploded.groupby('current_role')['primary_goal'].value_counts(normalize=True).reset_index().sort_values(by=['current_role','proportion'], ascending=False)

print(goal_pct)
print(goal_pct_by_role)

# Q1.3

print('='*50,"Q1.3",'='*50)
source_pct = data['source'].value_counts(normalize=True).sort_values(ascending=False)

print(source_pct)


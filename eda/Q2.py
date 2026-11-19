import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / 'data' / "survey_responses_cleaned.csv"

data = pd.read_csv(DATA_PATH)

# Q2.1

print('='*50,"Q1.2",'='*50)
data["pain_points"] = data["pain_points"].str.split(r",\s*(?![^()]*\))")
pain_exploded = data.explode(column="pain_points", ignore_index=True)
pain_exploded['pain_points'] = pain_exploded['pain_points'].str.strip()

valid_points = pain_exploded.groupby('pain_points').size()
valid_points = valid_points[valid_points > 1].reset_index()

mask = pain_exploded['pain_points'].isin(valid_points['pain_points'])
valid_pain_exploded = pain_exploded[mask][['current_role','pain_points']]

points_num = valid_pain_exploded.groupby('pain_points').size().sort_values(ascending=False)
points_pct = points_num / valid_pain_exploded.shape[0]
points_pct_by_role = valid_pain_exploded.groupby('current_role')['pain_points'].value_counts(normalize=True).reset_index().sort_values(by=['current_role','proportion'], ascending=False)

# print(points_pct)
# print(points_pct_by_role)

# Q2.2

print('='*50,"Q2.2",'='*50)
data["desired_courses"] = data["desired_courses"].str.split(r",\s*(?![^()]*\))")
courses_exploded = data.explode(column="desired_courses", ignore_index=True)
courses_exploded['desired_courses'] = courses_exploded['desired_courses'].str.strip()

valid_c = courses_exploded.groupby('desired_courses').size()
valid_c = valid_c[valid_c > 1].reset_index()

mask = courses_exploded['desired_courses'].isin(valid_c['desired_courses'])
valid_c_exploded = courses_exploded[mask][['current_role','desired_courses']]

courses_num = valid_c_exploded.groupby('desired_courses').size().sort_values(ascending=False)
courses_pct = courses_num / valid_c_exploded.shape[0]
courses_pct_by_role = valid_c_exploded.groupby('current_role')['desired_courses'].value_counts(normalize=True).reset_index().sort_values(by=['current_role','proportion'], ascending=False)

# print(courses_pct)
# print(courses_pct_by_role)

# Q2.3

data["selection_criteria"] = data["selection_criteria"].str.split(r",\s*(?![^()]*\))")
select_exploded = data.explode(column="selection_criteria", ignore_index=True)
select_exploded['selection_criteria'] = select_exploded['selection_criteria'].str.strip()
select_pct = select_exploded['selection_criteria'].value_counts(normalize=True).sort_values(ascending=False)

print(select_pct)


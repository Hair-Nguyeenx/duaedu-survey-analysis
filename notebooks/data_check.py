"""
data_check.py — Kiểm tra chất lượng dữ liệu thô (raw data)
Chạy file này TRƯỚC data_cleaning.py để nắm toàn cảnh vấn đề.
"""

import pandas as pd
import os

# ============================================================
# 1. LOAD DATA
# ============================================================
RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "survey_responses_cleaned.csv")
df = pd.read_csv(RAW_PATH, encoding="utf-8")

print("=" * 60)
print("1. TỔNG QUAN DATASET")
print("=" * 60)
print(f"Số dòng  : {df.shape[0]}")
print(f"Số cột   : {df.shape[1]}")
print(f"Tên cột  : {list(df.columns)}")
print()

# ============================================================
# 2. KIỂU DỮ LIỆU
# ============================================================
print("=" * 60)
print("2. KIỂU DỮ LIỆU TỪNG CỘT")
print("=" * 60)
print(df.dtypes.to_string())
print()

# ============================================================
# 3. NULL / BLANK CHECK
# ============================================================
print("=" * 60)
print("3. TỶ LỆ NULL / BLANK TỪNG CỘT")
print("=" * 60)

null_stats = pd.DataFrame({
    "null_count": df.isnull().sum(),
    "blank_count": df.apply(lambda col: col.astype(str).str.strip().eq("").sum()),
})
null_stats["total_missing"] = null_stats["null_count"] + null_stats["blank_count"]
null_stats["missing_pct"] = (null_stats["total_missing"] / len(df) * 100).round(2)
print(null_stats.to_string())
print()

# ============================================================
# 4. DUPLICATE CHECK (theo email)
# ============================================================
print("=" * 60)
print("4. KIỂM TRA DUPLICATE (theo email_address)")
print("=" * 60)

if "email_address" in df.columns:
    df_email = df[df["email_address"].notna() & (df["email_address"].str.strip() != "")]
    email_lower = df_email["email_address"].str.strip().str.lower()
    dup_emails = email_lower[email_lower.duplicated(keep=False)]

    if dup_emails.empty:
        print("Không có email trùng lặp.")
    else:
        dup_counts = dup_emails.value_counts()
        print(f"Số email trùng   : {dup_counts.shape[0]}")
        print(f"Tổng dòng trùng  : {dup_emails.shape[0]}")
        print()
        print("Chi tiết:")
        print(dup_counts.to_string())

    blank_email = df["email_address"].isna() | (df["email_address"].str.strip() == "")
    print(f"\nSố dòng email trống: {blank_email.sum()}")
else:
    print("Cột email_address không tồn tại.")
print()

# ============================================================
# 5. GIÁ TRỊ DUY NHẤT CỘT SINGLE-SELECT
# ============================================================
print("=" * 60)
print("5. GIÁ TRỊ DUY NHẤT — CỘT SINGLE-SELECT")
print("=" * 60)

single_select_cols = ["current_role", "desired_layout", "source"]
for col in single_select_cols:
    if col not in df.columns:
        continue
    vals = df[col].dropna().str.strip()
    vc = vals.value_counts()
    print(f"\n--- {col} ({vc.shape[0]} giá trị) ---")
    print(vc.to_string())
print()

# ============================================================
# 6. PHÂN BỐ ĐIỂM ĐÁNH GIÁ
# ============================================================
print("=" * 60)
print("6. PHÂN BỐ ĐIỂM ĐÁNH GIÁ")
print("=" * 60)

score_cols = ["exp_score", "ui_ux_score"]
for col in score_cols:
    if col not in df.columns:
        continue
    print(f"\n--- {col} ---")
    print(f"  Mean   : {df[col].mean():.2f}")
    print(f"  Median : {df[col].median():.1f}")
    print(f"  Std    : {df[col].std():.2f}")
    print(f"  Min    : {df[col].min()}")
    print(f"  Max    : {df[col].max()}")
    print(f"  Phân bố:")
    print(df[col].value_counts().sort_index().to_string())
print()

# ============================================================
# 7. KIỂM TRA TIMESTAMP
# ============================================================
print("=" * 60)
print("7. KIỂM TRA TIMESTAMP")
print("=" * 60)

ts = pd.to_datetime(df["timestamp"], format="%d/%m/%Y", errors="coerce")
failed = ts.isna().sum()
print(f"Parse thành công : {ts.notna().sum()}")
print(f"Parse thất bại   : {failed}")
if failed > 0:
    bad_idx = ts[ts.isna()].index.tolist()
    print(f"Dòng lỗi (index) : {bad_idx[:10]}")
    for i in bad_idx[:5]:
        print(f"  [{i}] {df.loc[i, 'timestamp']}")
if ts.notna().any():
    print(f"Earliest         : {ts.min()}")
    print(f"Latest           : {ts.max()}")
print()

# ============================================================
# 8. KIỂM TRA KHOẢNG TRẮNG THỪA
# ============================================================
print("=" * 60)
print("8. KHOẢNG TRẮNG THỪA (leading/trailing)")
print("=" * 60)

text_cols = df.select_dtypes(include="object").columns
for col in text_cols:
    has_space = df[col].dropna().apply(lambda x: x != x.strip())
    count = has_space.sum()
    if count > 0:
        print(f"  {col}: {count} dòng có khoảng trắng thừa")

if all(
    df[col].dropna().apply(lambda x: x == x.strip()).all()
    for col in text_cols
):
    print("  Không phát hiện khoảng trắng thừa.")
print()

# ============================================================
# 9. SAMPLE DATA
# ============================================================
print("=" * 60)
print("9. 5 DÒNG ĐẦU TIÊN")
print("=" * 60)
print(df.head().to_string())
print()
print("Done.")

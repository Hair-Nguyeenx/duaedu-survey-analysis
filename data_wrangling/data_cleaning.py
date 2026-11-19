"""
data_cleaning.py — Làm sạch dữ liệu survey DUA Edu
Input  : data/survey_responses_raw.csv
Output : data/survey_responses_cleaned.csv
"""

import pandas as pd
import os
import re

# ============================================================
# 1. LOAD RAW DATA
# ============================================================
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RAW_PATH = os.path.join(BASE_DIR, "data", "survey_responses_raw.csv")
CLEAN_PATH = os.path.join(BASE_DIR, "data", "survey_responses_cleaned.csv")

df = pd.read_csv(RAW_PATH, encoding="utf-8")
print(f"[1] Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ============================================================
# 2. LOẠI BỎ CỘT PII (email_address)
# ============================================================
# Giữ lại email tạm để xử lý duplicate, loại bỏ sau
email_col = df["email_address"].str.strip().str.lower()
print(f"[2] Cột email_address sẽ bị loại bỏ sau bước xử lý duplicate")

# ============================================================
# 3. XỬ LÝ DUPLICATE (theo email)
# ============================================================
# Chiến lược: giữ response cuối cùng (mới nhất) cho mỗi email
df["email_address"] = email_col

# Parse timestamp trước để sắp xếp
df["_ts_parsed"] = pd.to_datetime(
    df["timestamp"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
)

# Dòng có email trống: luôn giữ
mask_blank_email = df["email_address"].isna() | (df["email_address"] == "")
df_blank = df[mask_blank_email].copy()

# Dòng có email: giữ response cuối cùng
df_with_email = df[~mask_blank_email].copy()
df_with_email = df_with_email.sort_values("_ts_parsed", ascending=True)
before_dedup = len(df_with_email)
df_with_email = df_with_email.drop_duplicates(subset="email_address", keep="last")
after_dedup = len(df_with_email)

df = pd.concat([df_with_email, df_blank], ignore_index=True)
df = df.sort_values("_ts_parsed", ascending=True).reset_index(drop=True)

removed = before_dedup - after_dedup
print(f"[3] Xử lý duplicate: loại {removed} dòng trùng email, giữ response mới nhất")

# ============================================================
# 4. TRIM KHOẢNG TRẮNG TẤT CẢ CỘT TEXT
# ============================================================
text_cols = df.select_dtypes(include="object").columns.tolist()
for col in text_cols:
    df[col] = df[col].str.strip()
print(f"[4] Trim khoảng trắng: {len(text_cols)} cột text")

# ============================================================
# 5. CHUẨN HÓA NULL / BLANK
# ============================================================
# Chuyển chuỗi rỗng thành NaN
for col in text_cols:
    df[col] = df[col].replace("", pd.NA)
print(f"[5] Chuyển chuỗi rỗng thành NaN")

# ============================================================
# 6. CHUẨN HÓA CỘT SOURCE BẰNG REGEX
# ============================================================
# Danh sách giá trị gốc chuẩn từ form khảo sát
STANDARD_SOURCES = [
    'Group "GenZ làm Data"',
    "Thread",
    "Qua group Zalo",
    "Người quen giới thiệu",
    "Chưa biết đến website",
]

fb_pattern = r"(?i)\b(facebook|fb)\b"

def normalize_source(val):
    if pd.isna(val):
        return val
    if re.search(fb_pattern, str(val)):
        return "Facebook"
    if val in STANDARD_SOURCES:
        return val
    return "Khác"

df["source"] = df["source"].apply(normalize_source)
print(f"[6] Chuẩn hóa cột source: gom Facebook, giữ giá trị gốc, còn lại gán 'Khác'")

# ============================================================
# 7. CHUẨN HÓA CỘT CURRENT_ROLE
# ============================================================
# Gom các giá trị lẻ (< 5 lần) vào nhóm "Khác"
role_counts = df["current_role"].value_counts()
rare_roles = role_counts[role_counts < 5].index.tolist()

df["current_role"] = df["current_role"].apply(
    lambda x: "Khác" if x in rare_roles else x
)
print(f"[7] Chuẩn hóa current_role: gom {len(rare_roles)} giá trị lẻ vào 'Khác'")

# ============================================================
# 8. CHUẨN HÓA CỘT DESIRED_LAYOUT
# ============================================================
# 3 response free-text gán vào nhóm gần nhất hoặc "Khác"
LAYOUT_STANDARD = [
    "Đơn giản, tập trung vào các đầu mục học tập chính và tối giản các tính năng",
    "Nhiều tính năng, trò chơi thú vị, cân bằng giữa học và chơi",
    "Tối giản nhưng vẫn giữ lại một số tính năng nhỏ để tạo ra sự thú vị khi học",
]

df["desired_layout"] = df["desired_layout"].apply(
    lambda x: x if x in LAYOUT_STANDARD else "Khác" if pd.notna(x) else x
)
print(f"[8] Chuẩn hóa desired_layout: gom free-text vào 'Khác'")

# ============================================================
# 9. CHUẨN HÓA MULTI-SELECT (trim từng giá trị trong chuỗi)
# ============================================================
multi_select_cols = [
    "primary_goal",
    "desired_courses",
    "pain_points",
    "selection_criteria",
]

for col in multi_select_cols:
    df[col] = df[col].apply(
        lambda x: ", ".join(item.strip() for item in x.split(","))
        if pd.notna(x) else x
    )
print(f"[9] Chuẩn hóa multi-select: trim từng giá trị, thống nhất ', ' separator")

# ============================================================
# 10. ĐẢM BẢO KIỂU DỮ LIỆU SCORE
# ============================================================
df["exp_score"] = pd.to_numeric(df["exp_score"], errors="coerce").astype("Int64")
df["ui_ux_score"] = pd.to_numeric(df["ui_ux_score"], errors="coerce").astype("Int64")
print(f"[10] Ép kiểu exp_score, ui_ux_score sang integer")

# ============================================================
# 11. CHUẨN HÓA TIMESTAMP VÀ SẮP XẾP THEO THỜI GIAN
# ============================================================
# Sắp xếp theo datetime gốc (giờ:phút:giây)
df = df.sort_values("_ts_parsed", ascending=True).reset_index(drop=True)

# Format sang ngày/tháng/năm (DD/MM/YYYY)
df["timestamp"] = df["_ts_parsed"].dt.strftime("%d/%m/%Y")
df.drop(columns=["_ts_parsed"], inplace=True)
print(f"[11] Sắp xếp theo datetime gốc và chuẩn hóa timestamp (dd/mm/yyyy)")

# ============================================================
# 12. XUẤT FILE CLEANED
# ============================================================
df.to_csv(CLEAN_PATH, index=False, encoding="utf-8")
print(f"\n{'=' * 50}")
print(f"HOÀN TẤT")
print(f"  Input  : {os.path.basename(RAW_PATH)} ({pd.read_csv(RAW_PATH).shape[0]} rows)")
print(f"  Output : {os.path.basename(CLEAN_PATH)} ({df.shape[0]} rows, {df.shape[1]} columns)")
print(f"  Loại bỏ: {pd.read_csv(RAW_PATH).shape[0] - df.shape[0]} dòng (duplicate)")
print(f"  Cột    : {list(df.columns)}")
print(f"{'=' * 50}")

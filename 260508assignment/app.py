import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import koreanize_matplotlib

st.title("Heart Failure 시각화 과제")

# =========================
# 1. 데이터 불러오기 + merge
# =========================
BASE_DIR = Path(__file__).parent

df_a = pd.read_json(BASE_DIR / "heart_failure_a.json")
df_b = pd.read_json(BASE_DIR / "heart_failure_b.json")

df = pd.merge(df_a, df_b, on="person_id", how="inner")

dropped_num = (len(df_a) - len(df)) + (len(df_b) - len(df))

st.write("합쳐진 데이터 개수:", len(df))
st.write("merge 과정에서 사라진 데이터 개수:", dropped_num)

st.divider()


# =========================
# 그래프 1. jointplot
# =========================
st.subheader("1. 박출계수와 나이의 관계")

g = sns.jointplot(
    data=df,
    x="ejection_fraction",
    y="age",
    hue="DEATH_EVENT"
)

st.pyplot(g.fig)
plt.close(g.fig)

st.divider()


# =========================
# 그래프 2. violinplot
# =========================
st.subheader("2. 사망 여부와 혈소판 수치 관계")

smoking_select = st.radio(
    "흡연 여부 선택",
    ["비흡연", "흡연"],
    horizontal=True
)

if smoking_select == "비흡연":
    smoking_value = 0
else:
    smoking_value = 1

df_smoking = df[df["smoking"] == smoking_value]

fig, ax = plt.subplots(figsize=(7, 5))

sns.violinplot(
    data=df_smoking,
    x="DEATH_EVENT",
    y="platelets",
    ax=ax
)

ax.set_title(f"{smoking_select}자의 DEATH_EVENT별 platelets 분포")

st.pyplot(fig)
plt.close(fig)

st.divider()


# =========================
# 그래프 3. histplot
# =========================
st.subheader("3. time 컬럼 히스토그램")

min_ef = int(df["ejection_fraction"].min())
max_ef = int(df["ejection_fraction"].max())

ef_range = st.slider(
    "심박출계수 ejection_fraction 범위 선택",
    min_value=min_ef,
    max_value=max_ef,
    value=(min_ef, max_ef)
)

df_filtered = df[
    (df["ejection_fraction"] >= ef_range[0]) &
    (df["ejection_fraction"] <= ef_range[1])
]

fig, ax = plt.subplots(figsize=(7, 5))

sns.histplot(
    data=df_filtered,
    x="time",
    bins=20,
    hue="DEATH_EVENT",
    ax=ax
)

ax.set_title("ejection_fraction 범위에 따른 time 분포")

st.pyplot(fig)
plt.close(fig)

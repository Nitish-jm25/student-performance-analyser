import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
st.title("🏫 Student Exam Performance Dashboard")

uploaded_file = st.file_uploader("Upload StudentsPerformance.csv", type="csv")

if uploaded_file:
  df = pd.read_csv(uploaded_file)

df["Overall %"] = df[["math score","reading score","writing score"]].mean(axis=1)

def assign_grade(pct):
    if pct >= 90: return "A+"
    elif pct >= 80: return "A"
    elif pct >= 70: return "B"
    elif pct >= 60: return "C"
    elif pct >= 50: return "D"
    else: return "F"

df["Grade"] = df["Overall %"].apply(assign_grade)
df["At Risk"] = df["Overall %"].apply(lambda x: "Yes" if x < 50 else "No")

def grade_color(val):
    if val == "A+": color = 'green'
    elif val == "A": color = 'lightgreen'
    elif val == "B": color = 'yellow'
    elif val == "C": color = 'orange'
    elif val == "D": color = 'red'
    else: color = 'darkred'
    return f'background-color: {color}'

st.sidebar.header("🔎 Filters")
gender_filter = st.sidebar.multiselect("Select Gender", options=df["gender"].unique(), default=df["gender"].unique())
grade_filter = st.sidebar.multiselect("Select Grade", options=df["Grade"].unique(), default=df["Grade"].unique())
risk_filter = st.sidebar.multiselect("At Risk Status", options=df["At Risk"].unique(), default=df["At Risk"].unique())

filtered_df = df[df["gender"].isin(gender_filter) &
                 df["Grade"].isin(grade_filter) &
                 df["At Risk"].isin(risk_filter)]

tab1, tab2, tab3 = st.tabs(["📊 Table", "📈 Charts", "💾 Download"])

with tab1:
    st.subheader("🏆 Top Performers (Filtered)")
    top3 = filtered_df.sort_values(by="Overall %", ascending=False).head(3)
    st.table(top3[["gender","math score","reading score","writing score","Overall %","Grade"]])

    st.subheader("📊 KPI Metrics (Filtered)")

    if len(filtered_df) > 0:
        avg_scores = filtered_df[["math score","reading score","writing score"]].mean()
        pass_percentage = len(filtered_df[filtered_df["Overall %"] >= 50]) / len(filtered_df) * 100

        st.write(avg_scores)
        st.write(f"Pass Percentage: {pass_percentage:.2f}%")

        styled_df = filtered_df.style.applymap(grade_color, subset=['Grade'])
        st.dataframe(styled_df)

with tab2:
    if len(filtered_df) > 0:
        fig1 = px.histogram(filtered_df, x="Grade", color="Grade")
        st.plotly_chart(fig1)

        avg_scores_chart = filtered_df[["math score","reading score","writing score"]].mean()
        fig2 = px.bar(avg_scores_chart,
                      x=avg_scores_chart.index,
                      y=avg_scores_chart.values)
        st.plotly_chart(fig2)

with tab3:
    if len(filtered_df) > 0:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="Processed_Student_Performance_Filtered.csv",
            mime='text/csv'
        )
```

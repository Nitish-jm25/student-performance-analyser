import pandas as pd
import streamlit as st
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Performance Dashboard")
st.write("Analyze student performance using interactive charts and filters.")

# Load dataset
try:
    df = pd.read_csv("StudentsPerformance.csv")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Calculate Overall Percentage
df["Overall %"] = df[
    ["math score", "reading score", "writing score"]
].mean(axis=1)

# Grade Assignment
def assign_grade(pct):
    if pct >= 90:
        return "A+"
    elif pct >= 80:
        return "A"
    elif pct >= 70:
        return "B"
    elif pct >= 60:
        return "C"
    elif pct >= 50:
        return "D"
    else:
        return "F"

df["Grade"] = df["Overall %"].apply(assign_grade)

# At Risk Students
df["At Risk"] = df["Overall %"].apply(
    lambda x: "Yes" if x < 50 else "No"
)

# Sidebar Filters
st.sidebar.header("🔍 Filters")

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

grade_filter = st.sidebar.multiselect(
    "Grade",
    options=df["Grade"].unique(),
    default=df["Grade"].unique()
)

risk_filter = st.sidebar.multiselect(
    "At Risk",
    options=df["At Risk"].unique(),
    default=df["At Risk"].unique()
)

# Apply Filters
filtered_df = df[
    (df["gender"].isin(gender_filter)) &
    (df["Grade"].isin(grade_filter)) &
    (df["At Risk"].isin(risk_filter))
]

# Tabs
tab1, tab2, tab3 = st.tabs(
    ["📊 Data Table", "📈 Visualizations", "📥 Download"]
)

# ---------------- TAB 1 ----------------
with tab1:

    st.subheader("Top 3 Performers")

    top3 = filtered_df.sort_values(
        by="Overall %",
        ascending=False
    ).head(3)

    st.dataframe(top3)

    st.subheader("Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Students",
        len(filtered_df)
    )

    col2.metric(
        "Average %",
        round(filtered_df["Overall %"].mean(), 2)
    )

    pass_percent = (
        len(filtered_df[filtered_df["Overall %"] >= 50])
        / len(filtered_df)
        * 100
        if len(filtered_df) > 0 else 0
    )

    col3.metric(
        "Pass %",
        f"{pass_percent:.2f}%"
    )

    col4.metric(
        "At Risk",
        len(filtered_df[filtered_df["At Risk"] == "Yes"])
    )

    st.subheader("Filtered Dataset")
    st.dataframe(filtered_df)

# ---------------- TAB 2 ----------------
with tab2:

    st.subheader("Grade Distribution")

    fig1 = px.histogram(
        filtered_df,
        x="Grade",
        color="Grade"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Average Subject Scores")

    avg_scores = filtered_df[
        ["math score", "reading score", "writing score"]
    ].mean()

    fig2 = px.bar(
        x=avg_scores.index,
        y=avg_scores.values,
        labels={
            "x": "Subjects",
            "y": "Average Score"
        },
        title="Average Scores"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Overall Percentage Distribution")

    fig3 = px.histogram(
        filtered_df,
        x="Overall %",
        nbins=20
    )

    st.plotly_chart(fig3, use_container_width=True)

# ---------------- TAB 3 ----------------
with tab3:

    st.subheader("Download Filtered Data")

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="filtered_student_performance.csv",
        mime="text/csv"
    )
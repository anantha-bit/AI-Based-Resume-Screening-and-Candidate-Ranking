"""
Page 1: Executive Recruitment Dashboard.
Visualizes screening analytics, score distributions, candidate tier breakdowns, and top talent.
Academic context: Unit 4 (Building AI-Powered Dashboards & Visualizations).
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.storage.database import DatabaseManager

st.set_page_config(page_title="Dashboard | AI Screening", page_icon="📊", layout="wide")

st.title("📊 Executive Recruitment Dashboard")
st.caption("Real-time screening metrics, candidate score distributions, and talent analytics.")

db = DatabaseManager()
jds = db.get_all_job_descriptions()
resumes = db.get_all_resumes()
screenings = db.get_latest_screening_results()

if not screenings:
    st.warning("⚠️ No active screening runs found in the database. Please navigate to 'Candidate Screening' to run an evaluation, or run the master experiment suite.")
    st.stop()

df = pd.DataFrame(screenings)

# Top KPI Metric Row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Resumes Analyzed", len(resumes))
with col2:
    st.metric("Active Job Descriptions", len(jds))
with col3:
    st.metric("Screened Candidates", len(df))
with col4:
    top_cand = df.sort_values(by="overall_score", ascending=False).iloc[0]
    st.metric("Top-Ranked Candidate", f"{top_cand['candidate_name']}", f"{top_cand['overall_score']:.1f}%")
with col5:
    avg_score = df["overall_score"].mean()
    st.metric("Average Match Score", f"{avg_score:.1f}%")

st.markdown("---")

# Visual Analytics Section
c1, c2 = st.columns([3, 2])

with c1:
    st.subheader("📈 Candidate Score Distribution")
    fig_hist = px.histogram(
        df, x="overall_score", nbins=10,
        title="Distribution of Overall Candidate Match Scores",
        labels={"overall_score": "Composite Score (0-100)"},
        color_discrete_sequence=["#3B82F6"]
    )
    fig_hist.update_layout(bargap=0.1, template="plotly_white", height=320)
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    st.subheader("🏷️ Candidate Qualification Tiers")
    tier_counts = df["recommendation_badge"].value_counts().reset_index()
    tier_counts.columns = ["Tier", "Count"]
    fig_pie = px.pie(
        tier_counts, names="Tier", values="Count",
        title="Breakdown by Recommendation Tier",
        color="Tier",
        color_discrete_map={
            "Highly Recommended": "#10B981",
            "Strong Candidate": "#3B82F6",
            "Potential Match": "#F59E0B",
            "Low Fit": "#EF4444"
        }
    )
    fig_pie.update_layout(template="plotly_white", height=320)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Leaderboard Snippet
st.subheader("🏆 Top Ranked Talent Cohort")
display_cols = ["rank", "candidate_name", "candidate_id", "overall_score", "recommendation_badge", "explanation"]
df_display = df[display_cols].sort_values(by="rank").head(8)
df_display.columns = ["Rank", "Candidate Name", "ID", "Overall Score", "Tier", "Recruiter Summary"]

st.dataframe(
    df_display,
    column_config={
        "Overall Score": st.column_config.ProgressColumn(
            "Overall Score",
            help="Weighted composite score out of 100",
            format="%.1f%%",
            min_value=0,
            max_value=100
        )
    },
    use_container_width=True,
    hide_index=True
)

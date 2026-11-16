"""
Page 5: Candidate Rankings and Leaderboard.
Sortable candidate rankings with multi-criteria scores, tier badges, and CSV export.
Academic context: Maps to Unit 1 (Similarity Ranking) & Unit 4 (Recruitment Systems).
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
from src.storage.database import DatabaseManager

st.set_page_config(page_title="Candidate Rankings | AI Screening", page_icon="🏆", layout="wide")

st.title("🏆 Candidate Rankings & Leaderboard")
st.caption("Transparent, evidence-grounded candidate leaderboard. Candidates are ranked based on calibrated multi-dimensional scores.")

db = DatabaseManager()
results = db.get_latest_screening_results()

if not results:
    st.warning("⚠️ No candidate rankings available. Please run screening from the 'Candidate Screening' page.")
    st.stop()

df = pd.DataFrame(results)

# Filters Row
c1, c2, c3 = st.columns([2, 2, 2])
with c1:
    tier_filter = st.multiselect(
        "Filter by Recommendation Tier:",
        options=list(df["recommendation_badge"].unique()),
        default=list(df["recommendation_badge"].unique())
    )
with c2:
    min_score = st.slider("Minimum Composite Score:", min_value=0, max_value=100, value=0, step=5)
with c3:
    search_query = st.text_input("Search Candidate Name or ID:", "")

# Apply Filters
filtered_df = df[
    (df["recommendation_badge"].isin(tier_filter)) &
    (df["overall_score"] >= min_score)
]
if search_query:
    filtered_df = filtered_df[
        filtered_df["candidate_name"].str.contains(search_query, case=False, na=False) |
        filtered_df["candidate_id"].str.contains(search_query, case=False, na=False)
    ]

st.markdown("---")

# Format Display Table
display_rows = []
for idx, r in filtered_df.sort_values(by="overall_score", ascending=False).iterrows():
    comp = r.get("component_scores", {})
    display_rows.append({
        "Rank": r["rank"],
        "Candidate Name": r["candidate_name"],
        "Candidate ID": r["candidate_id"],
        "Overall Score": r["overall_score"],
        "Recommendation Tier": r["recommendation_badge"],
        "Skills Match (%)": comp.get("required_skills_match", 0),
        "Semantic Fit (%)": comp.get("semantic_similarity", 0),
        "Experience Score (%)": comp.get("experience_score", 0),
        "Education Score (%)": comp.get("education_score", 0)
    })

disp_df = pd.DataFrame(display_rows)

st.dataframe(
    disp_df,
    column_config={
        "Overall Score": st.column_config.ProgressColumn(
            "Overall Score",
            help="Weighted composite score out of 100",
            format="%.1f%%",
            min_value=0,
            max_value=100
        ),
        "Skills Match (%)": st.column_config.NumberColumn(format="%.1f%%"),
        "Semantic Fit (%)": st.column_config.NumberColumn(format="%.1f%%"),
    },
    use_container_width=True,
    hide_index=True
)

# Export Section
c_exp1, c_exp2 = st.columns([1, 1])
with c_exp1:
    csv = disp_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Leaderboard as CSV",
        data=csv,
        file_name="candidate_rankings_leaderboard.csv",
        mime="text/csv"
    )

with c_exp2:
    selected_for_dossier = st.selectbox(
        "Select Candidate for In-Depth Dossier Analysis:",
        options=disp_df["Candidate ID"].tolist() if not disp_df.empty else []
    )
    if st.button("🔍 Open In-Depth Candidate Analysis"):
        st.session_state["target_candidate_id"] = selected_for_dossier
        st.switch_page("pages/6_Individual_Candidate_Analysis.py")

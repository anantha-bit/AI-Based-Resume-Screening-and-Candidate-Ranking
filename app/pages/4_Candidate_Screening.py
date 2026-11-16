"""
Page 4: Candidate Screening Runner.
Executes multi-criteria evaluation with configurable scoring weights.
Academic context: Maps to Unit 1 (Similarity), Unit 2 (Classification) & Unit 3 (Prompt-Driven Evaluation).
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from src.classical_ml.baseline_screener import ClassicalBaselineScreener
from src.semantic_matching.semantic_screener import SemanticScreener
from src.llm.llm_client import LLMClient
from src.llm.llm_extractor import LLMExtractor
from src.ranking.ranker import CandidateRanker
from src.storage.database import DatabaseManager

st.set_page_config(page_title="Candidate Screening | AI Screening", page_icon="⚙️", layout="wide")

st.title("⚙️ Candidate Screening Engine")
st.caption("Select a Job Description and configure multi-criteria evaluation weights to screen candidate resumes in real time.")

db = DatabaseManager()
jds = db.get_all_job_descriptions()
resumes = db.get_all_resumes()

if not jds:
    st.warning("⚠️ No Job Descriptions found. Please go to 'Job Description Analysis' to create or select one.")
    st.stop()

if not resumes:
    st.warning("⚠️ No Resumes found. Please go to 'Upload Resumes' to ingest candidates.")
    st.stop()

# 1. Job Description Selection
st.subheader("1. Select Target Job Description")
jd_map = {f"{jd['job_title']} (ID: {jd['id']})": jd for jd in jds}
selected_jd_label = st.selectbox("Active Job Description:", list(jd_map.keys()))
active_jd = jd_map[selected_jd_label]

st.info(f"Target Role: **{active_jd['job_title']}** | Required Skills: {len(active_jd['required_skills'])} | Preferred: {len(active_jd['preferred_skills'])} | Experience: {active_jd['experience']}")

# 2. Configurable Weights Section
st.subheader("2. Configure Multi-Criteria Scoring Weights")
st.write("Adjust the relative importance of each dimension according to your hiring priorities. Weights are automatically normalized to 100%.")

c1, c2, c3 = st.columns(3)
with c1:
    w_req = st.slider("Required Skills Match (%)", min_value=0, max_value=60, value=35, step=5)
    w_pref = st.slider("Preferred Skills Match (%)", min_value=0, max_value=40, value=15, step=5)
with c2:
    w_edu = st.slider("Education Qualifications (%)", min_value=0, max_value=30, value=10, step=5)
    w_exp = st.slider("Work Experience Depth (%)", min_value=0, max_value=40, value=15, step=5)
with c3:
    w_proj = st.slider("Project Relevance (%)", min_value=0, max_value=30, value=10, step=5)
    w_sem = st.slider("Transformer Semantic Fit (%)", min_value=0, max_value=40, value=15, step=5)

raw_sum = w_req + w_pref + w_edu + w_exp + w_proj + w_sem
if raw_sum != 100:
    st.caption(f"ℹ️ Current sum: **{raw_sum}%**. The engine will automatically normalize this to sum to exactly 100%.")

weights = {
    "required_skills": w_req / max(1, raw_sum),
    "preferred_skills": w_pref / max(1, raw_sum),
    "education": w_edu / max(1, raw_sum),
    "experience": w_exp / max(1, raw_sum),
    "projects": w_proj / max(1, raw_sum),
    "semantic_similarity": w_sem / max(1, raw_sum)
}

st.markdown("---")

# 3. Execution Button
if st.button("🚀 Execute Screening Evaluation on All Resumes", type="primary"):
    with st.spinner("Initializing models and screening candidates..."):
        baseline_screener = ClassicalBaselineScreener()
        semantic_screener = SemanticScreener()
        llm_client = LLMClient()
        llm_extractor = LLMExtractor(llm_client)
        ranker = CandidateRanker(weights)

        scored_candidates = []
        progress_bar = st.progress(0)
        status_box = st.empty()

        for i, res in enumerate(resumes):
            status_box.text(f"Screening candidate ({i+1}/{len(resumes)}): {res['candidate_name']}...")
            
            classical_stats = baseline_screener.screen_candidate(active_jd, res)
            semantic_stats = semantic_screener.evaluate_semantic_fit(active_jd, res)
            llm_analysis = llm_extractor.analyze_candidate(active_jd, res)

            scored = ranker.score_candidate(
                active_jd, res, semantic_stats, classical_stats, llm_analysis
            )
            scored_candidates.append(scored)
            progress_bar.progress((i + 1) / len(resumes))

        # Sort and rank
        ranked = ranker.rank_candidates(scored_candidates)
        db.save_screening_results(active_jd["id"], ranked)
        status_box.text("✅ Screening evaluation completed!")
        st.session_state["latest_ranked"] = ranked
        st.success(f"Successfully screened and ranked {len(ranked)} candidates! Navigate to 'Candidate Rankings' to inspect the results.")

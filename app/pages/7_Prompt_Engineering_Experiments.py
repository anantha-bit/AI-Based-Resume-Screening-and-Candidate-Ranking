"""
Page 7: Prompt Engineering Research Experiments.
Interactive benchmarking and scientific comparison of 10 prompt engineering strategies.
Academic context: Maps to Unit 1 (Prompt Anatomy), Unit 2 (Prompt Tactics) & Unit 3 (CoT & Agentic Prompting).
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import plotly.express as px
from src.prompt_engineering.prompt_templates import PROMPT_STRATEGIES, PromptTemplates
from src.prompt_engineering.prompt_experiments import PromptExperimentRunner
from src.storage.database import DatabaseManager

st.set_page_config(page_title="Prompt Engineering | AI Screening", page_icon="🧪", layout="wide")

st.title("🧪 Prompt Engineering Research Experiments")
st.caption("Empirical benchmarking of 10 core prompt-engineering paradigms on the same screening task (PES University UE24AM343AB5).")

db = DatabaseManager()
benchmarks = db.get_experiment_summary()
jds = db.get_all_job_descriptions()
resumes = db.get_all_resumes()

# High-Level Strategy Overview Table
st.subheader("📊 Empirical Strategy Comparison Across Benchmark Cohort")

if benchmarks:
    bench_df = pd.DataFrame(benchmarks)
    display_bench = bench_df[[
        "strategy_name", "avg_score", "avg_latency", "avg_validity",
        "avg_completeness", "avg_evidence_support", "avg_consistency", "runs_count"
    ]].copy()
    display_bench.columns = [
        "Prompt Strategy", "Avg Score", "Latency (s)", "Valid JSON (%)",
        "Completeness (%)", "Evidence Support (%)", "Consistency", "Runs"
    ]

    st.dataframe(
        display_bench,
        column_config={
            "Avg Score": st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=100),
            "Latency (s)": st.column_config.NumberColumn(format="%.2f s"),
            "Valid JSON (%)": st.column_config.NumberColumn(format="%.0f%%"),
            "Evidence Support (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Consistency": st.column_config.NumberColumn(format="%.3f"),
        },
        use_container_width=True,
        hide_index=True
    )

    # Interactive Comparison Charts
    c1, c2 = st.columns(2)
    with c1:
        fig_lat = px.bar(
            display_bench, x="Latency (s)", y="Prompt Strategy", orientation="h",
            title="Execution Latency by Strategy (Lower is Faster)",
            color="Latency (s)", color_continuous_scale="Viridis"
        )
        fig_lat.update_layout(template="plotly_white", height=350, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_lat, use_container_width=True)

    with c2:
        fig_ev = px.bar(
            display_bench, x="Evidence Support (%)", y="Prompt Strategy", orientation="h",
            title="Evidence Grounding Fidelity (Higher Prevents Hallucination)",
            color="Evidence Support (%)", color_continuous_scale="Blues"
        )
        fig_ev.update_layout(template="plotly_white", height=350, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_ev, use_container_width=True)

st.markdown("---")

# Strategy Deep-Dive & Template Inspector
st.subheader("🔍 Prompt Template Inspector & Strategy Deep-Dive")

selected_strat = st.selectbox("Select a Prompt Engineering Strategy to Inspect:", PROMPT_STRATEGIES)

sample_jd = jds[0]["raw_text"] if jds else "Job Description Text..."
sample_res = resumes[0]["raw_text"] if resumes else "Candidate Resume Text..."

# Map strategy to prompt snippet
prompt_preview = ""
if selected_strat == "Zero-shot prompting":
    prompt_preview = PromptTemplates.zero_shot(sample_jd[:400], sample_res[:400])
elif selected_strat == "Few-shot prompting":
    prompt_preview = PromptTemplates.few_shot(sample_jd[:400], sample_res[:400])
elif selected_strat == "Role-based prompting":
    prompt_preview = PromptTemplates.role_based(sample_jd[:400], sample_res[:400])
elif selected_strat == "Chain-of-thought-inspired structured task decomposition":
    prompt_preview = PromptTemplates.chain_of_thought(sample_jd[:400], sample_res[:400])
elif selected_strat == "Least-to-most prompting":
    prompt_preview = PromptTemplates.least_to_most(sample_jd[:400], sample_res[:400])
elif selected_strat == "Chained prompting":
    prompt_preview = PromptTemplates.chained(1, sample_jd[:300], sample_res[:300])
elif selected_strat == "Grounded prompting":
    prompt_preview = PromptTemplates.grounded(sample_jd[:400], sample_res[:400])
elif selected_strat == "Structured JSON output prompting":
    prompt_preview = PromptTemplates.structured_json(sample_jd[:400], sample_res[:400])
elif selected_strat == "Critic and refinement prompting":
    prompt_preview = PromptTemplates.critic_and_refinement(sample_jd[:300], sample_res[:300], "Initial Assessment Draft...")
elif selected_strat == "Self-consistency prompting":
    prompt_preview = PromptTemplates.self_consistency(0, sample_jd[:400], sample_res[:400])

c_desc, c_code = st.columns([1, 2])
with c_desc:
    with st.container(border=True):
        st.markdown(f"#### 💡 Strategy: {selected_strat}")
        if "Few-shot" in selected_strat:
            st.write("Provides positive and negative in-context exemplars to calibrate model scoring boundaries (Brown et al., 2020).")
        elif "Chain-of-thought" in selected_strat:
            st.write("Deconstructs the reasoning process into intermediate verifiable steps before arriving at a final score (Wei et al., 2022).")
        elif "Least-to-most" in selected_strat:
            st.write("Solves easy sub-problems (degrees, eligibility) before tackling complex domain experience alignment (Zhou et al., 2022).")
        elif "Grounded" in selected_strat:
            st.write("Strictly prohibits unreferenced inferences and requires exact verbatim sentence citations for every match.")
        elif "Critic" in selected_strat:
            st.write("Employs a two-pass auditor prompt to catch hallucinations and remove demographic bias.")
        elif "Self-consistency" in selected_strat:
            st.write("Samples multiple independent evaluation passes to ensure ranking stability and consensus (Wang et al., 2022).")
        else:
            st.write("Standard foundational prompting baseline used to measure baseline LLM alignment.")

with c_code:
    st.markdown("#### 📜 Executable Prompt Template")
    st.code(prompt_preview, language="markdown")

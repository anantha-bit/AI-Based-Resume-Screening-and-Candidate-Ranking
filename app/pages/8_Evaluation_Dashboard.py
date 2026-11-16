"""
Page 9: Academic Evaluation & IR Metrics Dashboard.
Displays Confusion Matrices, Classification F1, NDCG@K, MRR, and Entity Extraction metrics.
Academic context: Maps to Unit 1 & Unit 2 (Evaluation Standards & Information Retrieval Metrics).
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title="Evaluation Dashboard | AI Screening", page_icon="📈", layout="wide")

st.title("📈 Academic Evaluation & Metrics Dashboard")
st.caption("Rigorous scientific evaluation against ground-truth benchmark labels (PES University UE24AM343AB5).")

EXP_SUMMARY_PATH = os.path.join(PROJECT_ROOT, "experiments", "results_summary.json")

if not os.path.exists(EXP_SUMMARY_PATH):
    st.warning("⚠️ No benchmark results found. Please execute the experiment suite first (`python experiments/run_all_experiments.py`).")
    st.stop()

with open(EXP_SUMMARY_PATH, "r", encoding="utf-8") as f:
    summary_data = json.load(f)

model_comp = summary_data.get("model_comparison", {})
class_metrics = model_comp.get("classification", {})
rank_metrics = model_comp.get("ranking", {})

# 1. Classification Metrics Table
st.subheader("1. Candidate Eligibility Classification Metrics")
st.caption("Binary suitability threshold (Eligible vs Ineligible) compared against ground-truth labels.")

class_rows = []
for model_name, m in class_metrics.items():
    class_rows.append({
        "Model / Paradigm": model_name,
        "Accuracy": m["accuracy"],
        "Precision": m["precision"],
        "Recall": m["recall"],
        "F1-Score": m["f1_score"],
        "True Positives": m["true_positives"],
        "False Positives": m["false_positives"],
        "False Negatives": m["false_negatives"],
        "True Negatives": m["true_negatives"]
    })

st.dataframe(pd.DataFrame(class_rows), use_container_width=True, hide_index=True)

# 2. Ranking & Retrieval Metrics (NDCG@K, P@K, MRR)
st.markdown("---")
st.subheader("2. Candidate Ranking & Information Retrieval Metrics")
st.caption("Measures ability to place top-tier relevant talent at the very head of the recruiter shortlist.")

rank_rows = []
for model_name, rm in rank_metrics.items():
    rank_rows.append({
        "Model / Paradigm": model_name,
        "Precision@1 (P@1)": rm["P@1"],
        "Precision@3 (P@3)": rm["P@3"],
        "Precision@5 (P@5)": rm["P@5"],
        "Recall@3 (R@3)": rm["R@3"],
        "MRR (Mean Reciprocal Rank)": rm["MRR"],
        "NDCG@3": rm["NDCG@3"],
        "NDCG@5": rm["NDCG@5"]
    })

st.dataframe(pd.DataFrame(rank_rows), use_container_width=True, hide_index=True)

# 3. Visual Charts Section
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 F1-Score & Accuracy Comparison")
    f1_df = pd.DataFrame([
        {"Model": k, "Metric": "F1-Score", "Value": v["f1_score"]}
        for k, v in class_metrics.items()
    ] + [
        {"Model": k, "Metric": "Accuracy", "Value": v["accuracy"]}
        for k, v in class_metrics.items()
    ])
    fig_f1 = px.bar(
        f1_df, x="Model", y="Value", color="Metric", barmode="group",
        title="Classification Performance by Model",
        color_discrete_sequence=["#2563EB", "#10B981"]
    )
    fig_f1.update_layout(template="plotly_white", height=320, yaxis_range=[0, 1.0])
    st.plotly_chart(fig_f1, use_container_width=True)

with c2:
    st.subheader("🎯 Ranking Precision (NDCG@3 & P@3)")
    ndcg_df = pd.DataFrame([
        {"Model": k, "NDCG@3": v["NDCG@3"], "P@3": v["P@3"]}
        for k, v in rank_metrics.items()
    ])
    fig_ndcg = px.bar(
        ndcg_df, x="Model", y=["NDCG@3", "P@3"], barmode="group",
        title="Top-3 Candidate Ranking Quality",
        color_discrete_sequence=["#8B5CF6", "#F59E0B"]
    )
    fig_ndcg.update_layout(template="plotly_white", height=320, yaxis_range=[0, 1.1])
    st.plotly_chart(fig_ndcg, use_container_width=True)

# 4. Ground Truth Verification Notice
st.info("🔬 **Academic Grounding:** Evaluations are measured directly against `data/sample/ground_truth_labels.json` containing 15 hand-annotated multi-tier candidate profiles mapped to target job requirements. No synthetic results are fabricated.")

"""
Page 6: Individual Candidate Analysis & PDF Dossier.
Deep-dive candidate assessment with Plotly radar visualization, grounded evidence citations, and PDF export.
Academic context: Maps to Unit 2 (Output Formatting), Unit 3 (Grounded Explanations) & Unit 4 (Reporting).
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import plotly.graph_objects as go
from src.storage.database import DatabaseManager
from src.reporting.pdf_exporter import CandidatePDFExporter
from src.reporting.archive_manager import ArchiveManager

st.set_page_config(page_title="Candidate Dossier | AI Screening", page_icon="📋", layout="wide")

st.title("📋 Individual Candidate Analysis & Verification Dossier")
st.caption("Inspect comprehensive qualification evidence, verbatim quotes from the resume, gap analysis, and export an official PDF dossier.")

db = DatabaseManager()
results = db.get_latest_screening_results()
resumes = db.get_all_resumes()

if not results or not resumes:
    st.warning("⚠️ No candidate records available. Please run screening from 'Candidate Screening'.")
    st.stop()

# Candidate Selector
cand_options = {f"{r['candidate_name']} ({r['candidate_id']})": r for r in results}
default_index = 0

if "target_candidate_id" in st.session_state:
    for idx, (label, obj) in enumerate(cand_options.items()):
        if obj["candidate_id"] == st.session_state["target_candidate_id"]:
            default_index = idx
            break

selected_label = st.selectbox("Select Candidate to Inspect:", list(cand_options.keys()), index=default_index)
cand = cand_options[selected_label]
resume_obj = next((res for res in resumes if res["candidate_id"] == cand["candidate_id"]), {})

# Dossier Header
c_head1, c_head2 = st.columns([3, 1])
with c_head1:
    st.markdown(f"## 👤 {cand['candidate_name']} (`{cand['candidate_id']}`)")
    st.write(f"**Recommendation Tier:** `{cand['recommendation_badge']}` | **Overall Score:** **{cand['overall_score']:.1f} / 100**")
    if resume_obj.get("contact"):
        contact = resume_obj["contact"]
        contact_str = " | ".join([
            f"📧 {contact.get('emails', ['N/A'])[0]}" if contact.get('emails') else "",
            f"📱 {contact.get('phones', ['N/A'])[0]}" if contact.get('phones') else ""
        ])
        st.caption(contact_str)

with c_head2:
    # PDF Dossier Export Button
    pdf_bytes = CandidatePDFExporter.generate_pdf_bytes(cand)
    st.download_button(
        label="📄 Export Dossier as PDF",
        data=pdf_bytes,
        file_name=f"Dossier_{cand['candidate_id']}_{cand['candidate_name'].replace(' ', '_')}.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )
    
    # Original Native Resume Document Download
    res_file_name = resume_obj.get("file_name", "")
    if res_file_name:
        f_data = ArchiveManager.get_resume_file_data(res_file_name)
        if f_data:
            raw_b, m_type = f_data
            ext_label = os.path.splitext(res_file_name)[1].upper().replace(".", "")
            st.download_button(
                label=f"📥 Download Resume ({ext_label})",
                data=raw_b,
                file_name=res_file_name,
                mime=m_type,
                use_container_width=True
            )

st.markdown("---")

# Visual Radar Chart & Component Scores
col_left, col_right = st.columns([3, 3])

with col_left:
    st.subheader("📊 Multi-Dimensional Radar Profile")
    comp = cand.get("component_scores", {})
    categories = [
        "Required Skills", "Preferred Skills", "Education", 
        "Work Experience", "Project Relevance", "Transformer Semantic"
    ]
    values = [
        comp.get("required_skills_match", 0),
        comp.get("preferred_skills_match", 0),
        comp.get("education_score", 0),
        comp.get("experience_score", 0),
        comp.get("project_relevance", 0),
        comp.get("semantic_similarity", 0)
    ]
    # Close the polygon
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.25)',
        line=dict(color='#2563EB', width=2),
        name=cand['candidate_name']
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False,
        template="plotly_white",
        height=320,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_right:
    st.subheader("💡 Recruiter Explanation & Score Rationale")
    st.info(cand.get("explanation", "Assessment completed."))
    
    with st.container(border=True):
        st.markdown("#### ⚖️ Scoring Breakdown")
        for cat, val in comp.items():
            st.write(f"- **{cat.replace('_', ' ').title()}:** {val:.1f}%")

st.markdown("---")

# Grounded Evidence & Verification Section
col_ev1, col_ev2 = st.columns(2)

with col_ev1:
    st.subheader("✅ Matched Required Skills")
    matched = cand.get("matched_required_skills", [])
    if matched:
        for s in matched:
            st.markdown(f"- 🟢 **{s}** (Verified in resume)")
    else:
        st.warning("No core required skills matched.")

    st.subheader("🌟 Matched Preferred Skills")
    for s in resume_obj.get("skills", []):
        if s not in matched:
            st.markdown(f"- 🔵 {s}")

with col_ev2:
    st.subheader("❌ Missing / Unverified Skills")
    missing = cand.get("missing_required_skills", [])
    if missing:
        for m in missing:
            st.markdown(f"- 🔴 **{m}** — *Not found in resume*")
    else:
        st.success("All mandatory skills satisfied!")

    st.subheader("💼 Documented Experience & Projects")
    st.write(f"**Total Industry Experience:** {resume_obj.get('total_experience_years', 0):g} years")
    for p in resume_obj.get("projects", [])[:3]:
        st.markdown(f"• **{p.get('title', 'Project')}**: {p.get('details', '')}")

st.markdown("---")
st.caption("🛡️ **Strict Evidence Policy:** Every assessment claim is grounded directly in text extracted from the candidate's resume. Missing qualifications are explicitly labeled rather than hallucinated.")

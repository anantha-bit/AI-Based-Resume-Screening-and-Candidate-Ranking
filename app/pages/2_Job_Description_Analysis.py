"""
Page 2: Job Description Analysis.
Ingests, extracts, and normalizes job descriptions into structured JSON requirements.
Academic context: Unit 1 & Unit 2 (Information Extraction & Text Processing).
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import json
from src.preprocessing.document_loader import DocumentLoader
from src.extraction.jd_extractor import JobDescriptionExtractor
from src.storage.database import DatabaseManager

st.set_page_config(page_title="Job Description Analysis | AI Screening", page_icon="📄", layout="wide")

st.title("📄 Job Description Analysis & Requirement Extraction")
st.caption("Browse catalog positions, upload custom job specifications, or paste raw text. The system automatically segments mandatory vs preferred qualifications into structured JSON.")

db = DatabaseManager()
existing_jds = db.get_all_job_descriptions()

# Deduplicate catalog options by ID and title
jd_options = {}
for jd in existing_jds:
    label = f"{jd['job_title']} (ID: {jd['id']})"
    jd_options[label] = jd

# Ensure session state initialization
if "active_jd_id" not in st.session_state:
    if existing_jds:
        st.session_state["active_jd_id"] = existing_jds[0]["id"]
        st.session_state["parsed_jd_cache"] = existing_jds[0]
        st.session_state["jd_source"] = existing_jds[0]["job_title"]
    else:
        st.session_state["active_jd_id"] = None
        st.session_state["parsed_jd_cache"] = None
        st.session_state["jd_source"] = "None"

# Top Input Tabs
tab_catalog, tab_upload, tab_manual = st.tabs([
    "📚 Select from Role Catalog",
    "📤 Upload JD Document",
    "✍️ Manual Text Entry"
])

# 1. CATALOG TAB
with tab_catalog:
    if jd_options:
        current_labels = list(jd_options.keys())
        current_idx = 0
        for i, l in enumerate(current_labels):
            if jd_options[l]["id"] == st.session_state.get("active_jd_id"):
                current_idx = i
                break

        selected_label = st.selectbox(
            "Choose a pre-loaded Job Description from Catalog:",
            current_labels,
            index=current_idx,
            key="catalog_jd_selectbox"
        )
        selected_jd_obj = jd_options[selected_label]

        # Check if user switched catalog selection
        if st.session_state.get("active_jd_id") != selected_jd_obj["id"]:
            st.session_state["active_jd_id"] = selected_jd_obj["id"]
            st.session_state["parsed_jd_cache"] = selected_jd_obj
            st.session_state["jd_source"] = selected_jd_obj["job_title"]
            st.rerun()

        col_cat1, col_cat2 = st.columns([2, 3])
        with col_cat1:
            if st.button("🔄 Reload this Catalog Job", type="primary", use_container_width=True):
                st.session_state["active_jd_id"] = selected_jd_obj["id"]
                st.session_state["parsed_jd_cache"] = selected_jd_obj
                st.session_state["jd_source"] = selected_jd_obj["job_title"]
                st.success(f"✅ Active Job Description updated to: **{selected_jd_obj['job_title']}** (ID: {selected_jd_obj['id']})")
                st.rerun()

        with col_cat2:
            st.caption(f"📌 Raw text length: {len(selected_jd_obj['raw_text'])} characters • Created: {selected_jd_obj['created_at']}")
    else:
        st.warning("No Job Descriptions found in catalog. Use Upload or Manual tabs to add one.")

# 2. UPLOAD TAB
with tab_upload:
    uploaded_file = st.file_uploader("Upload Job Description (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])
    if uploaded_file:
        file_bytes = uploaded_file.read()
        res = DocumentLoader.load_bytes(file_bytes, uploaded_file.name)
        if res["success"]:
            st.info(f"Loaded '{uploaded_file.name}' ({len(res['text'])} characters). Click button below to parse.")
            if st.button("🚀 Analyze Uploaded Document", type="primary"):
                with st.spinner("Extracting structured criteria..."):
                    parsed = JobDescriptionExtractor.extract_from_text(res["text"])
                    new_id = db.save_job_description(parsed)
                    parsed["id"] = new_id
                    st.session_state["active_jd_id"] = new_id
                    st.session_state["parsed_jd_cache"] = parsed
                    st.session_state["jd_source"] = uploaded_file.name
                    st.success(f"✅ Saved and activated new Job Description: **{parsed['job_title']}** (ID: {new_id})!")
                    st.rerun()
        else:
            st.error(res["error"])

# 3. MANUAL TAB
with tab_manual:
    manual_text = st.text_area(
        "Paste Full Job Description:",
        height=180,
        placeholder="Job Title: Senior Machine Learning Engineer\n\nRequirements:\n- 4+ years experience with Python, PyTorch, Transformers, SQL\n\nResponsibilities:\n- Design scalable ML models..."
    )
    if st.button("🚀 Parse & Save Manual JD", type="primary"):
        if manual_text.strip():
            with st.spinner("Parsing requirements..."):
                parsed = JobDescriptionExtractor.extract_from_text(manual_text.strip())
                new_id = db.save_job_description(parsed)
                parsed["id"] = new_id
                st.session_state["active_jd_id"] = new_id
                st.session_state["parsed_jd_cache"] = parsed
                st.session_state["jd_source"] = "Manual Input"
                st.success(f"✅ Saved and activated: **{parsed['job_title']}** (ID: {new_id})!")
                st.rerun()
        else:
            st.warning("Please paste some job description text first.")

st.markdown("---")

# DISPLAY CURRENT ACTIVE JOB DESCRIPTION
if st.session_state.get("parsed_jd_cache"):
    parsed = st.session_state["parsed_jd_cache"]
    st.subheader(f"🎯 Active Role: {parsed['job_title']} (ID: {parsed.get('id', 'N/A')})")
    st.caption(f"Source: {st.session_state.get('jd_source', 'Catalog')}")

    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown("#### ⚡ Mandatory Technical Skills (Required)")
        if parsed.get("required_skills"):
            st.write(" ".join([f"`{s}`" for s in parsed["required_skills"]]))
        else:
            st.info("None explicitly flagged as mandatory.")

        st.markdown("#### 🌟 Nice-to-Have Skills (Preferred)")
        if parsed.get("preferred_skills"):
            st.write(" ".join([f"`{s}`" for s in parsed["preferred_skills"]]))
        else:
            st.info("None explicitly flagged as preferred.")

        st.markdown("#### 📋 Key Responsibilities")
        resps = parsed.get("responsibilities", [])
        if resps:
            for r in resps:
                st.markdown(f"- {r}")
        else:
            st.write("Responsibilities extracted from job description summary.")

    with c2:
        with st.container(border=True):
            st.markdown("#### 🎓 Qualifications Thresholds")
            st.write(f"**Minimum Education:** {parsed.get('education', 'Bachelor Degree')}")
            st.write(f"**Required Experience:** {parsed.get('experience', '2+ years')} ({parsed.get('experience_years', 1.0)} years)")
            
            if parsed.get("certifications"):
                st.write(f"**Relevant Certifications:** {', '.join(parsed['certifications'])}")
            
            st.markdown("---")
            st.markdown("#### 📦 Structured JSON Output (Syllabus Format)")
            json_preview = {
                "job_title": parsed.get("job_title"),
                "required_skills": parsed.get("required_skills"),
                "preferred_skills": parsed.get("preferred_skills"),
                "education": parsed.get("education"),
                "experience": parsed.get("experience"),
                "experience_years": parsed.get("experience_years")
            }
            st.json(json_preview)

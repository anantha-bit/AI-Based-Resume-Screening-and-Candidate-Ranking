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
st.caption("Upload or paste a Job Description to parse mandatory vs optional skills, experience, and education into structured JSON.")

db = DatabaseManager()

# Input Method Tabs
tab1, tab2, tab3 = st.tabs(["✍️ Manual Text Entry", "📤 Upload JD Document", "📚 Select from Catalog"])

jd_raw_text = ""
source_name = "Manual Input"

with tab1:
    manual_text = st.text_area(
        "Paste Full Job Description:",
        height=220,
        placeholder="Job Title: Senior Machine Learning Engineer\n\nResponsibilities:\n- Build transformer models...\n\nRequirements:\n- 4+ years experience with Python, PyTorch, SQL, Transformers..."
    )
    if manual_text.strip():
        jd_raw_text = manual_text.strip()
        source_name = "Manual Text"

with tab2:
    uploaded_file = st.file_uploader("Upload Job Description (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])
    if uploaded_file:
        file_bytes = uploaded_file.read()
        res = DocumentLoader.load_bytes(file_bytes, uploaded_file.name)
        if res["success"]:
            jd_raw_text = res["text"]
            source_name = uploaded_file.name
            st.success(f"Successfully loaded '{uploaded_file.name}' ({len(jd_raw_text)} characters)")
        else:
            st.error(res["error"])

with tab3:
    existing_jds = db.get_all_job_descriptions()
    if existing_jds:
        jd_options = {f"{jd['job_title']} (ID: {jd['id']})": jd for jd in existing_jds}
        selected_option = st.selectbox("Choose a pre-loaded Job Description:", list(jd_options.keys()))
        if st.button("Load Selected JD"):
            selected_jd = jd_options[selected_option]
            jd_raw_text = selected_jd["raw_text"]
            source_name = selected_jd["job_title"]
            st.info(f"Loaded '{selected_jd['job_title']}' from database.")

if st.button("🚀 Analyze & Extract Structured Requirements", type="primary") or (jd_raw_text and "parsed_jd_cache" not in st.session_state):
    if not jd_raw_text:
        st.warning("Please provide a Job Description text or select one from the catalog.")
    else:
        with st.spinner("Analyzing text and extracting requirements..."):
            parsed = JobDescriptionExtractor.extract_from_text(jd_raw_text)
            st.session_state["parsed_jd_cache"] = parsed
            st.session_state["jd_source"] = source_name

if "parsed_jd_cache" in st.session_state:
    parsed = st.session_state["parsed_jd_cache"]
    st.markdown("---")
    st.subheader(f"🎯 Extracted Role: {parsed['job_title']}")

    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown("#### ⚡ Mandatory Technical Skills (Required)")
        if parsed["required_skills"]:
            st.write(" ".join([f"`{s}`" for s in parsed["required_skills"]]))
        else:
            st.info("None explicitly flagged as mandatory.")

        st.markdown("#### 🌟 Nice-to-Have Skills (Preferred)")
        if parsed["preferred_skills"]:
            st.write(" ".join([f"`{s}`" for s in parsed["preferred_skills"]]))
        else:
            st.info("None explicitly flagged as preferred.")

        st.markdown("#### 📋 Key Responsibilities")
        for r in parsed.get("responsibilities", []):
            st.markdown(f"- {r}")

    with c2:
        with st.container(border=True):
            st.markdown("#### 🎓 Qualifications Thresholds")
            st.write(f"**Minimum Education:** {parsed['education']}")
            st.write(f"**Required Experience:** {parsed['experience']} ({parsed['experience_years']} years)")
            
            if parsed.get("certifications"):
                st.write(f"**Relevant Certifications:** {', '.join(parsed['certifications'])}")
            
            st.markdown("---")
            st.markdown("#### 📦 Structured JSON Output (Syllabus Format)")
            json_preview = {
                "job_title": parsed["job_title"],
                "required_skills": parsed["required_skills"],
                "preferred_skills": parsed["preferred_skills"],
                "education": parsed["education"],
                "experience": parsed["experience"],
                "experience_years": parsed["experience_years"]
            }
            st.json(json_preview)

            if st.button("💾 Save Job Description to Database"):
                new_id = db.save_job_description(parsed)
                st.success(f"Saved to database with ID: {new_id}!")

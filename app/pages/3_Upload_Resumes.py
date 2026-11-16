"""
Page 3: Resume Upload and Batch Processing.
Ingests multiple PDF, DOCX, and TXT resumes, extracts sections, and converts into structured JSON.
Academic context: Unit 1 & Unit 2 (Document Ingestion & Section Identification).
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
from src.preprocessing.document_loader import DocumentLoader
from src.extraction.resume_extractor import ResumeExtractor
from src.storage.database import DatabaseManager

st.set_page_config(page_title="Upload Resumes | AI Screening", page_icon="📤", layout="wide")

st.title("📤 Resume Ingestion & Batch Document Processing")
st.caption("Upload multiple candidate resumes in PDF, DOCX, or TXT format. The system automatically segments sections, identifies skills, and extracts experience without crashes.")

db = DatabaseManager()

# Multi-file Uploader
uploaded_files = st.file_uploader(
    "Upload Candidate Resumes (PDF, DOCX, TXT):",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"📁 {len(uploaded_files)} file(s) selected for processing.")
    
    if st.button("🚀 Process & Parse Resumes", type="primary"):
        parsed_batch = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, f in enumerate(uploaded_files):
            status_text.text(f"Processing ({idx+1}/{len(uploaded_files)}): {f.name}...")
            file_bytes = f.read()
            doc_res = DocumentLoader.load_bytes(file_bytes, f.name)

            if not doc_res["success"]:
                st.error(f"❌ Error in '{f.name}': {doc_res['error']}")
                continue

            parsed_resume = ResumeExtractor.parse_resume(doc_res["text"], f.name)
            parsed_batch.append(parsed_resume)
            db.save_resume(parsed_resume)
            progress_bar.progress((idx + 1) / len(uploaded_files))

        status_text.text("✅ Ingestion complete!")
        st.session_state["recent_parsed_batch"] = parsed_batch
        st.success(f"Successfully processed and saved {len(parsed_batch)} resumes to database!")

# Display Processed Resumes
all_resumes = db.get_all_resumes()
if all_resumes:
    st.markdown("---")
    st.subheader(f"📑 Stored Candidate Profiles ({len(all_resumes)})")

    table_data = []
    for r in all_resumes:
        table_data.append({
            "Candidate ID": r["candidate_id"],
            "Candidate Name": r["candidate_name"],
            "File Name": r["file_name"],
            "Experience (Yrs)": f"{r['total_experience_years']:g}",
            "Top Skills": ", ".join(r["skills"][:6]) + ("..." if len(r["skills"]) > 6 else ""),
            "Projects Documented": len(r["projects"]),
            "Ingestion Date": r["created_at"]
        })

    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    # Detailed Inspect Expander
    with st.expander("🔍 Deep-Dive: Inspect Parsed Structured Resume (JSON)"):
        selected_id = st.selectbox("Select Candidate to View Raw JSON:", [r["candidate_id"] for r in all_resumes])
        matched_cand = next((r for r in all_resumes if r["candidate_id"] == selected_id), None)
        if matched_cand:
            st.json(matched_cand)

"""
Page 3: Resume Ingestion & Batch Document Processing.
Ingests multiple PDF, DOCX, and TXT resumes, extracts sections, and converts into structured JSON.
Includes one-click downloads for all 32 candidate benchmark resumes (Bulk ZIP and Individual).
Academic context: Unit 1 & Unit 2 (Document Ingestion & Section Identification).
"""

import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
from src.preprocessing.document_loader import DocumentLoader
from src.extraction.resume_extractor import ResumeExtractor
from src.storage.database import DatabaseManager
from src.reporting.archive_manager import ArchiveManager

st.set_page_config(page_title="Upload Resumes | AI Screening", page_icon="📤", layout="wide")

st.title("📤 Resume Ingestion & Batch Document Processing")
st.caption("Upload multiple candidate resumes in PDF, DOCX, or TXT format, or explore and download the pre-loaded benchmark catalog of 32 multi-tier candidate resumes.")

db = DatabaseManager()

# ==============================================================================
# SECTION 1: DOWNLOAD BENCHMARK RESUME CATALOG (ALL 32 PROFILES)
# ==============================================================================
st.markdown("### 📥 Download Pre-Loaded Candidate Resumes (32 Profiles)")
st.info("The system includes 32 pre-crafted candidate resumes across 8 technical domains, career switchers, and negative controls. You can download the entire dataset as a single ZIP archive or download any individual resume in its native format (.pdf, .docx, .txt).")

c_dl1, c_dl2 = st.columns([1, 1])

# Column 1: Bulk ZIP Download
with c_dl1:
    with st.container(border=True):
        st.markdown("#### 📦 Bulk Download Archive")
        st.write("Download all **32 candidate resumes** bundled into a single ZIP archive for offline examination or testing.")
        
        zip_bytes = ArchiveManager.create_resumes_zip_bytes()
        st.download_button(
            label="⬇️ Download All 32 Resumes (.ZIP)",
            data=zip_bytes,
            file_name="All_32_Candidate_Resumes.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True
        )
        st.caption("Includes 12 PDFs, 10 DOCXs, and 10 TXTs across Senior, Mid, Junior, and Control profiles (378 KB).")

# Column 2: Individual Resume Download
with c_dl2:
    with st.container(border=True):
        st.markdown("#### 📄 Single Resume Download")
        st.write("Select a specific candidate from the catalog to download their original document:")
        
        all_db_resumes = db.get_all_resumes()
        # Sort by candidate_id
        sorted_resumes = sorted(all_db_resumes, key=lambda x: x.get("candidate_id", ""))
        
        resume_options = {}
        for r in sorted_resumes:
            fname = r.get("file_name", "")
            ext = os.path.splitext(fname)[1].upper().replace(".", "")
            label = f"{r.get('candidate_name', 'Unknown')} ({r.get('candidate_id', '')}) — {ext}"
            resume_options[label] = r
            
        selected_res_label = st.selectbox(
            "Choose Candidate Resume:",
            list(resume_options.keys()) if resume_options else ["No resumes available"],
            key="individual_resume_picker"
        )
        
        if resume_options and selected_res_label in resume_options:
            selected_cand = resume_options[selected_res_label]
            file_name = selected_cand.get("file_name", "")
            file_data = ArchiveManager.get_resume_file_data(file_name)
            
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                if file_data:
                    raw_bytes, mime_type = file_data
                    ext_label = os.path.splitext(file_name)[1].upper().replace(".", "")
                    st.download_button(
                        label=f"📥 Download {ext_label} Resume",
                        data=raw_bytes,
                        file_name=file_name,
                        mime=mime_type,
                        use_container_width=True
                    )
                else:
                    st.warning("File binary not found on disk.")
                    
            with sub_col2:
                # Option to download parsed JSON representation
                json_str = json.dumps(selected_cand, indent=2)
                st.download_button(
                    label="📄 Download JSON Profile",
                    data=json_str,
                    file_name=f"{selected_cand.get('candidate_id', 'candidate')}_parsed.json",
                    mime="application/json",
                    use_container_width=True
                )

st.markdown("---")

# ==============================================================================
# SECTION 2: RESUME UPLOAD & PARSING
# ==============================================================================
st.markdown("### 📤 Upload New Candidate Resumes")
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
        st.rerun()

st.markdown("---")

# ==============================================================================
# SECTION 3: DISPLAY STORED CANDIDATE PROFILES
# ==============================================================================
all_resumes = db.get_all_resumes()
if all_resumes:
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
    with st.expander("🔍 Deep-Dive: Inspect Parsed Structured Resume (JSON) & Download File"):
        selected_id = st.selectbox("Select Candidate to Inspect:", [r["candidate_id"] for r in all_resumes])
        matched_cand = next((r for r in all_resumes if r["candidate_id"] == selected_id), None)
        if matched_cand:
            c_ins1, c_ins2 = st.columns([3, 1])
            with c_ins1:
                st.markdown(f"**Candidate:** {matched_cand.get('candidate_name')} | **File:** `{matched_cand.get('file_name')}`")
            with c_ins2:
                file_name = matched_cand.get("file_name", "")
                f_data = ArchiveManager.get_resume_file_data(file_name)
                if f_data:
                    raw_b, m_type = f_data
                    st.download_button(
                        f"⬇️ Download {file_name}",
                        data=raw_b,
                        file_name=file_name,
                        mime=m_type,
                        use_container_width=True
                    )
            st.json(matched_cand)

"""
AI-Based Resume Screening & Candidate Ranking.
Streamlit Main Application Entrypoint.
Academic context: PES University (UE24AM343AB5: Prompt Engineering for Generative AI).
Team Members: Ananthakrishna M, Amar Patil, Akash G K.
"""

import sys
import os

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from src.storage.database import DatabaseManager

# Page Configuration
st.set_page_config(
    page_title="AI Resume Screening & Candidate Ranking",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/fluency/96/resume.png", width=70)
st.sidebar.title("AI Recruitment Assistant")
st.sidebar.caption("PES University • B.Tech CSE (AI & ML)")
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Course:** UE24AM343AB5  
**Subject:** Prompt Engineering for GenAI  
**Team:**  
- Ananthakrishna M (PES1UG24AM036)  
- Amar Patil (PES1UG24AM031)  
- Akash G K (PES1UG24AM022)  
""")

# Main Content Header
st.markdown('<div class="main-header">🎯 AI-Based Resume Screening & Candidate Ranking</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">An explainable, evidence-grounded recruitment intelligence platform comparing Classical NLP, Transformer Semantic Embeddings, and 10 Prompt Engineering Strategies.</div>', unsafe_allow_html=True)

# System Health & Database Status
db = DatabaseManager()
jds = db.get_all_job_descriptions()
resumes = db.get_all_resumes()
screenings = db.get_latest_screening_results()
experiments = db.get_experiment_summary()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Catalog Job Roles", len(jds))
with col2:
    st.metric("Resumes Ingested", len(resumes))
with col3:
    st.metric("Candidates Screened", len(screenings))
with col4:
    st.metric("Prompt Benchmarks", len(experiments))

st.markdown("---")

# Quick Tour / Module Navigator Cards
st.subheader("📌 System Architecture & Core Modules")

c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True):
        st.markdown("### 📄 Job Description Analysis")
        st.write("Browse role catalog, extract technical skills, mandatory vs optional criteria, education, and experience into structured JSON.")
        st.page_link("pages/2_Job_Description_Analysis.py", label="Open JD Analysis →", icon="🔍")

    with st.container(border=True):
        st.markdown("### 📊 Candidate Rankings")
        st.write("Sortable leaderboard with multi-criteria weighted scoring, transparent explanations, and recruiter action badges.")
        st.page_link("pages/5_Candidate_Rankings.py", label="View Rankings →", icon="🏆")

with c2:
    with st.container(border=True):
        st.markdown("### 📂 Resume Ingestion & Catalog")
        st.write("Batch upload resumes or download all 32 candidate benchmark resumes (.ZIP or single files in PDF, DOCX, TXT). Automatic section segmentation.")
        st.page_link("pages/3_Upload_Resumes.py", label="Manage & Download Resumes →", icon="📤")

    with st.container(border=True):
        st.markdown("### 👤 Individual Candidate Dossier")
        st.write("In-depth candidate radar analysis, verbatim evidence citations, gap analysis, and one-click PDF export.")
        st.page_link("pages/6_Individual_Candidate_Analysis.py", label="Examine Candidate →", icon="📋")

with c3:
    with st.container(border=True):
        st.markdown("### ⚙️ Candidate Screening Engine")
        st.write("Execute real-time screening runs with configurable weights across skills, education, experience, and semantic fit.")
        st.page_link("pages/4_Candidate_Screening.py", label="Run Screening →", icon="⚡")

    with st.container(border=True):
        st.markdown("### 🧪 Prompt Engineering Suite")
        st.write("Benchmark 10 prompt strategies (Zero-shot, Few-shot, CoT, Grounded, JSON, Chaining, Refinement, Self-Consistency).")
        st.page_link("pages/7_Prompt_Engineering_Experiments.py", label="Run Experiments →", icon="🧪")

st.markdown("---")

# Bottom Highlights
c_eval1, c_eval2 = st.columns([2, 1])
with c_eval1:
    st.info("💡 **Getting Started:** Navigate to **Job Description Analysis** to inspect or switch role catalog items, then proceed to **Candidate Screening** or explore **Prompt Engineering Experiments**.")
with c_eval2:
    with st.container(border=True):
        st.markdown("#### 📈 Academic Evaluation")
        st.page_link("pages/8_Evaluation_Dashboard.py", label="Open IR Metrics Dashboard →", icon="📊")

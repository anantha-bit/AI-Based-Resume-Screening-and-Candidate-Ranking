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
    .highlight-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
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
    st.metric("Active Job Descriptions", len(jds))
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
        st.write("Extract technical skills, mandatory vs optional criteria, education, and experience requirements into structured JSON.")
        st.page_link("pages/2_Job_Description_Analysis.py", label="Open JD Analysis →", icon="🔍")

    with st.container(border=True):
        st.markdown("### 📊 Candidate Rankings")
        st.write("Sortable leaderboard with multi-criteria weighted scoring, transparent explanations, and recruiter action badges.")
        st.page_link("pages/5_Candidate_Rankings.py", label="View Rankings →", icon="🏆")

    with st.container(border=True):
        st.markdown("### 🔬 Model Comparison")
        st.write("Direct side-by-side evaluation between Classical TF-IDF, Sentence-BERT semantic matching, and Grounded LLMs.")
        st.page_link("pages/8_Model_Comparison.py", label="Compare Models →", icon="⚖️")

with c2:
    with st.container(border=True):
        st.markdown("### 📂 Resume Upload & Parsing")
        st.write("Batch upload resumes in PDF, DOCX, or TXT. Automatic section segmentation and entity extraction without crashes.")
        st.page_link("pages/3_Upload_Resumes.py", label="Upload Resumes →", icon="📤")

    with st.container(border=True):
        st.markdown("### 👤 Individual Candidate Dossier")
        st.write("In-depth candidate radar analysis, verbatim evidence citations, gap analysis, and one-click PDF export.")
        st.page_link("pages/6_Individual_Candidate_Analysis.py", label="Examine Candidate →", icon="📋")

    with st.container(border=True):
        st.markdown("### 📈 Evaluation Dashboard")
        st.write("Academic metrics: Confusion Matrix, Precision@K, Recall@K, NDCG@K, MRR, and entity extraction F1 scores.")
        st.page_link("pages/9_Evaluation_Dashboard.py", label="View Metrics →", icon="📊")

with c3:
    with st.container(border=True):
        st.markdown("### ⚙️ Candidate Screening Engine")
        st.write("Execute real-time screening runs with configurable weights across skills, education, experience, and semantic fit.")
        st.page_link("pages/4_Candidate_Screening.py", label="Run Screening →", icon="⚡")

    with st.container(border=True):
        st.markdown("### 🧪 Prompt Engineering Suite")
        st.write("Benchmark 10 prompt strategies (Zero-shot, Few-shot, CoT, Grounded, JSON, Chaining, Refinement, Self-Consistency).")
        st.page_link("pages/7_Prompt_Engineering_Experiments.py", label="Run Experiments →", icon="🧪")

    with st.container(border=True):
        st.markdown("### ℹ️ About Project & Syllabus")
        st.write("Syllabus mapping table (PES University UE24AM343AB5), team information, and academic references.")
        st.page_link("pages/10_About_Project.py", label="About Project →", icon="🎓")

st.markdown("---")
st.info("💡 **Getting Started:** Navigate to **Job Description Analysis** to inspect or upload a role, then proceed to **Candidate Screening** or explore **Prompt Engineering Experiments**.")

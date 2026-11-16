"""
Page 10: About Project, Team & Syllabus Mapping.
Documents institutional information, syllabus compliance, architecture, and academic citations.
Academic context: PES University (UE24AM343AB5: Prompt Engineering for Generative AI).
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

st.set_page_config(page_title="About Project | AI Screening", page_icon="🎓", layout="wide")

st.title("🎓 Academic Context, Team & Syllabus Compliance")
st.caption("PES University • Department of Computer Science & Engineering (Artificial Intelligence and Machine Learning)")

# Team Information Section
st.subheader("👥 Project Team Members")
c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True):
        st.markdown("### 👨‍💻 Ananthakrishna M")
        st.write("**SRN:** `PES1UG24AM036`")
        st.write("**Program:** B.Tech CSE (AI & ML)")
        st.write("**Institution:** PES University, Bengaluru")

with c2:
    with st.container(border=True):
        st.markdown("### 👨‍💻 Amar Patil")
        st.write("**SRN:** `PES1UG24AM031`")
        st.write("**Program:** B.Tech CSE (AI & ML)")
        st.write("**Institution:** PES University, Bengaluru")

with c3:
    with st.container(border=True):
        st.markdown("### 👨‍💻 Akash G K")
        st.write("**SRN:** `PES1UG24AM022`")
        st.write("**Program:** B.Tech CSE (AI & ML)")
        st.write("**Institution:** PES University, Bengaluru")

st.markdown("---")

# Course Details & Syllabus Mapping Table
st.subheader("📚 Subject Syllabus to Implementation Mapping")
st.markdown("""
**Course Code:** `UE24AM343AB5`  
**Course Title:** `Prompt Engineering for Generative AI`  
**Curriculum Year:** 2026–2027 • **Semester:** 5th Semester • **Elective Credit:** 4 Credits  
""")

mapping_data = [
    {
        "Syllabus Unit": "Unit 1: Foundations of GenAI & Prompting",
        "Key Course Topics": "Word Embeddings, Transformer Principles, Anatomy of Prompt (instructions, context, input, output), Zero-shot, Few-shot.",
        "Project Implementation Component": "Sentence-BERT dense embeddings, TF-IDF baseline, structured prompt architecture, Zero-shot, Few-shot and Role-based prompt strategies."
    },
    {
        "Syllabus Unit": "Unit 2: Practices for Text Generation with LLMs",
        "Key Course Topics": "Handling JSON, Lists, Summarization, Chunking text, Output parsers, Document loaders, Text splitters, Prompt chaining.",
        "Project Implementation Component": "PDF/DOCX document loaders, resume section chunking, structured JSON schema enforcement, multi-stage Chained Prompting pipeline."
    },
    {
        "Syllabus Unit": "Unit 3: Autonomous Agents with Memory & Tools",
        "Key Course Topics": "Vector databases (FAISS, Chroma), RAG, Chain-of-Thought (CoT), Agents with memory & tools, ReAct, Self-consistency.",
        "Project Implementation Component": "Vector similarity matching, Chain-of-Thought structured task decomposition, Grounded evidence citation, Self-consistency sampling."
    },
    {
        "Syllabus Unit": "Unit 4: AI Applications & Evaluation",
        "Key Course Topics": "Building AI-powered applications, multimodal/structured interfaces, prompt benchmarking, ethical AI & bias mitigation.",
        "Project Implementation Component": "Complete 10-page Streamlit application, SQLite persistence, PDF report exporter, multi-criteria ranking, Fairness & Audit checks."
    }
]
st.table(mapping_data)

st.markdown("---")

# Architectural Workflow
st.subheader("🏗️ System Architecture & Workflow Pipeline")
st.markdown("""
```mermaid
graph TD
    JD[Job Description Input] --> JDExtract[JD Extractor Module]
    JDExtract --> JD_JSON[Structured JD Requirements]

    Resumes[Candidate Resumes PDF/DOCX/TXT] --> DocLoader[Document Loader]
    DocLoader --> ResExtract[Resume Sectioner & Entity Extractor]
    ResExtract --> Res_JSON[Structured Candidate Profile]

    JD_JSON & Res_JSON --> Classical[Module 3: Classical NLP/ML Baseline]
    JD_JSON & Res_JSON --> Semantic[Module 4: Transformer Semantic Matcher]
    JD_JSON & Res_JSON --> LLM[Module 5: Grounded LLM Extractor]
    JD_JSON & Res_JSON --> Prompts[Module 6: 10 Prompt Engineering Strategies]

    Classical & Semantic & LLM --> Ranker[Module 7: Multi-Criteria Ranker]
    Ranker --> Leaderboard[Interactive Candidate Leaderboard]
    Ranker --> Dossier[Candidate Dossier + PDF Export]
    Prompts & Ranker --> EvalDash[Module 9: Academic Evaluation Dashboard]
```
""")

st.markdown("---")

# Academic References & Literature
st.subheader("📖 Academic References & Literature Survey")
st.markdown("""
1. **Brown, T. et al. (2020).** *Language Models are Few-Shot Learners.* NeurIPS.
2. **Wei, J. et al. (2022).** *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* NeurIPS.
3. **Zhou, D. et al. (2022).** *Least-to-Most Prompting Enables Complex Reasoning in Large Language Models.* ICLR.
4. **Wang, X. et al. (2022).** *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* ICLR.
5. **Yao, S. et al. (2023).** *ReAct: Synergizing Reasoning and Acting in Language Models.* ICLR.
6. **Sahoo, P. et al. (2024).** *A Systematic Survey of Prompt Engineering in Large Language Models.* arXiv.
7. **Phoenix, J. & Taylor, M. (2024).** *Prompt Engineering for Generative AI.* O'Reilly Media.
8. **Jurafsky, D. & Martin, J. H. (2024).** *Speech and Language Processing (3rd ed. draft).* Stanford University.
""")

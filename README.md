# 🎯 AI-Based Resume Screening & Candidate Ranking

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Sentence-Transformers](https://img.shields.io/badge/Sentence--Transformers-all--MiniLM--L6--v2-yellow.svg)](https://www.sbert.net/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Institution: PES University](https://img.shields.io/badge/Institution-PES%20University-orange.svg)](https://pes.edu/)
[![Course: UE24AM343AB5](https://img.shields.io/badge/Course-UE24AM343AB5-red.svg)](#-syllabus-compliance--academic-context)

> An explainable, evidence-grounded recruitment intelligence platform that evaluates candidate resumes against complex job descriptions, pairs deterministic multi-criteria scoring with dense Transformer semantic matching (Sentence-BERT), and benchmarks ten distinct Large Language Model prompt-engineering paradigms.

---

## 👥 Team Information

**Institution:** PES University, Bengaluru  
**Department:** Department of Computer Science & Engineering (Artificial Intelligence & Machine Learning)  
**Program:** Bachelor of Technology in CSE (AI & ML)  
**Course Code:** `UE24AM343AB5` — *Prompt Engineering for Generative AI* (5th Semester, 2026–2027)

| Team Member | Student Registration Number (SRN) | Primary Focus Areas |
| :--- | :--- | :--- |
| **Ananthakrishna M** | `PES1UG24AM036` | System Architecture, Prompt Engineering Benchmarking, Evaluation Suite |
| **Amar Patil** | `PES1UG24AM031` | Multi-Format Document Ingestion, Streamlit Web Platform, SQLite Persistence |
| **Akash G K** | `PES1UG24AM022` | Structured Information Extraction, S-BERT Semantic Matcher, Grounded Citations |

---

## 📑 Deliverables & Repository Navigation

- **Academic Project Report (Word):** [`reports/Project_Report.docx`](reports/Project_Report.docx)
- **Academic Project Report (PDF):** [`reports/Project_Report.pdf`](reports/Project_Report.pdf)
- **University Presentation (PowerPoint):** [`presentation/Project_Presentation.pptx`](presentation/Project_Presentation.pptx)
- **Architecture Documentation:** [`docs/architecture.md`](docs/architecture.md)
- **Methodology & Mathematical Models:** [`docs/methodology.md`](docs/methodology.md)
- **Research Gap & Literature Survey:** [`docs/research_gap.md`](docs/research_gap.md)
- **User & Administrator Guide:** [`docs/user_guide.md`](docs/user_guide.md)
- **Benchmark Dataset Documentation:** [`data/README.md`](data/README.md)

---

## 🔍 Problem Statement & Motivation

### The Problem
Modern corporate job openings attract hundreds to thousands of applicants. Manual line-by-line review takes 3–7 minutes per resume, creating severe hiring bottlenecks. Conventional Applicant Tracking Systems (ATS) rely on exact keyword matching and TF-IDF similarity, leading to two critical failure modes:
1. **Severe False-Negative Rejections:** Highly qualified candidates who describe skills using synonymous or alternative phrasing (e.g., *"PostgreSQL query optimization"* instead of *"Relational Database Management"*) are automatically disqualified.
2. **Vulnerability to Keyword Stuffing:** Unqualified candidates who repeat target keywords in hidden or white text achieve artificially elevated scores.

### The Research Motivation
While generative Large Language Models (LLMs) excel at contextual language understanding, unconstrained LLM screening introduces acute hazards:
- **Factual Hallucination:** Inferring unearned degrees, credentials, or years of experience.
- **Evaluation Drift:** Non-deterministic score variance across identical resumes.
- **Opacity & Demographic Bias:** Black-box decisions without verifiable proof.

### The Proposed Solution
Our system establishes a **controlled, evidence-grounded screening workflow** that couples:
1. **Deterministic Multi-Criteria Scoring** across six calibrated dimensions.
2. **Dense Transformer Semantic Embeddings** (`all-MiniLM-L6-v2`) to capture technical synonymy.
3. **Grounded Entity Extraction** mandating verbatim resume citations for every verified qualification with zero hallucinations.

---

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph Ingestion Layer
        JD_In[8 Catalog Job Descriptions: Text / PDF / DOCX] --> JDExtract[Job Description Extractor]
        Resume_In[32 Candidate Resumes: PDF / DOCX / TXT] --> DocLoader[Document Loader]
        DocLoader --> ResExtract[Resume Sectioner & Entity Extractor]
    end

    subgraph Analytical Engines
        JDExtract --> JD_JSON[Structured Requirements JSON]
        ResExtract --> Res_JSON[Structured Candidate Profile JSON]
        
        JD_JSON & Res_JSON --> Baseline[Module 3: Classical NLP/ML Baseline]
        JD_JSON & Res_JSON --> Semantic[Module 4: Transformer Semantic Matcher]
        JD_JSON & Res_JSON --> LLM_Engine[Module 5: Grounded Skill Extractor]
    end

    subgraph Scoring & Persistence
        Baseline & Semantic & LLM_Engine --> Ranker[Module 6: Multi-Criteria Weighted Ranker]
        Ranker --> DB[(SQLite Database: app_database.db)]
    end

    subgraph Streamlit Web Application
        DB --> UI_Dash[Page 1: Executive Dashboard]
        DB --> UI_JD[Page 2: JD Requirement Extraction & Catalog]
        DB --> UI_Upload[Page 3: Batch Resume Ingestion]
        DB --> UI_Screen[Page 4: Candidate Screening Runner]
        DB --> UI_Rank[Page 5: Candidate Leaderboard]
        DB --> UI_Dossier[Page 6: Candidate Dossier & PDF Export]
        DB --> UI_Prompt[Page 7: Prompt Engineering Suite]
        DB --> UI_Eval[Page 8: Academic Evaluation Dashboard]
    end
```

---

## 📚 Expanded Role Catalog & Candidate Cohort

The system includes **8 pre-configured industry Job Descriptions** and **32 multi-tier candidate resumes** across multiple technical domains:

### 1. Job Descriptions in Catalog
1. **Senior Machine Learning Engineer** (AI, Transformers, RAG, PyTorch)
2. **Full Stack Software Developer** (React, TypeScript, FastAPI, PostgreSQL)
3. **Data Analyst / Business Intelligence Specialist** (SQL, Power BI, Tableau, Python)
4. **Cloud DevOps & Site Reliability Engineer (SRE)** (AWS, Kubernetes, Terraform, Docker, CI/CD)
5. **Generative AI & LLM Solutions Architect** (LangChain, LlamaIndex, Vector DBs, Fine-Tuning)
6. **Backend Distributed Systems Engineer** (Python, Go, Kafka, Redis, Microservices)
7. **Mobile Application Developer** (Flutter, Dart, React Native, Mobile UI)
8. **Cybersecurity Analyst & DevSecOps Specialist** (SIEM, Vulnerability Assessment, Network Security)

### 2. Candidate Resumes (32 Multi-Tier Profiles)
- Formats provided: `.pdf`, `.docx`, `.txt`
- Spans Senior Specialists, Mid-Level Engineers, Junior Freshers, Career Switchers, and Negative Control Profiles (Civil Construction, Culinary Pastry Chef, Retail Sales, Mechanical Workshop, Banking Cashier, Hotel Front Desk).

---

## ⚖️ Candidate Scoring Methodology

The overall score $S_{\text{overall}}$ is computed via a configurable weighted linear combination:

$$S_{\text{overall}} = \sum_{i=1}^{6} w_i \cdot s_i$$

```
Required Skills Match:     35%  [w1 = 0.35]
Preferred Skills Match:    15%  [w2 = 0.15]
Education Qualifications:  10%  [w3 = 0.10]
Work Experience Depth:     15%  [w4 = 0.15]
Project Relevance:         10%  [w5 = 0.10]
Transformer Semantic Fit:  15%  [w6 = 0.15]
-------------------------------------------
Total Weighted Score:     100%  [Sum(w) = 1.0]
```

**Recommendation Action Tiers:**
- `Highly Recommended` ($\ge 82\%$): Advance directly to Technical Interview.
- `Strong Candidate` ($\ge 68\%$): Schedule Recruiter Phone Screen.
- `Potential Match` ($\ge 50\%$): Hold for secondary review or related roles.
- `Low Fit` ($< 50\%$): Flag for manual human audit (**No automated rejection**).

---

## 💻 Installation & Quickstart

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Git

### 1. Clone Repository & Install Dependencies
```bash
git clone https://github.com/anantha-bit/AI-Based-Resume-Screening-and-Candidate-Ranking.git
cd AI-Based-Resume-Screening-and-Candidate-Ranking
pip install -r requirements.txt
```

### 2. Launch the Streamlit Web Application
```bash
python run.py
```
*Or alternatively using the Streamlit CLI:*
```bash
streamlit run app/main.py
```

By default, Streamlit binds to **`http://localhost:8501`**. If port 8501 is already occupied by a background or previous process, Streamlit will automatically launch on **`http://localhost:8502`**.

> **Explicit Port Configuration:**  
> To explicitly specify your target port:
> ```bash
> # Force run on Port 8501:
> streamlit run app/main.py --server.port 8501
>
> # Or force run on Port 8502:
> streamlit run app/main.py --server.port 8502
> ```

---

### 📥 Downloading Candidate Resumes (All 32 Profiles)
The platform includes built-in download facilities accessible directly through the web UI:
- **Bulk Download:** On **Page 3 (Resume Ingestion & Batch Document Processing)** or **Page 5 (Candidate Rankings)**, click **`Download All 32 Resumes (.ZIP)`** to retrieve all 32 candidate resumes (14 PDFs, 10 DOCXs, 8 TXTs) in a single compressed archive.
- **Single Resume Download:** Select any candidate from the interactive dropdown on **Page 3** or on **Page 6 (Individual Candidate Analysis)** to download their native `.pdf`, `.docx`, or `.txt` resume document or their structured JSON profile.

### 3. Run Automated Tests
```bash
python run.py test
```
*Runs all 8 unit and integration test suites covering text cleaning, document loading, semantic similarity, prompt experiments, ranking, and evaluation.*

### 4. Execute Academic Experiment Benchmarks
```bash
python run.py benchmark
```
*Executes the complete experimental pipeline across 32 candidates and updates SQLite and `experiments/results_summary.json`.*

---

## 📁 Repository Structure

```
AI-Based-Resume-Screening-and-Candidate-Ranking/
├── .streamlit/
│   └── config.toml                  # Streamlit visual theme configuration
├── app/
│   ├── main.py                      # Main landing page & navigation
│   └── pages/
│       ├── 1_Dashboard.py           # Executive analytics & score distributions
│       ├── 2_Job_Description_Analysis.py # Structured requirement extraction & catalog
│       ├── 3_Upload_Resumes.py      # Batch PDF/DOCX resume ingestion
│       ├── 4_Candidate_Screening.py # Configurable weight screening runner
│       ├── 5_Candidate_Rankings.py  # Sortable leaderboard & CSV export
│       └── 6_Individual_Candidate_Analysis.py # Radar profile & PDF dossier
├── src/
│   ├── preprocessing/               # Text cleaning, contact extraction, loaders
│   ├── extraction/                  # Skill taxonomy (500+ skills), JD/resume parsers
│   ├── classical_ml/                # TF-IDF, Cosine similarity, baseline classifier
│   ├── semantic_matching/           # Sentence-BERT embeddings (all-MiniLM-L6-v2)
│   ├── llm/                         # Multi-provider client & grounded extractor
│   ├── prompt_engineering/          # 10 prompt templates & experimental harness
│   ├── ranking/                     # Multi-criteria ranker & explanation engine
│   ├── evaluation/                  # Classification & IR ranking metric calculations
│   ├── reporting/                   # ReportLab PDF dossier generator
│   └── storage/                     # SQLite database manager
├── data/
│   ├── sample/                      # 8 JDs + 32 sample resumes (PDF, DOCX, TXT)
│   ├── processed/
│   ├── app_database.db              # Pre-seeded SQLite database
│   └── README.md                    # Dataset documentation & attribution
├── experiments/
│   ├── results_summary.json         # Aggregated benchmark experimental results
│   └── run_all_experiments.py       # Master CLI experiment runner
├── reports/
│   ├── Project_Report.docx          # Comprehensive academic university project report
│   └── Project_Report.pdf           # Formatted academic project report PDF
├── presentation/
│   └── Project_Presentation.pptx    # Professional 10-slide academic PowerPoint presentation
├── docs/
│   ├── architecture.md              # Technical specifications
│   ├── methodology.md               # Mathematical formulations
│   ├── research_gap.md              # Literature review & motivation
│   └── user_guide.md                # User & administrator manual
├── tests/
│   └── test_full_suite.py           # Automated pytest suite (8 passing tests)
├── requirements.txt                 # Project dependencies
├── LICENSE                          # MIT License
├── README.md                        # Master repository documentation
└── run.py                           # Convenient multi-command runner
```

---

## 🎓 Syllabus Compliance & Academic Context

This project satisfies all learning outcomes and syllabus units of **PES University Course Code: `UE24AM343AB5` (*Prompt Engineering for Generative AI*)**:

| Syllabus Unit | Core Theoretical Topics | Project Implementation Component |
| :--- | :--- | :--- |
| **Unit 1: Foundations of GenAI & Prompting** | Word Embeddings, Transformers, Anatomy of a Prompt (instructions, context, input, output), Zero-shot, Few-shot | Pretrained Sentence-BERT embeddings, structured prompt anatomy, Zero-shot, Few-shot and Role-based prompt strategies |
| **Unit 2: Practices for Text Generation with LLMs** | Handling JSON, Summarization, Chunking text, Output parsers, Document loaders, Prompt chaining | Multi-format PDF/DOCX loaders, section splitters, strict JSON schema parsing, 3-stage Chained Prompting |
| **Unit 3: Autonomous Agents with Memory & Tools** | Vector databases, RAG, Chain-of-Thought (CoT), Grounded prompting, Self-consistency | Cosine vector similarity, 5-step Chain-of-Thought task decomposition, Grounded evidence citation, Self-consistency sampling |
| **Unit 4: AI Applications & Evaluation** | Building end-to-end applications, structured UI, prompt benchmarking, ethical AI & fairness | Streamlit application, SQLite persistence, ReportLab PDF exporter, Fairness & bias audit |

---

## 🛡️ Ethical Considerations & Fairness

1. **Demographic Neutrality:** Protected personal attributes (gender, age, caste, ethnicity, marital status, and photographs) are strictly excluded from all feature vectors and ranking models.
2. **Decision Support, Not Autonomous Hiring:** The system assists human recruiters by organizing evidence; it does not autonomously reject candidates.
3. **Verifiable Explanations:** Every positive qualification claim must cite an exact verbatim quotation from the candidate's uploaded resume.
4. **Transparent Audit Trail:** All applied weights, score components, and prompt outputs are logged in SQLite for auditability.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
Academic and research usage is permitted with attribution to the authors and PES University.

# User & Administrator Guide

## 1. Quick Start Guide

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Git installed
- Minimum 4GB RAM

### Installation
```bash
git clone https://github.com/anantha-bit/AI-Based-Resume-Screening-and-Candidate-Ranking.git
cd AI-Based-Resume-Screening-and-Candidate-Ranking
pip install -r requirements.txt
```

### Launching the Application
Launch the interactive Streamlit web application:
```bash
python run.py
```
Or directly:
```bash
streamlit run app/main.py
```

### Executing Automated Tests
Run the pytest test suite:
```bash
python run.py test
```

### Running Academic Experiments
Execute the benchmark experiment suite across all models and prompt paradigms:
```bash
python run.py benchmark
```

## 2. Navigating the Web Application

1. **Dashboard (`1_Dashboard.py`)**:
   - Inspect overall metrics, score distribution charts, candidate tier breakdowns, and top candidates.

2. **Job Description Analysis (`2_Job_Description_Analysis.py`)**:
   - Paste job description text, upload a JD document (.pdf, .docx, .txt), or select a pre-loaded catalog role.
   - Click **Analyze & Extract** to view mandatory skills, preferred skills, education, and experience in structured JSON.

3. **Upload Resumes (`3_Upload_Resumes.py`)**:
   - Drag and drop multiple resumes simultaneously.
   - The system automatically segments sections, extracts skills, and saves them to SQLite.

4. **Candidate Screening (`4_Candidate_Screening.py`)**:
   - Select the target job description.
   - Customize multi-criteria scoring weights using sliders.
   - Click **Execute Screening Evaluation** to run the complete evaluation pipeline.

5. **Candidate Rankings (`5_Candidate_Rankings.py`)**:
   - View the sortable leaderboard.
   - Filter candidates by tier, score threshold, or search keyword.
   - Export results as CSV or select a candidate for in-depth analysis.

6. **Individual Candidate Analysis (`6_Individual_Candidate_Analysis.py`)**:
   - View multi-dimensional radar charts.
   - Review verbatim resume evidence quotes and missing skill gaps.
   - Click **Export Dossier as PDF** to generate an official evaluation report.

7. **Prompt Engineering Experiments (`7_Prompt_Engineering_Experiments.py`)**:
   - Compare all 10 prompt strategies on latency, valid JSON rate, completeness, and consistency.
   - Inspect raw prompt templates and system instructions.

8. **Model Comparison (`8_Model_Comparison.py`)**:
   - View side-by-side performance of Classical Baseline, Transformer Semantic, and LLM Grounded models.
   - Explore the TF-IDF vs Semantic scatter plot.

9. **Evaluation Dashboard (`9_Evaluation_Dashboard.py`)**:
   - Review Confusion Matrices, F1-Score, Accuracy, Precision@K, NDCG@K, and MRR metrics.

10. **About Project (`10_About_Project.py`)**:
    - Review PES University course syllabus mapping, team member details, and academic citations.

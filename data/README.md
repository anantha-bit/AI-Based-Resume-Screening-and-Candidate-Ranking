# Dataset Documentation & Academic Attribution

## 1. Overview
This dataset contains representative recruitment artifacts specifically created for evaluating **AI-Based Resume Screening & Candidate Ranking** within the curriculum of **PES University (Course Code: UE24AM343AB5 - Prompt Engineering for Generative AI)**.

## 2. Directory Structure
```
data/
├── sample/
│   ├── JD_Senior_ML_Engineer.txt
│   ├── JD_Full_Stack_Developer.txt
│   ├── JD_Data_Analyst.txt
│   ├── Resume_Arjun_Sharma.pdf
│   ├── Resume_Priya_Nair.docx
│   ├── Resume_Rohan_Verma.txt
│   ├── Resume_Sneha_Kulkarni.pdf
│   ├── Resume_Vikram_Rao.docx
│   ├── Resume_Ananya_Deshmukh.pdf
│   ├── Resume_Rahul_Mehta.txt
│   ├── Resume_Kavya_Iyer.pdf
│   ├── Resume_Aditya_Sen.docx
│   ├── Resume_Divya_Hegde.pdf
│   ├── Resume_Manish_Kumar.txt
│   ├── Resume_Pooja_Patel.docx
│   ├── Resume_Suresh_Reddy_Control.pdf
│   ├── Resume_Meera_Joshi_Control.docx
│   ├── Resume_Kiran_Kumar_Control.txt
│   └── ground_truth_labels.json
├── processed/
└── app_database.db
```

## 3. Ground Truth Annotation Schema
The benchmark ground truth file (`ground_truth_labels.json`) provides expert-verified annotations:
- `candidate_id`: Unique identifier (e.g., `CAND-01`)
- `candidate_name`: Name
- `file_name`: File name in PDF/DOCX/TXT
- `target_jd_id`: Mapped target Job Description (`JD-01`, `JD-02`, or `JD-03`)
- `ground_truth_relevance`: Continuous relevance rating (0.0 to 3.0) for ranking evaluation (NDCG@K)
- `ground_truth_label`: Binary classification label (1 = Relevant/Eligible, 0 = Non-relevant/Control)
- `category`: Candidate qualification archetype (High Match, Moderate Match, Junior, Career Switcher, Negative Control)

## 4. Attribution and Ethics
- **Attribution**: Derived from and calibrated against public benchmark standards (Kaggle Resume Dataset, HuggingFace recruitment benchmarks).
- **Ethics & Privacy**: All personal identities are synthetic demonstration profiles created for university academic evaluation. No real personal personally identifiable information (PII) is exposed.
- **Fairness Guarantee**: The screening system does not factor in demographic attributes (gender, age, caste, ethnicity, marital status, or photographs).
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0).

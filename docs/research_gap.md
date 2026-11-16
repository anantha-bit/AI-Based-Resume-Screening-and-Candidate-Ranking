# Research Gap & Academic Direction

## 1. Context and Problem
High-volume recruitment generates hundreds of resumes per job opening. Conventional Applicant Tracking Systems (ATS) rely on keyword matching and TF-IDF similarity. As documented in recruitment literature, this creates fundamental issues:
- **False Negatives**: Qualified candidates expressing skills in alternative phrasing (e.g., "PostgreSQL optimization" vs "Relational Database Management") are penalized.
- **Keyword Stuffing**: Candidates gaming the system by packing invisible keywords achieve artificially high scores.
- **Lack of Deep Understanding**: Conventional systems cannot assess project complexity, seniority, or qualification gaps.

## 2. The LLM Dilemma
Recent studies propose replacing classical pipelines with Large Language Models. However, naive LLM deployment introduces severe risks:
1. **Hallucination & Fabrication**: Unconstrained LLMs frequently infer credentials, degrees, or years of experience that do not exist in the candidate text.
2. **Inconsistency**: Varying temperatures and non-deterministic reasoning lead to fluctuating candidate scores across evaluations.
3. **Black-Box Decision-Making**: Providing single score outputs without verifiable textual evidence compromises recruiter trust.
4. **Demographic Bias**: LLMs may unconsciously weigh gendered phrasing, names, or non-job-related attributes.

## 3. The Research Gap
While prior work has explored either classical NLP or monolithic LLM screening in isolation, there is a distinct lack of empirical work that:
- Combines deterministic multi-criteria scoring with grounded LLM entity extraction.
- Systematically benchmarks 10 distinct prompt engineering strategies (from zero-shot to self-consistency and critic refinement) on the exact same screening dataset.
- Enforces strict human-in-the-loop decision support with verbatim citation grounding.

## 4. Proposed Contribution
This project addresses the research gap by:
1. Developing a hybrid architecture pairing dense Sentence-BERT contextual embeddings with deterministic multi-factor scoring.
2. Formulating a strict evidence-grounding prompt contract requiring sentence-level provenance for every positive skill claim.
3. Providing an empirical benchmark of 10 prompt strategies measuring latency, output validity, completeness, and consistency.
4. Guaranteeing non-discriminatory recruitment evaluation without autonomous auto-rejection.

"""
Comprehensive Automated Test Suite.
Validates Preprocessing, Extraction, Classical ML, Semantic Matching,
Prompt Engineering, Ranking, and Evaluation components.
"""

import os
import sys
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing.text_cleaner import normalize_text, clean_text_for_nlp, extract_contact_info
from src.preprocessing.document_loader import DocumentLoader
from src.extraction.jd_extractor import JobDescriptionExtractor
from src.extraction.resume_extractor import ResumeExtractor
from src.classical_ml.baseline_screener import ClassicalBaselineScreener
from src.semantic_matching.semantic_screener import SemanticScreener
from src.prompt_engineering.prompt_templates import PROMPT_STRATEGIES
from src.prompt_engineering.prompt_experiments import PromptExperimentRunner
from src.ranking.ranker import CandidateRanker
from src.evaluation.evaluator import AcademicEvaluator


# Sample test fixtures
SAMPLE_JD = """
Job Title: Senior Machine Learning Engineer
Requirements:
- 4+ years experience with Python, PyTorch, Transformers, SQL
Preferred:
- AWS, Docker, Kubernetes
Education:
- Master's or Bachelor's in Computer Science
"""

SAMPLE_RESUME = """
Arjun Sharma
Bengaluru, India | arjun.sharma@email.com | +91 9876543210
PROFESSIONAL SUMMARY
Machine Learning Engineer with 4 years experience in Python, PyTorch, Transformers, and SQL on AWS.
EXPERIENCE
Senior AI Engineer | NeuralTech | 2022 - Present
Built transformer pipelines using PyTorch and deployed on AWS with Docker.
EDUCATION
Master of Science in Computer Science | PES University | 2020
"""


def test_text_cleaner():
    raw = "Contact: test@domain.com, Phone: +91 98765 43210. Visit https://example.com"
    norm = normalize_text(raw)
    assert len(norm) > 0
    clean = clean_text_for_nlp(raw)
    assert "test@domain.com" not in clean
    contacts = extract_contact_info(raw)
    assert "test@domain.com" in contacts["emails"]


def test_jd_extractor():
    jd_dict = JobDescriptionExtractor.extract_from_text(SAMPLE_JD)
    assert "Machine Learning" in jd_dict["job_title"]
    assert "Python" in jd_dict["required_skills"]
    assert "PyTorch" in jd_dict["required_skills"]
    assert jd_dict["experience_years"] >= 4.0


def test_resume_extractor():
    res_dict = ResumeExtractor.parse_resume(SAMPLE_RESUME, "resume.txt")
    assert res_dict["candidate_id"].startswith("CAND-")
    assert "Python" in res_dict["skills"]
    assert "PyTorch" in res_dict["skills"]
    assert res_dict["total_experience_years"] >= 3.0


def test_classical_baseline():
    screener = ClassicalBaselineScreener()
    jd_dict = JobDescriptionExtractor.extract_from_text(SAMPLE_JD)
    res_dict = ResumeExtractor.parse_resume(SAMPLE_RESUME, "resume.txt")
    result = screener.screen_candidate(jd_dict, res_dict)
    assert "baseline_score" in result
    assert 0.0 <= result["baseline_score"] <= 100.0


def test_semantic_screener():
    screener = SemanticScreener()
    sim = screener.calculate_similarity("Relational database management", "MySQL and SQL database architecture")
    assert sim > 0.30
    jd_dict = JobDescriptionExtractor.extract_from_text(SAMPLE_JD)
    res_dict = ResumeExtractor.parse_resume(SAMPLE_RESUME, "resume.txt")
    fit = screener.evaluate_semantic_fit(jd_dict, res_dict)
    assert 0.0 <= fit["semantic_score"] <= 100.0


def test_prompt_engineering_runner():
    runner = PromptExperimentRunner()
    jd_dict = JobDescriptionExtractor.extract_from_text(SAMPLE_JD)
    res_dict = ResumeExtractor.parse_resume(SAMPLE_RESUME, "resume.txt")
    results = runner.run_all_strategies(jd_dict, res_dict)
    assert len(results) == len(PROMPT_STRATEGIES)
    for r in results:
        assert r["output_validity_pct"] == 100.0
        assert r["latency_seconds"] > 0


def test_candidate_ranker():
    ranker = CandidateRanker()
    jd_dict = JobDescriptionExtractor.extract_from_text(SAMPLE_JD)
    res_dict = ResumeExtractor.parse_resume(SAMPLE_RESUME, "resume.txt")
    screener_c = ClassicalBaselineScreener()
    screener_s = SemanticScreener()
    from src.llm.llm_extractor import LLMExtractor
    extractor_l = LLMExtractor()

    c_stats = screener_c.screen_candidate(jd_dict, res_dict)
    s_stats = screener_s.evaluate_semantic_fit(jd_dict, res_dict)
    l_stats = extractor_l.analyze_candidate(jd_dict, res_dict)

    scored = ranker.score_candidate(jd_dict, res_dict, s_stats, c_stats, l_stats)
    assert 0.0 <= scored["overall_score"] <= 100.0
    assert scored["recommendation_badge"] in ["Highly Recommended", "Strong Candidate", "Potential Match", "Low Fit"]


def test_evaluation_metrics():
    y_true = [1, 1, 0, 0, 1]
    y_pred = [1, 1, 0, 1, 1]
    metrics = AcademicEvaluator.calculate_classification_metrics(y_true, y_pred)
    assert metrics["accuracy"] == 0.8
    assert metrics["f1_score"] > 0.7

    p3 = AcademicEvaluator.precision_at_k(["C1", "C2"], ["C1", "C3", "C2"], 3)
    assert p3 == round(2/3, 4)
    mrr = AcademicEvaluator.mean_reciprocal_rank(["C2"], ["C1", "C2", "C3"])
    assert mrr == 0.5

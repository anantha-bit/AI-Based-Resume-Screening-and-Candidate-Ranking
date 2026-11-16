"""
Master Experiment Runner.
Executes Classical, Semantic, LLM, and 10 Prompt-Engineering experiments across the benchmark dataset.
Saves all experiment records into SQLite and JSON for academic reporting and the Streamlit dashboard.
Academic context: Maps to Unit 1, Unit 2, Unit 3 & Unit 4 of PES University UE24AM343AB5.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json
import time
from typing import Dict, Any, List

from src.preprocessing.document_loader import DocumentLoader
from src.extraction.jd_extractor import JobDescriptionExtractor
from src.extraction.resume_extractor import ResumeExtractor
from src.classical_ml.baseline_screener import ClassicalBaselineScreener
from src.semantic_matching.semantic_screener import SemanticScreener
from src.llm.llm_client import LLMClient
from src.llm.llm_extractor import LLMExtractor
from src.prompt_engineering.prompt_experiments import PromptExperimentRunner
from src.ranking.ranker import CandidateRanker
from src.evaluation.evaluator import AcademicEvaluator
from src.storage.database import DatabaseManager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "sample")
EXP_DIR = os.path.join(BASE_DIR, "experiments")


def run_full_benchmark():
    print("================================================================================")
    print("STARTING ACADEMIC BENCHMARK EXPERIMENT SUITE")
    print("PES University - UE24AM343AB5: Prompt Engineering for Generative AI")
    print("Project: AI-Based Resume Screening & Candidate Ranking")
    print("================================================================================")

    db = DatabaseManager()
    baseline_screener = ClassicalBaselineScreener()
    semantic_screener = SemanticScreener()
    llm_client = LLMClient()
    llm_extractor = LLMExtractor(llm_client)
    prompt_runner = PromptExperimentRunner(llm_client)
    ranker = CandidateRanker()

    # 1. Load Ground Truth Metadata
    gt_file = os.path.join(DATA_DIR, "ground_truth_labels.json")
    with open(gt_file, "r", encoding="utf-8") as f:
        gt_data = json.load(f)

    # 2. Ingest and Parse Primary Job Description (Senior ML Engineer)
    jd_path = os.path.join(DATA_DIR, "JD_Senior_ML_Engineer.txt")
    jd_doc = DocumentLoader.load_file(jd_path)
    parsed_jd = JobDescriptionExtractor.extract_from_text(jd_doc["text"])
    jd_id = db.save_job_description(parsed_jd)
    print(f"[OK] Job Description parsed and saved: '{parsed_jd['job_title']}' (ID: {jd_id})")
    print(f"     Required Skills: {parsed_jd['required_skills']}")
    print(f"     Preferred Skills: {parsed_jd['preferred_skills']}")

    # Also parse remaining JDs into DB
    for other_jd_file in ["JD_Full_Stack_Developer.txt", "JD_Data_Analyst.txt"]:
        other_path = os.path.join(DATA_DIR, other_jd_file)
        other_doc = DocumentLoader.load_file(other_path)
        db.save_job_description(JobDescriptionExtractor.extract_from_text(other_doc["text"]))

    # 3. Ingest and Screen all 15 Candidate Resumes
    print("\n--- Ingesting and Screening Resumes ---")
    candidate_records = []
    all_prompt_experiment_records = []
    evaluation_benchmark_items = []

    for item in gt_data["candidates"]:
        cand_id = item["candidate_id"]
        fname = item["file_name"]
        file_path = os.path.join(DATA_DIR, fname)

        # Load document
        doc_result = DocumentLoader.load_file(file_path)
        if not doc_result["success"]:
            print(f"[Error] Failed to load {fname}: {doc_result['error']}")
            continue

        # Extract structured resume
        parsed_resume = ResumeExtractor.parse_resume(doc_result["text"], fname)
        parsed_resume["candidate_id"] = cand_id
        parsed_resume["candidate_name"] = item["candidate_name"]
        db.save_resume(parsed_resume)

        # Screen against primary JD using all 3 paradigms
        classical_stats = baseline_screener.screen_candidate(parsed_jd, parsed_resume)
        semantic_stats = semantic_screener.evaluate_semantic_fit(parsed_jd, parsed_resume)
        llm_analysis = llm_extractor.analyze_candidate(parsed_jd, parsed_resume)

        # Compute Composite Weighted Ranking Score
        scored_cand = ranker.score_candidate(
            parsed_jd, parsed_resume, semantic_stats, classical_stats, llm_analysis
        )
        candidate_records.append(scored_cand)

        # Run 10 Prompt Engineering Strategies on this candidate
        prompt_res_list = prompt_runner.run_all_strategies(parsed_jd, parsed_resume)
        for pres in prompt_res_list:
            pres["candidate_id"] = cand_id
            all_prompt_experiment_records.append(pres)

        # Prepare evaluation entry
        evaluation_benchmark_items.append({
            "candidate_id": cand_id,
            "candidate_name": item["candidate_name"],
            "ground_truth_relevance": item["ground_truth_relevance"],
            "ground_truth_label": item["ground_truth_label"],
            "baseline_score": classical_stats["baseline_score"],
            "semantic_score": semantic_stats["semantic_score"],
            "llm_score": scored_cand["overall_score"]
        })

        print(f"  Processed {cand_id} ({item['candidate_name']}) -> Baseline: {classical_stats['baseline_score']}, Semantic: {semantic_stats['semantic_score']}, LLM Composite: {scored_cand['overall_score']}")

    # 4. Rank Candidates
    ranked_candidates = ranker.rank_candidates(candidate_records)
    db.save_screening_results(jd_id, ranked_candidates)
    db.save_experiment_results(all_prompt_experiment_records)

    print("\n--- FINAL CANDIDATE LEADERBOARD ---")
    for c in ranked_candidates:
        print(f"Rank {c['rank']}: {c['candidate_name']} ({c['candidate_id']}) - Score: {c['overall_score']} - [{c['recommendation_badge']}]")

    # 5. Compute Comprehensive Evaluation Metrics
    eval_results = AcademicEvaluator.benchmark_model_paradigms(evaluation_benchmark_items)
    
    # Aggregate Prompt Engineering Metrics
    prompt_summary = db.get_experiment_summary()

    final_results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "curriculum_course": "UE24AM343AB5 - Prompt Engineering for Generative AI",
        "institution": "PES University, Bengaluru",
        "team_members": [
            {"name": "Ananthakrishna M", "srn": "PES1UG24AM036"},
            {"name": "Amar Patil", "srn": "PES1UG24AM031"},
            {"name": "Akash G K", "srn": "PES1UG24AM022"}
        ],
        "job_description_evaluated": parsed_jd["job_title"],
        "candidates_evaluated_count": len(ranked_candidates),
        "rankings": [
            {
                "rank": c["rank"],
                "candidate_id": c["candidate_id"],
                "candidate_name": c["candidate_name"],
                "overall_score": c["overall_score"],
                "badge": c["recommendation_badge"],
                "matched_skills": c["matched_required_skills"],
                "missing_skills": c["missing_required_skills"],
                "classical_score": c["classical_baseline_score"],
                "semantic_score": c["transformer_semantic_score"]
            }
            for c in ranked_candidates
        ],
        "model_comparison": eval_results,
        "prompt_engineering_benchmark": prompt_summary
    }

    # Save summary JSON
    summary_path = os.path.join(EXP_DIR, "results_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2)

    print(f"\n[SUCCESS] Benchmark complete! Summary saved to {summary_path}")
    print("\nModel Comparison Classification Metrics:")
    for model_name, metrics in eval_results["classification"].items():
        print(f"  {model_name}: Accuracy={metrics['accuracy']}, Precision={metrics['precision']}, Recall={metrics['recall']}, F1={metrics['f1_score']}")

    print("\nModel Comparison Ranking Metrics (NDCG@3 / MRR):")
    for model_name, metrics in eval_results["ranking"].items():
        print(f"  {model_name}: P@1={metrics['P@1']}, P@3={metrics['P@3']}, NDCG@3={metrics['NDCG@3']}, MRR={metrics['MRR']}")

    return final_results


if __name__ == "__main__":
    run_full_benchmark()

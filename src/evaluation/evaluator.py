"""
Academic Evaluation Suite and Benchmarking Engine.
Calculates Accuracy, Precision, Recall, F1, Confusion Matrix, P@K, R@K, NDCG@K, MRR,
and statistical comparisons across Classical, Transformer, and LLM paradigms.
Academic context: Unit 1 & Unit 2 (Model Evaluation, Classification Metrics & Information Retrieval Benchmarks).
"""

import numpy as np
from typing import Dict, Any, List, Tuple
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


class AcademicEvaluator:
    """Computes comprehensive scientific evaluation metrics for recruitment screening."""

    @staticmethod
    def calculate_classification_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, Any]:
        """
        Compute standard classification metrics:
        Accuracy, Precision, Recall, F1, and Confusion Matrix.
        """
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        cm = confusion_matrix(y_true, y_pred).tolist()

        return {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "confusion_matrix": cm,
            "true_negatives": cm[0][0] if len(cm) > 1 else 0,
            "false_positives": cm[0][1] if len(cm) > 1 else 0,
            "false_negatives": cm[1][0] if len(cm) > 1 else 0,
            "true_positives": cm[1][1] if len(cm) > 1 else 0
        }

    @staticmethod
    def precision_at_k(actual_relevant: List[str], predicted_ranked: List[str], k: int) -> float:
        """Calculate Precision@K."""
        if k <= 0 or not predicted_ranked:
            return 0.0
        top_k = predicted_ranked[:k]
        hits = len(set(top_k).intersection(set(actual_relevant)))
        return round(hits / k, 4)

    @staticmethod
    def recall_at_k(actual_relevant: List[str], predicted_ranked: List[str], k: int) -> float:
        """Calculate Recall@K."""
        if not actual_relevant:
            return 0.0
        top_k = predicted_ranked[:k]
        hits = len(set(top_k).intersection(set(actual_relevant)))
        return round(hits / len(actual_relevant), 4)

    @staticmethod
    def mean_reciprocal_rank(actual_relevant: List[str], predicted_ranked: List[str]) -> float:
        """Calculate Reciprocal Rank of the first relevant candidate."""
        for rank, cand_id in enumerate(predicted_ranked, 1):
            if cand_id in actual_relevant:
                return round(1.0 / rank, 4)
        return 0.0

    @staticmethod
    def ndcg_at_k(relevance_scores_true: List[float], candidate_ids_ranked: List[str], id_to_relevance: Dict[str, float], k: int) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain at K (NDCG@K).
        Measures ranking quality with position-discounted rewards.
        """
        if k <= 0 or not candidate_ids_ranked:
            return 0.0

        # DCG@K
        dcg = 0.0
        for i, cid in enumerate(candidate_ids_ranked[:k]):
            rel = id_to_relevance.get(cid, 0.0)
            dcg += (2**rel - 1) / np.log2(i + 2)

        # Ideal DCG@K (IDCG@K)
        ideal_rels = sorted(relevance_scores_true, reverse=True)[:k]
        idcg = 0.0
        for i, rel in enumerate(ideal_rels):
            idcg += (2**rel - 1) / np.log2(i + 2)

        if idcg == 0:
            return 0.0
        return round(float(dcg / idcg), 4)

    @staticmethod
    def evaluate_skill_extraction_f1(annotated_skills: List[str], extracted_skills: List[str]) -> Dict[str, float]:
        """Evaluate Entity Extraction Precision, Recall, and F1 against manual annotations."""
        gold_set = set(s.lower().strip() for s in annotated_skills)
        pred_set = set(s.lower().strip() for s in extracted_skills)

        if not gold_set:
            return {"precision": 1.0, "recall": 1.0, "f1": 1.0}

        true_pos = len(gold_set.intersection(pred_set))
        prec = true_pos / len(pred_set) if pred_set else 0.0
        rec = true_pos / len(gold_set) if gold_set else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        return {
            "entity_precision": round(prec, 4),
            "entity_recall": round(rec, 4),
            "entity_f1": round(f1, 4)
        }

    @classmethod
    def benchmark_model_paradigms(cls, ground_truth_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare the three primary paradigms against ground-truth recruitment labels:
        1. Classical NLP/ML Baseline
        2. Transformer Semantic Matching
        3. LLM-Enhanced Grounded Screening
        """
        y_true = [item["ground_truth_label"] for item in ground_truth_dataset]
        
        # Predict labels based on model scores (threshold >= 65 is positive)
        y_pred_baseline = [1 if item["baseline_score"] >= 65 else 0 for item in ground_truth_dataset]
        y_pred_semantic = [1 if item["semantic_score"] >= 65 else 0 for item in ground_truth_dataset]
        y_pred_llm = [1 if item["llm_score"] >= 65 else 0 for item in ground_truth_dataset]

        baseline_metrics = cls.calculate_classification_metrics(y_true, y_pred_baseline)
        semantic_metrics = cls.calculate_classification_metrics(y_true, y_pred_semantic)
        llm_metrics = cls.calculate_classification_metrics(y_true, y_pred_llm)

        # Ranking metrics on the candidate cohort
        actual_relevant = [item["candidate_id"] for item in ground_truth_dataset if item["ground_truth_label"] == 1]
        
        ranked_baseline = [c["candidate_id"] for c in sorted(ground_truth_dataset, key=lambda x: x["baseline_score"], reverse=True)]
        ranked_semantic = [c["candidate_id"] for c in sorted(ground_truth_dataset, key=lambda x: x["semantic_score"], reverse=True)]
        ranked_llm = [c["candidate_id"] for c in sorted(ground_truth_dataset, key=lambda x: x["llm_score"], reverse=True)]

        id_to_rel = {item["candidate_id"]: float(item["ground_truth_relevance"]) for item in ground_truth_dataset}
        all_true_rels = [float(item["ground_truth_relevance"]) for item in ground_truth_dataset]

        ranking_comparison = {
            "Classical NLP/ML": {
                "P@1": cls.precision_at_k(actual_relevant, ranked_baseline, 1),
                "P@3": cls.precision_at_k(actual_relevant, ranked_baseline, 3),
                "P@5": cls.precision_at_k(actual_relevant, ranked_baseline, 5),
                "R@3": cls.recall_at_k(actual_relevant, ranked_baseline, 3),
                "MRR": cls.mean_reciprocal_rank(actual_relevant, ranked_baseline),
                "NDCG@3": cls.ndcg_at_k(all_true_rels, ranked_baseline, id_to_rel, 3),
                "NDCG@5": cls.ndcg_at_k(all_true_rels, ranked_baseline, id_to_rel, 5)
            },
            "Transformer Semantic": {
                "P@1": cls.precision_at_k(actual_relevant, ranked_semantic, 1),
                "P@3": cls.precision_at_k(actual_relevant, ranked_semantic, 3),
                "P@5": cls.precision_at_k(actual_relevant, ranked_semantic, 5),
                "R@3": cls.recall_at_k(actual_relevant, ranked_semantic, 3),
                "MRR": cls.mean_reciprocal_rank(actual_relevant, ranked_semantic),
                "NDCG@3": cls.ndcg_at_k(all_true_rels, ranked_semantic, id_to_rel, 3),
                "NDCG@5": cls.ndcg_at_k(all_true_rels, ranked_semantic, id_to_rel, 5)
            },
            "LLM-Enhanced Grounded": {
                "P@1": cls.precision_at_k(actual_relevant, ranked_llm, 1),
                "P@3": cls.precision_at_k(actual_relevant, ranked_llm, 3),
                "P@5": cls.precision_at_k(actual_relevant, ranked_llm, 5),
                "R@3": cls.recall_at_k(actual_relevant, ranked_llm, 3),
                "MRR": cls.mean_reciprocal_rank(actual_relevant, ranked_llm),
                "NDCG@3": cls.ndcg_at_k(all_true_rels, ranked_llm, id_to_rel, 3),
                "NDCG@5": cls.ndcg_at_k(all_true_rels, ranked_llm, id_to_rel, 5)
            }
        }

        return {
            "classification": {
                "Classical NLP/ML": baseline_metrics,
                "Transformer Semantic": semantic_metrics,
                "LLM-Enhanced Grounded": llm_metrics
            },
            "ranking": ranking_comparison
        }

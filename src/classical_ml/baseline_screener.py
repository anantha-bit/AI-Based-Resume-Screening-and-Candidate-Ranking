"""
Classical NLP and Machine Learning Baseline Screener.
Implements TF-IDF vectorization, Cosine Similarity, Jaccard Keyword Matching,
and a trained Classical Classifier.
Academic context: Maps to Unit 1 (Text Representation, Word Embeddings & Classification Baselines).
"""

import numpy as np
from typing import Dict, Any, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from src.preprocessing.text_cleaner import clean_text_for_nlp


class ClassicalBaselineScreener:
    """Conventional NLP/ML Resume Screener using TF-IDF and Lexical Overlap."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=5000
        )
        self.classifier = None
        self._init_benchmark_classifier()

    def _init_benchmark_classifier(self):
        """Train a lightweight reference classifier on canonical recruitment text pairs."""
        # Reference synthetic training corpus mapping candidate text to fit (0=Low, 1=High)
        training_corpus = [
            # High fit pairs
            "Senior machine learning engineer experienced in python pytorch transformers deep learning sql cloud",
            "Full stack software engineer with react node.js javascript typescript postgresql rest api docker",
            "Data analyst skilled in python sql tableau power bi statistics data cleaning exploratory analysis",
            "Senior backend developer designing microservices java spring boot kubernetes aws ci/cd",
            "AI researcher with natural language processing llms bert prompt engineering rag hugging face",
            # Low / mismatch pairs
            "Store manager in retail inventory management point of sale cash handling customer greeting",
            "Executive chef culinary arts kitchen management menu planning food safety sanitation",
            "Real estate agent property sales client showings mortgage leasing contract negotiation",
            "Elementary school teacher curriculum planning classroom management parent communication",
            "Civil construction worker site safety scaffolding concrete pouring masonry heavy equipment"
        ]
        labels = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
        
        X = self.vectorizer.fit_transform(training_corpus)
        self.classifier = LogisticRegression(random_state=42)
        self.classifier.fit(X, labels)

    def calculate_tfidf_similarity(self, jd_text: str, resume_text: str) -> float:
        """Calculate TF-IDF Cosine Similarity between Job Description and Resume."""
        clean_jd = clean_text_for_nlp(jd_text)
        clean_res = clean_text_for_nlp(resume_text)
        
        if not clean_jd or not clean_res:
            return 0.0

        try:
            # Transform using pre-fitted or joint vectorizer
            local_vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
            tfidf_matrix = local_vec.fit_transform([clean_jd, clean_res])
            sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(np.clip(sim, 0.0, 1.0))
        except Exception:
            return 0.0

    def calculate_keyword_overlap(self, jd_skills: List[str], resume_skills: List[str]) -> Dict[str, Any]:
        """
        Compute lexical keyword overlap: Jaccard similarity, precision, and recall.
        Demonstrates the exact limitations of keyword matching (Slide 6 & Slide 9).
        """
        jd_set = set(s.lower() for s in jd_skills)
        res_set = set(s.lower() for s in resume_skills)

        if not jd_set:
            return {"jaccard": 0.0, "precision": 0.0, "recall": 0.0, "matched": [], "missing": []}

        matched = jd_set.intersection(res_set)
        missing = jd_set - res_set
        union = jd_set.union(res_set)

        jaccard = len(matched) / len(union) if union else 0.0
        recall = len(matched) / len(jd_set) if jd_set else 0.0
        precision = len(matched) / len(res_set) if res_set else 0.0

        return {
            "jaccard": round(float(jaccard), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "matched_count": len(matched),
            "total_jd_skills": len(jd_set),
            "matched_skills": sorted(list(matched)),
            "missing_skills": sorted(list(missing))
        }

    def predict_suitability_proba(self, resume_text: str) -> float:
        """Predict candidate technical suitability probability using classical classifier."""
        clean_res = clean_text_for_nlp(resume_text)
        if not clean_res:
            return 0.0
        try:
            X = self.vectorizer.transform([clean_res])
            proba = self.classifier.predict_proba(X)[0][1]
            return float(round(proba, 4))
        except Exception:
            return 0.5

    def screen_candidate(self, jd_dict: Dict[str, Any], resume_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run complete classical baseline screening.
        Generates composite baseline score (0 - 100).
        """
        jd_text = jd_dict.get("raw_text", "")
        resume_text = resume_dict.get("raw_text", "")
        
        tfidf_sim = self.calculate_tfidf_similarity(jd_text, resume_text)
        
        req_skills = jd_dict.get("required_skills", [])
        pref_skills = jd_dict.get("preferred_skills", [])
        all_jd_skills = req_skills + pref_skills
        res_skills = resume_dict.get("skills", [])
        
        keyword_stats = self.calculate_keyword_overlap(all_jd_skills, res_skills)
        suitability_proba = self.predict_suitability_proba(resume_text)
        
        # Classical Composite Score: 50% TF-IDF Sim + 30% Keyword Recall + 20% Classifier Proba
        score = (tfidf_sim * 0.50) + (keyword_stats["recall"] * 0.30) + (suitability_proba * 0.20)
        baseline_score = round(float(np.clip(score * 100, 0.0, 100.0)), 2)

        return {
            "method": "Classical NLP/ML Baseline",
            "baseline_score": baseline_score,
            "tfidf_similarity": round(tfidf_sim, 4),
            "keyword_recall": keyword_stats["recall"],
            "keyword_precision": keyword_stats["precision"],
            "keyword_jaccard": keyword_stats["jaccard"],
            "matched_skills_count": keyword_stats["matched_count"],
            "missing_skills_count": len(keyword_stats["missing_skills"]),
            "classifier_probability": suitability_proba,
            "matched_skills": keyword_stats["matched_skills"],
            "missing_skills": keyword_stats["missing_skills"]
        }

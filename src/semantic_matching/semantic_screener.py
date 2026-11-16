"""
Transformer-Based Semantic Matching Module.
Computes dense sentence embeddings using Sentence-BERT / all-MiniLM-L6-v2,
evaluates contextual semantic similarity, and detects semantic equivalence.
Academic context: Maps to Unit 1 (Transformers, Word & Sentence Embeddings) & Unit 3 (Vector Similarity).
"""

import numpy as np
from typing import Dict, Any, List, Optional
from sklearn.metrics.pairwise import cosine_similarity


class SemanticScreener:
    """Computes dense contextual semantic similarity using Sentence Transformers."""

    _model_instance = None

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = self._load_model()

    @classmethod
    def _load_model(cls, model_name: str = "all-MiniLM-L6-v2"):
        """Singleton loader for the pretrained Sentence Transformer model."""
        if cls._model_instance is None:
            try:
                from sentence_transformers import SentenceTransformer
                cls._model_instance = SentenceTransformer(model_name)
            except Exception as e:
                print(f"[Warning] Could not load SentenceTransformer '{model_name}': {e}. Using deterministic embedding fallback.")
                cls._model_instance = None
        return cls._model_instance

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode a list of text strings into dense vector representations."""
        if not texts:
            return np.zeros((0, 384))
        
        if self.model is not None:
            try:
                return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            except Exception as e:
                print(f"[Error] Encoding failed: {e}. Falling back.")
                
        # Deterministic lightweight fallback embedding (hash-based projection into 384 dimensions)
        return self._hash_vector_fallback(texts)

    def _hash_vector_fallback(self, texts: List[str], dim: int = 384) -> np.ndarray:
        """Lightweight deterministic projection used when transformer weights are unavailable."""
        vectors = []
        for text in texts:
            vec = np.zeros(dim, dtype=np.float32)
            words = text.lower().split()
            for i, w in enumerate(words):
                h = hash(w) % dim
                vec[h] += 1.0 / (1.0 + np.log1p(i))
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            vectors.append(vec)
        return np.array(vectors)

    def calculate_similarity(self, text_a: str, text_b: str) -> float:
        """Calculate cosine similarity between two pieces of text."""
        if not text_a.strip() or not text_b.strip():
            return 0.0
        embeddings = self.encode([text_a, text_b])
        sim = cosine_similarity(embeddings[0:1], embeddings[1:2])[0][0]
        return float(np.clip(sim, 0.0, 1.0))

    def evaluate_semantic_fit(self, jd_dict: Dict[str, Any], resume_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate candidate semantic fit across multiple dimensions:
        - Overall text similarity
        - Skills section similarity
        - Experience section similarity
        - Project relevance similarity
        """
        jd_text = jd_dict.get("raw_text", "")
        res_text = resume_dict.get("raw_text", "")
        
        # Sectional texts
        jd_reqs = " ".join(jd_dict.get("required_skills", []) + jd_dict.get("preferred_skills", []))
        jd_resps = " ".join(jd_dict.get("responsibilities", []))
        
        res_sections = resume_dict.get("sections", {})
        res_skills = res_sections.get("skills", "") or " ".join(resume_dict.get("skills", []))
        res_exp = res_sections.get("experience", "")
        res_proj = res_sections.get("projects", "")

        # Compute multi-dimensional similarities
        overall_sim = self.calculate_similarity(jd_text, res_text)
        skills_sim = self.calculate_similarity(jd_reqs, res_skills) if jd_reqs and res_skills else overall_sim
        exp_sim = self.calculate_similarity(jd_resps, res_exp) if jd_resps and res_exp else overall_sim
        proj_sim = self.calculate_similarity(jd_reqs, res_proj) if jd_reqs and res_proj else overall_sim

        # Weighted semantic score
        composite_semantic = (
            (overall_sim * 0.35) +
            (skills_sim * 0.35) +
            (exp_sim * 0.20) +
            (proj_sim * 0.10)
        )
        semantic_score = round(float(np.clip(composite_semantic * 100, 0.0, 100.0)), 2)

        return {
            "method": "Transformer Semantic Matching",
            "semantic_score": semantic_score,
            "overall_similarity": round(overall_sim, 4),
            "skills_similarity": round(skills_sim, 4),
            "experience_similarity": round(exp_sim, 4),
            "project_similarity": round(proj_sim, 4),
            "model_name": self.model_name
        }

    def detect_contextual_term_matches(self, jd_requirement: str, resume_sentences: List[str]) -> List[Dict[str, Any]]:
        """
        Find sentences in resume that have strong semantic affinity with a given JD requirement,
        even when exact phrasing differs (e.g. Relational DB vs MySQL).
        """
        if not jd_requirement or not resume_sentences:
            return []

        req_emb = self.encode([jd_requirement])
        sent_embs = self.encode(resume_sentences)

        sims = cosine_similarity(req_emb, sent_embs)[0]
        
        top_indices = np.argsort(sims)[::-1][:3]
        matches = []
        for idx in top_indices:
            score = float(sims[idx])
            if score > 0.40:
                matches.append({
                    "sentence": resume_sentences[idx],
                    "semantic_similarity": round(score, 4)
                })
        return matches

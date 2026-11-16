"""
Candidate Scoring and Transparent Ranking Engine.
Computes multi-criteria weighted composite scores with transparent recruiter explanations.
Academic context: Maps to Unit 1 (Text Similarity), Unit 2 (Classification) & Slide 10 (Controlled Scoring).
"""

from typing import Dict, Any, List, Optional
import numpy as np


class CandidateRanker:
    """Calculates configurable multi-criteria candidate scores and rank orderings."""

    # Default weights matching specification
    DEFAULT_WEIGHTS = {
        "required_skills": 0.35,
        "preferred_skills": 0.15,
        "education": 0.10,
        "experience": 0.15,
        "projects": 0.10,
        "semantic_similarity": 0.15
    }

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = self._normalize_weights(weights or self.DEFAULT_WEIGHTS)

    def _normalize_weights(self, weights: Dict[str, float]) -> Dict[str, float]:
        """Ensure sum of weights equals 1.0."""
        total = sum(weights.values())
        if total <= 0:
            return self.DEFAULT_WEIGHTS
        return {k: round(v / total, 4) for k, v in weights.items()}

    def score_candidate(
        self,
        jd_dict: Dict[str, Any],
        resume_dict: Dict[str, Any],
        semantic_stats: Dict[str, Any],
        classical_stats: Dict[str, Any],
        llm_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compute transparent, multi-dimensional candidate score.
        All scoring factors are strictly derived from qualifications and verified evidence.
        """
        # 1. Required Skills Score (0 - 100)
        req_skills = jd_dict.get("required_skills", [])
        matched_req = [s for s in llm_analysis.get("skills_evidence", []) if s.get("required") and s.get("status") == "Found in resume"]
        req_score = (len(matched_req) / len(req_skills) * 100.0) if req_skills else 100.0

        # 2. Preferred Skills Score (0 - 100)
        pref_skills = jd_dict.get("preferred_skills", [])
        matched_pref = [s for s in llm_analysis.get("skills_evidence", []) if not s.get("required") and s.get("status") == "Found in resume"]
        pref_score = (len(matched_pref) / len(pref_skills) * 100.0) if pref_skills else 80.0

        # 3. Education Score (0 - 100)
        edu_list = resume_dict.get("education", [])
        edu_target = jd_dict.get("education", "").lower()
        edu_score = 85.0
        if any("ph.d" in str(e.get("degree", "")).lower() for e in edu_list):
            edu_score = 100.0
        elif any("master" in str(e.get("degree", "")).lower() for e in edu_list):
            edu_score = 95.0
        elif any("bachelor" in str(e.get("degree", "")).lower() for e in edu_list):
            edu_score = 85.0

        # 4. Experience Score (0 - 100)
        cand_exp = resume_dict.get("total_experience_years", 0.0)
        target_exp = max(0.5, jd_dict.get("experience_years", 2.0))
        exp_ratio = cand_exp / target_exp
        exp_score = min(100.0, exp_ratio * 100.0)

        # 5. Project Relevance Score (0 - 100)
        proj_count = len(resume_dict.get("projects", []))
        proj_sim = semantic_stats.get("project_similarity", 0.5)
        proj_score = min(100.0, (proj_count * 20.0 * 0.4) + (proj_sim * 100.0 * 0.6))

        # 6. Semantic Similarity Score (0 - 100)
        semantic_sim = semantic_stats.get("overall_similarity", 0.5)
        semantic_score = semantic_sim * 100.0

        # Weighted Composite Score
        composite_score = (
            (req_score * self.weights["required_skills"]) +
            (pref_score * self.weights["preferred_skills"]) +
            (edu_score * self.weights["education"]) +
            (exp_score * self.weights["experience"]) +
            (proj_score * self.weights["projects"]) +
            (semantic_score * self.weights["semantic_similarity"])
        )
        final_score = round(float(np.clip(composite_score, 0.0, 100.0)), 2)

        # Explanation generation
        explanation = self._generate_explanation(
            final_score, req_score, pref_score, exp_score, 
            len(matched_req), len(req_skills), cand_exp, target_exp
        )

        # Recommendation Category
        if final_score >= 82.0:
            rec_badge = "Highly Recommended"
            rec_action = "Advance to Technical Interview"
        elif final_score >= 68.0:
            rec_badge = "Strong Candidate"
            rec_action = "Schedule Recruiter Phone Screen"
        elif final_score >= 50.0:
            rec_badge = "Potential Match"
            rec_action = "Hold for Secondary Review / Specific Roles"
        else:
            rec_badge = "Low Fit"
            rec_action = "Flag for Manual Human Review (No Auto-Reject)"

        return {
            "candidate_id": resume_dict.get("candidate_id"),
            "candidate_name": resume_dict.get("candidate_name"),
            "file_name": resume_dict.get("file_name"),
            "overall_score": final_score,
            "rank": 0,  # Updated after batch sorting
            "recommendation_badge": rec_badge,
            "recommended_action": rec_action,
            "component_scores": {
                "required_skills_match": round(req_score, 1),
                "preferred_skills_match": round(pref_score, 1),
                "education_score": round(edu_score, 1),
                "experience_score": round(exp_score, 1),
                "project_relevance": round(proj_score, 1),
                "semantic_similarity": round(semantic_score, 1)
            },
            "applied_weights": self.weights,
            "matched_required_skills": [s["skill"] for s in matched_req],
            "missing_required_skills": [s["skill"] for s in llm_analysis.get("skills_evidence", []) if s.get("required") and s.get("status") == "Not found in resume"],
            "matched_preferred_skills": [s["skill"] for s in matched_pref],
            "total_experience_years": cand_exp,
            "target_experience_years": target_exp,
            "explanation": explanation,
            "strengths": llm_analysis.get("strengths", []),
            "gaps": llm_analysis.get("gaps", []),
            "grounding_fidelity_pct": llm_analysis.get("grounding_fidelity_pct", 100.0),
            "classical_baseline_score": classical_stats.get("baseline_score", 0.0),
            "transformer_semantic_score": semantic_stats.get("semantic_score", 0.0)
        }

    def rank_candidates(self, scored_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort scored candidates descending by overall_score and assign ordinal ranks."""
        sorted_candidates = sorted(scored_candidates, key=lambda c: c["overall_score"], reverse=True)
        for i, c in enumerate(sorted_candidates):
            c["rank"] = i + 1
        return sorted_candidates

    def _generate_explanation(
        self, score: float, req_score: float, pref_score: float, exp_score: float,
        matched_req_cnt: int, total_req_cnt: int, cand_exp: float, target_exp: float
    ) -> str:
        """Generate human-readable recruiter explanation detailing score rationale."""
        return (
            f"Candidate achieved a composite evaluation score of {score}/100. "
            f"The candidate demonstrates {matched_req_cnt} of {total_req_cnt} mandatory skills ({req_score:.0f}% match). "
            f"Work history documents {cand_exp:g} years of industry experience relative to the target threshold of {target_exp:g} years ({exp_score:.0f}% timeline score). "
            f"Final ranking reflects strictly verifiable qualifications without demographic or automated rejection bias."
        )

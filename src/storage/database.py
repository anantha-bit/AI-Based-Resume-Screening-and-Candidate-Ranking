"""
SQLite Database Storage Module.
Persists Job Descriptions, Resumes, Candidate Rankings, and Experiment Metrics.
Academic context: Unit 2 (Data Storage & Query Systems).
"""

import sqlite3
import json
import os
from typing import Dict, Any, List, Optional

DB_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "app_database.db"
)


class DatabaseManager:
    """Manages SQLite storage for recruitment workflows and academic evaluation benchmarks."""

    def __init__(self, db_path: str = DB_FILE_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_tables()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_tables(self):
        """Create database tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Job Descriptions Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_descriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_title TEXT NOT NULL,
                    required_skills TEXT,
                    preferred_skills TEXT,
                    education TEXT,
                    experience TEXT,
                    experience_years REAL,
                    responsibilities TEXT,
                    certifications TEXT,
                    raw_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Resumes Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resumes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id TEXT UNIQUE NOT NULL,
                    candidate_name TEXT,
                    file_name TEXT,
                    contact_json TEXT,
                    skills_json TEXT,
                    education_json TEXT,
                    experience_json TEXT,
                    total_experience_years REAL,
                    projects_json TEXT,
                    certifications_json TEXT,
                    raw_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Screening Runs Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS screening_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jd_id INTEGER,
                    candidate_id TEXT,
                    candidate_name TEXT,
                    overall_score REAL,
                    rank_order INTEGER,
                    recommendation_badge TEXT,
                    component_scores_json TEXT,
                    matched_skills_json TEXT,
                    missing_skills_json TEXT,
                    explanation TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Prompt Experiments Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompt_experiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    strategy_name TEXT NOT NULL,
                    candidate_id TEXT,
                    score REAL,
                    latency_seconds REAL,
                    output_validity_pct REAL,
                    extraction_completeness_pct REAL,
                    evidence_support_pct REAL,
                    consistency_score REAL,
                    output_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_job_description(self, jd_dict: Dict[str, Any]) -> int:
        """Save or update a job description and return its ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            title = jd_dict.get("job_title", "Untitled Role")
            cursor.execute("SELECT id FROM job_descriptions WHERE job_title = ?", (title,))
            existing = cursor.fetchone()
            if existing:
                jd_id = existing[0]
                cursor.execute("""
                    UPDATE job_descriptions SET
                        required_skills = ?, preferred_skills = ?, education = ?, 
                        experience = ?, experience_years = ?, responsibilities = ?, 
                        certifications = ?, raw_text = ?
                    WHERE id = ?
                """, (
                    json.dumps(jd_dict.get("required_skills", [])),
                    json.dumps(jd_dict.get("preferred_skills", [])),
                    jd_dict.get("education", ""),
                    jd_dict.get("experience", ""),
                    jd_dict.get("experience_years", 1.0),
                    json.dumps(jd_dict.get("responsibilities", [])),
                    json.dumps(jd_dict.get("certifications", [])),
                    jd_dict.get("raw_text", ""),
                    jd_id
                ))
                conn.commit()
                return jd_id
            else:
                cursor.execute("""
                    INSERT INTO job_descriptions (
                        job_title, required_skills, preferred_skills, education, 
                        experience, experience_years, responsibilities, certifications, raw_text
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    title,
                    json.dumps(jd_dict.get("required_skills", [])),
                    json.dumps(jd_dict.get("preferred_skills", [])),
                    jd_dict.get("education", ""),
                    jd_dict.get("experience", ""),
                    jd_dict.get("experience_years", 1.0),
                    json.dumps(jd_dict.get("responsibilities", [])),
                    json.dumps(jd_dict.get("certifications", [])),
                    jd_dict.get("raw_text", "")
                ))
                conn.commit()
                return cursor.lastrowid

    def save_screening_results(self, jd_id: int, ranked_candidates: List[Dict[str, Any]]):
        """Save a batch of candidate screening ranking results (clears old results for same JD)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM screening_results WHERE jd_id = ?", (jd_id,))
            for c in ranked_candidates:
                cursor.execute("""
                    INSERT INTO screening_results (
                        jd_id, candidate_id, candidate_name, overall_score, rank_order,
                        recommendation_badge, component_scores_json, matched_skills_json,
                        missing_skills_json, explanation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    jd_id,
                    c.get("candidate_id"),
                    c.get("candidate_name"),
                    c.get("overall_score"),
                    c.get("rank"),
                    c.get("recommendation_badge"),
                    json.dumps(c.get("component_scores", {})),
                    json.dumps(c.get("matched_required_skills", [])),
                    json.dumps(c.get("missing_required_skills", [])),
                    c.get("explanation", "")
                ))
            conn.commit()

    def get_all_job_descriptions(self) -> List[Dict[str, Any]]:
        """Retrieve all stored job descriptions."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM job_descriptions ORDER BY id DESC")
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "id": r["id"],
                    "job_title": r["job_title"],
                    "required_skills": json.loads(r["required_skills"] or "[]"),
                    "preferred_skills": json.loads(r["preferred_skills"] or "[]"),
                    "education": r["education"],
                    "experience": r["experience"],
                    "experience_years": r["experience_years"],
                    "responsibilities": json.loads(r["responsibilities"] or "[]"),
                    "certifications": json.loads(r["certifications"] or "[]"),
                    "raw_text": r["raw_text"],
                    "created_at": r["created_at"]
                })
            return results

    def save_resume(self, resume_dict: Dict[str, Any]) -> int:
        """Save parsed resume record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO resumes (
                    candidate_id, candidate_name, file_name, contact_json,
                    skills_json, education_json, experience_json, total_experience_years,
                    projects_json, certifications_json, raw_text
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                resume_dict.get("candidate_id"),
                resume_dict.get("candidate_name"),
                resume_dict.get("file_name"),
                json.dumps(resume_dict.get("contact", {})),
                json.dumps(resume_dict.get("skills", [])),
                json.dumps(resume_dict.get("education", [])),
                json.dumps(resume_dict.get("experience", [])),
                resume_dict.get("total_experience_years", 0.0),
                json.dumps(resume_dict.get("projects", [])),
                json.dumps(resume_dict.get("certifications", [])),
                resume_dict.get("raw_text", "")
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all_resumes(self) -> List[Dict[str, Any]]:
        """Retrieve all stored resumes."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM resumes ORDER BY id DESC")
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "id": r["id"],
                    "candidate_id": r["candidate_id"],
                    "candidate_name": r["candidate_name"],
                    "file_name": r["file_name"],
                    "contact": json.loads(r["contact_json"] or "{}"),
                    "skills": json.loads(r["skills_json"] or "[]"),
                    "education": json.loads(r["education_json"] or "[]"),
                    "experience": json.loads(r["experience_json"] or "[]"),
                    "total_experience_years": r["total_experience_years"],
                    "projects": json.loads(r["projects_json"] or "[]"),
                    "certifications": json.loads(r["certifications_json"] or "[]"),
                    "raw_text": r["raw_text"],
                    "created_at": r["created_at"]
                })
            return results

    def get_latest_screening_results(self, jd_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retrieve latest screening ranking results for a specific JD or the most recently screened JD."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            target_jd_id = jd_id
            if target_jd_id is None:
                # Find the most recently screened job description
                cursor.execute("SELECT jd_id FROM screening_results ORDER BY id DESC LIMIT 1")
                latest_row = cursor.fetchone()
                if latest_row:
                    target_jd_id = latest_row["jd_id"]
                else:
                    return []

            cursor.execute("SELECT * FROM screening_results WHERE jd_id = ? ORDER BY rank_order ASC", (target_jd_id,))
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "id": r["id"],
                    "jd_id": r["jd_id"],
                    "candidate_id": r["candidate_id"],
                    "candidate_name": r["candidate_name"],
                    "overall_score": r["overall_score"],
                    "rank": r["rank_order"],
                    "recommendation_badge": r["recommendation_badge"],
                    "component_scores": json.loads(r["component_scores_json"] or "{}"),
                    "matched_required_skills": json.loads(r["matched_skills_json"] or "[]"),
                    "missing_required_skills": json.loads(r["missing_skills_json"] or "[]"),
                    "explanation": r["explanation"],
                    "created_at": r["created_at"]
                })
            return results

    def get_distinct_screened_jds(self) -> List[Dict[str, Any]]:
        """Retrieve list of all Job Descriptions that have active screening results."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT jd.id, jd.job_title 
                FROM job_descriptions jd
                INNER JOIN screening_results sr ON jd.id = sr.jd_id
                ORDER BY jd.id DESC
            """)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def save_experiment_results(self, experiment_results: List[Dict[str, Any]]):
        """Save prompt engineering experiment results."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for r in experiment_results:
                cursor.execute("""
                    INSERT INTO prompt_experiments (
                        strategy_name, candidate_id, score, latency_seconds,
                        output_validity_pct, extraction_completeness_pct,
                        evidence_support_pct, consistency_score, output_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    r.get("strategy"),
                    r.get("candidate_id", "GLOBAL_BENCHMARK"),
                    r.get("score"),
                    r.get("latency_seconds"),
                    r.get("output_validity_pct"),
                    r.get("extraction_completeness_pct"),
                    r.get("evidence_support_pct"),
                    r.get("consistency_score"),
                    json.dumps(r.get("output_data", {}))
                ))
            conn.commit()

    def get_experiment_summary(self) -> List[Dict[str, Any]]:
        """Get aggregated benchmark metrics for each prompt strategy."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    strategy_name,
                    AVG(score) as avg_score,
                    AVG(latency_seconds) as avg_latency,
                    AVG(output_validity_pct) as avg_validity,
                    AVG(extraction_completeness_pct) as avg_completeness,
                    AVG(evidence_support_pct) as avg_evidence_support,
                    AVG(consistency_score) as avg_consistency,
                    COUNT(*) as runs_count
                FROM prompt_experiments
                GROUP BY strategy_name
                ORDER BY avg_score DESC
            """)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

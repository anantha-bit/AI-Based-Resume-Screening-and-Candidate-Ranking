"""
Prompt Engineering Templates for all 10 Academic Strategies.
Academic context: Maps to Unit 1 (Anatomy of a Prompt), Unit 2 (Prompting Tactics & Chaining),
and Unit 3 (Chain-of-Thought & Autonomous Agentic Workflows) of PES University UE24AM343AB5.
"""

from typing import Dict, Any

PROMPT_STRATEGIES = [
    "Zero-shot prompting",
    "Few-shot prompting",
    "Role-based prompting",
    "Chain-of-thought-inspired structured task decomposition",
    "Least-to-most prompting",
    "Chained prompting",
    "Grounded prompting",
    "Structured JSON output prompting",
    "Critic and refinement prompting",
    "Self-consistency prompting"
]


class PromptTemplates:
    """Standardized prompt templates adhering to prompt engineering literature (Brown 2020, Wei 2022, Zhou 2022, Wang 2022)."""

    @staticmethod
    def zero_shot(jd_text: str, resume_text: str) -> str:
        return f"""Analyze whether the following candidate resume satisfies the job description requirements.

[JOB DESCRIPTION]
{jd_text}

[CANDIDATE RESUME]
{resume_text}

Provide:
1. Overall suitability score (0-100).
2. Matched qualifications.
3. Missing qualifications.
4. Summary."""

    @staticmethod
    def few_shot(jd_text: str, resume_text: str) -> str:
        return f"""Analyze candidate resumes against job descriptions based on the provided exemplars.

### EXEMPLAR 1:
Job: Senior Backend Developer (Python, Django, AWS, PostgreSQL)
Resume: Software Engineer with 4 years building Django APIs on AWS. Proficient in PostgreSQL and Redis.
Output:
{{
  "suitability_score": 92,
  "matched_skills": ["Python", "Django", "AWS", "PostgreSQL"],
  "missing_skills": [],
  "experience_match": "4 years meets requirement",
  "decision": "Recommended"
}}

### EXEMPLAR 2:
Job: NLP Research Scientist (PyTorch, Transformers, LLMs, PhD)
Resume: Frontend React developer with 2 years experience. Built HTML/CSS web apps.
Output:
{{
  "suitability_score": 18,
  "matched_skills": [],
  "missing_skills": ["PyTorch", "Transformers", "LLMs", "PhD"],
  "experience_match": "Unrelated field",
  "decision": "Not Recommended"
}}

### TARGET EVALUATION:
[JOB DESCRIPTION]
{jd_text}

[CANDIDATE RESUME]
{resume_text}

Output JSON:"""

    @staticmethod
    def role_based(jd_text: str, resume_text: str) -> str:
        return f"""You are a Principal Technical Recruiter and Senior Engineering Hiring Manager at a top-tier technology enterprise with 15+ years of experience conducting rigorous, unbiased candidate assessments.

Evaluate the following candidate objectively against the role criteria without making unsupported assumptions.

[JOB DESCRIPTION]
{jd_text}

[CANDIDATE RESUME]
{resume_text}

Respond in structured JSON format with professional recruiter justifications."""

    @staticmethod
    def chain_of_thought(jd_text: str, resume_text: str) -> str:
        return f"""Analyze the candidate using step-by-step reasoning decomposition.

[JOB DESCRIPTION]
{jd_text}

[CANDIDATE RESUME]
{resume_text}

Follow these explicit reasoning steps:
Step 1: Extract all mandatory technical skills from the Job Description.
Step 2: Cross-examine each mandatory skill against explicit textual evidence in the resume.
Step 3: Evaluate total years of relevant domain experience vs required years.
Step 4: Identify discrepancies, qualification gaps, and overqualifications.
Step 5: Synthesize a calibrated final suitability score (0-100) and structured decision."""

    @staticmethod
    def least_to_most(jd_text: str, resume_text: str) -> str:
        return f"""Deconstruct the screening evaluation into sequential sub-problems from least complex to most complex:

Sub-problem 1 (Basic Eligibility): Does the candidate meet the minimum educational and degree criteria?
Sub-problem 2 (Skill Inventory): Which required technical tools are explicitly documented in the resume?
Sub-problem 3 (Experience Depth): Does the candidate's work timeline satisfy the required seniority and responsibilities?
Sub-problem 4 (Final Synthesis): Based on sub-problems 1-3, compute the composite match score and recommendation.

[JOB DESCRIPTION]
{jd_text}

[CANDIDATE RESUME]
{resume_text}"""

    @staticmethod
    def chained(stage: int, jd_text: str, resume_text: str, intermediate_input: str = "") -> str:
        if stage == 1:
            return f"""[STAGE 1: ENTITY EXTRACTION]
Extract all candidate technical skills, years of experience, and degrees from this resume:
{resume_text}"""
        elif stage == 2:
            return f"""[STAGE 2: REQUIREMENT ALIGNMENT]
Compare these extracted candidate entities against the job requirements:
Job Requirements: {jd_text}
Candidate Entities: {intermediate_input}
Identify exact matches and gaps."""
        else:
            return f"""[STAGE 3: SCORING & EXPLANATION]
Given this requirement alignment:
{intermediate_input}
Generate final score (0-100), transparent explanation, and recruiter action."""

    @staticmethod
    def grounded(jd_text: str, resume_text: str) -> str:
        return f"""STRICT EVIDENCE GROUNDING PROTOCOL:
You are prohibited from extrapolating, hallucinating, or assuming qualifications not explicitly written in the resume.
Every positive skill assessment MUST cite an exact verbatim sentence snippet from the candidate's text.
If any skill or requirement is absent from the resume text, you MUST explicitly output: "Not found in resume".

[JOB DESCRIPTION]
{jd_text}

[CANDIDATE RESUME]
{resume_text}

Return JSON with explicit evidence quotations for each requirement."""

    @staticmethod
    def structured_json(jd_text: str, resume_text: str) -> str:
        return f"""Analyze the candidate and return strictly valid JSON matching this schema:
{{
  "candidate_name": "string",
  "suitability_score": "integer between 0 and 100",
  "matched_skills": ["array of matched skill strings"],
  "missing_skills": ["array of missing skill strings"],
  "experience_years_documented": "number",
  "verifiable_evidence": {{"skill_name": "exact quotation"}},
  "strengths": ["array of string highlights"],
  "gaps": ["array of string risks/gaps"],
  "recommendation": "Advance to Interview | Hold for Review | Not Qualified"
}}

Do not include markdown fences or preamble.
[JOB DESCRIPTION]
{jd_text}

[CANDIDATE RESUME]
{resume_text}"""

    @staticmethod
    def critic_and_refinement(jd_text: str, resume_text: str, initial_draft: str) -> str:
        return f"""You are an AI Quality & Fairness Auditor.
Review the initial candidate evaluation below for accuracy, hallucination prevention, and fairness.

[JOB DESCRIPTION]
{jd_text}

[CANDIDATE RESUME]
{resume_text}

[INITIAL EVALUATION DRAFT]
{initial_draft}

AUDIT TASKS:
1. Verify if any claimed skill is NOT present in the resume. Remove any hallucinations.
2. Verify that protected demographic attributes were not factored into the assessment.
3. Calibrate the score to reflect strictly verifiable qualifications.
Return the REFINED and AUDITED evaluation JSON."""

    @staticmethod
    def self_consistency(sample_index: int, jd_text: str, resume_text: str) -> str:
        return f"""[EVALUATION SAMPLE PASS #{sample_index + 1}]
Independently evaluate this candidate against the job criteria. Focus on objective qualification alignment.
Provide candidate score (0-100) and matched skills list.

[JOB DESCRIPTION]
{jd_text}

[CANDIDATE RESUME]
{resume_text}"""

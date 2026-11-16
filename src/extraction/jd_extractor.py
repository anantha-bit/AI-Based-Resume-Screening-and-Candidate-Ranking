"""
Job Description Information Extractor.
Extracts title, mandatory/optional skills, education, experience, responsibilities, and certifications.
Academic context: Unit 1 & 2 (Information Extraction & Structured JSON Parsing).
"""

import re
from typing import Dict, Any, List
from src.extraction.skills_taxonomy import FLAT_SKILLS_MAP, EDUCATION_PATTERNS, get_canonical_skill
from src.preprocessing.text_cleaner import normalize_text


class JobDescriptionExtractor:
    """Extracts structured entities and requirements from raw Job Description text."""

    @classmethod
    def extract_from_text(cls, jd_text: str) -> Dict[str, Any]:
        """Convert unstructured JD text into a structured JSON representation."""
        clean_text = normalize_text(jd_text)
        
        job_title = cls._extract_title(clean_text)
        req_skills, pref_skills = cls._extract_skills(clean_text)
        education = cls._extract_education(clean_text)
        exp_str, exp_years = cls._extract_experience(clean_text)
        responsibilities = cls._extract_responsibilities(clean_text)
        certifications = cls._extract_certifications(clean_text)
        
        return {
            "job_title": job_title,
            "required_skills": req_skills,
            "preferred_skills": pref_skills,
            "education": education,
            "experience": exp_str,
            "experience_years": exp_years,
            "responsibilities": responsibilities,
            "certifications": certifications,
            "raw_text": jd_text,
            "char_count": len(jd_text)
        }

    @classmethod
    def _extract_title(cls, text: str) -> str:
        """Extract job title from header or first lines."""
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if not lines:
            return "Role / Position"
        
        # Check first 5 lines for common title indicators
        for line in lines[:5]:
            m = re.search(r'(?:title|role|position|job\s+title)\s*[:\-]\s*(.+)', line, re.IGNORECASE)
            if m:
                return m.group(1).strip()
                
        # Common title patterns
        first_line = lines[0]
        if len(first_line) < 60 and not any(kw in first_line.lower() for kw in ["welcome", "about", "company", "description", "summary"]):
            return first_line
            
        return "Software / AI Engineering Specialist"

    @classmethod
    def _extract_skills(cls, text: str) -> (List[str], List[str]):
        """Distinguish required vs preferred skills based on section headings."""
        required = set()
        preferred = set()
        
        lower_text = text.lower()
        
        # Split into sections if possible
        sections = re.split(r'\n(?=[A-Z][A-Za-z\s]{3,30}:|\b(?:requirements|qualifications|preferred|responsibilities)\b)', text, flags=re.IGNORECASE)
        
        for sec in sections:
            sec_lower = sec.lower()
            is_pref = any(kw in sec_lower[:40] for kw in ["preferred", "nice to have", "plus", "bonus", "desirable", "good to have"])
            is_req = any(kw in sec_lower[:40] for kw in ["required", "mandatory", "must have", "minimum qualifications", "key skills"])
            
            # Find skills in this section
            found_in_sec = set()
            for skill_lower, canonical in FLAT_SKILLS_MAP.items():
                pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill_lower) + r'(?![a-zA-Z0-9])'
                if re.search(pattern, sec_lower):
                    found_in_sec.add(canonical)
                    
            if is_pref:
                preferred.update(found_in_sec)
            elif is_req:
                required.update(found_in_sec)
            else:
                # Default bucket
                required.update(found_in_sec)
                
        # If no explicit sections found, scan whole text
        if not required and not preferred:
            for skill_lower, canonical in FLAT_SKILLS_MAP.items():
                pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill_lower) + r'(?![a-zA-Z0-9])'
                if re.search(pattern, lower_text):
                    required.add(canonical)
                    
        # Ensure preferred skills don't duplicate required
        preferred = preferred - required
        
        return sorted(list(required)), sorted(list(preferred))

    @classmethod
    def _extract_education(cls, text: str) -> str:
        """Extract minimum educational requirement."""
        lower = text.lower()
        for pat, deg_name in EDUCATION_PATTERNS.items():
            regex = r'\b' + re.escape(pat) + r'\b'
            if re.search(regex, lower):
                return deg_name
        return "Bachelor's Degree in Computer Science, Engineering, or related field"

    @classmethod
    def _extract_experience(cls, text: str) -> (str, float):
        """Extract required years of experience."""
        # e.g., "3+ years", "3-5 years", "minimum 4 years"
        m = re.search(r'(\d+)\+?\s*(?:to|-)\s*(\d+)?\s*(?:years|yrs)\s*(?:of)?\s*(?:relevant|industry|work)?\s*experience', text, re.IGNORECASE)
        if m:
            min_y = float(m.group(1))
            return f"{m.group(0).strip()}", min_y
            
        m2 = re.search(r'(\d+)\+?\s*(?:years|yrs)\s*(?:of)?\s*(?:relevant|industry|work)?\s*experience', text, re.IGNORECASE)
        if m2:
            min_y = float(m2.group(1))
            return f"{min_y:g}+ years of experience", min_y
            
        return "1-3 years of experience", 1.0

    @classmethod
    def _extract_responsibilities(cls, text: str) -> List[str]:
        """Extract bullet points under responsibilities or duties."""
        resps = []
        lines = text.splitlines()
        in_resp_section = False
        
        for line in lines:
            l_strip = line.strip()
            l_lower = l_strip.lower()
            if any(k in l_lower for k in ["responsibilities", "duties", "what you will do", "what you'll do", "day-to-day"]):
                in_resp_section = True
                continue
            elif in_resp_section and any(k in l_lower for k in ["requirements", "qualifications", "skills", "benefits", "about us", "what we offer"]):
                in_resp_section = False
                
            if in_resp_section:
                if l_strip.startswith(("-", "•", "*", "–")) or re.match(r'^\d+\.', l_strip):
                    cleaned_bullet = re.sub(r'^[-•*–\d\.]+\s*', '', l_strip)
                    if len(cleaned_bullet) > 10:
                        resps.append(cleaned_bullet)
                        
        if not resps:
            # Fallback: grab any bullet lines that describe actions
            for line in lines:
                l_strip = line.strip()
                if l_strip.startswith(("-", "•", "*")) and len(l_strip) > 20:
                    resps.append(re.sub(r'^[-•*]+\s*', '', l_strip))
                    if len(resps) >= 6:
                        break
                        
        return resps[:10]

    @classmethod
    def _extract_certifications(cls, text: str) -> List[str]:
        """Extract desired certifications (AWS, GCP, Azure, PMP, etc.)."""
        certs = []
        cert_keywords = [
            "AWS Certified", "Solutions Architect", "Google Cloud Certified", 
            "Professional Machine Learning Engineer", "Azure Certified", 
            "TensorFlow Developer", "PMP", "Scrum Master", "CKA", "Kubernetes Certified"
        ]
        lower = text.lower()
        for c in cert_keywords:
            if c.lower() in lower:
                certs.append(c)
        return certs

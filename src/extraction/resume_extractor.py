"""
Resume Information Extractor.
Segments resume text into canonical sections and extracts structured entities.
Academic context: Unit 1 & Unit 2 (Structured Extraction, Section Chunking & NLP Pipelines).
"""

import re
import hashlib
from typing import Dict, Any, List
from src.extraction.skills_taxonomy import FLAT_SKILLS_MAP, EDUCATION_PATTERNS
from src.preprocessing.text_cleaner import normalize_text, extract_contact_info, tokenize_sentences


class ResumeExtractor:
    """Extracts structured entities and segmented sections from raw resume text."""

    SECTION_HEADERS = {
        "summary": ["summary", "professional summary", "about me", "profile", "objective", "career objective"],
        "skills": ["skills", "technical skills", "core competencies", "technologies", "expertise", "proficiencies", "tools"],
        "experience": ["experience", "work experience", "employment history", "professional experience", "work history", "internships"],
        "education": ["education", "academic background", "qualifications", "academics", "educational qualifications"],
        "projects": ["projects", "personal projects", "academic projects", "key projects", "notable projects"],
        "certifications": ["certifications", "certificates", "licenses", "courses & certifications", "accreditations"]
    }

    @classmethod
    def parse_resume(cls, text: str, file_name: str = "candidate_resume") -> Dict[str, Any]:
        """Parse raw resume text into fully structured JSON representation."""
        clean_text = normalize_text(text)
        candidate_id = cls._generate_candidate_id(clean_text, file_name)
        candidate_name = cls._extract_candidate_name(clean_text, file_name)
        contact_info = extract_contact_info(clean_text)
        
        # Segment sections
        sections = cls._segment_sections(clean_text)
        
        # Extract specific entities
        skills = cls._extract_skills(clean_text, sections.get("skills", ""))
        education_list = cls._extract_education(clean_text, sections.get("education", ""))
        experience_list, total_exp_years = cls._extract_experience(clean_text, sections.get("experience", ""))
        projects_list = cls._extract_projects(clean_text, sections.get("projects", ""))
        certs_list = cls._extract_certifications(clean_text, sections.get("certifications", ""))
        sentences = tokenize_sentences(clean_text)

        return {
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "file_name": file_name,
            "contact": contact_info,
            "skills": skills,
            "education": education_list,
            "experience": experience_list,
            "total_experience_years": total_exp_years,
            "projects": projects_list,
            "certifications": certs_list,
            "sections": sections,
            "sentences": sentences,
            "raw_text": text,
            "char_count": len(text)
        }

    @classmethod
    def _generate_candidate_id(cls, text: str, file_name: str) -> str:
        """Create deterministic anonymized candidate hash ID."""
        hash_seed = f"{file_name}_{text[:100]}"
        h = hashlib.sha256(hash_seed.encode("utf-8")).hexdigest()[:8].upper()
        return f"CAND-{h}"

    @classmethod
    def _extract_candidate_name(cls, text: str, file_name: str) -> str:
        """Extract candidate name from header or file name."""
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for line in lines[:3]:
            # If line is short, doesn't contain email/urls, and looks like a name
            if 3 < len(line) < 40 and not any(ch in line for ch in ["@", "http", "www", ".com", ":", "/", "|"]):
                words = line.split()
                if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
                    return line
        # Fallback to file name without extension
        base = file_name.rsplit(".", 1)[0]
        cleaned_base = re.sub(r'[-_]', ' ', base).title()
        return cleaned_base if cleaned_base else "Candidate"

    @classmethod
    def _segment_sections(cls, text: str) -> Dict[str, str]:
        """Split resume into standard sections using header heuristics."""
        lines = text.splitlines()
        sections: Dict[str, List[str]] = {
            "summary": [], "skills": [], "experience": [], 
            "education": [], "projects": [], "certifications": [], "other": []
        }
        current_section = "other"

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Check if line matches a section header
            clean_hdr = re.sub(r'[^a-zA-Z\s]', '', line_str).strip().lower()
            found_sec = None
            if len(clean_hdr) < 35:
                for sec_key, aliases in cls.SECTION_HEADERS.items():
                    if clean_hdr in aliases:
                        found_sec = sec_key
                        break
            
            if found_sec:
                current_section = found_sec
            else:
                sections[current_section].append(line_str)

        return {k: "\n".join(v).strip() for k, v in sections.items()}

    @classmethod
    def _extract_skills(cls, full_text: str, skills_section_text: str) -> List[str]:
        """Extract technical and domain skills."""
        found = set()
        # Prioritize search in skills section, then full text
        search_texts = [skills_section_text, full_text] if skills_section_text else [full_text]
        
        for st in search_texts:
            lower = st.lower()
            for skill_lower, canonical in FLAT_SKILLS_MAP.items():
                pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill_lower) + r'(?![a-zA-Z0-9])'
                if re.search(pattern, lower):
                    found.add(canonical)
                    
        return sorted(list(found))

    @classmethod
    def _extract_education(cls, full_text: str, edu_section: str) -> List[Dict[str, Any]]:
        """Extract degree, institution, and graduation year."""
        source = edu_section if edu_section else full_text
        entries = []
        lower = source.lower()

        # Find degree mentions
        for pat, deg_name in EDUCATION_PATTERNS.items():
            regex = r'\b' + re.escape(pat) + r'\b'
            m = re.search(regex, lower)
            if m:
                # Search for 4-digit year nearby
                idx = m.start()
                context = source[max(0, idx - 80): min(len(source), idx + 120)]
                year_match = re.search(r'\b(19\d\d|20\d\d)\b', context)
                grad_year = year_match.group(1) if year_match else "Completed"
                entries.append({
                    "degree": deg_name,
                    "year": grad_year,
                    "snippet": context.replace("\n", " ").strip()
                })
        
        # Deduplicate by degree
        unique = []
        seen = set()
        for e in entries:
            if e["degree"] not in seen:
                seen.add(e["degree"])
                unique.append(e)
                
        if not unique:
            unique.append({
                "degree": "Bachelor's Degree (Technical)",
                "year": "N/A",
                "snippet": "Inferred from technical experience"
            })
        return unique

    @classmethod
    def _extract_experience(cls, full_text: str, exp_section: str) -> (List[Dict[str, Any]], float):
        """Extract roles, companies, and total experience in years."""
        source = exp_section if exp_section else full_text
        
        # Calculate total years of experience
        # 1. Search for explicit statements like "5+ years of experience"
        m_exp = re.search(r'(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)\s*(?:of)?\s*(?:relevant|industry|work)?\s*experience', full_text, re.IGNORECASE)
        total_years = 2.0
        if m_exp:
            total_years = float(m_exp.group(1))
        else:
            # 2. Count year ranges e.g. 2021 - 2024
            ranges = re.findall(r'\b(20\d\d)\s*(?:-|to)\s*(20\d\d|present|current)\b', source, re.IGNORECASE)
            sum_years = 0
            for start_y, end_y in ranges:
                sy = int(start_y)
                ey = 2026 if any(k in end_y.lower() for k in ["present", "current"]) else int(end_y)
                diff = max(0, ey - sy)
                sum_years += diff
            if sum_years > 0:
                total_years = float(min(sum_years, 30))

        # Extract role paragraphs
        roles = []
        paragraphs = [p.strip() for p in source.split("\n\n") if len(p.strip()) > 30]
        for p in paragraphs[:5]:
            roles.append({
                "description": p.replace("\n", " ")
            })
            
        return roles, total_years

    @classmethod
    def _extract_projects(cls, full_text: str, proj_section: str) -> List[Dict[str, Any]]:
        """Extract projects and descriptions."""
        source = proj_section if proj_section else full_text
        projects = []
        lines = [l.strip() for l in source.splitlines() if l.strip()]
        
        for line in lines:
            if line.startswith(("-", "•", "*")) and len(line) > 25:
                projects.append({
                    "title": line[:50],
                    "details": line
                })
                if len(projects) >= 6:
                    break
        return projects

    @classmethod
    def _extract_certifications(cls, full_text: str, cert_section: str) -> List[str]:
        """Extract professional certifications."""
        certs = []
        source = (cert_section + " " + full_text).lower()
        targets = [
            "AWS Certified", "Azure Certified", "Google Cloud Certified", 
            "CKA", "Kubernetes", "TensorFlow Developer", "Scrum Master", "PMP",
            "Coursera Deep Learning", "Stanford Online", "Meta Frontend Developer"
        ]
        for t in targets:
            if t.lower() in source:
                certs.append(t)
        return certs

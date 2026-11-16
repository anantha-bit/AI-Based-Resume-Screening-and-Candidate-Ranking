"""
Archive Manager Module.
Provides centralized helpers to package, retrieve, and download candidate resumes in bulk (.ZIP)
or individually in their native document formats (.PDF, .DOCX, .TXT).
Academic context: Unit 1 & Unit 4 (Data Ingestion & Artifact Export).
"""

import io
import os
import glob
import zipfile
from typing import List, Dict, Any, Optional, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAMPLE_DIR = os.path.join(PROJECT_ROOT, "data", "sample")


class ArchiveManager:
    """Manages bulk archiving and individual document retrieval for candidate resumes."""

    MIME_TYPES = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".txt": "text/plain"
    }

    @staticmethod
    def get_all_sample_resume_paths() -> List[str]:
        """Returns sorted list of file paths for all 32 candidate resume files in data/sample."""
        return sorted(glob.glob(os.path.join(SAMPLE_DIR, "Resume_*.*")))

    @staticmethod
    def get_sample_resumes_catalog() -> List[Dict[str, Any]]:
        """Returns metadata for all available sample resumes."""
        paths = ArchiveManager.get_all_sample_resume_paths()
        catalog = []
        for p in paths:
            fname = os.path.basename(p)
            ext = os.path.splitext(fname)[1].lower()
            size = os.path.getsize(p)
            catalog.append({
                "file_name": fname,
                "file_path": p,
                "extension": ext.replace(".", "").upper(),
                "size_kb": round(size / 1024, 2),
                "mime_type": ArchiveManager.MIME_TYPES.get(ext, "application/octet-stream")
            })
        return catalog

    @staticmethod
    def create_resumes_zip_bytes() -> bytes:
        """Packages all 32 candidate resume files into an in-memory ZIP archive."""
        files = ArchiveManager.get_all_sample_resume_paths()
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                zf.write(f, arcname=os.path.basename(f))
        buf.seek(0)
        return buf.getvalue()

    @staticmethod
    def get_resume_file_data(file_name: str) -> Optional[Tuple[bytes, str]]:
        """
        Retrieves file bytes and MIME type for a specific resume file name.
        Returns (bytes, mime_type) or None if not found.
        """
        # Search directly by filename or in data/sample
        candidate_path = os.path.join(SAMPLE_DIR, file_name)
        if not os.path.exists(candidate_path):
            # Try searching by basename if full path was passed
            candidate_path = os.path.join(SAMPLE_DIR, os.path.basename(file_name))
        
        if not os.path.exists(candidate_path):
            return None

        with open(candidate_path, "rb") as f:
            data = f.read()

        ext = os.path.splitext(candidate_path)[1].lower()
        mime = ArchiveManager.MIME_TYPES.get(ext, "application/octet-stream")
        return data, mime

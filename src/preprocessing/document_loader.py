"""
Document Loader Module.
Extracts raw text and metadata from PDF, DOCX, and TXT files.
Academic context: Unit 2 (Document Loaders & Text Ingestion) of PES University UE24AM343AB5.
"""

import os
from typing import Dict, Any, Tuple
import pymupdf
import docx


class DocumentLoader:
    """Robust document loader for recruitment resumes and job descriptions."""

    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

    @classmethod
    def load_file(cls, file_path: str) -> Dict[str, Any]:
        """
        Load a document from a local file path.
        Returns dictionary with status, text, metadata, and error message if any.
        """
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File does not exist: {file_path}",
                "text": "",
                "metadata": {}
            }

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in cls.SUPPORTED_EXTENSIONS:
            return {
                "success": False,
                "error": f"Unsupported format '{ext}'. Supported formats: {list(cls.SUPPORTED_EXTENSIONS)}",
                "text": "",
                "metadata": {}
            }

        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return {
                "success": False,
                "error": "File is empty (0 bytes).",
                "text": "",
                "metadata": {"size_bytes": 0}
            }

        try:
            if ext == ".pdf":
                return cls._load_pdf(file_path)
            elif ext == ".docx":
                return cls._load_docx(file_path)
            elif ext == ".txt":
                return cls._load_txt(file_path)
        except Exception as e:
            return {
                "success": False,
                "error": f"Error parsing {ext.upper()} file: {str(e)}",
                "text": "",
                "metadata": {"file_name": os.path.basename(file_path)}
            }

    @classmethod
    def load_bytes(cls, file_bytes: bytes, file_name: str) -> Dict[str, Any]:
        """Load document directly from raw bytes (used for Streamlit file uploader)."""
        if not file_bytes:
            return {
                "success": False,
                "error": "Uploaded file is empty.",
                "text": "",
                "metadata": {"file_name": file_name}
            }

        ext = os.path.splitext(file_name)[1].lower()
        if ext not in cls.SUPPORTED_EXTENSIONS:
            return {
                "success": False,
                "error": f"Unsupported format '{ext}'. Supported formats: {list(cls.SUPPORTED_EXTENSIONS)}",
                "text": "",
                "metadata": {"file_name": file_name}
            }

        try:
            if ext == ".pdf":
                doc = pymupdf.open(stream=file_bytes, filetype="pdf")
                if doc.is_encrypted:
                    return {
                        "success": False,
                        "error": "PDF is password protected and cannot be extracted.",
                        "text": "",
                        "metadata": {"file_name": file_name}
                    }
                pages_text = []
                for p in doc:
                    pages_text.append(p.get_text())
                doc.close()
                full_text = "\n\n".join(pages_text).strip()
                return {
                    "success": True,
                    "error": None,
                    "text": full_text,
                    "metadata": {
                        "file_name": file_name,
                        "pages": len(pages_text),
                        "char_count": len(full_text),
                        "extension": ext
                    }
                }

            elif ext == ".docx":
                import io
                bio = io.BytesIO(file_bytes)
                doc = docx.Document(bio)
                paras = [p.text for p in doc.paragraphs if p.text.strip()]
                # Also extract table text
                for t in doc.tables:
                    for row in t.rows:
                        row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                        if row_text:
                            paras.append(row_text)
                full_text = "\n".join(paras).strip()
                return {
                    "success": True,
                    "error": None,
                    "text": full_text,
                    "metadata": {
                        "file_name": file_name,
                        "char_count": len(full_text),
                        "extension": ext
                    }
                }

            elif ext == ".txt":
                text = file_bytes.decode("utf-8", errors="replace").strip()
                return {
                    "success": True,
                    "error": None,
                    "text": text,
                    "metadata": {
                        "file_name": file_name,
                        "char_count": len(text),
                        "extension": ext
                    }
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error parsing uploaded file: {str(e)}",
                "text": "",
                "metadata": {"file_name": file_name}
            }

    @classmethod
    def _load_pdf(cls, file_path: str) -> Dict[str, Any]:
        doc = pymupdf.open(file_path)
        if doc.is_encrypted:
            return {
                "success": False,
                "error": "PDF is encrypted/password protected.",
                "text": "",
                "metadata": {"file_path": file_path}
            }
        pages_text = [p.get_text() for p in doc]
        page_count = len(doc)
        doc.close()
        full_text = "\n\n".join(pages_text).strip()
        return {
            "success": True,
            "error": None,
            "text": full_text,
            "metadata": {
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
                "pages": page_count,
                "char_count": len(full_text),
                "extension": ".pdf"
            }
        }

    @classmethod
    def _load_docx(cls, file_path: str) -> Dict[str, Any]:
        doc = docx.Document(file_path)
        paras = [p.text for p in doc.paragraphs if p.text.strip()]
        for t in doc.tables:
            for row in t.rows:
                row_text = " | ".join(c.text.strip() for c in row.cells if c.text.strip())
                if row_text:
                    paras.append(row_text)
        full_text = "\n".join(paras).strip()
        return {
            "success": True,
            "error": None,
            "text": full_text,
            "metadata": {
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
                "char_count": len(full_text),
                "extension": ".docx"
            }
        }

    @classmethod
    def _load_txt(cls, file_path: str) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read().strip()
        return {
            "success": True,
            "error": None,
            "text": text,
            "metadata": {
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
                "char_count": len(text),
                "extension": ".txt"
            }
        }

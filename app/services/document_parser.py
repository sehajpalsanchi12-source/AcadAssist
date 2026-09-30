import io
import re
from typing import Optional
from pypdf import PdfReader

class DocumentParser:
    """Parses uploaded study materials (PDF, TXT, Markdown, code files) into clean text."""
    
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF byte stream."""
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text_parts = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text_parts.append(f"--- Page {i + 1} ---\n" + page_text.strip())
            return "\n\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF document: {str(e)}")

    @staticmethod
    def extract_text_from_txt(file_bytes: bytes) -> str:
        """Extract text from TXT/MD byte stream."""
        for encoding in ["utf-8", "latin-1", "cp1252"]:
            try:
                return file_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue
        return file_bytes.decode("utf-8", errors="ignore")

    @classmethod
    def parse_uploaded_file(cls, filename: str, file_bytes: bytes) -> str:
        """Dispatch parser based on file extension."""
        ext = filename.lower().split(".")[-1] if "." in filename else ""
        if ext == "pdf":
            text = cls.extract_text_from_pdf(file_bytes)
        elif ext in ["txt", "md", "csv", "json", "c", "cpp", "java", "py", "html"]:
            text = cls.extract_text_from_txt(file_bytes)
        else:
            # Fallback text decoder
            text = cls.extract_text_from_txt(file_bytes)
        
        # Clean excessive whitespace
        text = re.sub(r"\r\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

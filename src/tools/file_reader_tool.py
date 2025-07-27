from tools.base_tool import BaseTool
import fitz  # PyMuPDF
import os

class FileReaderTool(BaseTool):
    name = "readfile"
    description = "Read text content from a PDF or Word document."
    parameters = {
        "type": "object",
        "properties": {
            "filepath": {"type": "string", "description": "Path to a .pdf or .docx file"}
        },
        "required": ["filepath"],
    }

    def run(self, **kwargs) -> str:
        filepath = kwargs["filepath"]
        if not os.path.exists(filepath):
            return "❌ File not found."

        if filepath.lower().endswith(".pdf"):
            return self._read_pdf(filepath)
        elif filepath.lower().endswith(".docx"):
            return self._read_docx(filepath)
        else:
            return "❌ Unsupported file format."

    def _read_pdf(self, path):
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text[:1000]

    def _read_docx(self, path):
        from docx import Document
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs])[:1000]
    
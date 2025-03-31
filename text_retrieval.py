import pdfplumber
import os
from langchain_core.documents import Document

def map_metadata(page_num):
    # Falta corregir mejor el metadato mapeado
    sections = {
        range(1, 6): "Introduction",
        range(6, 32): "InsurTech Team Corner",
        range(32, 40): "InsurTech Case Studies",
        range(40, 46): "Deal of the Quarter - Agentech",
        range(46, 52): "Partnership Case Study: Loadsure - Google Cloud",
        range(52, 58): "Incumbent Corner: Concirrus and United Risk",
        range(58, 64): "Gallagher's Vision",
        range(64, 68): "Thought Leadership",
        range(68, 73): "Investor Corner",
    }
    return next((title for key_range, title in sections.items() if page_num in key_range), "Otro")

def load_pages(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo PDF no se encuentra: {pdf_path}")

    docs = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                section_title = map_metadata(i)
                doc = Document(
                    page_content=f"{section_title}\n{text}",
                    metadata={"page": i, "section": section_title}
                )
                docs.append(doc)

    return docs
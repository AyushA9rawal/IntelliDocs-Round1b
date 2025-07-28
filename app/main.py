import os
import json
from datetime import datetime
from extract import extract_text_from_pdf
from persona_matcher import rank_sections

INPUT_FOLDER = "input"
OUTPUT_FILE = "output/result.json"

persona = "Investment Analyst"
job = "Analyze revenue trends, R&D investments, and market positioning strategies"

pdfs = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".pdf")]

doc_collection = []
for pdf in pdfs:
    pages = extract_text_from_pdf(os.path.join(INPUT_FOLDER, pdf))
    doc_collection.append({"name": pdf, "pages": pages})

ranked_sections = rank_sections(doc_collection, persona, job)

result = {
    "metadata": {
        "documents": pdfs,
        "persona": persona,
        "job_to_be_done": job,
        "timestamp": datetime.now().isoformat()
    },
    "extracted_sections": [
        {
            "document": sec["document"],
            "page_number": sec["page"],
            "section_text": sec["text"],
            "importance_rank": i + 1
        } for i, sec in enumerate(ranked_sections)
    ]
}

os.makedirs("output", exist_ok=True)
with open(OUTPUT_FILE, "w") as f:
    json.dump(result, f, indent=2)

print("Extraction complete. Output written to", OUTPUT_FILE)
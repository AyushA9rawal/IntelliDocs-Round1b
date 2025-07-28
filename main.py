import os
import json
from backend.processor import DocumentProcessor

def run(input_folder, output_folder):
    processor = DocumentProcessor(input_folder)
    persona_results = processor.process_documents_by_persona()

    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, "persona_insights.json"), "w", encoding="utf-8") as f:
        json.dump(persona_results, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    input_path = "input"
    output_path = "output"
    run(input_path, output_path)
import fitz
import os
import json
from sentence_transformers import SentenceTransformer, util
import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

class DocumentProcessor:
    def __init__(self, input_folder):
        self.input_folder = input_folder
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.personas = {
            "Developer": ["API", "integration", "authentication", "webhooks"],
            "Designer": ["layout", "typography", "color scheme", "UX"],
            "Manager": ["timeline", "budget", "milestone", "report"]
        }

    def extract_text(self, filepath):
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def extract_sentences(self, text):
        return sent_tokenize(text)

    def embed_sentences(self, sentences):
        return self.model.encode(sentences, convert_to_tensor=True)

    def process_documents_by_persona(self):
        persona_insights = {}
        for file in os.listdir(self.input_folder):
            if file.endswith(".pdf"):
                full_path = os.path.join(self.input_folder, file)
                raw_text = self.extract_text(full_path)
                sentences = self.extract_sentences(raw_text)
                sentence_embeddings = self.embed_sentences(sentences)

                doc_result = {}
                for persona, keywords in self.personas.items():
                    query_embeddings = self.embed_sentences(keywords)
                    scores = util.dot_score(query_embeddings, sentence_embeddings).cpu().numpy()

                    matched_sentences = set()
                    for row in scores:
                        for idx, val in enumerate(row):
                            if val > 0.4:
                                matched_sentences.add(sentences[idx])

                    doc_result[persona] = list(matched_sentences)
                persona_insights[file] = doc_result
        return persona_insights
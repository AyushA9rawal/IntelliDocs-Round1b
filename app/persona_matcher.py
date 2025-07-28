import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
nltk.download('punkt')

def rank_sections(documents, persona, job):
    all_sections = []
    vectorizer = TfidfVectorizer(stop_words='english')

    for doc in documents:
        for page in doc["pages"]:
            sections = nltk.sent_tokenize(page["text"])
            for section in sections:
                all_sections.append({
                    "document": doc["name"],
                    "page": page["page"],
                    "text": section
                })

    corpus = [persona + " " + job] + [s["text"] for s in all_sections]
    tfidf = vectorizer.fit_transform(corpus)
    scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    for i, score in enumerate(scores):
        all_sections[i]["score"] = float(score)

    all_sections.sort(key=lambda x: x["score"], reverse=True)

    return all_sections[:10]  # Top 10 sections

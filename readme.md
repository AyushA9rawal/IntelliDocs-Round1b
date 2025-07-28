This solution extracts relevant document sections tailored to a specific persona and job-to-be-done using a lightweight NLP pipeline:

1. **Text Extraction:** Uses PyMuPDF (fitz) to extract text from PDFs without any ML overhead.
2. **Text Segmentation:** Each page is split into sentences using NLTK.
3. **Representation:** Combines persona + job as a query, then vectorizes both query and sentence corpus using TF-IDF.
4. **Relevance Ranking:** Uses cosine similarity to rank how relevant each sentence is to the persona's goal.
5. **Output:** Top 10 most relevant sections are stored with metadata in JSON format.

This avoids heavy frameworks like PyTorch, ensuring the image stays <1GB and executes under 60 seconds on CPU with 3-5 PDF files.

# --- How to Run ---
1. Place PDFs in the `input/` directory.
2. Build the Docker image:
   ```bash
   docker build -t intellidocs-round1b .
   ```
3. Run the container:
   ```bash
   docker run --rm -v $(pwd):/app intellidocs-round1b
   ```
4. Output will be in `output/result.json`. Modify `main.py` to change the persona or job if needed.

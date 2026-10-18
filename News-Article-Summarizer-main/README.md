# 📰 News Article Summarizer

An end-to-end **extractive summarization** project. It fetches a news article from a URL and selects existing sentences from that article. It does not generate new sentences, paraphrase the text, or call a generative model.

This project follows a structured NLP pipeline including article extraction, text preprocessing, word frequency analysis, sentence scoring, and deployment using Streamlit.

---

## Problem Statement

The objective of this project is to build a text summarization system that condenses long news articles into key sentences — saving reading time while preserving the most important information.

The system provides:

- **Extractive Summary** — Top-ranked sentences from the article
- **Key Entities** — Named persons, organizations, locations, and events
- **Article Statistics** — Word count, sentence count, summary length, and a sentence-based reduction percentage

---

## Dataset / Input

The system accepts any publicly accessible news article URL and extracts:

- Article Title
- Authors
- Publish Date
- Full Article Text

### Supported Sources (Examples)

- TechCrunch
- Times of India
- India Today
- The Verge
- And many more open-access news sites

> ⚠️ Not every public URL returns a full article. Reuters blocks automated access (401 Forbidden). Some pages, including parts of BBC News, return only a short extract. A homepage or a non-article page can still produce text, but that text is not a news article.

---

## NLP Pipeline

The project follows a structured text processing workflow:

### 1. Article Extraction

- Downloads and parses the article using `newspaper3k`
- Extracts title, authors, publish date, and body text

---

### 2. Text Preprocessing

- Tokenized with `spaCy` (`en_core_web_sm`), including sentence boundaries from `doc.sents`
- Stop words removed by testing each token against `spacy.lang.en.stop_words.STOP_WORDS`
- Punctuation removed when the token text is in `string.punctuation`
- `NLTK` is imported and its `punkt` / `punkt_tab` data is downloaded at startup. Sentence scoring does not call NLTK. `newspaper3k`'s `article.nlp()` is not called.

---

### 3. Word Frequency Analysis

- Counts frequency of every meaningful word
- Normalizes frequencies to a 0–1 scale (dividing by max frequency)

---

### 4. Sentence Scoring

- Each sentence is scored by summing the normalized frequencies of its words
- Higher scores indicate more information-dense sentences

---

### 5. Summary Generation

- Top N sentences selected by score
- Re-ordered to preserve original article flow
- N is user-controlled (2 to 10 sentences)

---

### 6. Keyword / Entity Extraction

- Uses `spaCy` Named Entity Recognition (NER)
- Extracts entities of types: `PERSON`, `ORG`, `GPE`, `EVENT`, `PRODUCT`

---

##  Output Metrics

The app displays:

- Total Word Count
- Total Sentence Count
- Summary Length (sentences chosen)
- Reduction percentage, computed from sentence counts:

```text
round((1 - num_sentences / max(sentence_count, 1)) * 100)
```

`num_sentences` is the slider value. If the article has fewer sentences than the slider, this percentage can be negative. It is not a word-count compression ratio.

---

##  Deployment

The summarizer is deployed using **Streamlit**.

The web application allows users to:

- Paste any news article URL
- Select number of summary sentences via a slider
- View the generated summary instantly
- Explore extracted key entities
- See article metadata (title, authors, publish date)

---

##  Run Locally
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r Requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

`Requirements.txt` pins `click==8.1.7`. spaCy 3.7 uses Typer 0.9, and Click 8.2 or newer makes `python -m spacy download en_core_web_sm` request a missing model URL.

---

##  CLI Mode

You can also run the summarizer directly from the terminal:
```bash
python news_summarizer.py
```

---

##  Project Structure
```
news-article-summarizer/
│
├── app.py                     # Streamlit web application
├── news_summarizer.py         # Extractive summarization logic
├── log_code.py                # File logger used by both modules
├── Requirements.txt           # Python dependencies
├── LICENSE
├── README.md
└── log_files/
    ├── app_streamlit.log      # Streamlit session logs
    └── news_summarizer.log    # Summarizer execution logs
```

---

##  Tech Stack

- Python
- newspaper3k
- spaCy
- NLTK
- Streamlit

---

##  Requirements
```
nltk==3.8.1
newspaper3k==0.2.8
spacy==3.7.4
lxml==4.9.3
lxml_html_clean
Pillow==10.2.0
requests==2.31.0
streamlit
click==8.1.7
```

---

## Analytical Impact

- Demonstrates end-to-end NLP extractive summarization pipeline
- Ranks sentences by normalized word frequency, with no external API
- Applies spaCy named entity recognition to list people, organizations, places, events, and products
- Deploys the extractive pipeline in Streamlit and writes run logs to `log_files/`

---

## Author

**Hema Malini Gangumalla**  
Aspiring Data Scientist  
📧 hemamalinig07@gmail.com

---

## License

MIT License

''' NEWS ARTICLE SUMMARIZER
  Tools: Python, NLTK, spaCy, newspaper3k, Input: URL'''

# Import Libraries
import sys
import nltk
from newspaper import Article
import spacy
import string
from spacy.lang.en.stop_words import STOP_WORDS
from log_code import Logger

# ── Logger Setup ───────────────────────────────────────────
logger = Logger.get_logs('news_summarizer')

# ── NLTK Downloads ─────────────────────────────────────────
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# ── Load spaCy Model ───────────────────────────────────────
nlp = spacy.load("en_core_web_sm")
logger.info("spaCy model loaded successfully")


# ── CORE FUNCTION: Summarize a news article from URL ───────
def summarize_news(url, num_sentences=5):
    """
    Takes a news article URL and returns a clean summary.

    Parameters:
        url (str)          : The URL of the news article
        num_sentences (int): How many sentences to include in summary

    Returns:
        dict: title, authors, publish_date, summary, keywords,
              word_count, sentence_count
    """
    try:
        # Step A: Download & Parse the Article
        logger.info("Fetching article from URL: %s", url)
        article = Article(url)
        article.download()
        article.parse()

        title        = article.title
        authors      = article.authors
        publish_date = article.publish_date
        text         = article.text

        if not text:
            logger.error("Could not extract text from URL: %s", url)
            return {"error": "Could not extract text from this URL."}

        logger.info("Article fetched: '%s' | Characters: %d", title, len(text))

        # Process text with spaCy
        logger.debug("Processing text with spaCy...")
        doc = nlp(text)

        # Calculate Word Frequency
        logger.debug("Calculating word frequencies...")
        word_frequencies = {}
        for word in doc:
            if word.text.lower() not in STOP_WORDS and word.text not in string.punctuation:
                clean_word = word.text.lower()
                word_frequencies[clean_word] = word_frequencies.get(clean_word, 0) + 1

        # Normalize Frequencies (scale to 0-1)
        if word_frequencies:
            max_freq = max(word_frequencies.values())
            for word in word_frequencies:
                word_frequencies[word] = word_frequencies[word] / max_freq
        logger.debug("Word frequencies normalized. Unique words: %d", len(word_frequencies))

        # Score Each Sentence
        logger.debug("Scoring sentences...")
        sentence_scores = {}
        for sentence in doc.sents:
            for word in sentence:
                if word.text.lower() in word_frequencies:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word.text.lower()]

        # Pick Top N Sentences
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        top_sentences_ordered = sorted(top_sentences, key=lambda s: s.start)
        summary = " ".join([str(s).strip() for s in top_sentences_ordered])
        logger.info("Summary generated with %d sentences", num_sentences)

        # Extract Keywords via spaCy NER
        keywords = list(set([
            ent.text for ent in doc.ents
            if ent.label_ in ["PERSON", "ORG", "GPE", "EVENT", "PRODUCT"]
        ]))
        logger.info("Keywords extracted: %s", keywords[:10])

        word_count     = len([t for t in doc if not t.is_space])
        sentence_count = len(list(doc.sents))
        logger.info("Stats — Words: %d | Sentences: %d", word_count, sentence_count)

        return {
            "title"         : title,
            "authors"       : authors,
            "publish_date"  : publish_date,
            "summary"       : summary,
            "keywords"      : keywords[:10],
            "word_count"    : word_count,
            "sentence_count": sentence_count,
        }

    except Exception as e:
        exc_type, exc_msg, exc_line = sys.exc_info()
        logger.error("%s at line %d: %s", exc_type, exc_line.tb_lineno, exc_msg)
        return {"error": f"Something went wrong: {str(e)}"}


# ── DISPLAY FUNCTION ───────────────────────────────────────
def display_result(result):
    if "error" in result:
        logger.error("Error in result: %s", result['error'])
        print(f"\n[ERROR] {result['error']}")
        return

    logger.info("Displaying result for: %s", result['title'])
    print("\n" + "="*60)
    print("  NEWS ARTICLE SUMMARY")
    print("="*60)
    print(f"  Title        : {result['title']}")
    print(f"  Authors      : {', '.join(result['authors']) if result['authors'] else 'Not available'}")
    print(f"  Published    : {result['publish_date'] if result['publish_date'] else 'Not available'}")
    print("-"*60)
    print("  SUMMARY:\n")
    print(result['summary'])
    print()
    print("-"*60)
    print(f"  KEY ENTITIES : {', '.join(result['keywords']) if result['keywords'] else 'None found'}")
    print("="*60)


# ── MAIN ───────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("===== News Summarizer CLI Started =====")
    print("="*60)
    print("   Welcome to the News Article Summarizer")
    print("   Built with NLTK + spaCy + newspaper3k")
    print("="*60)

    try:
        num = int(input("\nHow many sentences in summary? (default=5): ") or 5)
    except ValueError:
        num = 5
        logger.warning("Invalid sentence count input. Defaulting to 5.")

    while True:
        url = input("\nPaste your news article URL (or type 'quit' to exit):\n> ").strip()

        if url.lower() == 'quit':
            logger.info("User exited the application.")
            print("\n[INFO] Goodbye! Happy learning!")
            break

        if not url.startswith("http"):
            logger.warning("Invalid URL entered: %s", url)
            print("[WARNING] Please enter a valid URL starting with http:// or https://")
            continue

        logger.info("User submitted URL: %s", url)
        result = summarize_news(url, num_sentences=num)
        display_result(result)
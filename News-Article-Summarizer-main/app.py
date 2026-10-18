import streamlit as st
from news_summarizer import summarize_news
from log_code import Logger

# ── Logger ─────────────────────────────────────────────────
logger = Logger.get_logs('app_streamlit')

# ── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="News Summarizer",
    page_icon="📰",
    layout="centered"
)

# ── Header ─────────────────────────────────────────────────
st.title("📰 News Article Summarizer")
st.divider()

logger.info("===== Streamlit App Started =====")

# ── Input ──────────────────────────────────────────────────
url = st.text_input("🔗 Paste News Article URL", placeholder="https://www.bbc.com/news/...")
num_sentences = st.slider("📝 Number of sentences in summary", min_value=2, max_value=10, value=5)
summarize_btn = st.button("Summarize →", use_container_width=True)

# ── Process ────────────────────────────────────────────────
if summarize_btn:
    if not url.strip():
        logger.warning("Empty URL submitted")
        st.warning("⚠ Please enter a news article URL.")

    elif not url.startswith("http"):
        logger.warning("Invalid URL: %s", url)
        st.warning("⚠ URL must start with http:// or https://")

    else:
        logger.info("Summarizing URL: %s", url)
        with st.spinner("Fetching and analyzing article..."):
            result = summarize_news(url, num_sentences=num_sentences)

        if "error" in result:
            logger.error("Error: %s", result["error"])
            st.error(f"❌ {result['error']}")

        else:
            logger.info("Result ready: %s", result["title"])

            # Stats
            st.divider()
            reduction = round((1 - num_sentences / max(result["sentence_count"], 1)) * 100)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Words",     result["word_count"])
            col2.metric("Total Sentences", result["sentence_count"])
            col3.metric("Summary Length",  num_sentences)
            col4.metric("Reduced By",      f"{reduction}%")

            # Article Info
            st.divider()
            st.subheader(result["title"])
            col_a, col_b = st.columns(2)
            col_a.write(f"**Authors:** {', '.join(result['authors']) if result['authors'] else 'Not available'}")
            col_b.write(f"**Published:** {str(result['publish_date'])[:10] if result['publish_date'] else 'Not available'}")

            # Summary
            st.divider()
            st.subheader("📄 Summary")
            st.info(result["summary"])

            # Keywords
            st.subheader("🏷️ Key Entities")
            if result["keywords"]:
                st.write(" · ".join(result["keywords"]))
            else:
                st.write("None detected")

# ── Footer ─────────────────────────────────────────────────
st.divider()
st.caption("Project Done by **Hema Malini** "
           "Built with Streamlit · NLP · spaCy · NLTK · newspaper3k")
"""
nlp/preprocessing.py

Reusable NLP text preprocessing utilities for the Digital Marketing FAQ Chatbot.

This module handles:
    - Lowercasing
    - Punctuation / special character removal
    - Tokenization (NLTK word_tokenize)
    - Stopword removal (NLTK stopwords)
    - Basic normalization (extra-whitespace collapsing, simple lemmatization)

It also takes care of downloading the required NLTK data files the first
time the module is used, so the project works out of the box after
`pip install -r requirements.txt`.
"""

import re
import string

import nltk

# ---------------------------------------------------------------------------
# NLTK resource setup
# ---------------------------------------------------------------------------
# The NLTK corpora/tokenizers used below are not bundled with the nltk
# package itself -- they must be downloaded once. We try to use them, and
# if they are missing we download them automatically so the project "just
# works" the first time it is run.

_REQUIRED_NLTK_RESOURCES = [
    ("tokenizers/punkt", "punkt"),
    ("tokenizers/punkt_tab", "punkt_tab"),
    ("corpora/stopwords", "stopwords"),
    ("corpora/wordnet", "wordnet"),
    ("corpora/omw-1.4", "omw-1.4"),
]


def ensure_nltk_resources() -> None:
    """
    Make sure all NLTK resources needed by this module are available
    locally, downloading any that are missing.

    This is safe to call multiple times -- nltk.data.find() is fast once
    resources are already downloaded, so repeated calls are cheap.
    """
    for resource_path, download_name in _REQUIRED_NLTK_RESOURCES:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(download_name, quiet=True)


# Run resource check on import so any module that imports preprocessing
# is guaranteed to have working tokenizers/stopwords.
ensure_nltk_resources()

from nltk.corpus import stopwords          # noqa: E402  (import after download)
from nltk.stem import WordNetLemmatizer    # noqa: E402
from nltk.tokenize import word_tokenize    # noqa: E402

_STOPWORDS = set(stopwords.words("english"))
_LEMMATIZER = WordNetLemmatizer()

# A handful of digital-marketing specific stopwords/filler words that add
# noise but carry little matching value. We deliberately do NOT remove
# domain-important short words like "seo", "ads", "ppc", "roi", "ctr".
_EXTRA_STOPWORDS = {"please", "could", "would", "hi", "hello", "thanks", "thank"}
_STOPWORDS |= _EXTRA_STOPWORDS


def clean_text(text: str) -> str:
    """
    Lowercase the text and strip punctuation/special characters,
    keeping only letters, numbers, and whitespace.
    """
    text = text.lower()
    # Replace punctuation with a space (not empty string) so words that
    # were separated only by punctuation don't get glued together.
    text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    # Remove any remaining non-alphanumeric characters (e.g. curly quotes).
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # Collapse multiple whitespace characters into a single space.
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list:
    """Tokenize cleaned text into a list of word tokens using NLTK."""
    return word_tokenize(text)


def remove_stopwords(tokens: list) -> list:
    """Remove common English stopwords from a list of tokens."""
    return [token for token in tokens if token not in _STOPWORDS]


def lemmatize(tokens: list) -> list:
    """Lemmatize tokens to their base dictionary form (e.g. 'running' -> 'run')."""
    return [_LEMMATIZER.lemmatize(token) for token in tokens]


def preprocess(text: str) -> str:
    """
    Full preprocessing pipeline used everywhere in the app.

    Steps:
        1. Lowercase + punctuation removal (clean_text)
        2. Tokenization (tokenize)
        3. Stopword removal (remove_stopwords)
        4. Lemmatization / normalization (lemmatize)
        5. Re-join tokens into a single normalized string, ready to be fed
           into TfidfVectorizer.

    Args:
        text: Raw input text (a user question or an FAQ question).

    Returns:
        A cleaned, normalized string of space-separated tokens.
    """
    if not text or not text.strip():
        return ""

    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)

    # If preprocessing stripped everything away (e.g. the input was only
    # stopwords/punctuation), fall back to the cleaned-but-unfiltered
    # tokens so we never hand an empty string to the vectorizer.
    if not tokens:
        tokens = remove_stopwords(tokenize(cleaned)) or tokenize(cleaned)

    return " ".join(tokens)


if __name__ == "__main__":
    # Small manual sanity check when running this file directly:
    #   python nlp/preprocessing.py
    sample = "How can I improve my website's ranking on Google?!"
    print("Original :", sample)
    print("Processed:", preprocess(sample))

"""
chatbot/matcher.py

Core matching engine for the Digital Marketing FAQ Chatbot.

Uses:
    - NLTK NLP preprocessing
    - TF-IDF vectorization
    - Unigrams + bigrams
    - Cosine similarity
    - FAQ question variations
    - Similarity threshold
"""

import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp.preprocessing import preprocess


SIMILARITY_THRESHOLD = 0.30

FALLBACK_RESPONSE = (
    "I'm sorry, I couldn't find a relevant answer to that question. "
    "Please try asking about SEO, social media marketing, online advertising, "
    "content marketing, email marketing, or analytics."
)

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "faqs.json"
)


class FAQMatcher:

    def __init__(
        self,
        data_path: str = _DATA_PATH,
        threshold: float = SIMILARITY_THRESHOLD
    ):
        self.data_path = data_path
        self.threshold = threshold

        self.faqs = self._load_faqs(self.data_path)

        if not self.faqs:
            raise ValueError(
                f"No FAQs were loaded from {self.data_path}"
            )

        # Create a searchable list containing the main question
        # and all optional question variations.
        self._training_questions = []
        self._training_faq_indexes = []

        for faq_index, faq in enumerate(self.faqs):

            # Main FAQ question
            questions = [faq["question"]]

            # Optional variations
            variations = faq.get("question_variations", [])

            if isinstance(variations, list):
                questions.extend(variations)

            for question in questions:
                self._training_questions.append(question)
                self._training_faq_indexes.append(faq_index)

        # Preprocess every training question.
        self._processed_questions = [
            preprocess(question)
            for question in self._training_questions
        ]

        # TF-IDF vectorizer.
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        self.faq_vectors = self.vectorizer.fit_transform(
            self._processed_questions
        )

    @staticmethod
    def _load_faqs(path: str) -> list:
        """Load FAQ data from JSON."""
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_best_match(self, user_message: str) -> dict:
        """
        Find the FAQ that best matches the user's question.
        """

        if not user_message or not user_message.strip():
            return {
                "answer": "Please type a question so I can help you.",
                "category": None,
                "similarity": 0.0,
                "matched_question": None,
                "faq_id": None,
            }

        processed_query = preprocess(user_message)

        if not processed_query:
            return {
                "answer": FALLBACK_RESPONSE,
                "category": None,
                "similarity": 0.0,
                "matched_question": None,
                "faq_id": None,
            }

        # Convert the user question into the same TF-IDF space.
        query_vector = self.vectorizer.transform(
            [processed_query]
        )

        # Compare user question against every question/variation.
        similarities = cosine_similarity(
            query_vector,
            self.faq_vectors
        )[0]

        best_training_index = similarities.argmax()

        best_score = float(
            similarities[best_training_index]
        )

        # Find which FAQ the winning question belongs to.
        best_faq_index = self._training_faq_indexes[
            best_training_index
        ]

        best_faq = self.faqs[best_faq_index]

        # Reject weak matches.
        if best_score < self.threshold:
            return {
                "answer": FALLBACK_RESPONSE,
                "category": None,
                "similarity": round(best_score, 4),
                "matched_question": None,
                "faq_id": None,
            }

        return {
            "answer": best_faq["answer"],
            "category": best_faq["category"],
            "similarity": round(best_score, 4),
            "matched_question": best_faq["question"],
            "faq_id": best_faq["id"],
        }


if __name__ == "__main__":

    matcher = FAQMatcher()

    test_questions = [
        "I want my website to appear higher on Google",
        "How do I get more people to find my website through Google?",
        "Can Instagram help me promote my business?",
        "I want to advertise my business online, what should I use?",
        "How can I promote my business through emails?",
        "What is the weather today?"
    ]

    for question in test_questions:

        result = matcher.get_best_match(question)

        print("\nQuestion:", question)
        print("Answer:", result["answer"])
        print("Category:", result["category"])
        print("Similarity:", result["similarity"])
        print("Matched FAQ:", result["matched_question"])
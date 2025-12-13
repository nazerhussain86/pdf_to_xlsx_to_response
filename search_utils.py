import re
import nltk
nltk.download('punkt')

def search_sentences(pages_data, search_text, mode="phrase"):
    """
    mode:
    - phrase : exact phrase
    - words  : all words must exist (any order)
    """

    results = []
    search_text = search_text.lower()
    search_words = search_text.split()

    for page in pages_data:
        sentences = nltk.sent_tokenize(page["text"])

        for sentence in sentences:
            s_lower = sentence.lower()

            if mode == "phrase" and search_text in s_lower:
                results.append({
                    "page": page["page"],
                    "sentence": sentence.strip()
                })

            elif mode == "words" and all(w in s_lower for w in search_words):
                results.append({
                    "page": page["page"],
                    "sentence": sentence.strip()
                })

    return results
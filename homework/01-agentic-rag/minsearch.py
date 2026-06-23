"""
Minimal in-memory full-text search engine.
Source: https://github.com/alexeygrigorev/minsearch
"""

import re
from collections import defaultdict


class Index:
    def __init__(self, text_fields, keyword_fields):
        self.text_fields = text_fields
        self.keyword_fields = keyword_fields
        self.docs = []
        self.index = defaultdict(lambda: defaultdict(list))
        self.keyword_index = defaultdict(lambda: defaultdict(list))

    def fit(self, docs):
        self.docs = docs
        self.index = defaultdict(lambda: defaultdict(list))
        self.keyword_index = defaultdict(lambda: defaultdict(list))

        for doc_id, doc in enumerate(docs):
            for field in self.text_fields:
                text = doc.get(field, "")
                tokens = self._tokenize(text)
                for token in tokens:
                    self.index[field][token].append(doc_id)

            for field in self.keyword_fields:
                value = doc.get(field, "")
                self.keyword_index[field][value].append(doc_id)

        return self

    def search(self, query, filter_dict=None, boost_dict=None, num_results=10):
        tokens = self._tokenize(query)
        scores = defaultdict(float)

        for field in self.text_fields:
            boost = (boost_dict or {}).get(field, 1.0)
            for token in tokens:
                for doc_id in self.index[field].get(token, []):
                    scores[doc_id] += boost

        if filter_dict:
            for field, value in filter_dict.items():
                allowed = set(self.keyword_index[field].get(value, []))
                scores = {doc_id: score for doc_id, score in scores.items() if doc_id in allowed}

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [self.docs[doc_id] for doc_id, _ in ranked[:num_results]]

    @staticmethod
    def _tokenize(text):
        return re.findall(r"\w+", text.lower())

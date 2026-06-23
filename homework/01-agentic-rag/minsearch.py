# Minimal search engine using TF-IDF + keyword filtering
# Source: https://github.com/alexeygrigorev/minsearch

import math
from collections import defaultdict

class Index:
    def __init__(self, text_fields, keyword_fields):
        self.text_fields = text_fields
        self.keyword_fields = keyword_fields
        self.index = {}
        self.keyword_index = defaultdict(list)
        self.docs = []

    def fit(self, docs):
        self.docs = docs
        self.index = {field: defaultdict(list) for field in self.text_fields}

        for i, doc in enumerate(docs):
            for field in self.text_fields:
                text = doc.get(field, "")
                for word in self._tokenize(text):
                    self.index[field][word].append(i)
            for field in self.keyword_fields:
                val = doc.get(field, "")
                self.keyword_index[f"{field}:{val}"].append(i)

        self.idf = {}
        n = len(docs)
        for field in self.text_fields:
            self.idf[field] = {}
            for word, postings in self.index[field].items():
                df = len(set(postings))
                self.idf[field][word] = math.log((n - df + 0.5) / (df + 0.5) + 1)

        return self

    def search(self, query, filter_dict=None, boost_dict=None, num_results=10):
        query_terms = self._tokenize(query)
        scores = defaultdict(float)

        for field in self.text_fields:
            boost = (boost_dict or {}).get(field, 1.0)
            for term in query_terms:
                idf = self.idf[field].get(term, 0)
                for doc_id in self.index[field].get(term, []):
                    scores[doc_id] += boost * idf

        if filter_dict:
            allowed = None
            for field, value in filter_dict.items():
                key = f"{field}:{value}"
                candidates = set(self.keyword_index.get(key, []))
                allowed = candidates if allowed is None else allowed & candidates
            if allowed is not None:
                scores = {k: v for k, v in scores.items() if k in allowed}

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [self.docs[i] for i, _ in ranked[:num_results]]

    def _tokenize(self, text):
        return text.lower().split()

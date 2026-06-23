import math
from collections import defaultdict


class Index:
    """Minimal full-text + keyword search index."""

    def __init__(self, text_fields, keyword_fields):
        self.text_fields = text_fields
        self.keyword_fields = keyword_fields
        self.docs = []
        self.index = defaultdict(lambda: defaultdict(list))  # term -> field -> [doc_ids]

    def fit(self, docs):
        self.docs = docs
        for idx, doc in enumerate(docs):
            for field in self.text_fields:
                text = doc.get(field, "")
                for token in self._tokenize(text):
                    self.index[token][field].append(idx)
        return self

    def _tokenize(self, text):
        return text.lower().split()

    def _score(self, query_tokens, field, boost):
        scores = defaultdict(float)
        field_index = {token: self.index.get(token, {}).get(field, []) for token in query_tokens}
        total_docs = len(self.docs)
        for token, doc_ids in field_index.items():
            if not doc_ids:
                continue
            idf = math.log((total_docs - len(doc_ids) + 0.5) / (len(doc_ids) + 0.5) + 1)
            tf_counts = defaultdict(int)
            for did in doc_ids:
                tf_counts[did] += 1
            for did, tf in tf_counts.items():
                scores[did] += boost * idf * (tf / (tf + 1.5))
        return scores

    def search(self, query, filter_dict=None, boost_dict=None, num_results=10):
        query_tokens = self._tokenize(query)
        boost_dict = boost_dict or {f: 1.0 for f in self.text_fields}

        total_scores = defaultdict(float)
        for field in self.text_fields:
            boost = boost_dict.get(field, 1.0)
            field_scores = self._score(query_tokens, field, boost)
            for did, s in field_scores.items():
                total_scores[did] += s

        # Apply keyword filters
        if filter_dict:
            filtered = []
            for did, score in total_scores.items():
                doc = self.docs[did]
                if all(doc.get(k) == v for k, v in filter_dict.items()):
                    filtered.append((did, score))
        else:
            filtered = list(total_scores.items())

        filtered.sort(key=lambda x: x[1], reverse=True)
        return [self.docs[did] for did, _ in filtered[:num_results]]

import os
import math
import re
from collections import defaultdict

class InfoDocument:
    def __init__(self, norma: float, index: int, cuerpo: str):
        self.norma = norma
        self.index = index
        self.cuerpo = cuerpo

class BBDD:
    def __init__(self, path: str, delimitors: str):
        self.delimitors = delimitors
        self.larousse = defaultdict(lambda: defaultdict(float))
        self.infos = {}
        self.tf_idf = {}
        self._load_files(path)

    def _load_files(self, path: str):
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]
        for file in files:
            self._add_file(file)
        self.tf_idf = self._compute_tf_idf()

    def _add_file(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file:
            body = file.read().lower()
        words = re.split(self.delimitors, body)
        word_count = defaultdict(float)
        for word in words:
            if word:
                word_count[word] += 1
                self.larousse[word][file_path] += 1
        norma = math.sqrt(sum(freq ** 2 for freq in word_count.values()))
        self.infos[file_path] = InfoDocument(norma, len(self.infos), body)

    def _compute_tf_idf(self):
        tf_idf = {}
        total_docs = len(self.infos)
        for word, doc_freqs in self.larousse.items():
            tf_idf[word] = {}
            for doc, freq in doc_freqs.items():
                tf_idf[word][doc] = (freq / sum(self.larousse[word].values())) * math.log10(total_docs / len(doc_freqs))
        return tf_idf

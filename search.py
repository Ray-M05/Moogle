from Levenshtein import distance as levenshtein_distance
from collections import defaultdict

class SearchEngine:
    def __init__(self, indexer):
        self.indexer = indexer

    def query(self, query):
        palabras_query = self.indexer.limpiar_texto(query)
        scores = defaultdict(float)
        sugerencias = {}

        for palabra in palabras_query:
            if palabra in self.indexer.Larousse:
                for doc, tfidf in self.indexer.TF_IDF[palabra].items():
                    scores[doc] += tfidf
            else:
                mejor_distancia = float('inf')
                mejor_palabra = None
                for palabra_indexada in self.indexer.Larousse.keys():
                    distancia = levenshtein_distance(palabra, palabra_indexada)
                    if distancia < mejor_distancia and distancia < 3:
                        mejor_distancia = distancia
                        mejor_palabra = palabra_indexada
                if mejor_palabra:
                    sugerencias[palabra] = mejor_palabra
                    for doc, tfidf in self.indexer.TF_IDF[mejor_palabra].items():
                        scores[doc] += tfidf

        resultados = sorted(scores.items(), key=lambda x: -x[1])
        return resultados, sugerencias
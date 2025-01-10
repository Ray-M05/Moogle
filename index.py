import os
import re
import math
import pdfplumber
from collections import defaultdict

class DocumentIndexer:
    def __init__(self):
        self.Larousse = defaultdict(dict)  # Índice invertido
        self.TF_IDF = defaultdict(dict)   # TF-IDF por palabra
        self.documentos = {}              # Documentos y su texto
        self.threshold = None             # Umbral dinámico para exclusión de palabras comunes

    def limpiar_texto(self, texto):
        texto = re.sub(r'[\W_]+', ' ', texto.lower())  # Eliminar puntuación y pasar a minúsculas
        return texto.split()  # Separar por palabras

    def calcular_umbral(self):
        """Calcula el umbral dinámico basado en la frecuencia de las palabras en todo el corpus."""
        palabra_frecuencia = defaultdict(int)
        for palabras in self.Larousse.values():
            for doc, freq in palabras.items():
                palabra_frecuencia[doc] += freq

        total_frecuencias = sum(palabra_frecuencia.values())
        if len(palabra_frecuencia) > 0:  # Verificar si hay palabras antes de dividir
            self.threshold = total_frecuencias / len(palabra_frecuencia)
        else:
            self.threshold = float('inf')  # Valor alto que excluye todas las palabras


    def cargar_documentos(self, ruta_carpeta):
        for archivo in os.listdir(ruta_carpeta):
            if archivo.endswith(".pdf"):
                ruta_pdf = os.path.join(ruta_carpeta, archivo)
                with pdfplumber.open(ruta_pdf) as pdf:
                    texto = ''
                    for pagina in pdf.pages:
                        texto += pagina.extract_text() or ''
                    self.documentos[archivo] = texto

    def construir_indices(self):
        total_documentos = len(self.documentos)
        for doc, texto in self.documentos.items():
            palabras = self.limpiar_texto(texto)
            total_palabras = len(palabras)
            frecuencias = defaultdict(int)

            for palabra in palabras:
                frecuencias[palabra] += 1

            for palabra, frecuencia in frecuencias.items():
                self.Larousse[palabra][doc] = frecuencia

            for palabra, frecuencia in frecuencias.items():
                if frecuencia <= self.threshold:  # Excluir palabras muy comunes
                    self.TF_IDF[palabra][doc] = (frecuencia / total_palabras) * math.log10(total_documentos / len(self.Larousse[palabra]))

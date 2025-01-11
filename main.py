from index import DocumentIndexer
from search import SearchEngine
from app import MoogleApp
import tkinter as tk

def main():
    # Crear el indexador y cargar documentos
    indexer = DocumentIndexer()
    #C:\Pro\Moogle in Py
    indexer.cargar_stop_words("C:\Pro\Moogle in Py\stop_words.txt")
    indexer.cargar_documentos("C:\Pro\Moogle in Py\Edgar allan poe")  # Ruta de documentos
    if not indexer.documentos:  # Verificar si se cargaron documentos
        print("No se encontraron documentos válidos en la ruta especificada.")
        return
    indexer.calcular_umbral()  # Calcular el umbral de exclusión dinámico
    indexer.construir_indices()  # Construir los índices necesarios para la búsqueda

    # Crear el motor de búsqueda
    engine = SearchEngine(indexer)

    # Crear la interfaz gráfica
    root = tk.Tk()
    app = MoogleApp(root, engine)
    root.mainloop()

if __name__ == "__main__":
    main()

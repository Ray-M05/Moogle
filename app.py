import tkinter as tk
from tkinter import ttk

class MoogleApp:
    def __init__(self, root, engine):
        self.root = root
        self.engine = engine
        self.root.title("Moogle! Search Engine")

        self.search_frame = ttk.Frame(root, padding="10")
        self.search_frame.grid(row=0, column=0, sticky="EW")

        self.query_label = ttk.Label(self.search_frame, text="Query:")
        self.query_label.grid(row=0, column=0, sticky="W")

        self.query_entry = ttk.Entry(self.search_frame, width=40)
        self.query_entry.grid(row=0, column=1, sticky="EW")

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.perform_search)
        self.search_button.grid(row=0, column=2, sticky="E")

        self.search_frame.columnconfigure(1, weight=1)

        self.results_frame = ttk.Frame(root, padding="10")
        self.results_frame.grid(row=1, column=0, sticky="NSEW")

        self.results_list = tk.Text(self.results_frame, wrap="word", height=20, state="disabled")
        self.results_list.pack(fill="both", expand=True)

    def perform_search(self):
        query = self.query_entry.get()  # Obtener la consulta
        resultados, sugerencias = self.engine.query(query)  # Realizar la búsqueda

        # Limpia la lista de resultados previa
        self.results_list.configure(state="normal")
        self.results_list.delete(1.0, tk.END)

        # Muestra los resultados
        if resultados:
            self.results_list.insert(tk.END, "Resultados:\n\n")
            for doc, score, snippet in resultados:
                titulo = doc.split("/")[-1]  # Obtiene solo el nombre del archivo
                self.results_list.insert(
                    tk.END, f"Título: {titulo}\nScore: {score:.4f}\nSnippet: {snippet}\n\n"
                )
        else:
            self.results_list.insert(tk.END, "No se encontraron resultados.\n")

        # Muestra sugerencias si existen
        if sugerencias:
            self.results_list.insert(tk.END, "\nSugerencias:\n")
            for palabra, sugerencia in sugerencias.items():
                self.results_list.insert(tk.END, f"{palabra} -> {sugerencia}\n")

        # Desactiva el widget para evitar edición
        self.results_list.configure(state="disabled")

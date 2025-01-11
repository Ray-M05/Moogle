import tkinter as tk
from tkinter import ttk

class MoogleApp:
    def __init__(self, root, engine):
        self.root = root
        self.engine = engine
        self.root.title("Moogle! Search Engine")
        self.root.geometry("600x400")
        self.root.configure(bg="#e6d8f1")

        # Encabezado estilo "Google"
        self.header = tk.Label(
            root, text="moogle", font=("Arial", 28, "bold"), fg="#9b59b6", bg="#e6d8f1"
        )
        self.header.pack(pady=20)

        # Marco de búsqueda
        self.search_frame = tk.Frame(root, bg="#e6d8f1")
        self.search_frame.pack(pady=20)

        self.query_entry = tk.Entry(
            self.search_frame, font=("Arial", 16), width=40, bd=2, relief="solid"
        )
        self.query_entry.grid(row=0, column=0, padx=10)

        self.search_button = tk.Button(
            self.search_frame,
            text="Search",
            font=("Arial", 14, "bold"),
            bg="#d1a3f0",
            fg="white",
            relief="flat",
            command=self.perform_search,
        )
        self.search_button.grid(row=0, column=1)

        # Marco de resultados
        self.results_frame = tk.Frame(root, bg="#e6d8f1")
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.results_list = tk.Text(
            self.results_frame,
            wrap="word",
            height=10,
            state="disabled",
            bg="#f3e5f5",
            fg="#6a1b9a",
            font=("Arial", 12),
            relief="flat",
            bd=0,
        )
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
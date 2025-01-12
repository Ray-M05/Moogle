import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  
import os

class MoogleApp:
    def __init__(self, root, engine):
        self.root = root
        self.engine = engine
        self.root.title("BatiGoogle Search Engine")
        self.root.geometry("800x500")
        self.root.configure(bg="black")

        # Canvas para el logo de Batman (ahora con imagen)
        self.logo_canvas = tk.Canvas(root, width=200, height=100, bg="black", highlightthickness=0)
        self.logo_canvas.pack(pady=10)
        self.display_batman_logo()

        # Encabezado estilo "Google"
        self.header = tk.Label(
            root, text="BATIGOOGLE", font=("Times New Roman", 32, "bold"), fg="white", bg="black"
        )
        self.header.pack(pady=10)

        # Marco de búsqueda
        self.search_frame = tk.Frame(root, bg="black")
        self.search_frame.pack(pady=20)

        self.query_entry = tk.Entry(
            self.search_frame, font=("Arial", 16), width=50, bd=2, relief="solid"
        )
        self.query_entry.grid(row=0, column=0, padx=10)

        self.search_button = tk.Button(
            self.search_frame,
            text="⌕",  # Ícono de lupa
            font=("Arial", 16),
            bg="#4a4a4a",
            fg="white",
            relief="flat",
            command=self.perform_search,
            width=3
        )
        self.search_button.grid(row=0, column=1)

        # Marco de resultados
        self.results_frame = tk.Frame(root, bg="black")
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.results_list = tk.Text(
            self.results_frame,
            wrap="word",
            height=15,
            state="disabled",
            bg="#333333",
            fg="white",
            font=("Arial", 12),
            relief="solid",
            bd=1,
        )
        self.results_list.pack(fill="both", expand=True)

    def display_batman_logo(self):
        # Mostrar la ruta actual para ayudar en la depuración
        print("Ruta actual del script:", os.getcwd())

        # Cargar y mostrar la imagen del logo de Batman
        try:
            image_path = "logo.jpg"  # Cambia al nombre o extensión correctos si es necesario
            image = Image.open(image_path)  # Asegúrate de que el archivo esté en la misma carpeta
            image = image.resize((200, 100), Image.Resampling.LANCZOS)  # Redimensionar la imagen
            self.logo_image = ImageTk.PhotoImage(image)
            self.logo_canvas.create_image(100, 50, image=self.logo_image)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {image_path}. Asegúrate de que esté en la misma carpeta que este script.")
        except Exception as e:
            print("Error al cargar la imagen:", e)

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

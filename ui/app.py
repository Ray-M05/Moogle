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
        query = self.query_entry.get()
        result = self.engine.query(query)

        self.results_list.config(state="normal")
        self.results_list.delete(1.0, tk.END)

        for item in result.items:
            self.results_list.insert(tk.END, f"Title: {item.title}\n")
            self.results_list.insert(tk.END, f"Snippet: {item.snippet}\n")
            self.results_list.insert(tk.END, f"Score: {item.score}\n\n")

        if result.suggestion:
            self.results_list.insert(tk.END, f"Suggestion: {result.suggestion}\n")

        self.results_list.config(state="disabled")

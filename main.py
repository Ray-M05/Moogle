from engine.database import BBDD
from engine.search import SearchEngine
from ui.app import MoogleApp
import tkinter as tk

if __name__ == "__main__":
    db_path = "./Content" 
    db = BBDD(db_path, delimitors=".,:;¿?¡()[]{}<>@#$%&_+-/ \\n")
    search_engine = SearchEngine(db)

    root = tk.Tk()
    app = MoogleApp(root, search_engine)
    root.mainloop()

import tkinter as tk
from gui import IntegratedScientificArticlesGUI

def main_integrated():
    root = tk.Tk()
    root.title("Gestor de Artículos Científicos")
    app = IntegratedScientificArticlesGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main_integrated()

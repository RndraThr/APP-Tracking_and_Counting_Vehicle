import tkinter as tk
from app.views.main_window import MainWindow
import os,sys

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
def resource_path(relative_path):
    """Mendapatkan path absolut untuk resource di development dan production."""
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def _resource_path(self, relative_path):
    """Mendapatkan absolute path untuk resource, bekerja baik dalam development maupun dalam executable."""
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, '..', '..', relative_path)
if __name__ == "__main__":
    main()
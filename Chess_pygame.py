import tkinter as tk
from Chess_pygame_app import ChessApplication

if __name__ == '__main__':
    main_root = tk.Tk()
    ChessApplication(main_root, width=800, height=800).pack(side="top", fill="both", expand=True)
    main_root.mainloop()
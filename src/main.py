from app.retouch_getimg import RetouchGetImg
from tkinterdnd2 import TkinterDnD

if __name__ == "__main__":

    # Use TkinterDnD for drag-and-drop
    root = TkinterDnD.Tk()  # This will create only one proper window
    app = RetouchGetImg(root)
    root.mainloop()

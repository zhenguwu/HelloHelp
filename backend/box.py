import threading
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

def draw_bounding_box(x1, y1, x2, y2):
    def run_gui():
        root = tk.Tk()
        root.wait_visibility(root)
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        root.config(bg='systemTransparent')
        root.attributes("-transparentcolor", "systemTransparent")

        canvas = Canvas(root, width=screen_width, height=screen_height)
        canvas.config(bg='systemTransparent')
        canvas.pack(fill="both", expand=True)

        box_color = "red"
        box_width = 2

        canvas.create_rectangle(x1, y1, x2, y2, outline=box_color, width=box_width)

        root.mainloop()

    if threading.current_thread() == threading.main_thread():
        run_gui()
    else:
        print("This code must be run in the main thread.")

import tkinter as tk

from PIL import ImageFilter, ImageGrab, ImageTk

COVER_MESSAGE = "Phone detected - screen hidden for data protection"
BLUR_SHRINK_FACTOR = 8
BLUR_RADIUS = 4


class ScreenCover:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.window = None
        self.photo = None

    def show(self):
        if self.window is not None:
            return

        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()

        screenshot = ImageGrab.grab()
        small = screenshot.resize((max(1, width // BLUR_SHRINK_FACTOR), max(1, height // BLUR_SHRINK_FACTOR)))
        screenshot.close()
        blurred_small = small.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
        small.close()
        blurred = blurred_small.resize((width, height))
        blurred_small.close()
        self.photo = ImageTk.PhotoImage(blurred, master=self.root)
        blurred.close()

        window = tk.Toplevel(self.root)
        window.overrideredirect(True)
        window.geometry(f"{width}x{height}+0+0")
        window.attributes("-topmost", True)

        canvas = tk.Canvas(window, width=width, height=height, highlightthickness=0, bd=0)
        canvas.pack()
        canvas.create_image(0, 0, image=self.photo, anchor="nw")
        text = canvas.create_text(
            width // 2,
            height // 2,
            text=COVER_MESSAGE,
            fill="white",
            font=("Segoe UI", 28, "bold"),
            width=int(width * 0.8),
            justify="center",
        )
        left, top, right, bottom = canvas.bbox(text)
        padding = 30
        backdrop = canvas.create_rectangle(
            left - padding, top - padding, right + padding, bottom + padding, fill="#1e1e1e", outline=""
        )
        canvas.tag_lower(backdrop, text)

        window.lift()
        window.update()
        self.window = window

    def hide(self):
        if self.window is None:
            return
        window, self.window = self.window, None
        self.photo = None
        window.destroy()
        self.root.update()

    def update(self):
        self.root.update()

    def close(self):
        try:
            self.hide()
        finally:
            self.photo = None
            self.root.destroy()

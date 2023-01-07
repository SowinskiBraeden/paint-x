#!/usr/bin/env python3.11
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw

WIDTH, HEIGHT = 500, 500
CENTER = WIDTH // 2
WHITE = (255, 255, 255)

class PaintGUI:
  def __init__(self):
    self.root = tk.Tk()
    self.root.title = "Paint X"

    self.brush_width = 15
    self.current_color = "#000000"

    self.saved = False

    self.canvas = tk.Canvas(self.root, width=WIDTH-10, height=HEIGHT-10, bg="white")
    self.canvas.pack()
    self.canvas.bind("<B1-Motion>", self.paint)

    self.image = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    self.draw = ImageDraw.Draw(self.image)

    self.button_frame = tk.Frame(self.root)
    self.button_frame.pack(fill=tk.X)

    self.button_frame.columnconfigure(0, weight=1)
    self.button_frame.columnconfigure(1, weight=1)
    self.button_frame.columnconfigure(2, weight=1)

    self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear)
    self.clear_button.grid(row=0, column=1, sticky=tk.W+tk.E)

    self.save_button = tk.Button(self.button_frame, text="Save as", command=self.save)
    self.save_button.grid(row=0, column=2, sticky=tk.W+tk.E)

    self.brushPlus_button = tk.Button(self.button_frame, text="Brush+", command=self.brush_plus)
    self.brushPlus_button.grid(row=0, column=0, sticky=tk.W+tk.E)

    self.brushMinus_button = tk.Button(self.button_frame, text="Brush-", command=self.brush_minus)
    self.brushMinus_button.grid(row=1, column=0, sticky=tk.W+tk.E)

    self.color_button = tk.Button(self.button_frame, text="Change Color", command=self.color_select)
    self.color_button.grid(row=1, column=1, sticky=tk.W+tk.E)

    self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    self.root.attributes("-topmost", True)
    self.root.mainloop()

  def paint(self, event):
    self.saved = False
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.current_color, fill=self.current_color, width=self.brush_width)
    self.draw.rectangle([x1, y1, x2 + self.brush_width, y2 + self.brush_width], outline=self.current_color, fill=self.current_color, width=self.brush_width)

  def clear(self):
    self.saved = False
    self.canvas.delete('all')
    self.draw.rectangle([0, 0, 1000, 1000], fill="white")

  def save(self):
    self.saved = True
    filename = filedialog.asksaveasfilename(initialfile="untitled.png",
                                            defaultextension="png",
                                            filetypes=[("PNG", "JPG"), (".png", ".jpg")])

    if filename != "": self.image.save(filename)
  
  def brush_plus(self):
    self.brush_width += 1

  def brush_minus(self):
    self.brush_width -= 1 if self.brush_width > 1 else 1

  def color_select(self):
    _, self.current_color = colorchooser.askcolor(title="Choose a color")

  def on_close(self):
    if not self.saved:
      a = messagebox.askyesno("Quit", "Are you sure you want to close? You have unsaved changes.", parent=self.root)
      if a:
        self.root.destroy()

    else: self.root.destroy()

PaintGUI()
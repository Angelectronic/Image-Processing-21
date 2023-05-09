import tkinter as tk
from PIL import ImageTk, Image
import os

# create a window like this
root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# draw something on the canvas
x = 10
y = 10
w = 150
h = 150
color = (0, 0, 255)
for i in range(4):
    canvas.create_rectangle(x+i*w/8, y+i*h/8, x+(i+1)*w/8, y+(i+1)*h/8, fill="#000000")

# convert image to PNG format
im = ImageTk.PhotoImage(canvas)
file = open("my_image.png", "wb")
im.save(file, format="PNG")
os._exit(0)

import tkinter as tk
import numpy as np

SIZE = 28
SCALE = 18
WINDOW = SIZE * SCALE

canvas_data = np.zeros((SIZE, SIZE), dtype=np.float32)

root = tk.Tk()
root.title("CNN from Scratch (NumPy)")

canvas = tk.Canvas(root, width=WINDOW, height=WINDOW, bg="black")
canvas.pack()

info = tk.Label(root, text="Draw a digit", font=("Arial", 16))
info.pack()

kernel = np.array([
    [1, 0, -1],
    [1, 0, -1],
    [1, 0, -1]
], dtype=np.float32)

weights = np.random.randn(10, SIZE*SIZE).astype(np.float32)

def convolve(img, k):
    out = np.zeros_like(img)
    for y in range(1, SIZE-1):
        for x in range(1, SIZE-1):
            out[y,x] = np.sum(img[y-1:y+2, x-1:x+2] * k)
    return out

def softmax(x):
    e = np.exp(x - np.max(x))
    return e / np.sum(e)

def draw_grid():
    for i in range(SIZE):
        canvas.create_line(i*SCALE, 0, i*SCALE, WINDOW, fill="#333")
        canvas.create_line(0, i*SCALE, WINDOW, i*SCALE, fill="#333")

def draw(event):
    x, y = event.x // SCALE, event.y // SCALE
    if 0 <= x < SIZE and 0 <= y < SIZE:
        canvas_data[y, x] = 1.0
        canvas.create_rectangle(
            x*SCALE, y*SCALE,
            (x+1)*SCALE, (y+1)*SCALE,
            fill="white", outline="white"
        )
        predict()

def predict():
    feature = convolve(canvas_data, kernel)
    pooled = np.mean(feature)
    flat = canvas_data.flatten()
    logits = weights @ flat
    probs = softmax(logits)
    digit = np.argmax(probs)
    conf = probs[digit] * 100
    info.config(text=f"Prediction: {digit} ({conf:.1f}%)")

def clear():
    canvas.delete("all")
    canvas_data[:] = 0
    draw_grid()
    info.config(text="Draw a digit")

canvas.bind("<B1-Motion>", draw)

tk.Button(root, text="Clear", command=clear).pack()

draw_grid()
root.mainloop()

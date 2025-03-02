import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

def generate_fox():
    img_url = requests.get("https://randomfox.ca/floof/").json()["image"]
    img_data = Image.open(BytesIO(requests.get(img_url).content)).resize((800, 600))
    label.config(image=(img_ref := ImageTk.PhotoImage(img_data)), text="")
    label.image = img_ref

#window
window = tk.Tk()
window.title("FOX GENERATOR")
label = tk.Label(window, text="Loading....", font=("Arial", 14))
label.pack()
btn = tk.Button(window, text="Get New Fox", command=generate_fox, font=("Arial", 12), bg ="black", fg="white")
btn.pack()

generate_fox()
window.mainloop()

import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

def generate_fox():
    """Fetches a random fox image and updates the UI."""
    try:
        response = requests.get("https://randomfox.ca/floof/", timeout=10)
        response.raise_for_status()  # Raises an error for HTTP issues
        img_url = response.json().get("image")

        if img_url:
            img_response = requests.get(img_url, timeout=10)
            img_response.raise_for_status()

            img_data = Image.open(BytesIO(img_response.content))
            img_data.thumbnail((800, 600))  # Resizing while keeping aspect ratio

            fox_image = ImageTk.PhotoImage(img_data)
            label.config(image=fox_image, text="")
            label.image = fox_image
        else:
            label.config(text="⚠ No image found!", image="")

    except requests.exceptions.RequestException:
        label.config(text="⚠ Error loading image. Check your internet connection.", image="")

# 🖼 Tkinter window setup
window = tk.Tk()
window.title("🐺 FOX GENERATOR")
window.geometry("820x650")  # Fixed size to keep layout consistent
window.resizable(False, False)

# Label to display the fox image
label = tk.Label(window, text="Loading....", font=("Arial", 14))
label.pack(pady=10)

# Button to fetch a new fox image
btn = tk.Button(window, text="Get New Fox 🦊", command=generate_fox, 
                font=("Arial", 12, "bold"), bg="black", fg="white", padx=10, pady=5)
btn.pack(pady=10)

generate_fox()  # Load the first fox image
window.mainloop()

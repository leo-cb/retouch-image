import tkinter as tk
from tkinterdnd2 import DND_FILES
from tkinter import messagebox
from PIL import Image, ImageTk
from abc import abstractmethod

class ImageProcessorBase:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Retouch")

        # Create a label for drag-and-drop area
        self.drop_area = tk.Label(root, text="Drag & Drop an Image Here", width=40, height=10, relief="groove")
        self.drop_area.pack(pady=10)

        # Bind drag-and-drop events
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_drop)

        # Create an entry widget for the text prompt
        self.text_prompt = tk.Entry(root, width=50)
        self.text_prompt.pack(pady=10)
        self.text_prompt.insert(0, "Enter your text prompt here...")

        # Create a button for image processing
        self.process_button = tk.Button(root, text="Retouch Image", command=self.process_image)
        self.process_button.pack(pady=10)

        # Create a label to display the image
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.image = None  # To store the loaded image

        # Adapter dropdown
        self.adapter_label = tk.Label(root, text="Adapter:")
        self.adapter_label.pack()
        self.adapter_var = tk.StringVar(value="content")
        self.adapter_dropdown = tk.OptionMenu(root, self.adapter_var, "content", "style", "face")
        self.adapter_dropdown.pack()

        # Strength slider
        self.strength_label = tk.Label(root, text="Strength (0.01-2.0):")
        self.strength_label.pack()
        self.strength_var = tk.DoubleVar(value=0.6)
        self.strength_slider = tk.Scale(root, from_=0.01, to=2.0, resolution=0.01, 
                                        orient=tk.HORIZONTAL, length=200, 
                                        variable=self.strength_var)
        self.strength_slider.pack()

        # Guidance slider
        self.guidance_label = tk.Label(root, text="Guidance (0-20):")
        self.guidance_label.pack()
        self.guidance_var = tk.DoubleVar(value=7.5)
        self.guidance_slider = tk.Scale(root, from_=0, to=20, resolution=0.1, 
                                        orient=tk.HORIZONTAL, length=200, 
                                        variable=self.guidance_var)
        self.guidance_slider.pack()

    def on_drop(self, event):
        file_path = event.data.strip('{}')  # Clean up the file path
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        try:
            self.image = Image.open(file_path)
            self.display_image(self.image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def display_image(self, img):
        # Resize for display purposes
        img_resized = img.resize((300, 300))
        tk_image = ImageTk.PhotoImage(img_resized)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image

    @abstractmethod
    def process_image(self):
        pass

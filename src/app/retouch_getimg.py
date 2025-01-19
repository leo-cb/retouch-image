from tkinter import messagebox
from base.image_processor_base import ImageProcessorBase

class RetouchGetImg(ImageProcessorBase):
    """Retouch image with getimg.ai API"""

    def __init__(self, root):
        super().__init__(root)
        
    def process_image(self):
        if not self.image:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        prompt = self.text_prompt.get()
        if not prompt.strip():
            messagebox.showwarning("Warning", "Please enter a text prompt!")
            return

        # Example image processing: convert to grayscale
        processed_image = self.image.convert("L")

        # Save and display the processed image
        processed_image.save("processed_image.jpg")
        self.display_image(processed_image)

        messagebox.showinfo("Success", "Image processed successfully!\nProcessed image saved as 'processed_image.jpg'.")

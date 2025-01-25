"""Implement an image to image model with getimg.ai API"""

import os
from datetime import datetime
from tkinter import messagebox
from src.lib.images import pil_to_base64, base64_to_pil, save_base64_image
from src.lib.ai import image_to_image_getimgai
from src.base.image_processor_base import ImageProcessorBase
from logger import logger

class RetouchGetImg(ImageProcessorBase):
    """Retouch image with getimg.ai API"""

    def __init__(self, root, **kwargs):
        """Initialize the RetouchGetImg class."""

        super().__init__(root)
        self.kwargs = kwargs

    def process_image(self) -> None:
        """
        Process the loaded image with the text prompt using the getimg.ai API
        and display the processed image.
        
        If no image is loaded or no text prompt is entered, a warning message
        will be shown. If the image processing fails, an error message will be
        shown with more details in the logs.
        """
       
        if not self.image:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        prompt = self.text_prompt.get()
        if not prompt.strip():
            messagebox.showwarning("Warning", "Please enter a text prompt!")
            return

        # Convert PIL image to base64
        image_base64 = pil_to_base64(self.image)
        if not image_base64:
            messagebox.showerror("Error", "Failed to convert image to base64")
            return

        # Apply prompt to image-to-image model
        processed_base64 = image_to_image_getimgai(
            prompt=prompt,
            image_base64=image_base64,
            output_file=None,  # We'll handle saving separately
            model_family="stable-diffusion-xl",
            adapter=self.adapter_var.get(),
            strength=self.strength_var.get(),
            guidance=self.guidance_var.get(),
            **self.kwargs
        )
        
        if processed_base64 is None:
            messagebox.showerror("Error", "Unable to generate the image. Check the logs for more details.")
            return

        # Convert processed base64 back to PIL for display
        processed_image = base64_to_pil(processed_base64)
        if not processed_image:
            messagebox.showerror("Error", "Failed to convert processed image")
            return

        # Save the processed image
        os.makedirs("output", exist_ok=True)
        dt = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"output/processed_image_{dt}.png"
        
        if save_base64_image(processed_base64, output_path):
            # Display the processed image
            self.display_image(processed_image)
            messagebox.showinfo("Success", f"Image processed successfully!\nProcessed image saved as '{output_path}'.")
        else:
            messagebox.showerror("Error", "Failed to save the processed image")

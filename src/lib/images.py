"""Image treatment functions"""

import base64
from io import BytesIO
import numpy as np
from PIL import Image
import cv2
from logger import logger

def image_to_base64(image_path : str) -> str:
    """Convert image to base64 string"""

    # Open the image in binary mode and convert it to Base64
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')

    return base64_string

def resize_image(input_image: np.ndarray, width: int, height: int) -> str:
    """
    Resize an image to the specified width and height and return it as a Base64 string.

    Args:
        input_image (np.ndarray): Input image as a NumPy array.
        width (int): Desired width of the resized image.
        height (int): Desired height of the resized image.

    Returns:
        str: Base64 string of the resized image.
    """
    # Resize the image
    resized_image = cv2.resize(input_image, (width, height), interpolation=cv2.INTER_LANCZOS4)
    
    # Convert the resized image to Base64
    pil_image = Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    base64_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    logger.debug(f"Image resized to {width}x{height} and converted to Base64.")
    return base64_string

def pil_to_base64(pil_image : object) -> str | None:
    """Convert PIL Image to base64 string"""

    try:
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        logger.error(f"Error converting PIL image to base64: {str(e)}")
        return None

def base64_to_pil(base64_string : str) -> object | None:
    """Convert base64 string to PIL Image"""
    try:
        # Remove data URL prefix if present
        if "base64," in base64_string:
            base64_string = base64_string.split("base64,")[1]
        
        image_data = base64.b64decode(base64_string)
        return Image.open(BytesIO(image_data))
    except Exception as e:
        logger.error(f"Error converting base64 to PIL image: {str(e)}")
        return None

def save_base64_image(base64_string : str, output_path : str) -> bool:
    """Save base64 string as image file"""
    try:
        pil_image = base64_to_pil(base64_string)
        if pil_image:
            pil_image.save(output_path)
            return True
        return False
    except Exception as e:
        logger.error(f"Error saving base64 image: {str(e)}")
        return False

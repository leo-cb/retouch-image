"""Functions to generate texts and images using AI"""

import os
import base64
import requests
from logger import logger

def image_to_image_getimgai(
    prompt : str,
    image_base64: str = "",
    model_version : str ="v1",
    model_family : str ="stable-diffusion-xl",
    output_file : str | None = None,
    truncate_prompt: bool = False,
    **kwargs
) -> str | None:
    """
    Generate an image using the Getimg.ai API and return it as base64 string.
    Saves image to 'output_file' if not None.
    
    Args:
        prompt (str): Text prompt for the image generation.
        image_base64 (str): Base64 encoded input image string.
        width (int): Width of the generated image.
        height (int): Height of the generated image.
        output_file (str): Optional file name for saving the generated image.
    
    Returns:
        str | None: Base64 encoded image string if successful, None otherwise.
    """
    # Get the API key from the environment variable
    api_key = os.getenv("GETIMG_API_KEY")
    if not api_key:
        logger.error("Error: GETIMG_API_KEY environment variable is not set.")
        return None

    # API endpoint
    url = f"https://api.getimg.ai/{model_version}/{model_family}/ip-adapter"

    # truncate if it exceeds the allowed maximum length
    if truncate_prompt and len(prompt) > 2048:
        prompt = prompt[:2048]
        logger.warning("Warning: Prompt length to generate image exceeds 2048 characters. Truncating the prompt.")

    # Define the payload
    payload = {
        "prompt": prompt
    }

    payload.update(**kwargs)

    # if base64 image is provided, add it to payload
    if image_base64:
        # Ensure the base64 string doesn't have the data URL prefix
        if "base64," in image_base64:
            image_base64 = image_base64.split("base64,")[1]
        payload["image"] = image_base64

    # Define the headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        # Make the API request
        response = requests.post(url, json=payload, headers=headers, timeout=60)

        # Check the response
        if response.status_code == 200:
            result = response.json()
            if "image" in result:  # Check for the 'image' key
                # Save the image to a file if output_file is provided
                if output_file:
                    image_data = base64.b64decode(result["image"])
                    with open(output_file, "wb") as img_file:
                        img_file.write(image_data)
                    logger.debug(f"Image saved as '{output_file}'")
                
                return result["image"]  # Return the base64 string
            else:
                logger.error("Error: No image found in the response.")
                return None
        else:
            logger.error(f"Error: {response.status_code}, {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error during API request: {str(e)}")
        return None

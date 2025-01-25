import os
import importlib
from src.processors.retouch_getimg import RetouchGetImg
from tkinterdnd2 import TkinterDnD
import config.configs as cfg
from logger import logger

# TODO: this goes to class
def setup_getimg():
    """Set up GetImg API key"""

    with open(".getimg_key", "r", encoding="utf-8") as f:
        getimg_key = f.read().replace("\n","")

    os.environ["GETIMG_API_KEY"] = getimg_key

if __name__ == "__main__":

    # Use TkinterDnD for drag-and-drop
    root = TkinterDnD.Tk()  # This will create only one proper window

    ##############################################
    ## Dynamically import the image-to-image module
    ##############################################
    
    # Get the module path and class name from configs
    module_path = cfg.IMG2IMG_MODEL["module"]
    class_name = cfg.IMG2IMG_MODEL["class"]

    try:
        # setup api key
        globals()[cfg.IMG2IMG_MODEL["api_key"]]()

        # Import module
        module = importlib.import_module(module_path)

        # Get the class from the imported module
        RetouchGetImg = getattr(module, class_name)
        
        # Instantiate the class (if desired)
        instance = RetouchGetImg(root,**cfg.IMG2IMG_MODEL["model_args"])
        logger.debug(f"Instance created: {instance}")
    except ModuleNotFoundError as e:
        logger.error(f"Error: Module '{module_path}' not found. {e}", exc_info=True)
    except AttributeError as e:
        logger.error(f"Error: Class '{class_name}' not found in '{module_path}'. {e}", exc_info=True)

    
    ##############################################
    ## Run main loop
    ##############################################

    root.mainloop()

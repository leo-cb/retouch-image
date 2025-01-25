"""Configurations for the application."""

# defines the image to image model to load
IMG2IMG_MODEL = {
    "module": "src.processors.retouch_getimg",
    "class": "RetouchGetImg",
    "api_key": "setup_getimg",  # function to setup the API key
    "model_args": {
        "model": "juggernaut-xl-v10",
        "steps": 100,
    },  # API model arguments
}

# IMG2IMG_MODEL = {
#     "module": "src.processors.retouch_getimg",
#     "class": "RetouchGetImg",
#     "api_key": "setup_getimg",  # function to setup the API key
#     "model_args": {
#         "adapter": "content",
#         "model": "reproduction-v3-31",
#         "steps": 100,
#     },  # API model arguments
# }

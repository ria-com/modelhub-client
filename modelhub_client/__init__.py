"""
The modelhub_client module.
"""
from .modelhub_client import ModelHub
from .models_example import models_example
from .cli import main

__version__ = '1.1.0'

__all__ = (
    '__version__',
    'ModelHub', 'models_example',
    'main',
)

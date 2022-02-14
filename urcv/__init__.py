from pathlib import Path

from . import hsv
from . import transform
from . import stack
from .input import wait_key, get_scaled_roi

with (Path(__file__).parent / './__version__').open() as f:
    __version__ = f.read()
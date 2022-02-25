from pathlib import Path

from . import draw
from . import hsv
from . import stack
from . import text
from . import transform
from .input import wait_key, get_scaled_roi

with (Path(__file__).parent / './__version__').open() as f:
    __version__ = f.read()
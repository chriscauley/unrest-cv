from pathlib import Path

with (Path(__file__).parent / './__version__').open() as f:
    __version__ = f.read()
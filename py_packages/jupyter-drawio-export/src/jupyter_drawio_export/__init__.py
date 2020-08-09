""" programmatic drawio export
"""
from ._version import __version__
from .serverextension import load_jupyter_server_extension

__all__ = [
    "load_jupyter_server_extension",
    "_jupyter_server_extension_paths",
    "__version__",
]


def _jupyter_server_extension_paths():
    return [{"module": "jupyter_drawio_export"}]

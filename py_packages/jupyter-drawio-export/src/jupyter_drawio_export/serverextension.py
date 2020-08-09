""" add language server support to the running jupyter notebook application
"""
import traitlets

from .handlers import add_handlers
from .manager import DrawioExportManager


def load_jupyter_server_extension(nbapp):
    """ create a DrawioExportManager and add handlers
    """
    nbapp.add_traits(drawio_manager=traitlets.Instance(DrawioExportManager))
    manager = nbapp.drawio_manager = DrawioExportManager(parent=nbapp, log=nbapp.log)
    manager.initialize()
    add_handlers(nbapp)
    nbapp.log.warning("drawio initialized %s", manager)

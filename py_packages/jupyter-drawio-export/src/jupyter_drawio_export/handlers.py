""" tornado handlers for managing and communicating with drawio export server
"""
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join as ujoin

from .manager import DrawioExportManager


class BaseHandler(IPythonHandler):
    manager = None  # type: DrawioExportManager

    def initialize(self, manager: DrawioExportManager):
        self.manager = manager


class PDFHandler(BaseHandler):
    def get(self, url):
        self.finish(f"WOO {url}")

    def post(self, url):
        self.finish(f"HA {url}")


def add_handlers(nbapp):
    """ Add drawio routes to the notebook server web application
    """
    url = ujoin(nbapp.base_url, "drawio", "export", "pdf", "(?P<url>.*)")

    opts = {"manager": nbapp.drawio_manager}

    nbapp.web_app.add_handlers(".*", [(url, PDFHandler, opts)])

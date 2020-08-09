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
    async def post(self, url):
        self.manager.parent.log.warning("DIO %s %s", url, self.request.body)
        params = {k: v[-1] for k, v in self.request.arguments.items()}
        pdf = await self.manager.pdf(params)
        self.finish(pdf)


def add_handlers(nbapp):
    """ Add drawio routes to the notebook server web application
    """
    url = ujoin(nbapp.base_url, "drawio", "export", r"(?P<url>.*)")

    opts = {"manager": nbapp.drawio_manager}

    nbapp.web_app.add_handlers(".*", [(url, PDFHandler, opts)])

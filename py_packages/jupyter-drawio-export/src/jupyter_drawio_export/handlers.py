"""
tornado handlers for managing and communicating with drawio export server

Copyright 2020 jupyterlab-drawio contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join as ujoin

from .manager import DrawioExportManager


class BaseHandler(IPythonHandler):
    manager = None  # type: DrawioExportManager

    def initialize(self, manager: DrawioExportManager):
        self.manager = manager


class PDFHandler(BaseHandler):
    async def post(self, url=None):
        params = {k: v[-1] for k, v in self.request.arguments.items()}
        params.pop("_xsrf", None)
        pdf = await self.manager.pdf([params])
        self.finish(pdf)


class StatusHandler(BaseHandler):
    async def get(self):
        status = await self.manager.status()
        self.finish(status)


class ProvisionHandler(BaseHandler):
    async def post(self):
        await self.manager.provision()
        status = await self.manager.status()
        self.finish(status)


def add_handlers(nbapp):
    """ Add drawio routes to the notebook server web application
    """
    ns_url = ujoin(nbapp.base_url, "drawio")
    pdf_url = ujoin(ns_url, "export", r"(?P<url>.*)")
    status_url = ujoin(ns_url, "status")
    provision_url = ujoin(ns_url, "provision")

    opts = {"manager": nbapp.drawio_manager}

    nbapp.web_app.add_handlers(
        ".*",
        [
            (status_url, StatusHandler, opts),
            (provision_url, ProvisionHandler, opts),
            (pdf_url, PDFHandler, opts),
        ],
    )

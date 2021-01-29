"""
tornado handlers for managing and communicating with drawio export server

Copyright 2021 ipydrawio contributors
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
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join as ujoin
from tornado.web import authenticated

from .manager import IPyDrawioExportManager


class BaseHandler(JupyterHandler):
    manager = None  # type: IPyDrawioExportManager

    def initialize(self, manager: IPyDrawioExportManager):
        self.manager = manager


class PDFHandler(BaseHandler):
    @authenticated
    async def post(self, url=None):
        params = {k: v[-1] for k, v in self.request.arguments.items()}
        params.pop("_xsrf", None)
        pdf = await self.manager.pdf([params])
        self.finish(pdf)


class StatusHandler(BaseHandler):
    @authenticated
    async def get(self):
        status = await self.manager.status()
        self.finish(status)


class ProvisionHandler(BaseHandler):
    @authenticated
    async def post(self):
        await self.manager.provision()
        status = await self.manager.status()
        self.finish(status)


def add_handlers(app):
    """Add ipydrawio routes to the notebook server web application"""
    ns_url = ujoin(app.base_url, "ipydrawio")
    pdf_url = ujoin(ns_url, "export", r"(?P<url>.*)")
    status_url = ujoin(ns_url, "status")
    provision_url = ujoin(ns_url, "provision")

    opts = {"manager": app.drawio_manager}

    app.log.debug(f"[ipydrawio] API: {status_url}")

    app.web_app.add_handlers(
        ".*",
        [
            (status_url, StatusHandler, opts),
            (provision_url, ProvisionHandler, opts),
            (pdf_url, PDFHandler, opts),
        ],
    )

"""
CLI for ipydrawio-export

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
import base64
import json
from pathlib import Path

import traitlets as T
from tornado import ioloop
from traitlets.config import Application

from ._version import __version__
from .constants import IPYNB_METADATA
from .manager import IPyDrawioExportManager


class BaseApp(Application):
    version = __version__

    @property
    def description(self):  # pragma: no cover
        return self.__doc__.splitlines()[0].strip()


class ManagedApp(BaseApp):
    drawio_manager = T.Instance(IPyDrawioExportManager)
    io_loop = T.Instance(ioloop.IOLoop)

    @T.default("io_loop")
    def _default_io_loop(self):
        return ioloop.IOLoop.current()

    @T.default("drawio_manager")
    def _default_drawio_manager(self):
        return IPyDrawioExportManager(parent=self, log=self.log)

    def start(self):
        self.drawio_manager.initialize()
        self.io_loop.add_callback(self.start_async)
        self.io_loop.start()

    def stop(self):
        def _stop():
            self.io_loop.stop()

        self.io_loop.add_callback(_stop)


class ProvisionApp(ManagedApp):
    """pre-provision drawio export tools"""

    async def start_async(self):
        try:
            await self.drawio_manager.provision(force=True)
        finally:
            self.stop()


class PDFApp(ManagedApp):
    """export a drawio as PDF"""

    dio_files = T.Tuple()

    def parse_command_line(self, argv=None):
        super().parse_command_line(argv)
        self.dio_files = [Path(p).resolve() for p in self.extra_args]

    async def start_async(self):
        try:
            await self.drawio_manager.provision()
            await self.drawio_manager.start_server()
            pdf_requests = []
            for dio in self.dio_files:
                # TODO: handle more request params
                pdf_request = {}
                if dio.name.endswith(".png"):
                    pdf_request["xml"] = base64.b64encode(dio.read_bytes()).decode(
                        "utf-8"
                    )
                elif dio.name.endswith(".ipynb"):
                    meta = json.loads(dio.read_text(encoding="utf-8"))["metadata"]
                    pdf_request["xml"] = meta[IPYNB_METADATA]["xml"]
                else:
                    pdf_request["xml"] = dio.read_text(encoding="utf-8")

                pdf_requests += [pdf_request]

            # TODO: traitlet for output name
            out = self.dio_files[0].parent / f"{self.dio_files[0].stem}.pdf"
            pdf_text = await self.drawio_manager.pdf(pdf_requests)
            if pdf_text is None:  # pragma: no cover
                self.log.error("No PDF text was created")
            else:
                pdf_bytes = base64.b64decode(pdf_text)
                self.log.warning("Writing %s bytes to %s", len(pdf_bytes), out)
                out.write_bytes(pdf_bytes)
        finally:
            self.stop()


class DrawioExportApp(BaseApp):
    """ipydrawio export tools"""

    name = "ipydrawio-export"
    subcommands = dict(
        provision=(ProvisionApp, ProvisionApp.__doc__.splitlines()[0]),
        pdf=(PDFApp, PDFApp.__doc__.splitlines()[0]),
    )


main = launch_instance = DrawioExportApp.launch_instance

if __name__ == "__main__":  # pragma: no cover
    main()

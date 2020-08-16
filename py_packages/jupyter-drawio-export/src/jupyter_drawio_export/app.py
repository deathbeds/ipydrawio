"""
CLI for jupyter-drawio-export

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

from pathlib import Path

import traitlets as T
from tornado import ioloop
from traitlets.config import Application

from ._version import __version__
from .manager import DrawioExportManager


class BaseApp(Application):
    version = __version__

    @property
    def description(self):
        return self.__doc__.splitlines()[0].strip()


class ManagedApp(BaseApp):
    drawio_manager = T.Instance(DrawioExportManager)
    io_loop = T.Instance(ioloop.IOLoop)

    @T.default("io_loop")
    def _default_io_loop(self):
        return ioloop.IOLoop.current()

    @T.default("drawio_manager")
    def _default_drawio_manager(self):
        return DrawioExportManager(parent=self, log=self.log)

    def start(self):
        self.drawio_manager.initialize()
        self.io_loop.add_callback(self.start_async)
        self.io_loop.start()

    def stop(self):
        def _stop():
            self.io_loop.stop()

        self.io_loop.add_callback(_stop)


class ProvisionApp(ManagedApp):
    """ pre-provision drawio export tools
    """

    async def start_async(self):
        try:
            await self.drawio_manager.provision(force=True)
        finally:
            self.stop()


class PDFApp(ManagedApp):
    """ export a drawio as PDF
    """

    dio_files = T.Tuple()

    def parse_command_line(self, argv=None):
        super().parse_command_line(argv)
        self.dio_files = [Path(p) for p in self.extra_args]

    async def start_async(self):
        try:
            await self.drawio_manager.provision()
            await self.drawio_manager.start_server()
            for dio in self.dio_files:
                xml = dio.read_text(encoding="utf-8")
                out = dio.parent / f"{dio.stem}.pdf"
                self.log.warning("Converting %s: %s bytes", dio, len(xml))
                pdf_request = dict(xml=xml.encode("utf-8"))
                pdf = await self.drawio_manager.pdf(pdf_request)
                self.log.warning("Writing %s bytes to %s", len(pdf), out)
                out.write_bytes(pdf.encode("utf-8"))
        finally:
            self.stop()


class DrawioExportApp(BaseApp):
    """ drawio export tools
    """

    name = "drawio-export"
    subcommands = dict(
        provision=(ProvisionApp, ProvisionApp.__doc__.splitlines()[0]),
        pdf=(PDFApp, PDFApp.__doc__.splitlines()[0]),
    )


main = launch_instance = DrawioExportApp.launch_instance

if __name__ == "__main__":  # pragma: no cover
    main()

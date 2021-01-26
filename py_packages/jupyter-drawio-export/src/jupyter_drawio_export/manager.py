"""
the drawio export manager

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
import asyncio
import atexit
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import urllib
from base64 import b64decode, b64encode
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

import lxml.etree as E
from jupyterlab.commands import get_app_dir
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from requests import Session
from requests_cache import CachedSession
from tornado.concurrent import run_on_executor
from traitlets import Bool, Dict, Instance, Int, Unicode, default
from traitlets.config import LoggingConfigurable

from .constants import DRAWIO_APP, PNG_DRAWIO_INFO

VEND = Path(__file__).parent / "vendor" / "draw-image-export2"

DRAWIO_STATIC = Path(get_app_dir()) / DRAWIO_APP

JLPM = shutil.which("jlpm")


class DrawioExportManager(LoggingConfigurable):
    """manager of (currently) another node-based server"""

    drawio_server_url = Unicode().tag(config=True)
    drawio_port = Int().tag(config=True)
    drawing_name = Unicode("drawing.dio.xml").tag(config=True)
    core_params = Dict().tag(config=True)
    drawio_export_workdir = Unicode().tag(config=True)
    pdf_cache = Unicode(allow_none=True).tag(config=True)
    attach_xml = Bool().tag(config=True)
    is_provisioning = Bool(False)
    is_starting = Bool(False)
    _server = Instance(subprocess.Popen, allow_none=True)
    _session = Instance(Session)

    executor = ThreadPoolExecutor(1)

    def initialize(self):
        atexit.register(self.stop_server)

    async def pdf(self, pdf_requests):
        if not self._server:
            await self.start_server()

        for pdf_request in pdf_requests:
            pdf_request["pdf"] = await self._pdf(pdf_request)

        if len(pdf_requests) == 1:
            return pdf_requests[0]["pdf"]

        return await self._merge(pdf_requests)

    def stop_server(self):
        if self._server is not None:
            self.log.warning("shutting down drawio export server")
            self._server.terminate()
            self._server.wait()
            self._server = None

    async def status(self):
        return {
            "has_jlpm": JLPM is not None,
            "is_provisioned": self.is_provisioned,
            "is_provisioning": self.is_provisioning,
            "is_starting": self.is_starting,
            "is_running": self.is_running,
        }

    @property
    def url(self):
        return f"http://localhost:{self.drawio_port}"

    @default("drawio_port")
    def _default_drawio_port(self):
        return self.get_unused_port()

    @default("drawio_server_url")
    def _default_drawio_server_url(self):
        return DRAWIO_STATIC.as_uri()

    @default("_session")
    def _default_session(self):
        if self.pdf_cache is not None:
            return CachedSession(self.pdf_cache, allowable_methods=["POST"])

        return Session()

    @default("core_params")
    def _default_core_params(self):
        return dict(format="pdf", base64="1")

    @default("drawio_export_workdir")
    def _default_drawio_export_workdir(self):
        data_root = Path(sys.prefix) / "share/jupyter"

        if "JUPYTER_DATA_DIR" in os.environ:
            data_root = Path(os.environ["JUPYTER_DATA_DIR"])

        return str(data_root / "drawio_export")

    @default("attach_xml")
    def _default_attach_xml(self):
        return True

    @run_on_executor
    def _pdf(self, pdf_request):
        """TODO: enable more customization... I guess over HTTP headers?
        X-JPYDIO-embed: 1
        """
        data = dict(pdf_request)
        data.update(**self.core_params)
        r = self._session.post(self.url, timeout=None, data=data)

        if r.status_code != 200:
            self.log.error(r.text)

        pdf_text = r.text
        self.log.warning("drawio PDF: %s bytes", len(r.text))

        return pdf_text

    def extract_diagrams(self, pdf_request):
        node = None

        errors = []
        try:
            node = E.fromstring(pdf_request["xml"])
        except Exception as err:
            errors += [err]

        if node is None:
            try:
                img = Image.open(BytesIO(b64decode(pdf_request["xml"].encode("utf-8"))))
                node = E.fromstring(urllib.parse.unquote(img.info[PNG_DRAWIO_INFO]))
            except Exception as err:
                errors += [err]

        if node is None:
            self.log.warning("errors encountered extracting xml %s", errors)
            return

        tag = node.tag

        if tag == "mxfile":
            for diagram in node.xpath("//diagram"):
                yield diagram
        elif tag == "mxGraphModel":
            diagram = E.Element("diagram")
            diagram.append(node)
            yield diagram
        elif tag == "{http://www.w3.org/2000/svg}svg":
            diagrams = E.fromstring(node.attrib["content"]).xpath("//diagram")
            for diagram in diagrams:
                yield diagram

    @run_on_executor
    def _merge(self, pdf_requests):
        tree = E.fromstring("""<mxfile version="13.3.6"></mxfile>""")
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            merger = PdfFileMerger()
            for i, pdf_request in enumerate(pdf_requests):
                self.log.warning("adding page %s", i)
                for diagram in self.extract_diagrams(pdf_request):
                    tree.append(diagram)
                next_pdf = tdp / f"doc-{i}.pdf"
                wrote = next_pdf.write_bytes(
                    b64decode(pdf_request["pdf"].encode("utf-8"))
                )
                if wrote:
                    merger.append(PdfFileReader(str(next_pdf)))
            output_pdf = tdp / "output.pdf"
            final_pdf = tdp / "final.pdf"
            merger.write(str(output_pdf))
            composite_xml = E.tostring(tree).decode("utf-8")
            final = PdfFileWriter()
            final.appendPagesFromReader(PdfFileReader(str(output_pdf), "rb"))
            final.addAttachment("drawing.drawio", composite_xml.encode("utf-8"))
            with final_pdf.open("wb") as fpt:
                final.write(fpt)
            return b64encode(final_pdf.read_bytes()).decode("utf-8")

    def add_files(self, pdf_text, attachments):
        with TemporaryDirectory() as td:
            tdp = Path(td)
            output_pdf = tdp / "output.pdf"
            final_pdf = tdp / "final.pdf"
            output_pdf.write_bytes(b64decode(pdf_text))
            writer = PdfFileWriter()
            writer.appendPagesFromReader(PdfFileReader(str(output_pdf), "rb"))

            for path, content in attachments.items():
                self.log.warning(
                    "adding PDF attachment %s %s %s", len(content), type(content), path
                )
                writer.addAttachment(path, content)

            with final_pdf.open("wb") as fpt:
                writer.write(fpt)

            pdf_text = b64encode(final_pdf.read_bytes()).decode("utf-8")

        self.log.warning("final pdf size %s", len(pdf_text))
        return pdf_text

    async def start_server(self):
        self.is_starting = True
        self.stop_server()

        if not self.is_provisioned:
            await self.provision()

        env = dict(os.environ)
        env.update(
            PORT=str(self.drawio_port),
            DRAWIO_SERVER_URL=self.drawio_server_url,
        )

        self._server = subprocess.Popen(
            [JLPM, "--silent", "start"], cwd=str(self.drawio_export_app), env=env
        )

        response = None
        while response is None:
            self.log.warning("drawio export server starting...")
            await asyncio.sleep(2)

            try:
                response = self._session.get(self.url, timeout=1)
            except Exception:
                pass

        self.log.warning("drawio export server started.")

        self.is_starting = False

    @property
    def is_provisioned(self):
        return self.drawio_export_integrity.exists()

    @property
    def is_running(self):
        return self._server is not None and self._server.returncode is None

    @property
    def drawio_export_app(self):
        return Path(self.drawio_export_workdir) / VEND.name

    @property
    def drawio_export_node_modules(self):
        return self.drawio_export_app / "node_modules"

    @property
    def drawio_export_integrity(self):
        return self.drawio_export_node_modules / ".yarn-integrity"

    @run_on_executor
    def provision(self, force=False):
        self.is_provisioning = True
        if not self.drawio_export_app.exists():
            if not self.drawio_export_app.parent.exists():
                self.drawio_export_app.parent.mkdir(parents=True)
            self.log.warning(
                "initializing drawio export app %s", self.drawio_export_app
            )
            shutil.copytree(VEND, self.drawio_export_app)
        else:
            self.log.warning(
                "using existing drawio export folder %s", self.drawio_export_app
            )

        if not self.drawio_export_node_modules.exists() or force:
            self.log.warning(
                "installing drawio export dependencies %s", self.drawio_export_app
            )
            subprocess.check_call([JLPM, "--silent"], cwd=str(self.drawio_export_app))
        self.is_provisioning = False

    def get_unused_port(self):
        """Get an unused port by trying to listen to any random port.

        Probably could introduce race conditions if inside a tight loop.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", 0))
        sock.listen(1)
        port = sock.getsockname()[1]
        sock.close()
        return port

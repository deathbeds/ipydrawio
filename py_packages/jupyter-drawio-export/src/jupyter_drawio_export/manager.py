import atexit
import base64
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

from jupyter_core.paths import jupyter_data_dir
from jupyterlab.commands import get_app_dir
from requests import Session
from tornado.concurrent import run_on_executor
from traitlets import Bool, Dict, Instance, Int, Unicode, default
from traitlets.config import LoggingConfigurable

VEND = Path(__file__).parent / "vendor" / "draw-image-export2"

DRAWIO_STATIC = Path(get_app_dir()) / (
    "static/node_modules/@deathbeds/jupyterlab-drawio-webpack/drawio/src/main/webapp"
)


class DrawioExportManager(LoggingConfigurable):
    """ manager of (currently) another node-based server
    """

    drawio_server_url = Unicode().tag(config=True)
    drawio_port = Int(8080).tag(config=True)
    drawing_name = Unicode("drawing.dio.xml").tag(config=True)
    core_params = Dict().tag(config=True)
    drawio_export_folder = Unicode().tag(config=True)
    pdf_cache = Unicode(allow_none=True).tag(config=True)
    attach_xml = Bool().tag(config=True)
    _server = Instance(subprocess.Popen, allow_none=True)
    _session = Instance(Session)

    executor = ThreadPoolExecutor(1)

    def initialize(self):
        atexit.register(self._atexit)

    async def pdf(self, pdf_request):
        if not self._server:
            await self.start_server()
        return await self._pdf(pdf_request)

    def _atexit(self):
        self.log.warn("shutting down drawio export server")
        if self._server is not None:
            self._server.terminate()
            self._server.wait()

    @property
    def url(self):
        return f"http://localhost:{self.drawio_port}"

    @default("drawio_server_url")
    def _default_drawio_server_url(self):
        return DRAWIO_STATIC.as_uri()

    @default("pdf_cache")
    def _default_pdf_cache(self):
        return str(Path(self.drawio_export_folder) / ".cache")

    @default("_session")
    def _default_session(self):
        if self.pdf_cache is not None:
            try:
                from requests_cache import CachedSession

                return CachedSession(self.pdf_cache, allowable_methods=["POST"])
            except ImportError:
                pass

        return Session()

    @default("core_params")
    def _default_core_params(self):
        return dict(format="pdf", base64="1")

    @default("drawio_export_folder")
    def _default_drawio_export_folder(self):
        return str(Path(jupyter_data_dir()) / "jupyter_drawio_export")

    @default("attach_xml")
    def _default_attach_xml(self):
        try:
            __import__("PyPDF2")
        except (ImportError, ValueError):
            self.log.warning("install PyPDF2 to enable attaching drawio XML in PDF")
            return False

        return True

    @run_on_executor
    def _pdf(self, pdf_request):
        """ TODO: enable more customization... I guess over HTTP headers?
            X-JPYDIO-embed: 1
        """
        data = dict(pdf_request)
        data.update(**self.core_params)
        r = self._session.post(self.url, timeout=None, data=data)

        if r.status_code != 200:
            self.log.error(r.text)

        pdf_text = r.text
        self.log.warning("drawio PDF: %s bytes", len(r.text))

        if self.attach_xml:
            pdf_text = self.add_files(pdf_text, {self.drawing_name: pdf_request["xml"]})

        return pdf_text

    def add_files(self, pdf_text, attachments):
        try:
            from PyPDF2 import PdfFileReader, PdfFileWriter
        except ImportError:
            self.log.warning("could not import pypdf2, drawio XML will not be attached")
            return pdf_text

        with TemporaryDirectory() as td:
            tdp = Path(td)
            output_pdf = tdp / "output.pdf"
            final_pdf = tdp / "final.pdf"
            output_pdf.write_bytes(base64.b64decode(pdf_text))
            writer = PdfFileWriter()
            writer.appendPagesFromReader(PdfFileReader(str(output_pdf), "rb"))

            for path, content in attachments.items():
                self.log.warning(
                    "adding PDF attachment %s %s %s", len(content), type(content), path
                )
                writer.addAttachment(path, content)

            with final_pdf.open("wb") as fpt:
                writer.write(fpt)

            pdf_text = base64.b64encode(final_pdf.read_bytes()).decode("utf-8")

        self.log.warning("final pdf size %s", len(pdf_text))
        return pdf_text

    async def start_server(self):
        dx_path = Path(self.drawio_export_folder)

        if not dx_path.exists():
            dx_path.mkdir(parents=True)

        dest = dx_path / VEND.name
        if not dest.exists():
            self.log.warn("initializing drawio export folder", dest)
            shutil.copytree(VEND, dest)
        else:
            self.log.warn("using existing drawio export folder", dest)

        if not (dest / "node_modules" / ".yarn-integrity").exists():
            self.log.warn("installing drawio export dependencies", dest)
            subprocess.check_call(["jlpm"], cwd=str(dest))

        env = dict(os.environ)
        env["PORT"] = str(self.drawio_port)
        env["DRAWIO_SERVER_URL"] = self.drawio_server_url

        self._server = subprocess.Popen(["jlpm", "start"], cwd=str(dest), env=env)

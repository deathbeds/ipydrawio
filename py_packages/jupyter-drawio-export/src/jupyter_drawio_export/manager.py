import atexit
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from jupyter_core.paths import jupyter_data_dir
from jupyterlab.commands import get_app_dir
from requests_cache import CachedSession
from tornado.concurrent import run_on_executor
from traitlets import Dict, Instance, Int, Unicode, default
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
    core_params = Dict().tag(config=True)
    drawio_export_folder = Unicode().tag(config=True)
    _server = Instance(subprocess.Popen, allow_none=True)
    _session = Instance(CachedSession)

    executor = ThreadPoolExecutor(1)

    def initialize(self):
        atexit.register(self._atexit)

    def _atexit(self):
        if self._server is not None:
            self._server.terminate()
            self._server.wait()

    @property
    def url(self):
        return f"http://localhost:{self.drawio_port}"

    @default("drawio_server_url")
    def _default_drawio_server_url(self):
        return DRAWIO_STATIC.as_uri()

    @default("_session")
    def _default_session(self):
        return CachedSession(
            str(Path(self.drawio_export_folder) / ".cache"), allowable_methods=["POST"]
        )

    @default("core_params")
    def _default_core_params(self):
        return dict(format="pdf", base64="1")

    @default("drawio_export_folder")
    def _default_drawio_export_folder(self):
        return str(Path(jupyter_data_dir()) / "jupyter_drawio_export")

    @run_on_executor
    def _pdf(self, pdf_request):
        data = dict(pdf_request)
        data.update(**self.core_params)
        r = self._session.post(self.url, timeout=None, data=data)
        if r.status_code != 200:
            self.log.error(r.text)
        return r.text

    async def pdf(self, pdf_request):
        if not self._server:
            await self.start_server()
        return await self._pdf(pdf_request)

    async def start_server(self):
        dx_path = Path(self.drawio_export_folder)

        if not dx_path.exists():
            dx_path.mkdir(parents=True)

        dest = dx_path / VEND.name
        if not dest.exists():
            shutil.copytree(VEND, dest)

        if not (dest / "node_modules" / ".yarn-integrity").exists():
            subprocess.check_call(["jlpm"], cwd=str(dest))

        env = dict(os.environ)
        env = dict(os.environ)
        env["PORT"] = str(self.drawio_port)
        env["DRAWIO_SERVER_URL"] = self.drawio_server_url

        self._server = subprocess.Popen(["jlpm", "start"], cwd=str(dest), env=env)

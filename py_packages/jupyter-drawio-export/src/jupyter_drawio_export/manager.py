import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from jupyter_core.paths import jupyter_data_dir
from tornado.concurrent import run_on_executor
from traitlets import Dict, Instance, Int, Unicode, default
from traitlets.config import LoggingConfigurable

VEND = Path(__file__).parent / "vendor" / "draw-image-export2"


class DrawioExportManager(LoggingConfigurable):
    """ manager of (currently) another node-based server
    """

    drawio_port = Int().tag(config=True)
    core_params = Dict().tag(config=True)
    drawio_export_folder = Unicode().tag(config=True)
    _server = Instance(subprocess.Popen)

    executor = ThreadPoolExecutor(1)

    def initialize(self):
        pass

    @default("core_params")
    def _default_core_params(self):
        return dict(format="pdf", base64="1")

    @default("drawio_export_folder")
    def _default_drawio_export_folder(self):
        return str(Path(jupyter_data_dir) / "jupyter_drawio_export")

    @run_on_executor
    def _pdf(self, pdf_request):
        r = requests.post(
            self.url, timeout=None, data=dict(**pdf_request, **self.core_params)
        )
        if r.status_code != 200:
            self.error = r.text
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

        self._server = subprocess.Popen(
            ["jlpm", "start"],
            cwd=str(dest),
            # env=dict(DRAWIO_SERVER_URL=DRAWIO_SERVER_URL),
        )

import atexit
import os
import socket
import subprocess
import sys

from pathlib import Path

from jupyterlab.commands import get_app_dir

HERE = Path(__file__).parent
APP = HERE.parent / "drawio-export"
DRAWIO_STATIC = Path(get_app_dir()) / (
    "static/node_modules/jupyterlab-drawio/drawio/src/main/webapp"
)

def get_unused_port():
    """ Get an unused port by trying to listen to any random port.
        Probably could introduce race conditions if inside a tight loop.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 0))
    sock.listen(1)
    port = sock.getsockname()[1]
    sock.close()
    return port


def main():
    """ start the drawio-export, and (usually) a local http server to serve the assets

        - drawio-export assumes PORT has been set, or defaults to 8000
    """
    local_files = None

    if not (APP / "node_modules").exists():
        subprocess.check_call(["jlpm"], cwd=str(APP))

    env = dict(os.environ)

    if env.get("DRAWIO_SERVER_URL") is None:
        port = get_unused_port()
        local_files = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
            cwd=str(DRAWIO_STATIC)
        )
        env["DRAWIO_SERVER_URL"] = f"http://localhost:{port}"

    exporter = subprocess.Popen(["jlpm", "devstart"], cwd=str(APP), env=env)

    def stop():
        exporter.terminate(kill=True)
        if local_files is not None:
            local_files.terminate(kill=True)
        exporter.wait()

    atexit.register(stop)

    try:
        return exporter.wait()
    finally:
        stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())

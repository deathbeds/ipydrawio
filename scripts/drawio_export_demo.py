import subprocess
import os
import sys
from pathlib import Path
from jupyterlab.commands import get_app_dir
import socket
import atexit


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
    """
    local_files = None

    if not (APP / "node_modules").exists():
        print("Installing drawio-export deps in:\n\t", str(APP), flush=True)
        subprocess.check_call(["jlpm"], cwd=str(APP))

    env = dict(os.environ)

    if env.get("PORT") is None:
        # drawio-export assumes PORT has been set, and defaults to 8000, but explicit is...
        env["PORT"] = "8000"

    if env.get("DRAWIO_SERVER_URL") is None:
        # assuming we're running in a jupyterlab-drawio setup
        port = get_unused_port()
        env["DRAWIO_SERVER_URL"] = f"http://localhost:{port}"
        print("Starting local drawio asset server for", str(DRAWIO_STATIC), "\n\t", env["DRAWIO_SERVER_URL"], flush=True)
        local_files = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
            cwd=str(DRAWIO_STATIC)
        )

    exporter = subprocess.Popen(["jlpm", "start"], cwd=str(APP), env=env)
    print("Starting drawio-export server\n\t", f"""http://localhost:{env["PORT"]}""", flush=True)

    def stop():
        exporter.terminate()
        if local_files is not None:
            local_files.terminate()
            local_files.wait()
        exporter.wait()

    atexit.register(stop)

    try:
        return exporter.wait()
    finally:
        stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())

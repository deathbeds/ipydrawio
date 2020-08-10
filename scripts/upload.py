""" release on pypi and npm
"""
import json
import os
from subprocess import check_call

from . import project as P

FOR_REAL = json.loads(os.environ.get("FOR_REAL", "0"))

PYPI_REGISTRY = (
    "https://pypi.org/legacy/" if FOR_REAL else "https://test.pypi.org/legacy/"
)


def upload():
    """ upload releases
    """
    if not FOR_REAL:
        print("Not uploading FOR_REAL: set the environment variable for a real release")

    for pkg, sdist in P.PY_SDIST.items():
        args = ["twine", "upload", "--repository-url", PYPI_REGISTRY, "dist/*"]
        cwd = str(sdist.parent.parent)
        print(">>>", " ".join(args), "\n in", cwd, flush=True)
        if FOR_REAL:
            check_call(args, cwd=cwd)

    for pkg, tgz in P.JS_TARBALL.items():
        args = ["jlpm", "upload"]
        cwd = tgz.parent
        print(">>>", " ".join(args), "\n in", cwd, flush=True)
        if FOR_REAL:
            check_call(args, cwd=cwd)


if __name__ == "__main__":
    upload()

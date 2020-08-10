""" create release tags
"""
import json
import os
from subprocess import check_call

from . import project as P

FOR_REAL = json.loads(os.environ.get("FOR_REAL", "0"))


def tag():
    """ upload releases
    """
    if not FOR_REAL:
        print("Not uploading FOR_REAL: set the environment variable for a real release")

    for pkg, version in P.PY_VERSION.items():
        args = ["git", "tag", f"release/{pkg}/{version}"]
        print(">>>", " ".join(args), flush=True)
        if FOR_REAL:
            check_call(args)

    for pkg, data in P.JS_PKG_DATA.items():
        if pkg.startswith("_"):
            continue
        args = ["git", "tag", f"""release/{pkg}/{data["version"]}"""]
        print(">>>", " ".join(args), flush=True)
        if FOR_REAL:
            check_call(args)


if __name__ == "__main__":
    tag()

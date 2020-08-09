import sys
import tarfile
from pathlib import Path

import pytest

if True:
    sys.path.append(str(Path(__file__).parent.parent))
    from scripts import project as P


def test_drawio_versions():
    dv = (P.JDW / "drawio/VERSION").read_text(encoding="utf-8")
    pdv = P.JS_PKG_DATA[P.JDW.name]["version"]
    assert pdv.startswith(dv), "drawio version out of sync"


@pytest.mark.parametrize("tarball", [*P.JS_TARBALL.values()])
def test_tarball(tarball):
    with tarfile.open(str(tarball), "w") as tar:
        all_names = list(tar.getnames())
        licenses = [p for p in all_names if "LICENSE.txt" in p]
        assert licenses
        readmes = [p for p in all_names if "README.md" in p]
        assert readmes

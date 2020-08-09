import sys
import tarfile
from pathlib import Path

import pytest

if True:
    sys.path.append(str(Path(__file__).parent.parent))
    from scripts import project as P


@pytest.fixture
def the_changelog():
    return (P.ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "pkg,version",
    [
        *[[k, v] for k, v in P.PY_VERSION.items()],
        *[
            [v["name"], v["version"]]
            for k, v in P.JS_PKG_DATA.items()
            if not k.startswith("_")
        ],
    ],
)
def test_changelog(pkg, version, the_changelog):
    version_string = f"## {pkg} {version}"
    assert version_string in the_changelog, version_string


def test_drawio_versions():
    dv = (P.JDW / "drawio/VERSION").read_text(encoding="utf-8")
    pdv = P.JS_PKG_DATA[P.JDW.name]["version"]
    assert pdv.startswith(dv), "drawio version out of sync"


@pytest.mark.parametrize("key,tarball", [*P.JS_TARBALL.items(), *P.PY_SDIST.items()])
def test_tarball(key, tarball):
    with tarfile.open(str(tarball), "r") as tar:
        all_names = list(tar.getnames())
        licenses = [p for p in all_names if "LICENSE.txt" in p]
        assert licenses, f"{key} doesn't have LICENSE"
        readmes = [p for p in all_names if "README.md" in p]
        assert readmes, f"{key} doesn't have README"

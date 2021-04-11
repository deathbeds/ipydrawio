"""ipydrawio repo integrity tests"""

# Copyright 2021 ipydrawio contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    """are the current versions referenced in the CHANGELOG?"""
    version_string = f"### {pkg} {version}"
    assert version_string in the_changelog, version_string


def test_drawio_versions():
    """is the drawio version up-to-date with the submodule?"""
    dv = (P.IPDW / "drawio/VERSION").read_text(encoding="utf-8")
    pdv = P.JS_PKG_DATA[P.IPDW.name]["version"]
    assert pdv.startswith(dv), "drawio version out of sync"


@pytest.mark.parametrize("path", P.ALL_HEADERS)
def test_headers(path):
    text = path.read_text(encoding="utf-8")
    assert (
        "Copyright 2021 ipydrawio contributors" in text
    ), f"{path.relative_to(P.ROOT)} needs copyright header"
    assert (
        'Licensed under the Apache License, Version 2.0 (the "License");' in text
    ), f"{path.relative_to(P.ROOT)} needs license header"


@pytest.mark.parametrize("key,tarball", [*P.JS_TARBALL.items(), *P.PY_SDIST.items()])
def test_tarball(key, tarball):
    with tarfile.open(str(tarball), "r") as tar:
        all_names = list(tar.getnames())
        licenses = [p for p in all_names if "LICENSE.txt" in p]
        assert licenses, f"{key} doesn't have LICENSE"
        readmes = [p for p in all_names if "README.md" in p]
        assert readmes, f"{key} doesn't have README"

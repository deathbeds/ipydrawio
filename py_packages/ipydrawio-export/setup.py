"""dynamic setup information for setuptools, also see package.json and setup.cfg"""

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

import json
from pathlib import Path

HERE = Path(__file__).parent
EXT = HERE / "src/ipydrawio_export/ext"

PDF = EXT / "ipdpdf"

SHARE = "share/jupyter/labextensions"

__js__ = json.loads((PDF / "package.json").read_text(encoding="utf-8"))

FILES = []

for package_json in EXT.glob("*/package.json"):
    pkg = json.loads(package_json.read_text(encoding="utf-8"))

    FILES += [(f"""{SHARE}/{pkg["name"]}""", ["src/ipydrawio_export/etc/install.json"])]

    for path in package_json.parent.rglob("*"):
        if path.is_dir():
            continue
        parent = path.parent.relative_to(package_json.parent).as_posix()
        FILES += [
            (
                f"""{SHARE}/{pkg["name"]}/{parent}""",
                [str(path.relative_to(HERE).as_posix())],
            )
        ]

for app in ["server", "notebook"]:
    FILES += [
        (
            f"etc/jupyter/jupyter_{app}_config.d",
            [f"src/ipydrawio_export/etc/jupyter_{app}_config.d/ipydrawio-export.json"],
        )
    ]

if __name__ == "__main__":
    import setuptools

    setuptools.setup(version=__js__["version"], data_files=FILES)

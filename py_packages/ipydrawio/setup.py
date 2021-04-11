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

import re
from pathlib import Path
import json

HERE = Path(__file__).parent


EXT = HERE / "src/ipydrawio/labextensions"
CORE = EXT / "@deathbeds/ipydrawio"

SHARE = "share/jupyter/labextensions"

__js__ = json.loads((CORE / "package.json").read_text(encoding="utf-8"))

EXT_FILES = {}

for ext_path in [EXT] + [d for d in EXT.rglob("*") if d.is_dir()]:
    if ext_path == EXT:
        target = str(SHARE)
    else:
        target = f"{SHARE}/{ext_path.relative_to(EXT)}"
    EXT_FILES[target] = [
        str(p.relative_to(HERE).as_posix())
        for p in ext_path.glob("*")
        if not p.is_dir()
    ]

ALL_FILES = sum(EXT_FILES.values(), [])

EXT_FILES[str(SHARE)] += ["install.json"]


if __name__ == "__main__":
    import setuptools

    setuptools.setup(
        version=__js__["version"],
        data_files=[
            *[(k, v) for k, v in EXT_FILES.items()],
        ],
    )

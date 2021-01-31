"""
Copyright 2021 ipydrawio contributors
Copyright 2020 jupyterlab-drawio contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
EXT = HERE / "src/ipydrawio_export/labextensions"
VERSION = HERE / "src/ipydrawio_export/_version.py"

EXT_FILES = {}
SHARE = "share/jupyter/labextensions"

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

for app  in ["server", "notebook"]:
    EXT_FILES[f"etc/jupyter/jupyter_{app}_config.d"] = [
        f"src/ipydrawio_export/etc/jupyter_{app}_config.d/ipydrawio-export.json"
    ]

if __name__ == "__main__":
    import setuptools

    setuptools.setup(
        version=re.findall(
            r"""__version__\s*=\s*"([^"]+)""",
            VERSION.read_text(encoding="utf-8")
        )[0],
        data_files=[
            *[(k, v) for k, v in EXT_FILES.items()],
        ],
    )

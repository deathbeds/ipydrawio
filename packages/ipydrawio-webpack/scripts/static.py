"""update the vendored drawio"""

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

from fnmatch import fnmatch
from pathlib import Path
from pprint import pprint

HERE = Path(__file__).parent
ROOT = HERE.parent.resolve()
DRAWIO = ROOT / "drawio"
IGNORE = ROOT / ".npmignore"
IGNORED = {
    glob.strip(): 0
    for glob in IGNORE.read_text().strip().splitlines()
    if glob.startswith("drawio/")
}
STATIC = ROOT / "lib" / "_static.js"
HEADER = """
/**
    All files that should be copied to the labextension folder, available as:

    This file generated from https://github.com/jgraph/drawio
*/
"""
TMPL = """
import '!!file-loader?name=[path][name].[ext]&context=.!../drawio{}';
"""


def is_ignored(path):
    for ignore in IGNORED:
        if fnmatch(str(path.relative_to(ROOT)), ignore):
            IGNORED[ignore] += 1
            return True
    return False


def update_static():
    print("ignoring\n", "\n".join(IGNORED))
    lines = []

    for path in sorted(DRAWIO.rglob("*")):
        if path.is_dir():
            continue
        if is_ignored(path):
            continue
        lines += [
            TMPL.format(
                str(path.as_posix()).replace(str(DRAWIO.as_posix()), "")
            ).strip()
        ]

    assert lines

    STATIC.write_text("\n".join([HEADER, *lines]))
    print(f"wrote {len(lines)} lines")
    pprint(IGNORED)


if __name__ == "__main__":
    update_static()

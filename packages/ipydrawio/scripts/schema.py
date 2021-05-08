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

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
PKG = HERE.parent
ROOT = PKG.parent.parent

IN_FILE = PKG / "schema/plugin.json"
OUT_FILE = PKG / "src/_schema.d.ts"

HEADER = """/*
  Copyright 2021 ipydrawio contributors

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/"""


def patch():
    out = subprocess.check_output(["jlpm", "--silent", "json2ts", IN_FILE])
    OUT_FILE.write_text("\n".join([HEADER, out.decode("utf-8")]), encoding="utf-8")
    subprocess.check_call(
        ["jlpm", "prettier", "--write", OUT_FILE.resolve()], cwd=str(ROOT)
    )
    return 0


if __name__ == "__main__":
    sys.exit(patch())

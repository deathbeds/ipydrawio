"""test basic CLI functionality"""

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

import shutil

import pytest

from .. import __version__


def test_cli_version(script_runner):
    ret = script_runner.run("jupyter", "ipydrawio", "--version")
    assert ret.success
    assert __version__ in ret.stdout


@pytest.mark.parametrize(
    "pretty,indent,tabs,mx_attrs",
    [
        [True, None, None, None],
        [False, None, None, None],
        [True, 4, None, ["host"]],
        [True, 1, True, ["agent"]],
    ],
)
def test_cli_clean(
    script_runner, tmp_path, an_empty_dio_file, pretty, indent, tabs, mx_attrs
):
    dest = tmp_path / an_empty_dio_file.name
    shutil.copy2(an_empty_dio_file, dest)

    before = dest.read_text(encoding="utf-8").strip()

    args = "jupyter", "ipydrawio", "clean"

    if not pretty:
        args = [*args, "--no-pretty"]

    if indent is not None:
        args = [*args, "--indent", f"{indent}"]

    if tabs:
        args = [*args, "--tabs"]

    if mx_attrs:
        args = [*args, "--mx-attrs", str(mx_attrs)]

    args = [*args, str(dest)]

    ret = script_runner.run(*args)

    assert ret.success

    cleaned = dest.read_text(encoding="utf-8").strip()

    assert cleaned != before

    for attr in "host", "agent", "etag", "modified":
        if mx_attrs is None or attr in mx_attrs:
            assert f"{attr}=" not in cleaned, f"should _not_ have contained {attr}"
        else:
            assert f"{attr}=" in cleaned, f"should have contained {attr}"

    if pretty:
        assert len(cleaned.splitlines()) > 1, "should have been multiple lines"
    else:
        assert len(cleaned.splitlines()) == 1, "should have been one line"

    ret2 = script_runner.run(*args)

    assert ret2.success

    cleaned_again = dest.read_text(encoding="utf-8").strip()

    assert cleaned == cleaned_again, "should have been the same"

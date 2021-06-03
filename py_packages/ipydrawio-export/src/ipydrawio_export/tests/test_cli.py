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

import platform

import pytest

from .. import __version__


@pytest.mark.skipif(platform.system() == "Windows", reason="no capture on win")
def test_cli_version(script_runner):
    ret = script_runner.run("jupyter", "ipydrawio-export", "--version")
    assert ret.success
    assert __version__ in ret.stdout


def test_cli_workdir(script_runner):
    ret = script_runner.run("jupyter", "ipydrawio-export", "provision", "--workdir")
    assert ret.success

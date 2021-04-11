"""ipydrawio-export test environment"""

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
from pathlib import Path

import pytest

from ..app import PDFApp

FIXTURES = Path(__file__).parent / "fixtures"
FIXTURE_FILES = sorted([f for f in FIXTURES.glob("*") if not f.is_dir()])

pytest_plugins = ["jupyter_server.pytest_plugin"]


@pytest.fixture(params=FIXTURE_FILES)
def any_diagram(request, tmp_path):
    dest = tmp_path / request.param.name
    shutil.copy2(request.param, dest)
    return dest


@pytest.fixture
def export_app(tmp_path):
    app = PDFApp()
    yield app
    app.drawio_manager.stop_server()


@pytest.fixture
def empty_dio(tmp_path):
    src = FIXTURES / "empty.dio"
    dest = tmp_path / src.name
    shutil.copy2(src, dest)
    return dest


@pytest.fixture
def svg(tmp_path):
    src = FIXTURES / "a.svg"
    dest = tmp_path / src.name
    shutil.copy2(src, dest)
    return dest


@pytest.fixture
def png(tmp_path):
    src = FIXTURES / "a.svg"
    dest = tmp_path / src.name
    shutil.copy2(src, dest)
    return dest


@pytest.fixture
def ipynb(tmp_path):
    src = FIXTURES / "empty.ipynb"
    dest = tmp_path / src.name
    shutil.copy2(src, dest)
    return dest

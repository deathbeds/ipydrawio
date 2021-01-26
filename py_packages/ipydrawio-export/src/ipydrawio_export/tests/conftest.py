import shutil
from pathlib import Path

import pytest

from ..app import PDFApp, ProvisionApp

FIXTURES = Path(__file__).parent / "fixtures"
FIXTURE_FILES = sorted([f for f in FIXTURES.glob("*") if not f.is_dir()])


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
def provision_app(tmp_path):
    app = ProvisionApp()
    app.drawio_manager.drawio_export_workdir = str(tmp_path)
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

import shutil
from pathlib import Path

import pytest
from PyPDF2 import PdfFileReader

from ..app import PDFApp

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def empty_dio(tmp_path):
    src = FIXTURES / "empty.dio"
    dest = tmp_path / src.name
    shutil.copy2(src, dest)
    return dest


@pytest.fixture
def export_app(tmp_path):
    app = PDFApp()
    app.drawio_manager.drawio_export_workdir = str(tmp_path)
    yield app
    app.drawio_manager.stop_server()


def test_export(export_app, empty_dio, tmp_path):
    export_app.dio_files = [empty_dio]
    export_app.start()
    out = tmp_path / f"{empty_dio.stem}.pdf"
    assert out.exists()
    reader = PdfFileReader(str(out), "rb")
    assert reader.getNumPages() == 1

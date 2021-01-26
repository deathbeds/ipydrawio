from PyPDF2 import PdfFileReader


def test_export_empty(export_app, any_diagram, tmp_path):
    export_app.dio_files = [any_diagram]
    export_app.start()
    out = tmp_path / f"{any_diagram.stem}.pdf"
    reader = PdfFileReader(str(out), "rb")
    assert reader.getNumPages() == 1


def test_export_merged(export_app, empty_dio, svg, png, ipynb, tmp_path):
    export_app.dio_files = [empty_dio, svg, png, ipynb]
    export_app.start()
    out = tmp_path / f"{empty_dio.stem}.pdf"
    reader = PdfFileReader(str(out), "rb")
    assert reader.getNumPages() == 4

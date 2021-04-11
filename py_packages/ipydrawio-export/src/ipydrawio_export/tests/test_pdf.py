"""ipydrawio-export pdf tests"""

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

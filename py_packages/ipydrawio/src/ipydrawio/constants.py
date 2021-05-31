"""constants for ipydrawio"""

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


A_SHORT_DRAWIO = """<mxfile version="14.6.10">
<diagram id="x" name="Page-1">
  <mxGraphModel dx="1450" dy="467" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
  </root>
  </mxGraphModel>
</diagram>
</mxfile>
"""

DEFAULT_PAGE_FORMAT = {"x": 0, "y": 0, "width": 850, "height": 1100}

DEFAULT_DRAWIO_CONFIG = {
    "compressXml": False,
    "showStartScreen": False,
    "override": True,
}

# key set in notebook#/metadata/
IPYNB_METADATA = "@deathbeds/ipydrawio"

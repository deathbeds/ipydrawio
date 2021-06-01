"""utilities for ipydrawio"""

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

from pathlib import Path

import lxml.etree as ET

# attributes to clean from the mxfile
MX_CLEAN_ATTRS = ["host", "modified", "agent", "etag"]
MX_PRESERVE_ENTITIES = dict(ATTR_NEWLINE="&#10;")


def clean_drawio_file(
    path: Path, pretty=True, indent=2, tabs=False, mx_attrs=MX_CLEAN_ATTRS
):
    """strip headers and identifying information from drawio files"""
    in_xml = path.read_text(encoding="utf-8")
    out_xml = clean_drawio_xml(in_xml, pretty, indent, tabs, mx_attrs)
    path.write_text(out_xml, encoding="utf-8")


def clean_drawio_xml(
    in_xml: str, pretty=True, indent=2, tabs=False, mx_attrs=MX_CLEAN_ATTRS
):
    if pretty:
        # inject placeholders
        for name, entity in MX_PRESERVE_ENTITIES.items():
            in_xml = in_xml.replace(entity, f"__IPYDRAWIO__{name}")

    mx = ET.fromstring(in_xml)

    for key in mx_attrs:
        if key in mx.attrib:
            del mx.attrib[key]

    if pretty:
        ET.indent(mx, space=indent * ("\t" if tabs else " "))
        out_xml = ET.tostring(mx, pretty_print=True, encoding=str)

        # revert placeholders
        for name, entity in MX_PRESERVE_ENTITIES.items():
            pretty = out_xml.replace(f"__IPYDRAWIO__{name}", entity)
    else:
        out_xml = ET.tostring(mx, encoding=str)
    return out_xml

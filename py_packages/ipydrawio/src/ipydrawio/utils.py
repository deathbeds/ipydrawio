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

from .constants import MX_FILE_TAG, MX_GRAPH_TAG, SVG_NS_TAG

# attributes to clean from the mxfile
MX_CLEAN_ATTRS = ["host", "modified", "agent", "etag"]
MX_PRESERVE_ENTITIES = dict(ATTR_NEWLINE="&#10;")


def clean_drawio_file(
    path: Path, pretty=True, indent=2, tabs=False, mx_attrs=MX_CLEAN_ATTRS
):
    """strip headers and identifying information from drawio files"""
    print(path)
    in_xml = path.read_text(encoding="utf-8")
    out_xml = clean_drawio_xml(in_xml, pretty, indent, tabs, mx_attrs)
    if out_xml is not None:
        path.write_text(out_xml, encoding="utf-8")
    else:
        print("... No Change")


def clean_drawio_xml(
    in_xml: str, pretty=True, indent=2, tabs=False, mx_attrs=MX_CLEAN_ATTRS
) -> str:
    if pretty and not in_xml.strip().startswith("<svg"):
        in_xml = inject_entity_placeholders(in_xml)

    root = ET.fromstring(in_xml)

    if root.tag == MX_GRAPH_TAG:
        return None
    elif root.tag == MX_FILE_TAG:
        mx = root
    elif root.tag == SVG_NS_TAG:
        content = root.attrib["content"]
        if pretty:
            content = inject_entity_placeholders(content)
        mx = ET.fromstring(content)

    for key in mx_attrs:
        if key in mx.attrib:
            del mx.attrib[key]

    if pretty:
        ET.indent(mx, space=indent * ("\t" if tabs else " "))
        out_xml = ET.tostring(mx, pretty_print=True, encoding=str)
        out_xml = restore_entity_placeholders(out_xml)
    else:
        out_xml = ET.tostring(mx, encoding=str)

    if root.tag == SVG_NS_TAG:
        root.attrib["content"] = out_xml
        if pretty:
            ET.indent(root, space=indent * ("\t" if tabs else " "))
            out_xml = ET.tostring(root, pretty_print=True, encoding=str)

    if in_xml == out_xml:
        return None
    return out_xml


def inject_entity_placeholders(in_xml: str) -> str:
    for name, entity in MX_PRESERVE_ENTITIES.items():
        in_xml = in_xml.replace(entity, f"__IPYDRAWIO__{name}")
    return in_xml


def restore_entity_placeholders(out_xml: str) -> str:
    for name, entity in MX_PRESERVE_ENTITIES.items():
        out_xml = out_xml.replace(f"__IPYDRAWIO__{name}", entity)

    return out_xml

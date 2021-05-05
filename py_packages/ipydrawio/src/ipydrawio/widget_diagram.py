""" jupyter widgets for drawio"""

# Copyright 2021 ipydrawio contributors
# Copyright 2020 jupyterlab-drawio contributors
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

import ipywidgets as W
import traitlets as T

from ._version import __js__
from .constants import A_SHORT_DRAWIO, DEFAULT_DRAWIO_CONFIG, DEFAULT_PAGE_FORMAT

module_name = __js__["name"]
module_version = "^{version}".format(**__js__)


class DiagramBase(W.Widget):
    """Module metadata for SVG"""

    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    _view_module = T.Unicode(module_name).tag(sync=True)
    _view_module_version = T.Unicode(module_version).tag(sync=True)


class XML(DiagramBase, W.Widget):
    """A Drawio XML-native Document"""

    value = T.Unicode().tag(sync=True)
    _model_name = T.Unicode("XMLModel").tag(sync=True)
    _view_name = T.Unicode("XMLView").tag(sync=True)

    @T.default("value")
    def _default_value(self):
        return A_SHORT_DRAWIO


class Diagram(DiagramBase, W.Box):
    """A Drawio Diagram"""

    _model_name = T.Unicode("DiagramModel").tag(sync=True)
    _view_name = T.Unicode("DiagramView").tag(sync=True)

    source = T.Instance(XML, help="a drawio xml document").tag(
        sync=True, **W.widget_serialization
    )

    scroll_x = T.Float(help="the current viewport scroll x position").tag(sync=True)
    scroll_y = T.Float(help="the current viewport scroll y position").tag(sync=True)
    zoom = T.Float(help="the current zoom level").tag(sync=True)
    page_ids = W.trait_types.TypedTuple(T.Unicode(), help="known page ids").tag(
        sync=True
    )
    current_page = T.Int(0, min=0, help="the current, 0-based, page index").tag(
        sync=True
    )
    page_format = T.Dict(
        help=(
            "the physical size of the diagram media in milli-inches (or something): "
            "x, y, width, height"
        )
    ).tag(sync=True)
    grid_enabled = T.Bool(
        True, help="show on-screen grid behind shapes (above background)"
    ).tag(sync=True)
    grid_color = T.Unicode("#66666666").tag(sync=True)
    grid_size = T.Float(10, min=0.01).tag(sync=True)
    selected_cells = W.trait_types.TypedTuple(T.Unicode()).tag(sync=True)
    # these are important, but advanced
    url_params = T.Dict(help="drawio URL params").tag(sync=True)
    config = T.Dict(help="drawio JSON Configuration").tag(sync=True)

    @T.default("source")
    def _default_source(self):
        return XML()

    @T.default("url_params")
    def _default_url_params(self):
        from .schema import get_schema

        return get_schema()["properties"]["drawioUrlParams"]["default"]

    @T.default("config")
    def _default_config(self):
        return {**DEFAULT_DRAWIO_CONFIG}

    @T.default("page_format")
    def _default_page_format(self):
        return {**DEFAULT_PAGE_FORMAT}

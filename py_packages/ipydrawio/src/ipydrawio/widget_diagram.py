import ipywidgets as W
import traitlets as T

module_name = "@deathbeds/ipydrawio"
module_version = "^1.0.0"

A_SHORT_DRAWIO = """<mxfile version="13.3.6">
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

DEFAULT_URL_PARAMS = {
    "gapi": 0,
    "gl": 0,
    "noExitBtn": 1,
    "noSaveBtn": 1,
    "od": 0,
    "stealth": 1,
    "tr": 0,
    "ui": "min",
    "format": 0,
    "p": "ex;tips;svgdata;sql;anim;trees;replay;anon;flow;webcola;tags",
}

DEFAULT_DRAWIO_CONFIG = {
    "compressXml": False,
    "showStartScreen": False,
    "override": True,
}


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
        return {**DEFAULT_URL_PARAMS}

    @T.default("config")
    def _default_config(self):
        return {**DEFAULT_DRAWIO_CONFIG}

    @T.default("page_format")
    def _default_page_format(self):
        return {**DEFAULT_PAGE_FORMAT}

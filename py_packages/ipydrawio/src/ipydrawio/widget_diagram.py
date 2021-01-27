import ipywidgets as W
import traitlets as T

module_name = "@deathbeds/ipydrawio"
module_version = "^1.0.0-alpha0"

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


DEFAULT_URL_PARAMS = {
    "gapi": 0,
    "gl": 0,
    "noExitBtn": 1,
    "noSaveBtn": 1,
    "od": 0,
    "stealth": 1,
    "tr": 0,
    "ui": "min",
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


class Diagram(DiagramBase, W.Box):
    """A Drawio Diagram"""

    _model_name = T.Unicode("DiagramModel").tag(sync=True)
    _view_name = T.Unicode("DiagramView").tag(sync=True)

    value = T.Unicode(A_SHORT_DRAWIO, help="the drawio XML").tag(sync=True)
    scroll_x = T.Float(help="the current viewport scroll x position").tag(sync=True)
    scroll_y = T.Float(help="the current viewport scroll y position").tag(sync=True)
    zoom = T.Float(help="the current zoom level").tag(sync=True)
    url_params = T.Dict().tag(sync=True)
    config = T.Dict().tag(sync=True)

    @T.default("url_params")
    def _default_url_params(self):
        return DEFAULT_URL_PARAMS

    @T.default("config")
    def _default_config(self):
        return DEFAULT_DRAWIO_CONFIG

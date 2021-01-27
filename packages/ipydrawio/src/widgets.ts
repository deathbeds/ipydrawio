import { BoxModel, BoxView } from '@jupyter-widgets/controls';
import { Diagram } from './editor';
import { DRAWIO_URL } from '@deathbeds/ipydrawio-webpack';
// import { XML_NATIVE } from '@deathbeds/ipydrawio/lib/io';
import { DEBUG, IDiagramManager, NS, VERSION } from './tokens';

import '../style/widget.css';

const A_SHORT_DRAWIO = `<mxfile version="13.3.6">
<diagram id="x" name="Page-1">
    <mxGraphModel dx="1450" dy="467" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
    <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
    </root>
    </mxGraphModel>
</diagram>
</mxfile>
`;

const DEFAULT_URL_PARAMS = {
  gapi: 0,
  gl: 0,
  noExitBtn: 1,
  noSaveBtn: 1,
  od: 0,
  stealth: 1,
  tr: 0,
  ui: 'min',
  p: 'ex;tips;svgdata;sql;anim;trees;replay;anon;flow;webcola;tags',
};

const DEFAULT_DRAWIO_CONFIG = {
  compressXml: false,
  showStartScreen: false,
  override: true,
};

export class DiagramModel extends BoxModel {
  static model_name = 'DiagramModel';
  static model_module = NS;
  static model_module_version = VERSION;

  static view_name = 'DiagramView';
  static view_module = NS;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: DiagramModel.model_name,
      _model_module: NS,
      _model_module_version: VERSION,
      _view_name: DiagramModel.view_name,
      _view_module: NS,
      _view_module_version: VERSION,
      value: A_SHORT_DRAWIO,
      scroll_x: 0.0,
      scroll_y: 0.0,
      zoom: 1.0,
      url_params: DEFAULT_URL_PARAMS,
      config: DEFAULT_DRAWIO_CONFIG,
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
  }
}

export class DiagramView extends BoxView {
  static diagrmManager: IDiagramManager;
  model: DiagramModel;

  protected diagram: Diagram;

  initialize(parameters: any) {
    super.initialize(parameters);
  }

  render() {
    super.render();
    this.pWidget.addClass('jp-IPyDiagram');
    const init = setInterval(() => {
      if (!this.pWidget.isVisible) {
        return;
      }
      clearInterval(init);
      this.diagram = this.initDiagram();
      this.pWidget.addWidget(this.diagram);
      this.model.on('value:change', () => this.diagram.onContentChanged());
      this.diagram.onAfterShow();
      this.diagram.onContentChanged();
    }, 100);
  }

  initDiagram() {
    DEBUG && console.warn('creating diagram widget');
    const format = DiagramView.diagrmManager.formatForModel({
      path: 'widget.dio',
    });
    this.diagram = new Diagram({
      adapter: {
        // this probably is evented
        // format: () => XML_NATIVE,
        saveNeedsExport: () => false,
        drawioUrl: () => DRAWIO_URL,
        drawioConfig: () => this.model.get('config'),
        urlParams: () => this.model.get('url_params'),
        format: () => format,
        toXML: () => this.model.get('value'),
        fromXML: (xml) => {
          DEBUG && console.warn('fromXML', xml, 'was', this.model.get('value'));
          this.model.set('value', xml);
          this.touch();
        },
      },
    });
    return this.diagram;
  }
}

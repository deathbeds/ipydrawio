import { Throttler } from '@lumino/polling';
import { JSONExt } from '@lumino/coreutils';

import {
  unpack_models as deserialize,
  WidgetModel,
  WidgetView,
} from '@jupyter-widgets/base';
import { BoxModel, BoxView } from '@jupyter-widgets/controls';

import { DRAWIO_URL } from '@deathbeds/ipydrawio-webpack';

import { Diagram } from './editor';

import {
  DEBUG,
  IDiagramManager,
  IMXCell,
  IMXEvent,
  IMXEventSource,
  MX_APP_MODEL_EVENTS,
  MX_EDITOR_EVENTS,
  MX_GRAPH_EVENTS,
  MX_GRAPH_MODEL_EVENTS,
  MX_GRAPH_PAN_EVENTS,
  MX_GRAPH_SELECT_EVENTS,
  MX_GRAPH_VIEW_EVENTS,
  NS,
  VERSION,
} from './tokens';

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
  format: 0,
  p: 'ex;tips;svgdata;sql;anim;trees;replay;anon;flow;webcola;tags',
};

const DEFAULT_DRAWIO_CONFIG = {
  compressXml: false,
  showStartScreen: false,
  override: true,
};

export class XMLModel extends WidgetModel {
  static model_name = 'XMLModel';
  static model_module = NS;
  static model_module_version = VERSION;

  static view_name = 'XMLView';
  static view_module = NS;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: XMLModel.model_name,
      _model_module: NS,
      _model_module_version: VERSION,
      _view_name: XMLModel.view_name,
      _view_module: NS,
      _view_module_version: VERSION,
      value: A_SHORT_DRAWIO,
    };
  }
}

export class XMLView extends WidgetView {
  model: XMLModel;
}

export class DiagramModel extends BoxModel {
  static model_name = 'DiagramModel';
  static model_module = NS;
  static model_module_version = VERSION;

  static view_name = 'DiagramView';
  static view_module = NS;
  static view_module_version = VERSION;

  static serializers = {
    ...BoxModel.serializers,
    source: { deserialize },
  };

  defaults() {
    return {
      ...super.defaults(),
      _model_name: DiagramModel.model_name,
      _model_module: NS,
      _model_module_version: VERSION,
      _view_name: DiagramModel.view_name,
      _view_module: NS,
      _view_module_version: VERSION,
      scroll_x: 0.0,
      scroll_y: 0.0,
      zoom: 1.0,
      page_ids: [],
      selected_page: 0,
      selected_cells: [],
      grid_enabled: true,
      grid_color: '#66666666',
      grid_size: 10,
      url_params: DEFAULT_URL_PARAMS,
      config: DEFAULT_DRAWIO_CONFIG,
      page_format: { x: 0, y: 0, width: 850, height: 1100 },
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
      this.initDiagram();
      this.pWidget.addWidget(this.diagram);
      this.diagram.onContentChanged();
      this.diagram.onAfterShow();
      this.model.on('change:source', this.onModelSourceChange, this);
      this.onModelSourceChange();
    }, 100);
  }

  onModelSourceChange() {
    const oldSource = (this.model.changed as any).source as XMLModel;
    if (oldSource != null) {
      oldSource.off('change:value', this.onSourceValue, this);
    }
    const source = this.model.get('source');
    if (source != null) {
      source.on('change:value', this.onSourceValue, this);
    }
  }

  onSourceValue() {
    DEBUG && console.warn('change:value');
    this.diagram.onContentChanged();
  }

  initDiagram() {
    DEBUG && console.warn('creating diagram widget');
    // TODO: consider hoisting this to the source
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
        toXML: () => this.xml(),
        fromXML: (xml) => {
          if ((this.xml() || '').trim() === (xml || '').trim()) {
            return;
          }
          this.xml(xml);
        },
      },
    });
    this.diagram.appChanged.connect(this.onAppChanged, this);
  }

  xml(value?: string) {
    const source: XMLModel = this.model.get('source');

    if (value == null) {
      return source?.get('value');
    }

    if (source != null) {
      source.set({ value });
      source.save_changes(this.callbacks());
    }

    return;
  }

  onAppChanged() {
    const { app } = this.diagram;
    if (!app) {
      return;
    }
    DEBUG && console.warn('installing handlers on', app);

    const { editor } = app;
    const { graph } = editor;
    const { view, model, panningHandler, selectionModel } = graph;

    const emitters = [
      { src: app, evts: MX_APP_MODEL_EVENTS },
      { src: editor, evts: MX_EDITOR_EVENTS },
      { src: graph, evts: MX_GRAPH_EVENTS },
      { src: view, evts: MX_GRAPH_VIEW_EVENTS },
      { src: model, evts: MX_GRAPH_MODEL_EVENTS },
      { src: panningHandler, evts: MX_GRAPH_PAN_EVENTS },
      { src: selectionModel, evts: MX_GRAPH_SELECT_EVENTS },
    ];

    // mxgraph model, not widget model
    // app.editor.graph.model.eventListeners
    for (const { src, evts } of emitters) {
      for (const evt of evts) {
        (src as any).addListener(evt, this.onDrawioEvent);
      }
    }

    // wire up listeners from opposite direction
    // edge: 'trailing',
    const bounceOpts: Throttler.IOptions = { limit: 10 };
    [
      { evt: 'change:zoom', fn: this.onModelZoom },
      { evt: 'change:scroll_x change:scroll_y', fn: this.onModelScroll },
      { evt: 'change:page_format', fn: this.onModelPageFormat },
      { evt: 'change:current_page', fn: this.onModelPageSelected },
      { evt: 'change:grid_enabled', fn: this.onModelGridEnabled },
      { evt: 'change:grid_size', fn: this.onModelGridSize },
      { evt: 'change:grid_color', fn: this.onModelGridColor },
      { evt: 'change:selected_cells', fn: this.onModelSelectedCells },
    ].forEach(({ evt, fn }) => {
      const throttle = new Throttler(fn, bounceOpts);
      this.model.on(evt, () => throttle.invoke(), this);
    });
  }

  onModelZoom = () => {
    const { view } = this.app.editor.graph;
    const wz = this.model.get('zoom');
    if (view.getScale() !== wz) {
      view.setScale(wz);
    }
  };

  onModelScroll = () => {
    const { view } = this.app.editor.graph;
    const wx = this.model.get('scroll_x');
    const wy = this.model.get('scroll_y');
    const tx = view.getTranslate();
    if (tx.x !== wx || tx.y !== wy) {
      view.setTranslate(wx, wy);
    }
  };

  onModelPageFormat = () => {
    const newFmt = this.model.get('page_format');
    const oldFmt = this.app.editor.graph.pageFormat as any;
    if (!JSONExt.deepEqual(newFmt, oldFmt)) {
      DEBUG && console.warn('pageFormat', newFmt);
      this.app.setPageFormat({ ...newFmt });
    }
  };

  onModelPageSelected = () => {
    this.app.selectPage(this.app.pages[this.model.get('current_page')]);
  };

  onModelGridEnabled = () => {
    this.app.editor.graph.setGridEnabled(this.model.get('grid_enabled'));
    this.app.editor.graph.refresh();
  };

  onModelGridSize = () => {
    this.app.editor.graph.setGridSize(this.model.get('grid_size'));
    this.app.editor.graph.refresh();
  };

  onModelGridColor = () => {
    this.app.setGridColor(this.model.get('grid_color'));
  };

  onModelSelectedCells = () => {
    const cells = this.model
      .get('selected_cells')
      .reduce((m: IMXCell[], id: string) => {
        return [...m, ...this.app.editor.graph.getCellsById(id)];
      }, []);
    this.app.editor.graph.selectionModel.setCells(cells);
  };

  get app() {
    return this.diagram.app;
  }

  // handle "native" mxEvent stuff
  onDrawioEvent = (sender: IMXEventSource, event: IMXEvent) => {
    let needsUpdate = {};
    switch (event.name) {
      case 'change':
        needsUpdate = {
          selected_cells: this.app.editor.graph.selectionModel.cells.map((c) =>
            c.getId()
          ),
        };
        break;
      case 'scale':
      case 'scaleAndTranslate':
        needsUpdate = { zoom: this.app.editor.graph.view.getScale() };
        break;
      case 'pan':
      case 'translate':
      case 'size':
        needsUpdate = this.translateToScroll();
        break;
      case 'pageSelected':
        needsUpdate = {
          current_page: this.app.pages.indexOf(this.app.currentPage),
          page_ids: this.app.pages.map((p) => p.getId()),
        };
        break;
      case 'pageFormatChanged':
        needsUpdate = { page_format: this.app.editor.graph.pageFormat };
        break;
      case 'gridEnabledChanged':
        needsUpdate = { grid_enabled: this.app.editor.graph.gridEnabled };
        break;
      case 'gridSizeChanged':
        needsUpdate = { grid_size: this.app.editor.graph.gridSize };
        break;
      case 'gridColorChanged':
        needsUpdate = { grid_color: this.app.editor.graph.view.gridColor };
        break;
      case 'fireMouseEvent':
        break; // these are too noisy, even for us
      default:
        DEBUG && console.warn('unhandled', event.name, event, 'from', sender);
        break;
    }

    const old: any = {};

    for (const k of Object.keys(needsUpdate)) {
      old[k] = this.model.attributes[k];
    }

    if (!JSONExt.deepEqual(old, needsUpdate)) {
      this.model.set(needsUpdate);
      this.touch();
    }
  };

  translateToScroll() {
    const { x, y } = this.app.editor.graph.view.getTranslate();
    return { scroll_x: x, scroll_y: y };
  }
}

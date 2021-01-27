import { Application, IPlugin } from '@lumino/application';
import { Widget } from '@lumino/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import { IDiagramManager } from './tokens';

import { NS, VERSION, DEBUG } from './tokens';

const EXTENSION_ID = `${NS}:widgets`;

const plugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry, IDiagramManager],
  autoStart: true,
  activate: (
    _: Application<Widget>,
    registry: IJupyterWidgetRegistry,
    diagramManager: IDiagramManager
  ) => {
    const reg = {
      name: NS,
      version: VERSION,
      exports: async () => {
        const widgetExports = await import('./widgets');
        widgetExports.DiagramView.diagrmManager = diagramManager;
        return widgetExports;
      },
    };
    DEBUG && console.warn('registering widgets', reg);
    registry.registerWidget(reg);
  },
};

export default plugin;

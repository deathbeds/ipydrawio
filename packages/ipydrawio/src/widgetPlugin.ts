/*
  Copyright 2021 ipydrawio contributors
  Copyright 2020 jupyterlab-drawio contributors

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/

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

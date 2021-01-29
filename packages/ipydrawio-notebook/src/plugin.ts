// Copyright 2021 ipydrawio contributors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { JupyterLab, JupyterFrontEndPlugin } from '@jupyterlab/application';

import { drawioPlainIcon, IDiagramManager } from '@deathbeds/ipydrawio';

import { CommandIds, PLUGIN_ID } from './tokens';
import { IPyDrawioNotebookButton } from './toolbar';
import { ALL_FORMATS, IPYNB_DIO } from './io';
import { INotebookTracker } from '@jupyterlab/notebook';

/**
 * The editor tracker extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  activate,
  id: PLUGIN_ID,
  requires: [IDiagramManager, INotebookTracker],
  autoStart: true,
};

export default plugin;

function activate(
  app: JupyterLab,
  diagrams: IDiagramManager,
  notebooks: INotebookTracker
) {
  for (const format of ALL_FORMATS) {
    diagrams.addFormat(format);
  }
  const button = new IPyDrawioNotebookButton();
  button.commands = app.commands;
  app.docRegistry.addWidgetExtension('Notebook', button);
  app.commands.addCommand(CommandIds.open, {
    icon: drawioPlainIcon,
    caption: 'Open as Diagram',
    execute: async () => {
      const path = notebooks.currentWidget?.context.path;
      if (path != null) {
        app.commands.execute('docmanager:open', {
          path,
          factory: IPYNB_DIO.factoryName,
        });
      }
    },
  });
}

/*
  Copyright 2021 ipydrawio contributors

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
import { JupyterLab, JupyterFrontEndPlugin } from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';

import { IStatusBar } from '@jupyterlab/statusbar';

import { IDiagramManager } from '@deathbeds/ipydrawio';

import { PDF_PLAIN } from './io';
import { PDFStatus } from './status';
import { DrawioPDFManager } from './manager';
import { CommandIds, PLUGIN_ID, NS } from './tokens';

/**
 * The editor tracker extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  activate,
  id: PLUGIN_ID,
  requires: [ICommandPalette, IDiagramManager],
  optional: [IStatusBar],
  autoStart: true,
};

export default plugin;

function activate(
  app: JupyterLab,
  palette: ICommandPalette,
  diagrams: IDiagramManager,
  statusBar?: IStatusBar
) {
  const manager = new DrawioPDFManager();

  diagrams.addFormat({
    ...PDF_PLAIN,
    exporter: manager.exportPDF,
  });

  app.commands.addCommand(CommandIds.provision, {
    label: 'Provision Drawio PDF Export Server',
    execute: async () => {
      await manager.provision();
    },
  });

  palette.addItem({
    command: CommandIds.provision,
    category: `Diagram Export`,
  });

  if (statusBar) {
    const statusItem = new PDFStatus(manager.status);
    statusBar.registerStatusItem(`${NS}:status`, {
      item: statusItem,
      align: 'right',
      rank: 4,
      isActive: () => diagrams.activeWidget != null,
    });
    manager.fetchStatus().catch(console.warn);
  }
}

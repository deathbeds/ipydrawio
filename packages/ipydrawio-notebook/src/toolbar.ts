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

import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { CommandRegistry } from '@lumino/commands';

import { CommandToolbarButton } from '@jupyterlab/apputils';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { NotebookPanel, INotebookModel } from '@jupyterlab/notebook';

import { CommandIds } from './tokens';

/**
 * A notebook widget extension that adds a button to the toolbar.
 */
export class IPyDrawioNotebookButton
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  commands: CommandRegistry;

  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    const btn = new CommandToolbarButton({
      commands: this.commands,
      id: CommandIds.open,
    });
    panel.toolbar.insertItem(9, 'ipydrawio', btn);

    return new DisposableDelegate(() => btn.dispose());
  }
}

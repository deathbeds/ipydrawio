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
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
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

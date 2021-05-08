/*
  Copyright 2021 ipydrawio contributors
  Copyright 2020 jupyterlab-drawio contributors
  Copyright 2018 Wolf Vollprecht

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

import { IStatusBar } from '@jupyterlab/statusbar';
import { Menu } from '@lumino/widgets';

import {
  ILayoutRestorer,
  JupyterLab,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { IFileBrowserFactory } from '@jupyterlab/filebrowser';

import { ILauncher } from '@jupyterlab/launcher';

import { IMainMenu } from '@jupyterlab/mainmenu';

import * as IO from './io';
import { DrawioStatus } from './status';

import {
  IDiagramManager,
  CommandIds,
  DEBUG,
  NS,
  PLUGIN_ID,
  DIAGRAM_MENU_RANK,
  UI_THEMES,
  ISetUrlParamsArgs,
} from './tokens';
import { DiagramManager } from './manager';
import { RenderedDiagram } from './mime';
import widgetPlugin from './widgetPlugin';

/**
 * The editor tracker extension.
 */
const plugin: JupyterFrontEndPlugin<IDiagramManager> = {
  activate,
  id: PLUGIN_ID,
  requires: [
    IFileBrowserFactory,
    ILayoutRestorer,
    IMainMenu,
    ICommandPalette,
    ISettingRegistry,
  ],
  optional: [ILauncher, IStatusBar],
  provides: IDiagramManager,
  autoStart: true,
};

export default [plugin, widgetPlugin];

function activate(
  app: JupyterLab,
  browserFactory: IFileBrowserFactory,
  restorer: ILayoutRestorer,
  menu: IMainMenu,
  palette: ICommandPalette,
  settingsRegistry: ISettingRegistry,
  launcher: ILauncher | null,
  statusBar: IStatusBar | null
): IDiagramManager {
  const { commands } = app;
  const manager = new DiagramManager({
    app,
    restorer,
    palette,
    browserFactory,
  });
  let statusItem: DrawioStatus | null = null;

  if (statusBar) {
    statusItem = new DrawioStatus(manager.status);
    statusBar.registerStatusItem(`${NS}:status`, {
      item: statusItem,
      align: 'right',
      rank: 3,
      isActive: () => manager.activeWidget != null,
    });
  }

  // add first-party file types
  for (const format of IO.ALL_FORMATS) {
    manager.addFormat(format);
  }

  settingsRegistry
    .load(PLUGIN_ID)
    .then((loadedSettings) => {
      DEBUG && console.warn('settings loaded', loadedSettings.composite);
      manager.settings = loadedSettings;
    })
    .catch((err) => console.error(err));

  // Add a launcher item if the launcher is available.
  if (launcher) {
    for (const ui of UI_THEMES) {
      launcher.add({
        command: CommandIds.createNew,
        args: {
          drawioUrlParams: { ui },
        },
        rank: 1,
        category: IO.XML_NATIVE.label,
      });
    }
  }

  commands.addCommand(CommandIds.setUrlParams, {
    label: (args) => {
      const { drawioUrlParams } = (args as any) as ISetUrlParamsArgs;
      const entries = Object.entries(drawioUrlParams || {});
      if (entries.length == 1 && args.justValue) {
        return entries.map(([k, v]) => v).join(', ');
      } else {
        const msg = entries.map(([k, v]) => `${k}: ${v}`.trim(), '');
        return `${IO.XML_NATIVE.label} ` + msg.join(', ');
      }
    },
    isToggleable: true,
    isToggled: (args) => {
      const drawioUrlParams =
        manager.settings?.composite?.drawioUrlParams || {};
      for (const [k, v] of Object.entries(args.drawioUrlParams || {})) {
        if (
          drawioUrlParams.hasOwnProperty(k) &&
          (drawioUrlParams as any)[k] !== v
        ) {
          return false;
        }
      }
      return true;
    },
    execute: async (args) => {
      const drawioUrlParams =
        manager.settings?.composite?.drawioUrlParams || {};
      await manager.settings.set('drawioUrlParams', {
        ...(drawioUrlParams as any),
        ...(args.drawioUrlParams as any),
      });
    },
  });

  for (const ui of UI_THEMES) {
    palette.addItem({
      command: CommandIds.setUrlParams,
      args: { drawioUrlParams: { ui } },
      category: `${IO.XML_NATIVE.label} Settings`,
    });
  }

  if (menu) {
    // Add new text file creation to the file menu.
    menu.fileMenu.newMenu.addGroup([{ command: CommandIds.createNew }], 40);

    const theme = new Menu({ commands });
    theme.title.label = `${IO.XML_NATIVE.label} Theme`;

    for (const ui of UI_THEMES) {
      theme.addItem({
        command: CommandIds.setUrlParams,
        args: { drawioUrlParams: { ui }, justValue: true },
        type: 'command',
      });
    }

    // actually add the thing
    menu.settingsMenu.addGroup(
      [{ submenu: theme, type: 'submenu' }],
      DIAGRAM_MENU_RANK
    );
  }

  RenderedDiagram.manager = manager;
  return manager;
}

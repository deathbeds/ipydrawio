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
import { Widget } from '@lumino/widgets';
import {
  IWidgetTracker,
  WidgetTracker,
  ICommandPalette,
  MainAreaWidget,
} from '@jupyterlab/apputils';
import { JupyterLab, ILayoutRestorer } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { URLExt, PathExt } from '@jupyterlab/coreutils';
import {
  IDiagramManager,
  CommandIds,
  DEBUG,
  IFormat,
  ICreateNewArgs,
  ITemplate,
} from './tokens';
import { Diagram } from './editor';
import { DiagramFactory, DiagramDocument } from './document';
import { Contents } from '@jupyterlab/services';
import { DrawioStatus } from './status';
import * as IO from './io';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { DRAWIO_URL } from '@deathbeds/ipydrawio-webpack';
import { CreateAdvanced } from './createAdvanced';

const DEFAULT_EXPORTER = async (
  drawio: Diagram,
  key: string,
  settings: any = null
) => {
  return await drawio.exportAs(key);
};

export class DiagramManager implements IDiagramManager {
  private _formats = new Map<string, IFormat>();
  private _trackers = new Map<string, IWidgetTracker<DiagramDocument>>();
  private _settings: ISettingRegistry.ISettings;
  private _palette: ICommandPalette;
  private _browserFactory: IFileBrowserFactory;
  private _restorer: ILayoutRestorer;
  private _app: JupyterLab;
  private _status: DrawioStatus.Model;
  private _mimeExport = new Map<string, IFormat>();

  constructor(options: DiagramManager.IOptions) {
    this._app = options.app;
    this._restorer = options.restorer;
    this._palette = options.palette;
    this._browserFactory = options.browserFactory;
    this._status = new DrawioStatus.Model();
    this._initCommands();
  }

  protected _initCommands() {
    const { commands } = this._app;
    // Add a command for creating a new diagram file.
    commands.addCommand(CommandIds.createNew, {
      label: (args) => {
        const { drawioUrlParams } = (args as any) as ICreateNewArgs;
        const { ui } = drawioUrlParams || {};
        return !ui
          ? IO.XML_NATIVE.label
          : `${IO.XML_NATIVE.label} [${drawioUrlParams?.ui}]`;
      },
      icon: (args) => {
        const { drawioUrlParams } = (args as any) as ICreateNewArgs;
        const { ui } = drawioUrlParams || {};
        return ui ? IO.drawioThemeIcons[ui] : IO.drawioIcon;
      },
      caption: `Create a blank ${IO.XML_NATIVE.ext} file`,
      execute: async (args) => {
        let cwd = this._browserFactory.defaultBrowser.model.path;
        return this.createNew({ ...(args as any), cwd });
      },
    });

    commands.addCommand(CommandIds.createNewCustom, {
      label: `Advanced ${IO.XML_NATIVE.label}...`,
      caption: 'Create a diagram with customized formats, templates, and UI',
      execute: () => {
        const model = new CreateAdvanced.Model({ manager: this });
        const settingsChanged = () => model.stateChanged.emit(void 0);
        this._settings.changed.connect(settingsChanged);
        const content = new CreateAdvanced(model);
        const main = new MainAreaWidget({ content });
        model.documentRequested.connect(async () => {
          await commands.execute(CommandIds.createNew, model.args as any);
          main.dispose();
          model.dispose();
          this._settings.changed.disconnect(settingsChanged);
        });
        this._app.shell.add(main);
      },
      icon: IO.drawioIcon,
    });
  }

  get formats() {
    return [...this._formats.values()];
  }

  formatForModel(contentsModel: Partial<Contents.IModel>) {
    DEBUG && console.warn('getting format', contentsModel);
    const { path } = contentsModel;

    let longestExt: string = '';
    let candidateFmt = (null as any) as IFormat;

    for (const fmt of this._formats.values()) {
      if (fmt.wantsModel != null && fmt.wantsModel(contentsModel)) {
        return fmt;
      }
      if (
        path &&
        path.endsWith(fmt.ext) &&
        fmt.ext.length > longestExt.length
      ) {
        candidateFmt = fmt;
        longestExt = fmt.ext;
      }
    }

    return candidateFmt || null;
  }

  get drawioURL() {
    return DRAWIO_URL;
  }

  get status() {
    return this._status;
  }

  set status(status) {
    this._status = status;
  }

  get settings() {
    return this._settings;
  }

  set settings(settings) {
    this._settings = settings;
    this._settings.changed.connect(this._onSettingsChanged, this);
  }
  get activeWidget() {
    const { currentWidget } = this._app.shell;
    for (const tracker of this._trackers.values()) {
      if (tracker.currentWidget === currentWidget) {
        return tracker.currentWidget;
      }
    }
    return null;
  }

  // Create a new untitled diagram file, given the current working directory.
  async createNew(args: ICreateNewArgs) {
    let { cwd } = args;

    const format =
      (args.format ? this._formats.get(args.format) : null) || IO.XML_NATIVE;

    this._status.status = `Creating Diagram in ${cwd}...`;

    const model: Contents.IModel = await this._app.commands.execute(
      'docmanager:new-untitled',
      {
        path: cwd,
        type: format.contentType || 'file',
        ext: format.ext,
      }
    );

    this._status.status = `Opening Diagram...`;

    const diagram: DiagramDocument = await this._app.commands.execute(
      'docmanager:open',
      { path: model.path, factory: format.factoryName }
    );

    if (args.drawioUrlParams) {
      diagram.urlParams = args.drawioUrlParams;
      const template = args.drawioUrlParams['template-filename'];
      if (template) {
        await diagram.content.ready;
        const response = await fetch(template);
        const xml = await response.text();
        diagram.content.load(xml);
      }
    }

    return diagram;
  }

  protected _onSettingsChanged() {
    this._status.status = `settings changed`;
    for (const tracker of this._trackers.values()) {
      tracker.forEach(this.updateWidgetSettings);
    }
  }

  /**
   * Retrieve all available templates
   */
  async templates(): Promise<ITemplate[]> {
    const templates: ITemplate[] = [];
    const response = await fetch(
      URLExt.join(DRAWIO_URL, '../templates/index.xml')
    );
    const xmlStr = await response.text();
    const parser = new DOMParser();
    const xml = parser.parseFromString(xmlStr, 'application/xml');
    for (const tmpl of xml.querySelectorAll('template')) {
      let url = tmpl.getAttribute('url');
      if (!url) {
        continue;
      }
      const [group, label] = url
        .replace(/.xml$/, '')
        .replace(/_/g, ' ')
        .split('/')
        .slice(-2);
      url = URLExt.join(DRAWIO_URL, '../templates/', url);
      templates.push({
        url,
        label,
        thumbnail: url.replace(/.xml$/, '.png'),
        tags: [group],
      });
    }
    return templates;
  }

  addFormat(format: IFormat) {
    DEBUG && console.warn(`adding format ${format.name}`, format);
    if (this._formats.has(format.key)) {
      throw Error(`cannot reregister ${format.key}`);
    }
    this._formats.set(format.key, format);
    this._app.docRegistry.addFileType({
      name: format.name,
      contentType: format.contentType || 'file',
      displayName: format.label,
      mimeTypes: [format.mimetype],
      extensions: [format.ext],
      icon: format.icon,
      fileFormat: format.format,
      ...(format.pattern ? { pattern: format.pattern } : {}),
    });

    if (format.isExport) {
      DEBUG && console.warn(`...export ${format.name}`);
      this._initExportCommands(format);
    }

    this._initTracker(
      format.modelName,
      format.factoryName,
      `drawio-${format.key}`,
      [format],
      format.isDefault ? [format] : []
    );
    DEBUG && console.warn(`...tracked ${format.name}`);
  }

  protected updateWidgetSettings(widget: DiagramDocument) {
    widget.updateSettings();
  }

  escapeCurrent(widget: Widget) {
    if (this._settings.composite['disableEscapeFocus']) {
      return;
    }
    this._app.shell.activateById(widget.id);
    const { status } = this.status;

    this.status.status = 'Escaped';
    setTimeout(() => (this.status.status = status), 1000);
    window.focus();
  }

  protected _initExportCommands(exportFormat: IFormat) {
    const { ext, key, format, label, mimetype, icon } = exportFormat;
    const save = exportFormat.save || String;
    const _exporter = async (cwd: string) => {
      let drawio = this._app.shell.currentWidget as DiagramDocument;
      let stem = PathExt.basename(drawio.context.path).replace(
        /\.dio($|\.(svg|png|ipynb|pdf)$)/,
        ''
      );

      this._status.status = `Exporting Diagram ${stem} to ${label}...`;

      const rawContent = await (exportFormat.exporter || DEFAULT_EXPORTER)(
        drawio.content,
        key,
        this._settings
      );

      if (rawContent == null) {
        this._status.status = `Failed to export to ${label}... please retry`;
        return;
      }

      this._status.status = `${stem} ready, saving...`;

      let model: Contents.IModel = await this._app.commands.execute(
        'docmanager:new-untitled',
        {
          path: cwd,
          type: exportFormat.contentType || 'file',
          ext,
        }
      );

      const newPath = await this._getAvaialablePath(cwd, stem, ext);

      model = await this._app.serviceManager.contents.rename(
        model.path,
        newPath
      );

      if (rawContent != null) {
        await this._app.serviceManager.contents.save(model.path, {
          ...model,
          format,
          mimetype,
          content: save(rawContent),
        });
      }

      this._status.status = `${stem} ${label} saved as ${PathExt.basename(
        newPath
      )}, launching...`;

      // TODO: make this behavior configurable

      const factories = this._app.docRegistry
        .preferredWidgetFactories(model.path)
        .map((f) => f.name);

      if (factories.length) {
        await this._app.commands.execute('docmanager:open', {
          factory: factories[0],
          path: model.path,
        });
      }

      this._status.status = `${PathExt.basename(newPath)} launched`;
    };

    this._app.commands.addCommand(`drawio:export-${key}`, {
      label: `Export ${IO.XML_NATIVE.label} as ${label}`,
      icon,
      execute: () => {
        let cwd = this._browserFactory.defaultBrowser.model.path;
        return _exporter(cwd);
      },
      isEnabled: () => this.activeWidget != null,
    });

    this._palette.addItem({
      command: `drawio:export-${key}`,
      category: `${IO.XML_NATIVE.label} Export`,
    });
  }

  /**
   * Create a best-effort short file derived from the original stem
   * e.g. from Untitled.dio, get in order:
   * - Untitled.png.dio
   * - Untitled-01.png.dio
   * - Untitled-02.png.dio
   *
   * In the future, this may become configurable via settings.
   */
  protected async _getAvaialablePath(
    cwd: string,
    stem: string,
    ext: string,
    retries = 99
  ): Promise<string> {
    let newPath = `${stem}ext`;
    const opts = { content: false };
    const { contents } = this._app.serviceManager;
    for (const salt in [...Array(retries).keys()]) {
      const padded = salt.length == 1 ? `0${salt}` : `${salt}`;
      newPath = PathExt.join(
        cwd,
        salt ? `${stem}-${padded}${ext}` : `${stem}ext`
      );
      try {
        const model = await contents.get(newPath, opts);
        console.warn('Path not available', model);
      } catch {
        return newPath;
      }
    }

    throw new Error(`Couldn't find a writeable path for ${stem}${ext}`);
  }

  /**
   * Create a widget tracker and associated factory for this model type
   */
  protected _initTracker(
    modelName: string,
    name: string,
    namespace: string,
    fileTypes: IFormat[],
    defaultFor: IFormat[]
  ) {
    if (this._trackers.has(namespace)) {
      throw Error(name);
    }

    const factory = new DiagramFactory({
      modelName,
      name,
      fileTypes: fileTypes.map(({ name }) => name),
      defaultFor: defaultFor.map(({ name }) => name),
      getSettings: () => this._settings.composite || {},
      manager: this,
    });
    const tracker = new WidgetTracker<DiagramDocument>({ namespace });

    // Handle state restoration.
    this._restorer
      .restore(tracker, {
        command: 'docmanager:open',
        args: (widget) => ({ path: widget.context.path, factory: name }),
        name: (widget) => widget.context.path,
      })
      .catch(console.warn);

    factory.widgetCreated.connect((sender, widget) => {
      this._status.status = `Loading Diagram...`;

      widget.content.frameClicked.connect(() => {
        if (widget !== this._app.shell.currentWidget) {
          widget.node.focus();
        }
      });

      // initialize icon
      widget.title.icon = IO.drawioIcon;

      // Notify the instance tracker if restore data needs to update.
      widget.context.pathChanged.connect(() => tracker.save(widget));

      // capture clicks inside the frame
      widget.content.frameClicked.connect((drawio) => {
        this._app.shell.activateById(widget.id);
        this._status.status = `Editing ${widget.context.path}`;
      });

      // complete initialization once context is ready;
      widget.context.ready
        .then(() => {
          if (widget.context.contentsModel == null) {
            console.warn('widget not ready');
            return;
          }
          const { mimetype } = widget.context.contentsModel;
          const icon = this._mimeExport.get(mimetype)?.icon;
          if (icon != null) {
            widget.title.icon = icon;
          }
          this._status.status = `${widget.context.path} ready`;
        })
        .catch(console.warn);

      // add to tracker
      tracker.add(widget).catch(console.warn);
    });
    this._app.docRegistry.addWidgetFactory(factory);

    this._trackers.set(namespace, tracker);

    return tracker;
  }
}

export namespace DiagramManager {
  export interface IOptions extends IDiagramManager.IOptions {
    app: JupyterLab;
    restorer: ILayoutRestorer;
    palette: ICommandPalette;
    browserFactory: IFileBrowserFactory;
  }
}

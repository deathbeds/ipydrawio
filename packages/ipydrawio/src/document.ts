// Copyright 2021 ipydrawio contributors
// Copyright 2020 jupyterlab-drawio contributors
// Copyright 2018 Wolf Vollprecht
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
import { ReadonlyPartialJSONObject } from '@lumino/coreutils';

import { PathExt } from '@jupyterlab/coreutils';
import {
  ABCWidgetFactory,
  DocumentRegistry,
  DocumentWidget,
} from '@jupyterlab/docregistry';

import '../style/index.css';
import { IDiagramManager, DEBUG } from './tokens';
import { Diagram } from './editor';

export class DiagramDocument extends DocumentWidget<Diagram> {
  protected _manager: IDiagramManager;
  getSettings: ISettingsGetter;

  readonly context: DocumentRegistry.Context;

  constructor(options: DiagramDocument.IOptions) {
    super(options);
    this.context = options.context;
    this._manager = options.manager;
    this.getSettings = options.getSettings;

    this._onTitleChanged();
    this.context.pathChanged.connect(this._onTitleChanged, this);
    this.context.ready
      .then(async () => {
        DEBUG && console.warn('format', this.format);
        this._onContextReady();
      })
      .catch(console.warn);
  }

  private _onContextReady(): void {
    this.context.model.contentChanged.connect(
      this.content.onContentChanged,
      this.content
    );
    this.content.onContentChanged();
    this.content.onAfterShow();
  }

  /**
   * Handle a change to the title.
   */
  private _onTitleChanged(): void {
    DEBUG && console.warn('contentsModel', this.context.contentsModel);

    this.title.label = PathExt.basename(this.context.localPath);
  }

  get format() {
    if (this.context.contentsModel == null) {
      return null;
    }
    let format = this._manager.formatForModel(this.context.contentsModel);
    return format || null;
  }

  /**
   * Handle receiving settings from the extension
   */
  updateSettings() {
    this.content.maybeReloadFrame(true);
  }
}

export interface ISettingsGetter {
  (): ReadonlyPartialJSONObject;
}

export namespace DiagramDocument {
  export interface IOptions extends DocumentWidget.IOptions<Diagram> {
    getSettings: ISettingsGetter;
    manager: IDiagramManager;
  }
}

/**
 * A widget factory for a diagram documents.
 */
export class DiagramFactory extends ABCWidgetFactory<
  DiagramDocument,
  DocumentRegistry.IModel
> {
  protected getSettings: ISettingsGetter;
  manager: IDiagramManager;
  /**
   * Create a new widget given a context.
   */
  constructor(options: DiagramFactory.IOptions) {
    super(options);
    this.getSettings = options.getSettings;
    this.manager = options.manager;
  }

  protected createNewWidget(
    context: DocumentRegistry.Context
  ): DiagramDocument {
    const doc: DiagramDocument = new DiagramDocument({
      context,
      content: new Diagram({
        adapter: {
          format: () => {
            return doc.format;
          },
          urlParams: () => {
            return this.getSettings()
              ?.drawioUrlParams as ReadonlyPartialJSONObject;
          },
          drawioConfig: () => {
            return this.getSettings()
              ?.drawioConfig as ReadonlyPartialJSONObject;
          },
          saveNeedsExport: () => {
            const isTransformed = doc.format?.isTransformed;
            DEBUG && console.warn('needs export', isTransformed);
            return isTransformed == null ? true : isTransformed;
          },
          toXML: () => {
            const { model } = doc.context;
            const { format } = doc;
            if (format?.toXML) {
              return format.toXML(model);
            }
            return model.toString();
          },
          drawioUrl: () => {
            return this.manager.drawioURL;
          },
          fromXML: (xml, hardSave) => {
            const { format } = doc;
            if (format?.fromXML) {
              format.fromXML(doc.context.model, xml);
            } else {
              doc.context.model.fromString(xml);
            }

            if (hardSave) {
              doc.context.save().catch(console.warn);
            }
          },
        },
      }),
      getSettings: this.getSettings,
      manager: this.manager,
    });
    return doc;
  }
}

export namespace DiagramFactory {
  export interface IOptions extends DocumentRegistry.IWidgetFactoryOptions {
    getSettings: () => ReadonlyPartialJSONObject;
    manager: IDiagramManager;
  }
}

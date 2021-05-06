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

import { IRenderMime } from '@jupyterlab/rendermime-interfaces';
import { Panel, PanelLayout } from '@lumino/widgets';
import { ALL_MIME_FORMATS } from './io';
import { DEBUG, IFormat, IDiagramManager, NS } from './tokens';
import { Diagram } from './editor';
import { DRAWIO_URL } from '@deathbeds/ipydrawio-webpack';
import { ReadonlyPartialJSONObject } from '@lumino/coreutils';

export const MIME_CLASS = 'jp-DiagramMedia';

export const extensions: IRenderMime.IExtension[] = ALL_MIME_FORMATS.map(
  (fmt) => {
    const { name } = fmt;
    return {
      id: `${NS}:rendermime-${name}`,
      name,
      rendererFactory: {
        safe: true,
        mimeTypes: [fmt.mimetype],
        createRenderer: (options) => {
          DEBUG && console.error('creating renderer');
          return new RenderedDiagram({
            ...options,
            format: fmt,
          });
        },
      },
      dataType: 'string',
    };
  }
);

export default extensions;

export class RenderedDiagram extends Panel implements IRenderMime.IRenderer {
  content: Diagram;
  format: IFormat;
  lastModel: IRenderMime.IMimeModel;
  initialized = false;

  static manager: IDiagramManager;

  constructor(options: RenderedDiagram.IOptions) {
    super();
    this.addClass(MIME_CLASS);
    this.format = options.format;
    this.content = new Diagram({
      adapter: {
        format: () => this.format,
        urlParams: () => {
          let params = {};

          const { manager } = RenderedDiagram;
          if (manager != null) {
            params =
              (manager.settings?.composite
                ?.drawioUrlParams as ReadonlyPartialJSONObject) || {};
          }
          const meta = this.lastModel?.metadata;
          const mimeParams = ((meta[this.format.mimetype] || {}) as any)[
            'drawioUrlParams'
          ];
          if (mimeParams != null) {
            params = { ...params, ...mimeParams };
          }

          return params;
        },
        drawioUrl: () => DRAWIO_URL,
        saveNeedsExport: () => {
          return this.format?.isTransformed || true;
        },
        drawioConfig: () => {
          let config = {};
          const { manager } = RenderedDiagram;
          if (manager != null) {
            config =
              (manager.settings?.composite
                ?.drawioConfig as ReadonlyPartialJSONObject) || {};
          }

          const meta = this.lastModel?.metadata;
          const mimeConfig = ((meta[this.format.mimetype] || {}) as any)[
            'drawioConfig'
          ];
          if (mimeConfig != null) {
            config = { ...config, ...mimeConfig };
          }
          return config;
        },
        toXML: () => {
          if (this.lastModel == null) {
            return '';
          }
          return this.lastModel.data[this.format.mimetype]?.toString() || '';
        },
        fromXML: () => {
          return;
        },
      },
    });
    (this.layout as PanelLayout).addWidget(this.content);
  }

  onAfterShow() {
    if (!this.initialized) {
      this.content.onAfterShow();
      this.initialized = true;
    }
    this.content.onContentChanged();
  }

  async renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    const meta = model.metadata || {};
    const mimeMeta = meta
      ? (meta[this.format.mimetype] as ReadonlyPartialJSONObject)
      : null;
    if (mimeMeta != null) {
      const height = mimeMeta['height'] ? `${mimeMeta['height']}` : '';
      this.node.style.minHeight = height;
    }

    this.lastModel = model;
    if (this.initialized) {
      this.content.onContentChanged();
    } else if (this.isVisible) {
      this.onAfterShow();
    } else {
      setTimeout(() => this.onAfterShow(), 100);
    }
    return;
  }
}

export namespace RenderedDiagram {
  export interface IOptions extends IRenderMime.IRendererOptions {
    format: IFormat;
  }
}

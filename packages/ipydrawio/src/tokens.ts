// Copyright 2021 ipydrawio contributors
// Copyright 2020 jupyterlab-drawio contributors
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

import { Token } from '@lumino/coreutils';
import { Contents } from '@jupyterlab/services';
import { LabIcon } from '@jupyterlab/ui-components';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { ReadonlyPartialJSONObject } from '@lumino/coreutils';

export const NS = '@deathbeds/ipydrawio';
export const VERSION = '1.0.0-alpha0';
export const PLUGIN_ID = `${NS}:plugin`;

import { Diagram } from './editor';
import { DiagramDocument } from './document';

import ICON_SVG from '../style/img/drawio.svg';
export const CMD_NS = 'ipydrawio';

/**
 * The name of the factory that creates text editor widgets.
 */
export const TEXT_FACTORY = 'Diagram';
export const BINARY_FACTORY = 'Diagram Image';
export const JSON_FACTORY = 'Diagram Notebook';

export const DRAWIO_ICON_SVG = ICON_SVG;

export const DRAWIO_METADATA = NS;

/**
 * Escape hatch for runtime debugging.
 */
export const DEBUG = window.location.hash.indexOf('DRAWIO_DEBUG') > -1;
export const DEBUG_LEVEL = DEBUG
  ? window.location.hash.indexOf('DRAWIO_DEBUG')
  : 0;

export interface IDiagramManager {
  addFormat(format: IFormat): void;
  formatForModel(contentsModel: Partial<Contents.IModel>): IFormat | null;
  activeWidget: DiagramDocument | null;
  drawioURL: string;
  settings: ISettingRegistry.ISettings;
}

export const DRAWIO_ICON_CLASS_RE = /jp-icon-warn0/;

export const IDiagramManager = new Token<IDiagramManager>(PLUGIN_ID);

export namespace CommandIds {
  export const createNew = 'drawio:create-new';
}

export namespace IDiagramManager {
  export interface IOptions {}
}

export interface IFormat<T = string> {
  key: string;
  name: string;
  ext: string;
  label: string;
  icon: LabIcon;
  format: Contents.FileFormat;
  mimetype: string;
  pattern?: string;
  contentType?: Contents.ContentType;
  save?: (raw: string) => string;
  load?: (raw: string) => string;
  toXML?: (model: DocumentRegistry.IModel) => string;
  fromXML?: (model: DocumentRegistry.IModel, xml: string) => void;
  exporter?: (
    drawio: Diagram,
    key: string,
    settings: ISettingRegistry.ISettings
  ) => Promise<T | null>;
  // factory info
  factoryName: string;
  modelName: 'base64' | 'notebook' | 'text';
  wantsModel?(contentsModel: Partial<Contents.IModel>): boolean;
  // behavior switches
  isExport?: boolean;
  isBinary?: boolean;
  isText?: boolean;
  isJson?: boolean;
  isEditable?: boolean;
  isDefault?: boolean;
  isTransformed: boolean;
}

export interface IAdapter {
  format(): IFormat | null;
  // TODO: generate these from schema
  /** a dictionary encoding of the drawio JSON API Config Object */
  drawioConfig(): ReadonlyPartialJSONObject;
  /** a dictionary encoding of the drawio JSON API URL Params */
  urlParams(): ReadonlyPartialJSONObject;
  /** Use a an exporter to generate non-XML */
  saveNeedsExport(): boolean;
  /** load the XML from somewhere */
  toXML(): string;
  /** where to download drawio assets */
  drawioUrl(): string;
  /** store the XML somewhere */
  fromXML(xml: string, hardSave: boolean): void;
}

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

import { NS, PLUGIN_ID } from '.';
import { DiagramWidget } from './editor';

import ICON_SVG from '../style/img/drawio.svg';
export const CMD_NS = 'drawio';

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

export interface IDiagramManager {
  addFormat(format: IFormat): void;
  isExportable(mimetype: string): boolean;
  formatForModel(
    contentsModel: Contents.IModel
  ): IFormat | null;
  activeWidget: DiagramWidget | null;
  drawioURL: string;
}

export const DRAWIO_ICON_CLASS_RE = /jp-icon-warn0/;

export const IDiagramManager = new Token<IDiagramManager>(PLUGIN_ID);

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
    drawio: DiagramWidget,
    key: string,
    settings: ISettingRegistry.ISettings
  ) => Promise<T | null>;
  // factory info
  factoryName: string;
  modelName: 'base64' | 'notebook' | 'text';
  wantsModel?(contentsModel: Contents.IModel): boolean;
  // behavior switches
  isExport?: boolean;
  isBinary?: boolean;
  isText?: boolean;
  isJson?: boolean;
  isEditable?: boolean;
  isDefault?: boolean;
}

export namespace CommandIds {
  export const createNew = 'drawio:create-new';
}

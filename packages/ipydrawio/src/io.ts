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
import { LabIcon } from '@jupyterlab/ui-components';

import DRAWIO_ICON_SVG from '../style/img/drawio.svg';

import {
  IFormat,
  DRAWIO_ICON_CLASS_RE,
  TEXT_FACTORY,
  BINARY_FACTORY,
} from './tokens';

import { stripDataURI, unbase64SVG } from './utils';

export const drawioPlainIcon = new LabIcon({
  name: 'drawio:plain',
  svgstr: DRAWIO_ICON_SVG.replace(DRAWIO_ICON_CLASS_RE, 'jp-icon3'),
});

export const drawioIcon = new LabIcon({
  name: 'drawio:drawio',
  svgstr: DRAWIO_ICON_SVG,
});

export const drawioSvgIcon = new LabIcon({
  name: 'drawio:svg',
  svgstr: DRAWIO_ICON_SVG.replace(DRAWIO_ICON_CLASS_RE, 'jp-icon-contrast1'),
});

export const drawioPngIcon = new LabIcon({
  name: 'drawio:png',
  svgstr: DRAWIO_ICON_SVG.replace(DRAWIO_ICON_CLASS_RE, 'jp-icon-contrast0'),
});

export const XML_NATIVE: IFormat = {
  ext: '.dio',
  format: 'text',
  icon: drawioIcon,
  key: 'drawio',
  label: 'Diagram',
  mimetype: 'application/x-drawio',
  name: 'dio',
  modelName: 'text',
  factoryName: TEXT_FACTORY,
  // behavior
  isExport: true,
  isEditable: true,
  isText: true,
  isDefault: true,
  isTransformed: false,
  exporter: async (drawio, key, settings) => {
    return await drawio.adapter.toXML();
  },
};

export const XML_LEGACY: IFormat = {
  ext: '.drawio',
  format: 'text',
  icon: drawioIcon,
  key: 'dio',
  label: 'Diagram (mxgraph)',
  mimetype: 'application/x-mxgraph',
  name: 'dio-legacy',
  modelName: 'text',
  factoryName: `${TEXT_FACTORY} (Legacy)`,
  isExport: true,
  isEditable: true,
  isText: true,
  isDefault: true,
  isTransformed: false,
};

export const SVG_PLAIN: IFormat = {
  ext: '.svg',
  format: 'text',
  factoryName: `${TEXT_FACTORY} (SVG)`,
  modelName: 'text',
  icon: drawioSvgIcon,
  key: 'svg',
  label: 'SVG',
  mimetype: 'image/svg+xml',
  name: 'svg',
  save: unbase64SVG,
  isDefault: false,
  isExport: true,
  isText: true,
  isTransformed: true,
};

export const SVG_EDITABLE: IFormat = {
  ...SVG_PLAIN,
  factoryName: `${TEXT_FACTORY} (Editable SVG)`,
  ext: '.dio.svg',
  key: 'xmlsvg',
  label: 'SVG (Editable)',
  name: 'diosvg',
  pattern: '^.*.dio.svg$',
  isEditable: true,
  isDefault: true,
  isTransformed: true,
};

export const PNG_PLAIN: IFormat = {
  ext: '.png',
  format: 'base64',
  modelName: 'base64',
  factoryName: `${BINARY_FACTORY} (PNG)`,
  icon: drawioPngIcon,
  key: 'png',
  label: 'PNG',
  mimetype: 'image/png',
  name: 'png',
  save: stripDataURI,
  isBinary: true,
  isExport: true,
  isTransformed: true,
};

export const PNG_EDITABLE: IFormat = {
  ...PNG_PLAIN,
  factoryName: `${BINARY_FACTORY} (Editable PNG)`,
  ext: '.dio.png',
  key: 'xmlpng',
  label: 'PNG (Editable)',
  name: 'diopng',
  pattern: '^.*.dio.png$',
  isEditable: true,
  isDefault: true,
};

export const ALL_BINARY_FORMATS = [PNG_PLAIN, PNG_EDITABLE];

export const ALL_TEXT_FORMATS = [
  SVG_EDITABLE,
  SVG_PLAIN,
  XML_NATIVE,
  XML_LEGACY,
];

/** these are last-in-wins, don't claim existing ones*/
export const ALL_MIME_FORMATS = [XML_NATIVE];

export const ALL_FORMATS = [...ALL_BINARY_FORMATS, ...ALL_TEXT_FORMATS];

import { LabIcon } from '@jupyterlab/ui-components';

import DRAWIO_ICON_SVG from '../style/img/drawio.svg';

import {
  IDiagramManager,
  DRAWIO_ICON_CLASS_RE,
  TEXT_FACTORY,
  BINARY_FACTORY,
} from './tokens';

import { stripDataURI, unbase64SVG } from './utils';

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

export const XML_NATIVE: IDiagramManager.IFormat = {
  ext: '.dio',
  format: 'text',
  icon: drawioIcon,
  key: 'drawio',
  label: 'Diagram',
  mimetype: 'application/dio',
  name: 'dio',
  modelName: 'text',
  factoryName: TEXT_FACTORY,
  // behavior
  isExport: true,
  isEditable: true,
  isText: true,
  isDefault: true,
};

export const XML_LEGACY: IDiagramManager.IFormat = {
  ext: '.drawio',
  format: 'text',
  icon: drawioIcon,
  key: 'dio',
  label: 'Diagram (mxgraph)',
  mimetype: 'application/mxgraph',
  name: 'dio-legacy',
  modelName: 'text',
  factoryName: `${TEXT_FACTORY} (Legacy)`,
  isExport: true,
  isEditable: true,
  isText: true,
  isDefault: true,
};

export const SVG_PLAIN: IDiagramManager.IFormat = {
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
  isExport: true,
  isText: true,
};

export const SVG_EDITABLE: IDiagramManager.IFormat = {
  ...SVG_PLAIN,
  factoryName: `${TEXT_FACTORY} (Editable SVG)`,
  ext: '.dio.svg',
  key: 'xmlsvg',
  label: 'SVG (Editable)',
  name: 'diosvg',
  pattern: '^.*.dio.svg$',
  isEditable: true,
  isDefault: true,
};

export const PNG_PLAIN: IDiagramManager.IFormat = {
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
};

export const PNG_EDITABLE: IDiagramManager.IFormat = {
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

export const ALL_FORMATS = [...ALL_BINARY_FORMATS, ...ALL_TEXT_FORMATS];

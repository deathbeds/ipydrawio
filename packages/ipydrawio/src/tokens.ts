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

import { Widget } from '@lumino/widgets';
import { ISignal } from '@lumino/signaling';
import { ReadonlyPartialJSONObject, Token } from '@lumino/coreutils';
import { Contents } from '@jupyterlab/services';
import { LabIcon } from '@jupyterlab/ui-components';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { DocumentRegistry } from '@jupyterlab/docregistry';

import * as _PACKAGE from '../package.json';

export const PACKAGE = _PACKAGE;

export const NS = PACKAGE.name;
export const VERSION = PACKAGE.version;
export const PLUGIN_ID = `${NS}:plugin`;

import { Diagram } from './editor';
import { DiagramDocument } from './document';

import ICON_SVG from '../style/img/drawio.svg';

/**
 * A namespace for commands
 */
export const CMD_NS = 'ipydrawio';

/**
 * The name of the factory that creates text-based diagram widgets.
 */
export const TEXT_FACTORY = 'Diagram';

/**
 * The name of the factory that creates binary-based diagram widgets.
 */
export const BINARY_FACTORY = 'Diagram Image';

/**
 * The name of the factory that creates JSON-based diagram widgets.
 */
export const JSON_FACTORY = 'Diagram Notebook';

/**
 * The raw icon SVG
 */
export const DRAWIO_ICON_SVG = ICON_SVG;

/**
 * The metadata key for diagrams in notebooks
 */
export const IPYDRAWIO_METADATA = NS;

/**
 * The extracted schema type
 */
import SCHEMA from './_schema';
/**
 * The concrete schema
 */
import SCHEMA_JSON from '../schema/plugin.json';

/**
 * Escape hatch for runtime debugging.
 */
export const DEBUG = window.location.href.indexOf('DRAWIO_DEBUG') > -1;

/**
 * A template which will appear in _Custom Diagram..._
 */
export interface ITemplate {
  /** A unique URL for template */
  url: string;
  /** The human-readable name for the template */
  label: string;
  /** The path to a thumbnail image */
  thumbnail?: string;
  /** A list of tags to help describe the template */
  tags?: string[];
}

/**
 * The main manager interface
 */
export interface IDiagramManager {
  addFormat(format: IFormat): void;
  formats: IFormat[];
  formatForModel(contentsModel: Partial<Contents.IModel>): IFormat | null;
  activeWidget: DiagramDocument | null;
  drawioURL: string;
  settings: ISettingRegistry.ISettings;
  escapeCurrent(widget: Widget): void;
  templates(): Promise<ITemplate[]>;
  addTemplates(...template: ITemplate[]): void;
  templatesChanged: ISignal<IDiagramManager, void>;
}

/**
 * A namespace for diagram manager concerns
 */
export namespace IDiagramManager {
  /**
   * Initialization options
   */
  export interface IOptions {}
}

/**
 * A regular expression for rewriting icons
 */
export const DRAWIO_ICON_CLASS_RE = /jp-icon-warn0/;

/**
 * A rank for adding to menus
 */
export const DIAGRAM_MENU_RANK = 99;

/**
 * A hoisted set definition of theme elements
 */
export type TUIThemes = SCHEMA.UITheme;

/**
 * A concrete list of themes
 */
export const UI_THEMES = SCHEMA_JSON.definitions['ui-theme'][
  'enum'
] as TUIThemes[];

/**
 * The theme color to replace
 */
export const UI_THEME_BASE_COLOR = '#f08705';

/**
 * A type for describing how to transform a UI theme branding
 */
export type TUIThemeOverrides = Record<SCHEMA.UITheme, [string, string][]>;

/**
 * Override colors for theme icons
 */
export const UI_THEME_COLORS: TUIThemeOverrides = {
  sketch: [[UI_THEME_BASE_COLOR, '#fff2a1']],
  dark: [[UI_THEME_BASE_COLOR, '#666']],
  min: [[UI_THEME_BASE_COLOR, '#eee']],
  kennedy: [[UI_THEME_BASE_COLOR, '#0052cc']],
  atlas: [[UI_THEME_BASE_COLOR, '#0049B0']],
};

/**
 * The token for the main extension, which can be used by other extensions
 */
export const IDiagramManager = new Token<IDiagramManager>(PLUGIN_ID);

/**
 * A namespace for capturing extension commands
 */
export namespace CommandIds {
  export const createNew = 'drawio:create-new';
  export const createNewCustom = 'drawio:create-new-custom';
  export const setUrlParams = 'drawio:url-params';
}

/**
 * The shape of a setUrlParams command
 */
export interface ISetUrlParamsArgs {
  drawioUrlParams: SCHEMA.DrawioURLParams;
}

/**
 * The shape of a createNew command
 */
export interface ICreateNewArgs extends ISetUrlParamsArgs {
  /**
   * The path in which to create a new untitled file.
   */
  cwd: string;
  /**
   * The format to use for a new file
   */
  format?: string;
  /**
   * The base name for a new file (without extension)
   */
  name?: string;
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

/*
  TODO: really didn't want to go here, but here we are

  - to learn more about what's _actually_ in there, load up the iframe in a console
    and look at `window.mxEvent`.
  - when you have scope on an App, look at `eventListeners`
*/
type TMXAppModelEvent =
  | 'backgroundColorChanged'
  | 'backgroundImageChanged'
  | 'connectionArrowsChanged'
  | 'connectionPointsChanged'
  | 'copyConnectChanged'
  | 'customFontsChanged'
  | 'foldingEnabledChanged'
  | 'formatWidthChanged'
  | 'gridColorChanged'
  | 'gridEnabledChanged'
  | 'guidesEnabledChanged'
  | 'mathEnabledChanged'
  | 'pageFormatChanged'
  | 'pageScaleChanged'
  | 'pageViewChanged'
  | 'pageViewChanged'
  | 'shadowVisibleChanged'
  | 'styleChanged';

export const MX_APP_MODEL_EVENTS: TMXAppModelEvent[] = [
  'backgroundColorChanged',
  'backgroundImageChanged',
  'connectionArrowsChanged',
  'connectionPointsChanged',
  'copyConnectChanged',
  'customFontsChanged',
  'foldingEnabledChanged',
  'formatWidthChanged',
  'gridColorChanged',
  'gridEnabledChanged',
  'guidesEnabledChanged',
  'mathEnabledChanged',
  'pageFormatChanged',
  'pageScaleChanged',
  'pageViewChanged',
  'pageViewChanged',
  'shadowVisibleChanged',
  'styleChanged',
];

type TMXMEditorEvent =
  | 'autosaveChanged'
  | 'fileLoaded'
  | 'fileLoaded'
  | 'pageSelected'
  | 'resetGraphView'
  | 'statusChanged';

export const MX_EDITOR_EVENTS: TMXMEditorEvent[] = [
  'autosaveChanged',
  'fileLoaded',
  'fileLoaded',
  'pageSelected',
  'resetGraphView',
  'statusChanged',
];

type TMXGraphEvent =
  | 'cellsAdded'
  | 'cellsInserted'
  | 'editingStarted'
  | 'editingStopped'
  | 'escape'
  | 'fireMouseEvent'
  | 'gesture'
  | 'gridSizeChanged'
  | 'moveCells'
  | 'pan'
  | 'resizeCells'
  | 'root'
  | 'shadowVisibleChanged'
  | 'size'
  | 'startEditing'
  | 'tapAndHold'
  | 'textInserted'
  | 'viewStateChanged';

export const MX_GRAPH_EVENTS: TMXGraphEvent[] = [
  'cellsAdded',
  'cellsInserted',
  'editingStarted',
  'editingStopped',
  'escape',
  'fireMouseEvent',
  'gesture',
  'gridSizeChanged',
  'moveCells',
  'pan',
  'resizeCells',
  'root',
  'shadowVisibleChanged',
  'size',
  'startEditing',
  'tapAndHold',
  'textInserted',
  'viewStateChanged',
];

type TMXGraphModelEvent = 'change';
export const MX_GRAPH_MODEL_EVENTS: TMXGraphModelEvent[] = ['change'];

type TMXGraphViewEvent =
  | 'down'
  | 'scale'
  | 'scaleAndTranslate'
  | 'translate'
  | 'undo'
  | 'unitChanged'
  | 'up';

export const MX_GRAPH_VIEW_EVENTS: TMXGraphViewEvent[] = [
  'down',
  'scale',
  'scaleAndTranslate',
  'translate',
  'undo',
  'unitChanged',
  'up',
];

export type TMXGraphPanningEvent = 'panStart' | 'panEnd' | 'pan';

export const MX_GRAPH_PAN_EVENTS: TMXGraphPanningEvent[] = [
  'panStart',
  'panEnd',
  'pan',
];

export type TMXGraphSelectionEvent = 'change';

export const MX_GRAPH_SELECT_EVENTS: TMXGraphSelectionEvent[] = ['change'];

export type TMXGraphSelectionModelEvent = 'change';

export const MX_GRAPH_SELECT_MODEL_EVENTS: TMXGraphSelectionModelEvent[] = [
  'change',
];

type TMXEvent =
  | TMXAppModelEvent
  | TMXGraphModelEvent
  | TMXGraphEvent
  | TMXGraphViewEvent
  | TMXGraphModelEvent
  | TMXGraphViewEvent
  | TMXMEditorEvent
  | TMXGraphPanningEvent
  | TMXGraphSelectionEvent;

// TODO: use an enum or something to make all these type nicely
export interface IMXEventHandler<T extends IMXEventSource = any> {
  (sender: T, evt: IMXEvent): void;
}

export interface IMXEventSource<T = TMXEvent> {
  addListener(name: T, handler: IMXEventHandler): void;
}

export interface IMXEvent {
  name: TMXEvent;
}

export interface IMXGraphModel extends IMXEventSource<TMXGraphModelEvent> {
  dx: number;
  dy: number;
}

export interface IMXGraphView extends IMXEventSource<TMXGraphViewEvent> {
  getScale(): number;
  setScale(scale: number): void;
  getTranslate(): IMXPoint;
  setTranslate(x: number, y: number): void;
  gridColor: string;
}

export interface IMXGraphPanningHandler
  extends IMXEventSource<TMXGraphPanningEvent> {}

export interface IMXGraphSelectionHandler
  extends IMXEventSource<TMXGraphSelectionEvent> {}

export interface IMXGraphSelectionModel
  extends IMXEventSource<TMXGraphSelectionModelEvent> {
  cells: IMXCell[];
  setCells(cells: IMXCell[]): void;
}

export interface IMXGraph extends IMXEventSource<TMXGraphEvent> {
  model: IMXGraphModel;
  view: IMXGraphView;
  panningHandler: IMXGraphPanningHandler;
  pageFormat: IMXRectangle;
  gridEnabled: boolean;
  setGridEnabled(gridEnabled: boolean): void;
  refresh(): void;
  setGridSize(size: number): void;
  gridSize: number;
  selectionCellsHandler: IMXGraphSelectionHandler;
  selectionModel: IMXGraphSelectionModel;
  getCellsById(id: string): IMXCell[];
}

export interface IMXEditor extends IMXEventSource<TMXMEditorEvent> {
  graph: IMXGraph;
}

// TODO: what does this do
export interface IMXPage extends IMXEventSource<any> {
  getId(): string;
}

export interface IMXApp extends IMXEventSource<TMXAppModelEvent> {
  editor: IMXEditor;
  container: HTMLBodyElement;
  pages: IMXPage[];
  currentPage: IMXPage;
  setPageFormat(pageFormat: IMXRectangle): void;
  selectPage(page: IMXPage): void;
  setGridColor(color: string): void;

  // DOM
  diagramContainer: HTMLDivElement;
}

export interface IMXPoint {
  x: number;
  y: number;
}

export interface IMXRectangle {
  height: number;
  width: number;
  x: number;
  y: number;
}

export interface IMXCell {
  getId(): string;
}

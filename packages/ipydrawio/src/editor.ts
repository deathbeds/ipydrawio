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

import { PromiseDelegate } from '@lumino/coreutils';
import { Message } from '@lumino/messaging';
import { Signal, ISignal } from '@lumino/signaling';

import { IFrame } from '@jupyterlab/apputils';

import '../style/index.css';
import { IFormat, DEBUG, IAdapter, IMXApp } from './tokens';

/**
 * Core URL params that are required to function properly
 */
const CORE_EMBED_PARAMS = {
  embed: 1,
  proto: 'json',
  configure: 1,
};

/**
 * Additional capabilities to allow to sandbox
 */
const SANDBOX_EXCEPTIONS: IFrame.SandboxExceptions[] = [
  'allow-downloads',
  'allow-forms',
  'allow-modals',
  'allow-orientation-lock',
  'allow-pointer-lock',
  'allow-popups',
  'allow-presentation',
  'allow-same-origin',
  'allow-scripts',
  'allow-top-navigation',
];

const DRAWIO_CLASS = 'jp-Diagram';

const READY_CLASS = 'jp-Diagram-ready';

export namespace Diagram {
  export interface IOptions extends IFrame.IOptions {
    adapter: IAdapter;
  }
}

/**
 * A document for using offline drawio in an iframe
 */
export class Diagram extends IFrame {
  adapter: IAdapter;
  private _ready = new PromiseDelegate<void>();
  public revealed: Promise<void>;
  private _initialLoad = false;
  private _exportPromise: PromiseDelegate<string> | null;
  private _saveWithExportPromise: PromiseDelegate<string> | null;
  private _frame: HTMLIFrameElement;
  private _lastEmitted: string;
  private _frameClicked = new Signal<Diagram, void>(this);
  private _app: IMXApp;
  private _appChanged = new Signal<Diagram, void>(this);
  private _escaped = new Signal<Diagram, void>(this);

  constructor(options: Diagram.IOptions) {
    super({ sandbox: SANDBOX_EXCEPTIONS, ...options });
    this.addClass(DRAWIO_CLASS);
    this.adapter = options.adapter;
  }

  /**
   * Get a an export string in one of the supported formats.
   */
  exportAs(format: string): Promise<string> {
    this._exportPromise = new PromiseDelegate();

    this.postMessage({ action: 'export', format });

    return this._exportPromise.promise;
  }

  get app() {
    return this._app;
  }

  set app(app) {
    DEBUG && console.warn('drawio app', app);
    if (this._app != app) {
      this._app = app;
      if (app == null) {
        console.warn('drawio app was not available');
      } else {
        // TODO: get a much better understanding of this
        app?.container.addEventListener('mousedown', () => {
          this._frameClicked.emit(void 0);
        });
      }
      this._appChanged.emit(void 0);
    }

    // TODO: restore as real feature
    // if (this._app) {
    //   const file = this._app.getCurrentFile();
    //   file.sync = new (this._frame.contentWindow as any).DrawioFileSync(file);
    //   file.sync.start();
    // }
  }

  /**
   * A signal emitted when the underlying drawio app changes
   */
  get appChanged() {
    return this._appChanged;
  }

  /**
   * A signal emitted when the user indicates they want to return focus to the main app
   */
  get escaped(): ISignal<Diagram, void> {
    return this._escaped;
  }

  /**
   * Handle messages from the iframe over the drawio embed protocol
   */
  handleMessageEvent(evt: MessageEvent) {
    let msg: any;

    try {
      msg = JSON.parse(evt.data);
    } catch {
      return;
    }

    if (
      this._frame?.contentWindow == null ||
      evt.source !== this._frame.contentWindow
    ) {
      return;
    }

    DEBUG && console.warn('drawio message received', msg);

    switch (msg.event) {
      case 'configure':
        this.configureDrawio();
        break;
      case 'init':
        this.onContentChanged();
        break;
      case 'load':
        this.app = (this._frame?.contentWindow as any).IPYDRAWIO_APP;
        this._ready.resolve(void 0);
        this._initialLoad = true;
        this.addClass(READY_CLASS);
        break;
      case 'save':
        if (this.format?.isTransformed) {
          this.saveWithExport(true);
          break;
        }
        this._lastEmitted = msg.xml;
        this.save(msg.xml, true);
        break;
      case 'autosave':
        if (this.adapter.saveNeedsExport()) {
          this.saveWithExport();
          break;
        }
        this._lastEmitted = msg.xml;
        this.save(msg.xml);
        break;
      case 'export':
        if (this._exportPromise != null) {
          this._exportPromise.resolve(msg.data);
          this._exportPromise = null;
        }

        if (this._saveWithExportPromise != null) {
          this._saveWithExportPromise.resolve(msg.data);
          this._saveWithExportPromise = null;
        }
        break;
      default:
        DEBUG && console.warn('unhandled message', msg.event, msg);
        break;
    }
  }

  /**
   * Install the message listener, the first time, and potentially reload the frame
   */
  onAfterShow(msg?: Message): void {
    if (this._frame?.contentWindow == null) {
      this._frame = this.node.querySelector('iframe') as HTMLIFrameElement;
      window.addEventListener('message', (evt) => this.handleMessageEvent(evt));
      // this.maybeReloadFrame();
    }
    this.maybeReloadFrame();
  }

  private save(xml: string, hardSave: boolean = false) {
    this.adapter.fromXML(xml, hardSave);
  }

  /**
   * Handle round-tripping to formats that require an export
   */
  private saveWithExport(hardSave: boolean = false) {
    const { format } = this;
    if (format == null) {
      console.warn('cannot save without context');
      return;
    }
    const { mimetype } = format;
    if (format?.save == null) {
      console.error(`Unexpected save with export of ${mimetype}`);
      return;
    }
    this._saveWithExportPromise = new PromiseDelegate();
    this.postMessage({
      action: 'export',
      format: format.key,
    });
    this._saveWithExportPromise.promise
      .then((raw) => {
        if (format?.save == null) {
          console.warn('format cannot save', format);
          return;
        }
        const stripped = format.save(raw);
        if (stripped === this._lastEmitted) {
          return;
        }
        this._lastEmitted = stripped;
        this.save(stripped, hardSave);
      })
      .catch((err) => {
        console.error(err);
      });
  }

  /**
   * Prepare and post the message for configuring the drawio application
   */
  private configureDrawio() {
    let settingsConfig = this.adapter.drawioConfig();
    const config = {
      ...(settingsConfig || {}),
      version: `${+new Date()}`,
    };
    DEBUG && console.warn('configuring drawio', config);
    this.postMessage({ action: 'configure', config });
  }

  /**
   * Post to the iframe, if available. Should be buffered?
   */
  private postMessage(msg: any) {
    if (this._frame?.contentWindow == null) {
      return false;
    }
    this._frame.contentWindow.postMessage(JSON.stringify(msg), '*');
    return true;
  }

  /**
   * Determine the URL for the iframe src, reload if changed
   */
  maybeReloadFrame(force: boolean = false) {
    if (this.isHidden || !this.isVisible) {
      return;
    }
    const query = new URLSearchParams();
    const settingsUrlParams = this.adapter.urlParams();
    const params = {
      ...(settingsUrlParams || {}),
      ...CORE_EMBED_PARAMS,
    };
    // [p]lugins should not be URL encoded
    let plugins = '';
    for (const p in params) {
      if (p == 'p') {
        plugins = (params as any)[p];
        continue;
      }
      query.append(p, (params as any)[p]);
    }
    const url =
      this.adapter.drawioUrl() + '?' + query.toString() + `&p=${plugins}`;

    if (force || this.url !== url) {
      DEBUG && console.warn('configuring iframe', params);
      this.removeClass(READY_CLASS);
      this.url = url;
      this._initialLoad = false;
      this._frame.onload = () => {
        this._frame.contentDocument?.addEventListener('keydown', (evt) => {
          switch (evt.keyCode) {
            case 27: // escape
              this._escaped.emit(void 0);
              break;
            default:
              break;
          }
        });

        if (this._frame.contentDocument == null) {
          console.warn('contentDocument not ready');
          return;
        }
      };
    }
  }

  /**
   * Handle a change to the raw document
   */
  onContentChanged(): void {
    if (!this._frame?.contentWindow || !this.format) {
      DEBUG &&
        console.warn(
          'contentWindow or format not ready',
          this._frame?.contentWindow,
          this.format
        );
      return;
    }

    let xml = this.adapter.toXML();

    if (xml === this._lastEmitted) {
      DEBUG && console.warn('content has not changed');
      return;
    }

    if (this.format.modelName === 'base64') {
      xml = `data:${this.format.mimetype};base64,${xml}`;
    }

    if (!this._initialLoad) {
      this.postMessage({
        action: 'load',
        autosave: 1,
        noSaveBtn: 1,
        noExitBtn: 1,
        xml,
      });
    } else {
      this.postMessage({
        action: 'merge',
        xml,
      });
    }
  }

  load(xml: string) {
    this.postMessage({
      action: 'load',
      xml,
    });
  }

  get format(): IFormat | null {
    return this.adapter.format();
  }

  get frameClicked() {
    return this._frameClicked;
  }

  /**
   * A promise that resolves when drawio is ready.
   */
  get ready(): Promise<void> {
    return this._ready.promise;
  }
}

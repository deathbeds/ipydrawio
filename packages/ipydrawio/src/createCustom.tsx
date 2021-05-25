import * as React from 'react';

import { Signal, ISignal } from '@lumino/signaling';
import { VDomModel, VDomRenderer } from '@jupyterlab/apputils';
import {
  ICreateNewArgs,
  IDiagramManager,
  IFormat,
  ITemplate,
  UI_THEMES,
} from './tokens';
import * as IO from './io';
import * as SCHEMA from './_schema';

const CARDS = 'jp-IPyDiagram-cards';

const NULL_TEMPLATE: ITemplate = {
  label: 'blank',
  url: '',
  thumbnail: '',
  tags: [],
};

const FULL_UI = ['pages', 'layers'];
const DARK = ['dark'];
const LIGHT = ['light'];

let THEME_TAGS: Record<SCHEMA.UITheme, string[]> = {
  kennedy: [...FULL_UI, ...LIGHT],
  dark: [...FULL_UI, ...DARK],
  sketch: [...LIGHT, ...DARK],
  min: [...FULL_UI, ...LIGHT, ...DARK],
  atlas: [...FULL_UI, ...LIGHT],
};

export class CreateCustom extends VDomRenderer<CreateCustom.Model> {
  constructor(model: CreateCustom.Model) {
    super(model);
    this.title.icon = IO.drawioIcon;
    this.title.label = 'New Diagram';
    this.addClass('jp-IPyDiagram-CreateCustom');
    this.addClass('jp-RenderedHTMLCommon');
  }

  protected render(): JSX.Element[] {
    const icon = IO.drawioThemeIcons[this.model.ui || this.model.settingsUi];
    let what = this.model.template?.label || NULL_TEMPLATE.label;
    what = `${what} ${this.model.format.ext}`;
    return [
      <header key="header">
        <h1>New Diagram</h1>
        <input
          type="text"
          className="jp-mod-styled"
          defaultValue={this.model.name}
          placeholder="untitled"
          onChange={(evt) => (this.model.name = evt.currentTarget.value)}
        />
        <button
          onClick={this.model.requestDocument}
          type="button"
          className="jp-mod-styled jp-mod-accept"
        >
          <icon.react width={24} tag="span" />
          <label>NEW {what.toLocaleUpperCase()}</label>
        </button>
      </header>,
      <form key="form">
        {this.renderFormats()}
        {this.renderThemes()}
        {this.renderTemplates()}
      </form>,
    ];
  }

  protected renderFormats() {
    return (
      <section>
        <h2>Format</h2>
        <ul className={CARDS}>{this.model.formats.map(this.renderFormat)}</ul>
      </section>
    );
  }

  protected renderThemes() {
    return (
      <section>
        <h2>Theme</h2>
        <ul className={CARDS}>
          {this.renderTheme(null, -1)}
          {UI_THEMES.map(this.renderTheme)}
        </ul>
      </section>
    );
  }

  protected renderTemplates() {
    return (
      <section>
        <h2>
          Template{' '}
          <input
            type="text"
            className="jp-mod-styled"
            onChange={this.onSearch}
            title="Search Templates"
            placeholder="Search Templates"
          ></input>
        </h2>
        <ul className={CARDS}>
          {this.renderTemplate(NULL_TEMPLATE, -1)}
          {this.model.templates.map(this.renderTemplate)}
        </ul>
      </section>
    );
  }

  onSearch = (evt: React.ChangeEvent<HTMLInputElement>) => {
    this.model.templateSearchText = evt.currentTarget.value;
  };

  protected renderFormat = (format: IFormat, index: number) => {
    const id = `ipydrawio-format-${format.name}`;
    let tags: string[] = [];
    if (format.isBinary) {
      tags.push('binary');
    }
    if (format.isText) {
      tags.push('text');
    }
    if (format.isJson) {
      tags.push('json');
    }
    return (
      <li key={format.name} data-ipydrawio-format={format.ext}>
        <input
          type="radio"
          name="ipydrawio-format"
          id={id}
          onChange={() => (this.model.format = format)}
          defaultChecked={!index}
        />
        <label htmlFor={id}>
          <code>{format.ext}</code>
          <format.icon.react width={100} tag="span"></format.icon.react>
          {this.renderTags(tags)}
        </label>
      </li>
    );
  };

  protected renderTheme = (
    theme: SCHEMA.UITheme | null,
    index: number = -1
  ) => {
    const effectiveTheme = theme ? theme : this.model.settingsUi;
    const icon = IO.drawioThemeIcons[effectiveTheme];
    const id = `ipydrawio-theme-${index}`;
    const tags = [...THEME_TAGS[effectiveTheme], ...(theme ? [] : ['default'])];
    return (
      <li key={theme} data-ipydrawio-theme={theme}>
        <input
          type="radio"
          name="ipydrawio-theme"
          id={id}
          onChange={() => (this.model.ui = theme)}
          defaultChecked={index === -1}
        />
        <label htmlFor={id}>
          {effectiveTheme}
          <icon.react width={100} tag="span" />
          {this.renderTags(tags)}
        </label>
      </li>
    );
  };

  protected renderTemplate = (template: ITemplate, index: number = -1) => {
    const id = `ipydrawio-template-${index}`;
    return (
      <li
        key={template.url || '__blank__'}
        data-ipydrawio-template={template.url}
      >
        <input
          type="radio"
          name="ipydrawio-template"
          id={id}
          value={template.url}
          onChange={() => (this.model.template = template)}
          defaultChecked={index === -1}
        ></input>
        <label htmlFor={id}>
          {template.label}
          {template.thumbnail ? <img src={template.thumbnail}></img> : []}
          {this.renderTags(template.tags || [])}
        </label>
      </li>
    );
  };

  protected renderTags(tags: string[]) {
    return <ul className="jp-IPyDiagram-tags">{tags.map(this.renderTag)}</ul>;
  }

  protected renderTag = (tag: string) => {
    return <li key={tag}>{tag}</li>;
  };
}

export namespace CreateCustom {
  export interface IOptions {
    manager: IDiagramManager;
  }

  export class Model extends VDomModel {
    private _manager: IDiagramManager;
    private _templates: ITemplate[] = [];
    private _ui: SCHEMA.UITheme | null;
    private _template: ITemplate;
    private _templateSearchText = '';
    private _documentRequested = new Signal<Model, void>(this);
    private _format: IFormat = IO.XML_NATIVE;
    private _name: string = '';

    constructor(options: IOptions) {
      super();
      this._manager = options.manager;
      this._manager
        .templates()
        .then((templates) => {
          this._templates = templates;
          this.stateChanged.emit(void 0);
        })
        .catch(console.warn);
    }

    get args() {
      return {
        name: this._name,
        format: this._format.key,
        drawioUrlParams: {
          ...(this._ui ? { ui: this._ui } : {}),
          ...(this._template
            ? { 'template-filename': this._template.url }
            : {}),
        },
      } as ICreateNewArgs;
    }

    get manager() {
      return this._manager;
    }

    get name() {
      return this._name;
    }

    set name(name: string) {
      this._name = name;
      this.stateChanged.emit(void 0);
    }

    get templates() {
      const query = this._templateSearchText.trim().split(' ');
      if (!query.length) {
        return this._templates;
      }

      let matches: ITemplate[] = [];

      for (const template of this._templates) {
        let hits = 0;
        const text = `${template.label} ${(template.tags || []).join(' ')}`;

        for (const q of query) {
          if (text.indexOf(q) !== -1) {
            hits++;
          }
        }

        if (hits === query.length) {
          matches.push(template);
        }
      }

      return matches;
    }

    get formats() {
      const formats = this._manager.formats.filter((f) => f.isEditable);
      formats.sort((a, b) => a.ext.length - b.ext.length);
      return formats;
    }

    get format() {
      return this._format;
    }

    set format(format: IFormat) {
      this._format = format;
      this.stateChanged.emit(void 0);
    }

    get ui() {
      return this._ui;
    }

    set ui(ui: SCHEMA.UITheme | null) {
      this._ui = ui;
      this.stateChanged.emit(void 0);
    }

    get template() {
      return this._template;
    }

    set template(template: ITemplate) {
      this._template = template;
      this.stateChanged.emit(void 0);
    }

    set templateSearchText(searchText: string) {
      this._templateSearchText = searchText;
      this.stateChanged.emit(void 0);
    }

    get templateSearchText() {
      return this._templateSearchText;
    }

    get settingsUi(): SCHEMA.UITheme {
      const params: any =
        (this._manager.settings.composite || {})['drawioUrlParams'] || {};
      return params['ui'] ? params['ui'] : 'kennedy';
    }

    get documentRequested(): ISignal<Model, void> {
      return this._documentRequested;
    }

    requestDocument = () => {
      this._documentRequested.emit(void 0);
    };
  }
}

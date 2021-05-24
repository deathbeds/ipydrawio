/*
  Copyright 2021 ipydrawio contributors

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

import { PageConfig } from '@jupyterlab/coreutils';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { DEBUG, Diagram } from '@deathbeds/ipydrawio';

import { PDFStatus } from './status';

const DEFAULT_EXPORT_URL = './ipydrawio/export/';
const DEFAULT_STATUS_URL = './ipydrawio/status';
const DEFAULT_PROVISION_URL = './ipydrawio/provision';
const DATA_URI_PREFIX = 'application/pdf;base64';

export class DrawioPDFManager {
  status: PDFStatus.Model;

  constructor() {
    this.status = new PDFStatus.Model();
  }

  async fetchStatus() {
    const url = this.statusUrl();
    if (url == null) {
      return;
    }
    const response = await fetch(url, { method: 'GET' });

    if (response.status >= 400) {
      console.warn('Unknown PDF status', response);
      return null;
    }

    const status = await response.json();
    this.status.running = status.is_running;
    this.status.provisioned = status.is_provisioned;
    this.status.provisioning = status.is_provisioning;
    this.status.starting = status.is_starting;
  }

  async provision() {
    await this.fetchStatus();
    const url = this.provisionUrl();
    if (url == null) {
      return;
    }

    const request = fetch(url, {
      method: 'POST',
      headers: this.defaultHeaders(),
    });

    await this.fetchStatus();

    const response = await request;

    if (response.status >= 400) {
      console.warn('PDF provision failed', response);
      return null;
    }

    await this.fetchStatus();
  }

  defaultHeaders() {
    return {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-XSRFToken': Private.getCookie('_xsrf') || '',
    };
  }

  exportUrl(settings: ISettingRegistry.ISettings) {
    let url = DEFAULT_EXPORT_URL;
    try {
      url = (settings?.composite?.drawioExportUrl as any)['url'];
    } catch (err) {
      DEBUG && console.warn('using fallback url', err);
    }
    if (url.indexOf('./') !== 0) {
      console.error(`don't know how to handle non-relative URLs`);
      return null;
    }
    return `${PageConfig.getBaseUrl()}${url.slice(2)}`;
  }

  statusUrl() {
    let url = DEFAULT_STATUS_URL;
    if (url.indexOf('./') !== 0) {
      console.error(`don't know how to handle non-relative URLs`);
      return null;
    }
    return `${PageConfig.getBaseUrl()}${url.slice(2)}`;
  }

  provisionUrl() {
    let url = DEFAULT_PROVISION_URL;
    if (url.indexOf('./') !== 0) {
      console.error(`don't know how to handle non-relative URLs`);
      return null;
    }
    return `${PageConfig.getBaseUrl()}${url.slice(2)}`;
  }

  exportPDF = async (
    widget: Diagram,
    key: string,
    settings: ISettingRegistry.ISettings
  ) => {
    await this.fetchStatus();

    let url = this.exportUrl(settings);

    if (url == null) {
      return null;
    }

    const xml = widget.adapter.toXML();

    url += url.endsWith('/') ? '' : '/';
    const query = new URLSearchParams();
    // TODO: expose, understand, schematize this form API
    query.append('xml', xml);
    query.append('format', 'pdf');
    query.append('base64', '1');

    const response = await fetch(url, {
      method: 'POST',
      headers: this.defaultHeaders(),
      body: query.toString(),
    });

    if (response.status >= 400) {
      console.warn('PDF export failed', response);
      return null;
    }

    const text = await response.text();

    return `${DATA_URI_PREFIX},${text}`;
  };
}

namespace Private {
  export function getCookie(name: string): string | undefined {
    // From http://www.tornadoweb.org/en/stable/guide/security.html
    const matches = document.cookie.match('\\b' + name + '=([^;]*)\\b');
    return matches?.[1];
  }
}

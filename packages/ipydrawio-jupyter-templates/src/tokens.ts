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

import { ITemplate } from '@deathbeds/ipydrawio';
import * as PACKAGE_ from '../package.json';

import { PageConfig, URLExt } from '@jupyterlab/coreutils';

import '!!file-loader?name=[path][name].[ext]&context=.!../tmpl/JupyterLab Mockups.dio';
import '!!file-loader?name=[path][name].[ext]&context=.!../tmpl/JupyterLab Mockups.png';

/**
 * The hoisted `package.json`
 */
export const PACKAGE = PACKAGE_;

/**
 * The namespace for template-level concerns
 */
export const NS = PACKAGE.name;

/**
 * The plugin id
 */
export const PLUGIN_ID = `${NS}:plugin`;

export const TEMPLATE_BASE = URLExt.join(
  PageConfig.getOption('fullLabextensionsUrl'),
  NS,
  'static/tmpl'
);

/** The static templates */
export const TEMPLATES: ITemplate[] = [
  {
    url: 'JupyterLab Mockups.dio',
    tags: ['jupyter', 'mockup', 'lab'],
  },
].map((tmpl) => {
  return {
    ...tmpl,
    label: tmpl.url.replace(/.dio$/, ''),
    url: URLExt.join(TEMPLATE_BASE, tmpl.url),
    thumbnail: URLExt.join(TEMPLATE_BASE, tmpl.url.replace(/.dio$/, '.png')),
  };
});

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

import { JupyterLab, JupyterFrontEndPlugin } from '@jupyterlab/application';

import { IDiagramManager } from '@deathbeds/ipydrawio';

import { PLUGIN_ID, TEMPLATES } from './tokens';

/**
 * The Jupyter template plugin.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  activate,
  id: PLUGIN_ID,
  requires: [IDiagramManager],
  autoStart: true,
};

/** Activate the Jupyter templates plugin */
function activate(app: JupyterLab, diagrams: IDiagramManager) {
  diagrams.addTemplates(...TEMPLATES);
}

export default plugin;

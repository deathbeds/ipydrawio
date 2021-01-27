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
import {
  DRAWIO_ICON_CLASS_RE,
  DRAWIO_ICON_SVG,
  IFormat,
} from '@deathbeds/ipydrawio/lib/tokens';

import { stripDataURI } from '@deathbeds/jupyterlab-drawio/lib/utils';

import { LabIcon } from '@jupyterlab/ui-components';

export const drawioPdfIcon = new LabIcon({
  name: 'drawio:pdf',
  svgstr: DRAWIO_ICON_SVG.replace(DRAWIO_ICON_CLASS_RE, 'jp-icon-contrast2'),
});

export const PDF_PLAIN: IFormat = {
  ext: '.pdf',
  format: 'base64',
  factoryName: `Diagram (PDF)`,
  icon: drawioPdfIcon,
  key: 'pdf',
  label: 'PDF',
  mimetype: 'application/pdf',
  modelName: 'base64',
  name: 'pdf',
  isExport: true,
  isBinary: true,
  isTransformed: true,
  save: stripDataURI,
  // this is replaced with the manager function
  exporter: async (widget, key, settings) => null,
};

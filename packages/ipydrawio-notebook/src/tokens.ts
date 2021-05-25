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

import * as PACKAGE_ from '../package.json';

/**
 * The hoisted `package.json`
 */
export const PACKAGE = PACKAGE_;

/**
 * The namespace for notebook-level concerns
 */
export const NS = PACKAGE.name;

/**
 * The plugin id
 */
export const PLUGIN_ID = `${NS}:plugin`;

/**
 * The command namespace
 */
export const CMD_NS = 'ipydrawio-notebook';

/**
 * A namespace for diagram notebook commands
 */
export namespace CommandIds {
  export const open = `${CMD_NS}:open`;
}

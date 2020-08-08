// Copyright 2020 Dead Pixels Collective
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

let DEBUG = false;

const plugin = {
  id: "@deathbeds/jupyterlab-drawio-webpack:plugin",
  activate: async () => {
    console.log("activating", plugin.id);
    if(DEBUG) {
      await import("./_static");
    }
    console.log("activated", plugin.id);
  },
  autoStart: true
};

export default plugin;

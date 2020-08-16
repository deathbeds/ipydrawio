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
import React from 'react';

import { VDomRenderer, VDomModel } from '@jupyterlab/apputils';

import { drawioPdfIcon } from './io';

import { interactiveItem, TextItem, GroupItem } from '@jupyterlab/statusbar';

namespace PDFStatusComponent {
  export interface IProps {
    provisioned: boolean;
    running: boolean;
    starting: boolean;
    provisioning: boolean;
  }
}

/**
 * A pure functional component for rendering the Drawio status.
 */
function PDFStatusComponent(
  props: PDFStatusComponent.IProps
): React.ReactElement<PDFStatusComponent.IProps> {
  const { provisioning, provisioned, running, starting } = props;
  let status = provisioning
    ? 'provisioning...'
    : starting
    ? 'starting...'
    : running
    ? 'running'
    : provisioned
    ? 'ready'
    : 'not provisioned';
  return (
    <GroupItem spacing={4}>
      <TextItem
        source={status}
        title={`Drawio PDF export server is ${status}`}
      />
      <drawioPdfIcon.react stylesheet={'statusBar'} />
    </GroupItem>
  );
}

/**
 * A VDomRenderer for Drawio PDF status
 */
export class PDFStatus extends VDomRenderer<PDFStatus.Model> {
  /**
   * Create a new tab/space status item.
   */
  constructor(model: PDFStatus.Model) {
    super(model);
    this.addClass(interactiveItem);
  }

  render(): React.ReactElement<PDFStatusComponent.IProps> | null {
    if (this.model == null) {
      return null;
    } else {
      return (
        <PDFStatusComponent
          provisioned={this.model.provisioned}
          running={this.model.running}
          provisioning={this.model.provisioning}
          starting={this.model.starting}
        />
      );
    }
  }
}

export namespace PDFStatus {
  export class Model extends VDomModel {
    protected _provisioned = false;
    protected _running = false;
    protected _provisioning = false;
    protected _starting = false;

    get provisioned() {
      return this._provisioned;
    }

    set provisioned(provisioned) {
      if (this._provisioned !== provisioned) {
        this._provisioned = provisioned;
        this.stateChanged.emit(void 0);
      }
    }

    get running() {
      return this._running;
    }

    set running(running) {
      if (this._running !== running) {
        this._running = running;
        this.stateChanged.emit(void 0);
      }
    }

    get starting() {
      return this._starting;
    }

    set starting(starting) {
      if (this._starting !== starting) {
        this._starting = starting;
        this.stateChanged.emit(void 0);
      }
    }

    get provisioning() {
      return this._starting;
    }

    set provisioning(provisioning) {
      if (this._provisioning !== provisioning) {
        this._provisioning = provisioning;
        this.stateChanged.emit(void 0);
      }
    }
  }

  export interface IOptions {
    //
  }
}

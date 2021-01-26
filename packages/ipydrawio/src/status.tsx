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
import React from 'react';

import { VDomRenderer, VDomModel } from '@jupyterlab/apputils';

import {
  interactiveItem,
  clickedItem,
  Popup,
  showPopup,
  TextItem,
} from '@jupyterlab/statusbar';

import { Menu } from '@lumino/widgets';

namespace DrawioStatusComponent {
  export interface IProps {
    /**
     * A simple status
     */
    status: string;
    handleClick: () => void;
  }
}

/**
 * A pure functional component for rendering the Drawio status.
 */
function DrawioStatusComponent(
  props: DrawioStatusComponent.IProps
): React.ReactElement<DrawioStatusComponent.IProps> {
  if (!props.status?.length) {
    return <span></span>;
  }
  return (
    <TextItem
      onClick={props.handleClick}
      source={`drawio: ${props.status || 'ready'}`}
      title={`TBD…`}
    />
  );
}

/**
 * A VDomRenderer for Drawio status
 */
export class DrawioStatus extends VDomRenderer<DrawioStatus.Model> {
  /**
   * Create a new tab/space status item.
   */
  constructor(model: DrawioStatus.Model) {
    super(model);
    this.addClass(interactiveItem);
  }

  render(): React.ReactElement<DrawioStatusComponent.IProps> | null {
    if (this.model == null) {
      return null;
    } else {
      return (
        <DrawioStatusComponent
          handleClick={() => this._handleClick()}
          status={this.model.status}
        />
      );
    }
  }

  /**
   * Handle a click on the status item.
   */
  private _handleClick(): void {
    const menu = this._menu;
    if (this._popup) {
      this._popup.dispose();
    }

    menu.aboutToClose.connect(this._menuClosed, this);

    this._popup = showPopup({
      body: menu,
      anchor: this,
      align: 'right',
    });
  }

  private _menuClosed(): void {
    this.removeClass(clickedItem);
  }

  private _menu: Menu;
  private _popup: Popup | null = null;
}

export namespace DrawioStatus {
  export class Model extends VDomModel {
    _status: string = '';

    get status() {
      return this._status;
    }

    set status(status) {
      if (this._status != status) {
        this._status = status;
        this.stateChanged.emit(void 0);
      }
    }
  }

  export interface IOptions {
    //
  }
}

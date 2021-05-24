# Copyright 2021 ipydrawio contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#                 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

*** Variables ***
${FIXTURES}       ${CURDIR}${/}fixtures
${NBSERVER CONF}    jupyter_notebook_config.json
${SPLASH}         id:jupyterlab-splash
# to help catch hard-coded paths
${BASE}           /@est/
# override with `python scripts/atest.py --variable HEADLESS:0`
${HEADLESS}       1
${CMD PALETTE INPUT}    css:#command-palette .lm-CommandPalette-input
${CMD PALETTE ITEM ACTIVE}    css:#command-palette .lm-CommandPalette-item.lm-mod-active
${JLAB XP TOP}    //div[@id='jp-top-panel']
${JLAB XP MENU ITEM LABEL}    //div[contains(@class, 'lm-Menu-itemLabel')]
${JLAB XP MENU LABEL}    //div[contains(@class, 'lm-MenuBar-itemLabel')]
${JLAB XP DOCK TAB}    xpath://div[contains(@class, 'lm-DockPanel-tabBar')]//li[contains(@class, 'lm-TabBar-tab')]
${JLAB CSS VERSION}    css:.jp-About-version
${CSS DIALOG OK}    css:.jp-Dialog .jp-mod-accept
${MENU OPEN WITH}    xpath://div[contains(@class, 'lm-Menu-itemLabel')][contains(text(), "Open With")]
# N is missing on purpose
${MENU NOTEBOOK}    xpath://div[contains(@class, 'lm-Menu-itemLabel')][contains(., "otebook")]
${DIALOG WINDOW}    css:.jp-Dialog
${DIALOG INPUT}    css:.jp-Input-Dialog input
${DIALOG ACCEPT}    css:button.jp-Dialog-button.jp-mod-accept
# TODO: get ours
# ${STATUSBAR}    css:div.lsp-statusbar-item
${MENU EDITOR}    xpath://div[contains(@class, 'lm-Menu-itemLabel')][contains(., "Editor")]
${MENU SETTINGS}    xpath://div[contains(@class, 'lm-MenuBar-itemLabel')][contains(text(), "Settings")]
${MENU RENAME}    xpath://div[contains(@class, 'lm-Menu-itemLabel')][contains(., "ename")]
# settings
${DIO PLUGIN ID}    @deathbeds/ipydrawio:plugin
${DIO PLUGIN SETTINGS FILE}    @deathbeds${/}ipydrawio${/}plugin.jupyterlab-settings
${CSS USER SETTINGS}    .jp-SettingsRawEditor-user
${JLAB XP CLOSE SETTINGS}    ${JLAB XP DOCK TAB}\[contains(., 'Settings')]/*[contains(@class, 'm-TabBar-tabCloseIcon')]
# launcher
${XP LAUNCH TAB}    ${JLAB XP DOCK TAB}//*[contains(text(), 'Launcher')]
${CSS LAUNCHER}    css:.jp-Launcher-body
${CSS LAUNCH DIO}    css:.jp-LauncherCard[title='Create a blank .dio file'] svg
${CSS LAUNCH ADVANCED}    css:.jp-LauncherCard[title='Create a diagram with customized formats, templates, and UI'] svg
${CSS LAUNCH IPYNB}    css:.jp-LauncherCard[data-category='Notebook'][title='Python 3'] .jp-LauncherCard-icon
${CSS DIO READY}    css:.jp-Diagram-ready
${CSS DIO IFRAME}    ${CSS DIO READY} iframe
# drawio
${CSS DIO BG}     css:.geDiagramContainer svg
${CSS DIO SHAPE POPUP}    css:.geToolbarContainer.geSidebarContainer.geSidebar
${CSS DIO SHAPE POPUP SHAPE}    ${CSS DIO SHAPE POPUP} .geItem
${CSS DIO EDITABLE}    css:.mxCellEditor.geContentEditable
# advanced
${CSS CREATE ADVANCED}    css:.jp-IPyDiagram-CreateAdvanced
${CSS ACCEPT ADVANCED}    ${CSS CREATE ADVANCED} header .jp-mod-accept
# from jupyterlibrary
${JLAB CSS ACCEPT}    .jp-mod-accept
${JLAB CSS ACTIVE DOC}    .jp-Document:not(.jp-mod-hidden)
${JLAB CSS ACTIVE DOC CELLS}    ${JLAB CSS ACTIVE DOC} .jp-Cell
${JLAB CSS ACTIVE CELL}    ${JLAB CSS ACTIVE DOC} .jp-Cell.jp-mod-active
${JLAB CSS ACTIVE INPUT}    ${JLAB CSS ACTIVE CELL} .CodeMirror
${JLAB CSS ACTIVE OUTPUT CHILDREN}    ${JLAB CSS ACTIVE CELL} .jp-OutputArea-child
${JLAB CSS OUTPUT}    .jp-OutputArea-output
${JLAB CSS ACTIVE CELL MARKDOWN}    ${JLAB CSS ACTIVE CELL} .jp-MarkdownOutput:not(.jp-mod-hidden)
${JLAB CSS ACTIVE SIDEBAR}    .jp-SideBar .p-TabBar-tab.p-mod-current
${JLAB CSS BUSY KERNEL}    .jp-Toolbar-kernelStatus.jp-FilledCircleIcon
${JLAB CSS CMD INPUT}    .p-CommandPalette-input
${JLAB CSS CMD ITEM}    .p-CommandPalette-item
${JLAB CSS NB TOOLBAR}    .jp-NotebookPanel-toolbar
${JLAB CSS SIDEBAR TAB}    .jp-SideBar .p-TabBar-tab
${JLAB CSS SPINNER}    .jp-Spinner
${JLAB ID SPLASH}    jupyterlab-splash
${JLAB TEXT BUSY PROMPT}    In [*]:
${JLAB XP CARD}    //div[@class='jp-LauncherCard']
${JLAB XP DOCK}    //div[@id='jp-main-dock-panel']
${JW XP ACCORD CHILD}    //div[contains(@class, '-Accordion-child')]
${JW XP ACCORD CHILD HEAD}    ${JW XP ACCORD CHILD}/div[contains(@class, 'p-Collapse-header')]
# notebook
${JLAB CSS ICON ADD}    .jp-ToolbarButtonComponent [data-icon='ui-components:add']
${JLAB CSS ICON RUN}    .jp-ToolbarButtonComponent [data-icon='ui-components:run']
${XP DIO FORMAT TITLE}    //*[contains(@class, 'mxWindowTitle')][contains(text(), 'Format')]
${XP DIO FORMAT TOGGLE}    ${XP DIO FORMAT TITLE}/div
${XP DIO FORMAT PANE}    ${XP DIO FORMAT TITLE}/../..//td/div[contains(@class, 'mxWindowPane')]
${XP DIO FORMAT PANE VISIBLE}    ${XP DIO FORMAT PANE}\[not(contains(@style, 'display: none'))]
${XP DIO PAGE SIZE}    //div[contains(@class, "geFormatSection")][contains(., "Paper Size")]//select
# mime
${MIME STDERR}    application/vnd.jupyter.stderr

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
${JLAB XP MENU ITEM LABEL}    //div[@class='lm-Menu-itemLabel']
${JLAB XP MENU LABEL}    //div[@class='lm-MenuBar-itemLabel']
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
# settings
${DIO PLUGIN ID}    @deathbeds/jupyterlab-drawio:plugin
${DIO PLUGIN SETTINGS FILE}    @deathbeds${/}jupyterlab-drawio${/}plugin.jupyterlab-settings
${CSS USER SETTINGS}    .jp-SettingsRawEditor-user
${JLAB XP CLOSE SETTINGS}    ${JLAB XP DOCK TAB}\[contains(., 'Settings')]/*[contains(@class, 'm-TabBar-tabCloseIcon')]
# launcher
${XP LAUNCH TAB}    ${JLAB XP DOCK TAB}//*[contains(text(), 'Launcher')]
${CSS LAUNCHER}    css:.jp-Launcher-body
${CSS LAUNCH DIO}    css:.jp-LauncherCard[title='Create a new dio file'] svg
${CSS DIO READY}    css:.jp-Diagram-ready
${CSS DIO IFRAME}    ${CSS DIO READY} iframe

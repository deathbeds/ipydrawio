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

*** Settings ***
Resource          _Variables.robot
Library           SeleniumLibrary
Library           OperatingSystem
Library           Process
Library           String
Library           ./ports.py

*** Keywords ***
Setup Server and Browser
    ${port} =    Get Unused Port
    Set Global Variable    ${PORT}    ${port}
    Set Global Variable    ${URL}    http://localhost:${PORT}${BASE}
    ${accel} =    Evaluate    "COMMAND" if "${OS}" == "Darwin" else "CTRL"
    Set Global Variable    ${ACCEL}    ${accel}
    ${token} =    Generate Random String
    Set Global Variable    ${TOKEN}    ${token}
    ${home} =    Set Variable    ${OUTPUT DIR}${/}home
    Set Global Variable    ${HOME}    ${home}
    ${root} =    Normalize Path    ${OUTPUT DIR}${/}..${/}..${/}..
    Create Directory    ${home}
    Create Notebok Server Config    ${home}
    Initialize User Settings
    ${cmd} =    Create Lab Launch Command    ${root}
    Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots
    Set Global Variable    ${LAB LOG}    ${OUTPUT DIR}${/}lab.log
    Set Global Variable    ${PREVIOUS LAB LOG LENGTH}    0
    ${server} =    Start Process    ${cmd}    shell=yes    env:HOME=${home}    cwd=${home}    stdout=${LAB LOG}
    ...    stderr=STDOUT
    Set Global Variable    ${SERVER}    ${server}
    Open JupyterLab
    ${script} =    Get Element Attribute    id:jupyter-config-data    innerHTML
    ${config} =    Evaluate    __import__("json").loads(r"""${script}""")
    Set Global Variable    ${PAGE CONFIG}    ${config}
    Set Global Variable    ${LAB VERSION}    ${config["appVersion"]}

Create Lab Launch Command
    [Arguments]    ${root}
    [Documentation]    Create a JupyterLab CLI shell string, escaping for traitlets
    ${WORKSPACES DIR} =    Set Variable    ${OUTPUT DIR}${/}workspaces
    ${app args} =    Set Variable
    ...    --no-browser --debug --ServerApp.base_url\='${BASE}' --port\=${PORT} --ServerApp.token\='${TOKEN}'
    ${path args} =    Set Variable
    ...    --LabApp.user_settings_dir\='${SETTINGS DIR.replace('\\', '\\\\')}' --LabApp.workspaces_dir\='${WORKSPACES DIR.replace('\\', '\\\\')}'
    ${cmd} =    Set Variable    jupyter-lab ${app args} ${path args}
    [Return]    ${cmd}

Create Notebok Server Config
    [Arguments]    ${home}
    [Documentation]    Copies in notebook server config file to disables npm/build checks
    Copy File    ${FIXTURES}${/}${NBSERVER CONF}    ${home}${/}${NBSERVER CONF}

Setup Suite For Screenshots
    [Arguments]    ${folder}
    Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots${/}${folder}
    Set Tags    lab:${LAB VERSION}

Initialize User Settings
    Set Suite Variable    ${SETTINGS DIR}    ${OUTPUT DIR}${/}user-settings    children=${True}
    Create File
    ...    ${SETTINGS DIR}${/}@jupyterlab${/}codemirror-extension${/}commands.jupyterlab-settings
    ...    {"styleActiveLine": true}
    Create File
    ...    ${SETTINGS DIR}${/}@jupyterlab${/}extensionmanager-extension${/}plugin.jupyterlab-settings
    ...    {"enabled": false}
    Create File
    ...    ${SETTINGS DIR}${/}@jupyterlab${/}apputils-extension${/}palette.jupyterlab-settings
    ...    {"modal": false}

Reset Plugin Settings
    Create File    ${SETTINGS DIR}${/}${DIO PLUGIN SETTINGS FILE}    {}

Tear Down Everything
    Close All Browsers
    Evaluate    __import__("urllib.request").request.urlopen("${URL}api/shutdown?token=${TOKEN}", data=[])
    Wait For Process    ${SERVER}    timeout=30s
    Terminate All Processes
    Terminate All Processes    kill=${True}

Wait For Splash
    Go To    ${URL}lab?reset&token=${TOKEN}
    Set Window Size    1920    1080
    Wait Until Page Contains Element    ${SPLASH}    timeout=30s
    Wait Until Page Does Not Contain Element    ${SPLASH}    timeout=10s
    Execute Javascript    window.onbeforeunload \= function (){}

Open JupyterLab
    # Open Browser    about:blank    headlessfirefox
    Set Environment Variable    MOZ_HEADLESS    1
    ${service args} =    Create List    --log    warn
    Create WebDriver    Firefox
    ...    service_log_path=${OUTPUT DIR}${/}geckodriver.log
    ...    service_args=${service args}
    Wait Until Keyword Succeeds    3x    5s    Wait For Splash

Get Firefox Binary
    [Documentation]    Get Firefox path from the environment... or hope for the best
    ${from which} =    Which    firefox
    ${from env} =    Get Environment Variable    FIREFOX_BINARY    ${EMPTY}
    ${firefox} =    Set Variable If    "${from env}"
    ...    %{FIREFOX_BINARY}
    ...    ${from which}
    [Return]    ${firefox}

Close JupyterLab
    Close All Browsers

Close All Tabs
    Accept Default Dialog Option
    Lab Command    Close All Tabs
    Accept Default Dialog Option

Try to Close All Tabs
    Wait Until Keyword Succeeds    5x    50ms    Close All Tabs

Maybe Reset Application State
    ${pabot} =    Get Variable Value    ${PABOTEXECUTIONPOOLID}    ${EMPTY}
    Run Keyword If    not(len("${pabot}"))    Reset Application State

Reset Application State
    Try to Close All Tabs
    Accept Default Dialog Option
    Ensure All Kernels Are Shut Down
    Lab Command    Reset Application State
    Wait Until Keyword Succeeds    3x    5s    Wait For Splash

Accept Default Dialog Option
    [Documentation]    Accept a dialog, if it exists
    ${el} =    Get WebElements    ${CSS DIALOG OK}
    Run Keyword If    ${el.__len__()}    Click Element    ${CSS DIALOG OK}

Ensure All Kernels Are Shut Down
    Enter Command Name    Shut Down All Kernels
    ${els} =    Get WebElements    ${CMD PALETTE ITEM ACTIVE}
    Run Keyword If    ${els.__len__()}    Click Element    ${CMD PALETTE ITEM ACTIVE}
    ${accept} =    Set Variable    css:.jp-mod-accept.jp-mod-warn
    Run Keyword If    ${els.__len__()}    Wait Until Page Contains Element    ${accept}
    Run Keyword If    ${els.__len__()}    Click Element    ${accept}

Open Command Palette
    Ensure Command Palette is Open
    Wait Until Element Is Visible    ${CMD PALETTE INPUT}
    Click Element    ${CMD PALETTE INPUT}

Enter Command Name
    [Arguments]    ${cmd}
    Open Command Palette
    Input Text    ${CMD PALETTE INPUT}    ${cmd}

Lab Command
    [Arguments]    ${cmd}
    Enter Command Name    ${cmd}
    Wait Until Page Contains Element    ${CMD PALETTE ITEM ACTIVE}
    Click Element    ${CMD PALETTE ITEM ACTIVE}

Which
    [Arguments]    ${cmd}
    ${path} =    Evaluate    __import__("shutil").which("${cmd}")
    [Return]    ${path}

Click JupyterLab Menu
    [Arguments]    ${label}
    [Documentation]    Click a top-level JupyterLab menu bar item with by ``label``,
    ...    e.g. File, Help, etc.
    ${xpath} =    Set Variable    ${JLAB XP TOP}${JLAB XP MENU LABEL}\[text() = '${label}']
    Wait Until Page Contains Element    ${xpath}
    Mouse Over    ${xpath}
    Click Element    ${xpath}

Click JupyterLab Menu Item
    [Arguments]    ${label}
    [Documentation]    Click a currently-visible JupyterLab menu item by ``label``.
    ${item} =    Set Variable    ${JLAB XP MENU ITEM LABEL}\[text() = '${label}']
    Wait Until Page Contains Element    ${item}
    Mouse Over    ${item}
    Click Element    ${item}

Open With JupyterLab Menu
    [Arguments]    ${menu}    @{submenus}
    [Documentation]    Click into a ``menu``, then a series of ``submenus``
    Click JupyterLab Menu    ${menu}
    FOR    ${submenu}    IN    @{submenus}
        Click JupyterLab Menu Item    ${submenu}
    END

Ensure File Browser is Open
    ${sel} =    Set Variable
    ...    css:.lm-TabBar-tab[data-id="filebrowser"]:not(.lm-mod-current)
    ${els} =    Get WebElements    ${sel}
    Run Keyword If    ${els.__len__()}    Click Element    ${sel}

Ensure Command Palette is Open
    ${sel} =    Set Variable
    ...    css:.lm-TabBar-tab[data-id="command-palette"]:not(.lm-mod-current)
    ${els} =    Get WebElements    ${sel}
    Run Keyword If    ${els.__len__()}    Click Element    ${sel}

Ensure Sidebar Is Closed
    [Arguments]    ${side}=left
    ${els} =    Get WebElements    css:#jp-${side}-stack
    Run Keyword If    ${els.__len__()}
    ...    Click Element    css:.jp-mod-${side} .lm-TabBar-tab.lm-mod-current

Open Context Menu for File
    [Arguments]    ${file}
    Ensure File Browser is Open
    Click Element    css:button[title="Refresh File List"]
    ${selector} =    Set Variable    xpath://span[@class\='jp-DirListing-itemText']/span[text() = '${file}']
    Wait Until Page Contains Element    ${selector}
    Open Context Menu    ${selector}

Rename Jupyter File
    [Arguments]    ${old}    ${new}
    Open Context Menu for File    ${old}
    Mouse Over    ${MENU RENAME}
    Click Element    ${MENU RENAME}
    Press Keys    None    CTRL+a
    Press Keys    None    ${new}
    Press Keys    None    RETURN

Input Into Dialog
    [Arguments]    ${text}
    Wait For Dialog
    Click Element    ${DIALOG INPUT}
    Input Text    ${DIALOG INPUT}    ${text}
    Click Element    ${DIALOG ACCEPT}

Open ${file} in ${editor}
    Open Context Menu for File    ${file}
    Mouse Over    ${MENU OPEN WITH}
    Wait Until Page Contains Element    ${editor}
    Mouse Over    ${editor}
    Click Element    ${editor}

Clean Up After Working With File
    [Arguments]    ${file}
    Remove File    ${OUTPUT DIR}${/}home${/}${file}
    Reset Application State
    Lab Log Should Not Contain Known Error Messages

Wait For Dialog
    Wait Until Page Contains Element    ${DIALOG WINDOW}    timeout=180s

Gently Reset Workspace
    Try to Close All Tabs

Wait Until Fully Initialized
    Wait Until Element Contains    ${STATUSBAR}    Fully initialized    timeout=60s

Open Context Menu Over
    [Arguments]    ${sel}
    Wait Until Keyword Succeeds    10 x    0.1 s    Mouse Over    ${sel}
    Wait Until Keyword Succeeds    10 x    0.1 s    Click Element    ${sel}
    Wait Until Keyword Succeeds    10 x    0.1 s    Open Context Menu    ${sel}

Open in Advanced Settings
    [Arguments]    ${plugin id}
    Lab Command    Advanced Settings Editor
    ${sel} =    Set Variable    css:[data-id="${plugin id}"]
    Wait Until Page Contains Element    ${sel}
    Click Element    ${sel}
    Wait Until Page Contains    System Defaults

Set Editor Content
    [Arguments]    ${text}    ${css}=${EMPTY}
    Execute JavaScript    return document.querySelector('${css} .CodeMirror').CodeMirror.setValue(`${text}`)

Configure JupyterLab Plugin
    [Arguments]    ${settings json}={}    ${plugin id}=${DIO PLUGIN ID}
    Open in Advanced Settings    ${plugin id}
    Set Editor Content    ${settings json}    ${CSS USER SETTINGS}
    Wait Until Page Contains    No errors found
    Click Element    css:button[title\='Save User Settings']
    Click Element    ${JLAB XP CLOSE SETTINGS}

Clean Up After Working with File and Settings
    [Arguments]    ${file}
    Clean Up After Working With File    ${file}
    Reset Plugin Settings

Launch Untitled Diagram
    Lab Command    New Launcher
    Ensure Sidebar Is Closed
    Click Element    ${XP LAUNCH TAB}
    Wait Until Element is Enabled    ${CSS LAUNCH DIO}
    Click Element    ${CSS LAUNCH DIO}
    Sleep    1s
    Unselect Frame
    Wait Until Element is Visible    ${CSS DIO IFRAME}    timeout=20s

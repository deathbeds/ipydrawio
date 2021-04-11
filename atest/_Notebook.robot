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
Resource          ./_Variables.robot
Resource          ./_CodeMirror.robot

*** Keywords ***
Add and Run JupyterLab Code Cell
    [Arguments]    ${code}=print("hello world")
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    Click Element    css:${JLAB CSS NB TOOLBAR} ${JLAB CSS ICON ADD}
    Sleep    0.1s
    ${cell} =    Get WebElement    css:${JLAB CSS ACTIVE INPUT}
    Click Element    ${cell}
    Set CodeMirror Value    ${JLAB CSS ACTIVE INPUT}    ${code}
    Run Current JupyterLab Code Cell
    Click Element    ${cell}

Wait Until JupyterLab Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain Element    ${JLAB CSS BUSY KERNEL}
    Wait Until Page Does Not Contain    ${JLAB TEXT BUSY PROMPT}

Save JupyterLab Notebook
    Lab Command    Save Notebook

Run Current JupyterLab Code Cell
    Click Element    css:${JLAB CSS ICON RUN}
    Sleep    0.5s

Launch Untitled Notebook
    Lab Command    New Launcher
    Ensure Sidebar Is Closed
    Click Element    ${XP LAUNCH TAB}
    Wait Until Element is Enabled    ${CSS LAUNCH IPYNB}
    Click Element    ${CSS LAUNCH IPYNB}
    Sleep    1s
    Wait Until Page Does Not Contain    css:${JLAB CSS SPINNER}

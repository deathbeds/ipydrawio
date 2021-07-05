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
Documentation     Are Diagram settings usable?
Resource          _Keywords.robot
Library           OperatingSystem
Force Tags        component:settings    app:lab

*** Test Cases ***
Min
    [Documentation]    Does the min theme work?
    Validate a Diagram Theme    min

Atlas
    [Documentation]    Does the atlas theme work?
    Validate a Diagram Theme    atlas

Dark
    [Documentation]    Does the dark theme work?
    Validate a Diagram Theme    dark

Kennedy
    [Documentation]    Does the kennedy theme work?
    Validate a Diagram Theme    kennedy

Sketch
    [Documentation]    Does the kennedy theme work?
    Validate a Diagram Theme    sketch

*** Keywords ***
Validate a Diagram Theme
    [Arguments]    ${ui}
    [Documentation]    Change the theme
    Set Tags    settings:urlparams:ui    ui:${ui}
    Set Screenshot Directory    ${OUTPUT DIR}${/}settings${/}ui${/}${ui}
    Reset Plugin Settings
    Launch Untitled Diagram
    Wait Until Element is Visible    ${CSS DIO READY}
    Unselect Frame
    Capture Page Screenshot    10-theme.png
    Open With JupyterLab Menu    Settings    Diagram Theme    ${ui}
    Sleep    2s
    Capture Page Screenshot    99-theme-after.png
    [Teardown]    Clean Up after Settings Test

Clean Up after Settings Test
    Unselect Frame
    Remove File    ${HOME}${/}untitled*
    Remove File    ${HOME}${/}Untitled*

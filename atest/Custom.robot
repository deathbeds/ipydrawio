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
Documentation     Does custom create work?
Resource          _Keywords.robot
Library           OperatingSystem
Force Tags        component:document    component:custom
Suite Setup       Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots${/}custom

*** Test Cases ***
Defaults
    [Documentation]    Does taking the defaults work?
    Launch Custom Diagram
    Capture Page Screenshot    00-configured.png
    Accept Custom Options
    Capture Page Screenshot    10-launched.png
    [Teardown]    Clean up After Custom Test

Min Classes Notebook
    [Documentation]    Does Min Classes Notebook?
    Validate Custom Create    mcn    ipynb    min    classes.xml

Kennedy Flowchart PNG
    [Documentation]    Kennedy Classes PNG?
    Validate Custom Create    kfp    dio.png    kennedy    flowchart.xml

Sketch Business Model SVG
    [Documentation]    Kennedy Classes PNG?
    Validate Custom Create    kfp    dio.svg    sketch    business_model_1.xml

*** Keywords ***
Validate Custom Create
    [Arguments]    ${stem}    ${ext}    ${ui}    ${template}
    Set Tags    format:${ext}    ui:${ui}    template:${template}
    Launch Custom Diagram
    Choose Format    ${ext}
    Choose Theme    ${ui}
    Choose Template    ${template}
    Capture Page Screenshot    ${stem}-00-configured.png
    Accept Custom Options
    Capture Page Screenshot    ${stem}-10-launched.png
    [Teardown]    Clean up After Custom Test

Clean up After Custom Test
    Unselect Frame
    Remove File    ${HOME}${/}untitled*

Choose Format
    [Arguments]    ${ext}
    Click Element    css:li[data-ipydrawio-format=".${ext}"]

Choose Theme
    [Arguments]    ${ui}
    Click Element    css:li[data-ipydrawio-theme="${ui}"]

Choose Template
    [Arguments]    ${template}
    Click Element    css:li[data-ipydrawio-template*="${template}"]

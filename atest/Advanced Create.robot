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
Documentation     Does advanced create work?
Resource          _Keywords.robot
Library           OperatingSystem
Force Tags        component:document    component:advanced-create
Suite Setup       Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots${/}advanced-create

*** Test Cases ***
Defaults
    [Documentation]    Does taking the defaults work?
    Launch Advanced Diagram
    Capture Page Screenshot    00-configured.png
    Accept Advanced Options
    Capture Page Screenshot    10-launched.png

Min Classes Notebook
    [Documentation]    Does Min Classes Notebook?
    Validate Advanced Create    mcn    ipynb    min    classes.xml

Kennedy Flowchart PNG
    [Documentation]    Kennedy Classes PNG?
    Validate Advanced Create    kfp    dio.png    kennedy    flowchart.xml

Sketch Business Model SVG
    [Documentation]    Kennedy Classes PNG?
    Validate Advanced Create    kfp    dio.svg    sketch    business_model_1.xml

*** Keywords ***
Validate Advanced Create
    [Arguments]    ${stem}    ${ext}    ${ui}    ${template}
    Set Tags    format:${ext}    ui:${ui}    template:${template}
    Launch Advanced Diagram
    Choose Format    ${ext}
    Choose Theme    ${ui}
    Choose Template    ${template}
    Capture Page Screenshot    ${stem}-00-configured.png
    Accept Advanced Options
    Capture Page Screenshot    ${stem}-10-launched.png
    [Teardown]    Clean Up After Advanced Test

Clean up After Advanced Test
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

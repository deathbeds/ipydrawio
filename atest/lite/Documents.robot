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
Documentation     Test some diagrams in lite
Resource          ../_Keywords.robot
Resource          ./_Keywords.robot
Library           OperatingSystem
Force Tags        component:document
Suite Setup       Set Screenshot Directory    ${OUTPUT DIR}${/}lite${/}documents

*** Test Cases ***
Test Examples
    [Documentation]    Do all of the examples work?
    ${examples} =    List Files In Directory    ${DEMO}
    FOR    ${file}    IN    @{EXAMPLES}
        Try to Close All Tabs
        Run Keyword If    ${file.__contains__('.dio')}    Example Should Load    ${file}
    END

*** Keywords ***
Example Should Load
    [Arguments]    ${file}
    [Documentation]    Does one example work?
    Ensure File Browser is Open
    Double Click Element    css:[title*\="${file}"]
    Unselect Frame
    Wait Until Element is Visible    ${CSS DIO IFRAME}    timeout=20s
    Capture Page Screenshot    00-${file}-loaded.png

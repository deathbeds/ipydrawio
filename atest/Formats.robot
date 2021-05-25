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
Documentation     Are export formats sane?
Resource          _Keywords.robot
Library           OperatingSystem
Library           ./pdf.py
Force Tags        component:document

*** Variables ***
&{EXT EDIT WITH} =
...               dio.ipynb=Diagram Notebook (Diagram Notebook),Notebook,Editor,JSON
...               dio.png=Diagram Image (Editable PNG),Image,Editor,Diagram Image (PNG)
...               dio.svg=Diagram (Editable SVG),Image (Text),Editor,Image,Diagram (SVG)
...               ipynb=Notebook,Editor,Diagram Notebook (Notebook),JSON
...               pdf=PDF,Editor
...               png=Image,Editor,Diagram Image (PNG)
...               svg=Image (Text),Editor,Image,Diagram (SVG)

*** Test Cases ***
SVG
    [Documentation]    does read-only SVG work?
    Validate Export Format    SVG    svg

SVG (Editable)
    [Documentation]    does editable SVG work?
    Validate Export Format    SVG (Editable)    dio.svg    editable=${True}

PNG
    [Documentation]    does read-only PNG work?
    Validate Export Format    PNG    png

PNG (Editable)
    [Documentation]    does editable PNG work?
    Validate Export Format    PNG (Editable)    dio.png    editable=${True}

Diagram Notebook
    [Documentation]    does editable Diagram Notebook work?
    Validate Export Format    Notebook    dio.ipynb    editable=${True}

Notebook
    [Documentation]    does plain Notebook work?
    Validate Export Format    Notebook    ipynb    editable=${True}    rename=renamed.ipynb

PDF
    [Documentation]    does read-only PDF work?
    Wait Until Keyword Succeeds    5x    30s    IPyDrawio Export Server Should be Provisioned
    Wait Until Keyword Succeeds    5x    10s    Validate Export Format    PDF    pdf    timeout=30s    extra_text=Exporting Diagram
# TODO: restore someday
# PDF (Editable)
#    [Documentation]    does editable PDF work?
#    Validate Export Format    PDF    pdf    timeout=60s

*** Keywords ***
Validate Export Format
    [Arguments]    ${format}    ${ext}    ${editable}=${False}
    # menu items the format should appear before/after in _Edit With_ menu
    ...    ${before}=${EMPTY}    ${after}=${EMPTY}
    # page text that must appear while an export is occuring (then disappear)
    ...    ${extra_text}=${EMPTY}
    # will we rename the file
    ...    ${rename}=${EMPTY}
    ...    ${timeout}=10s
    Set Tags    format:${ext}    editable:${editable}
    Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots${/}${ext}
    ${doc id} =    Prepare a Diagram for Export
    Add a Shape to a Diagram
    Export a Diagram    ${format}    ${ext}    ${timeout}    ${extra_text}    ${rename}
    Verify a Diagram    ${format}    ${ext}    ${editable}    ${doc id}
    [Teardown]    Clean Up After Export Test

Prepare a Diagram for Export
    Launch Untitled Diagram
    ${doc id} =    Get Element Attribute    ${CSS DIO READY}    id
    Select Frame    ${CSS DIO IFRAME}
    Double Click Element    ${CSS DIO BG}
    Capture Page Screenshot    00-launched.png
    [Return]    ${doc id}

Add a Shape to a Diagram
    ${a shape} =    Set Variable    ${CSS DIO SHAPE POPUP SHAPE}:nth-child(2)
    Wait Until Element Is Visible    ${a shape}
    Click Element    ${a shape}
    Unselect Frame
    Capture Page Screenshot    10-edited.png

Export a Diagram
    [Arguments]    ${format}    ${ext}    ${timeout}    ${extra_text}    ${rename}
    Lab Command    Export Diagram as ${format}
    Ensure File Browser is Open
    Run Keyword If    "${extra_text}"    Wait Until Page Contains    ${extra_text}    timeout=${timeout}
    Run Keyword If    "${extra_text}"    Wait Until Page Does Not Contain    ${extra_text}    timeout=${timeout}
    ${file item} =    Wait Until Keyword Succeeds    5x    1s    Get File Item    ${ext}
    Wait Until Page Contains Element    ${file item}    timeout=${timeout}
    ${filename} =    Get File Item    ${ext}    name
    Run Keyword If    ${rename.__len__()}    Rename Jupyter File    ${filename}    ${rename}
    [Return]    ${file item}

Get File Item
    [Arguments]    ${frag}    ${field}=${EMPTY}
    ${sel} =    Set Variable    css:.jp-DirListing-item[title*\="${frag}"]
    ${title} =    Get Element Attribute    ${sel}    title
    ${res} =    Set Variable If    "${field}"
    ...    ${title.strip().splitlines()[0].split(":", 1)[1].strip()}
    ...    ${sel}
    [Return]    ${res}

Verify a Diagram
    [Arguments]    ${format}    ${ext}    ${editable}    ${doc id}
    Ensure File Browser is Open
    ${file item} =    Get File Item    ${ext}
    Click Element    ${file item}
    ${filename} =    Get File Item    ${ext}    Name
    Run Keyword If    '''${ext}''' in &{EXT EDIT WITH}
    ...    Verify Edit With Menu    ${ext}    ${filename}
    Double Click Element    ${file item}
    Ensure Sidebar Is Closed
    Run Keyword If    ${editable}
    ...    Validate Editable Format    ${format}    ${ext}    ${doc id}
    Capture Page Screenshot    99-exported.png

Verify Edit With Menu
    [Arguments]    ${ext}    ${filename}
    Open Context Menu for File    ${filename}
    Mouse Over    ${MENU OPEN WITH}
    Click Element    ${MENU OPEN WITH}
    Sleep    0.25s
    Capture Page Screenshot    98-edit-with-menu.png
    ${opener} =    Set Variable    xpath://li[@data-command\="filebrowser:open"]
    @{factories} =    Set Variable    ${EXT EDIT WITH.get('''${ext}''').strip().split(',')}
    FOR    ${i}    IN RANGE    ${factories.__len__()}
        ${factory} =    Set Variable    ${factories[${i}].strip()}
        Mouse Over
        ...    ${opener}\[position()=${i + 1}]/div[contains(@class, 'lm-Menu-itemLabel')][contains(., '${factory}')]
    END

IPyDrawio Export Server Should be Provisioned
    Lab Command    Provision Drawio PDF Export Server
    ${status} =    Get IPyDrawio Export Status    ${URL}ipydrawio/status?token=${TOKEN}
    Log    ${status}
    Should Be True    ${status["is_provisioned"]}

Clean Up After Export Test
    Unselect Frame
    Remove File    ${HOME}${/}untitled*
    Remove File    ${HOME}${/}Untitled*

Validate Editable Format
    [Arguments]    ${format}    ${ext}    ${doc id}
    Wait Until Element is Visible    ${CSS DIO READY}:not([id='${doc id}']) iframe

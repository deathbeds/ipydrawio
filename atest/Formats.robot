*** Settings ***
Documentation     Are export formats sane?
Resource          _Keywords.robot
Library           OperatingSystem

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

*** Keywords ***
Validate Export Format
    [Arguments]    ${format}    ${ext}    ${editable}=${False}
    Set Tags    format:${ext}    editable:${editable}
    Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots${/}${ext}
    Launch Untitled Diagram
    ${doc id} =    Get Element Attribute    ${CSS DIO READY}    id
    Capture Page Screenshot    00-launched.png
    Select Frame    ${CSS DIO IFRAME}
    Double Click Element    ${CSS DIO BG}
    Click Element    ${CSS DIO SHAPE MENU SHAPE}:nth-child(2)
    Unselect Frame
    Capture Page Screenshot    10-edited.png
    Lab Command    Export Diagram as ${format}
    Wait Until Page Contains Element    ${JLAB XP DOCK TAB}\[contains(., 'untitled')][contains(., '.${ext}')]
    Run Keyword If    ${editable}    Validate Editable Format    ${format}    ${ext}    ${doc id}
    Capture Page Screenshot    99-exported.png
    [Teardown]    Clean Up After Export Test

Clean Up After Export Test
    Unselect Frame
    Remove File    ${HOME}${/}untitled*

Validate Editable Format
    [Arguments]    ${format}    ${ext}    ${doc id}
    Wait Until Element is Visible    ${CSS DIO READY}:not([id='${doc id}']) iframe

Launch Untitled Diagram
    Lab Command    New Launcher
    Ensure Sidebar Is Closed
    Click Element    ${XP LAUNCH TAB}
    Wait Until Element is Enabled    ${CSS LAUNCH DIO}
    Click Element    ${CSS LAUNCH DIO}
    Wait Until Element is Visible    ${CSS DIO IFRAME}

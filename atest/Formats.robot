*** Settings ***
Documentation     Are export formats sane?
Resource          _Keywords.robot

*** Test Cases ***
SVG
    [Documentation]    does read-only SVG work?
    Validate Export Format    SVG    .svg

*** Keywords ***
Validate Export Format
    [Arguments]    ${format}    ${ext}
    Launch Untitled Diagram
    Select Frame    ${CSS DIO IFRAME}
    # TODO: some stuff
    [Teardown]    Unselect Frame

Launch Untitled Diagram
    Lab Command    New Launcher
    Ensure Sidebar Is Closed
    Click Element    ${XP LAUNCH TAB}
    Wait Until Element is Enabled    ${CSS LAUNCH DIO}
    Click Element    ${CSS LAUNCH DIO}
    Wait Until Page Contains Element    ${CSS DIO IFRAME}

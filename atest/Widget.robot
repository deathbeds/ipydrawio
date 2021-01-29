*** Settings ***
Documentation     Does the Jupyter Widget work?
Resource          _Keywords.robot
Resource          _Notebook.robot
Force Tags        component:widget
Library           OperatingSystem

*** Test Cases ***
Diagram Widget
    [Documentation]    does the Jupyter Widget work?
    Create Diagram Widget    smoke
    Capture Page Screenshot    00-on-page.png
    Edit the Widget
    Capture Page Screenshot    01-edited.png
    Update The Diagram Widget Value    ${FIXTURES}${/}test.dio
    Diagram Should Contain    TEST123
    Capture Page Screenshot    02-updated.png

*** Keywords ***
Create Diagram Widget
    [Arguments]    ${label}
    Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots${/}widget${/}${label}
    Launch Untitled Notebook
    Add and Run JupyterLab Code Cell    from ipydrawio import Diagram
    Add and Run JupyterLab Code Cell    d = Diagram(layout\=dict(min_height\="60vh")); d
    Wait Until Page Contains Element    ${CSS DIO READY} iframe

Edit the Widget
    Select Frame    ${CSS DIO IFRAME}
    Double Click Element    ${CSS DIO BG}
    ${a shape} =    Set Variable    ${CSS DIO SHAPE POPUP SHAPE}:nth-child(2)
    Wait Until Element Is Visible    ${a shape}
    Click Element    ${a shape}
    Sleep    0.5s
    [Teardown]    Unselect Frame

Diagram Should Contain
    [Arguments]    ${text}
    Select Frame    ${CSS DIO IFRAME}
    Wait Until Page Contains    ${text}
    [Teardown]    Unselect Frame

Update The Diagram Widget Value
    [Arguments]    ${path}
    ${xml} =    Get File    ${path}
    Add and Run JupyterLab Code Cell    d.source.value = '''${xml.strip()}'''

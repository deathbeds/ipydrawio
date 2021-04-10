*** Settings ***
Documentation     Are Diagram settings usable?
Resource          _Keywords.robot
Library           OperatingSystem
Force Tags        component:settings

*** Test Cases ***
Use Min Theme
    [Documentation]    Does the min theme work?
    Validate a Diagram Theme    min

Use Atlas Theme
    [Documentation]    Does the atlas theme work?
    Validate a Diagram Theme    atlas

Use Dark Theme
    [Documentation]    Does the dark theme work?
    Validate a Diagram Theme    dark

Use Kenedy Theme
    [Documentation]    Does the kennedy theme work?
    Validate a Diagram Theme    kennedy

*** Keywords ***
Validate a Diagram Theme
    [Arguments]    ${ui}
    [Documentation]    Change the theme
    Set Tags    settings:urlParams:ui    settings:urlParams:ui:${ui}
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

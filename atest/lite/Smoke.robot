*** Settings ***
Documentation     Check the vitals of a lite site
Resource          ../_Keywords.robot
Resource          ./_Keywords.robot

*** Test Cases ***
Does it load?
    [Documentation]    Can we load the JupyterLite site?
    Capture Page Screenshot    00-lite-smoke.png

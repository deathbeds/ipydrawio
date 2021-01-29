*** Settings ***
Documentation     IPyDrawio
Resource          _Keywords.robot
Resource          _Variables.robot
Suite Setup       Setup Server and Browser
Suite Teardown    Tear Down Everything
Test Setup        Maybe Reset Application State
Test Teardown     Maybe Reset Application State
Force Tags        os:${OS.lower()}    py:${PY}

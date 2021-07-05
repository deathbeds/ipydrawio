*** Settings ***
Library           OperatingSystem
Force Tags        app:lite
Resource          ./_Keywords.robot
Resource          ../_Keywords.robot
Suite Setup       Start Lite Suite
Suite Teardown    Clean Up Lite Suite
Test Setup        Start Lite Test
Test Teardown     Clean Up Lite Test

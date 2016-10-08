*** Settings ***
Library     OperatingSystem
Library     test

*** Keywords ***
Run Two File Comparison
    diffContext	v2g_new	v2g_old	v2g_diff
    ${rc}  ${result}=  Run and Return RC and Output	cat v2g_diff
    Should Be Empty  ${result}
Run v2g Helper 
    ${rc}  ${result}=  Run and Return RC and Output	v2g -h
    ${rc2}  ${result2}=  Run and Return RC and Output	cat v2ghelper_temple
    Should Be Equal	${result}	${result2}
Chech User Error Usage
    

*** Test Cases ***
v2g Helper
    Run v2g Helper
Compare v2g Output
    Run Two File Comparison

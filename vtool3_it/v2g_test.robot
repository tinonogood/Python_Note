*** Settings ***
Library     OperatingSystem
Library     diff
Resource    common_keyword/v2g_keyword.robot
Suite setup  File Should Exist  ${poscar}  ${gjf_temple}  
...  File Should Exist  ${helper_temple}  ${gjf_ABC_temple}


*** Variables ***
${poscar}=  13xH2O_CONT
${gjf}=  13xH2O_CONT_py3.gjf
${gjf_temple}=  13xH2O_CONT_temple.gjf
${gjf_ABC_temple}=  13xH2O_CONT_ABC_temple.gjf
${gjf_diff_result}=   v2g_diff
${helper}=  helper
${helper_temple}=  helper_temple
${helper_diff_result}=  helper_diff


*** Keywords ***

Generate gjf From POSCAR
    Run v2g  ${poscar}  ${gjf}
    
Generate gjf From POSCAR With Elements Tag
    Run v2g  ${poscar}  ${gjf}  A,B,C
    
Check gjf
    diff_context  ${gjf}  ${gjf_temple}  ${gjf_diff_result}

Generate v2g Helper  
    Run v2g 

Check gjf Helper
    diff_context  ${helper}  ${helper_temple}  ${helper_diff_result}

Clean
    rm  ${gjf}  ${gjf_temple}  ${helper}  ${helper_temple}


*** Test Cases ***
Convert POSCAR To gjf
    Generate gjf From POSCAR
    Check gjf
    Test Teardown  

Convert POSCAR To gjf With Elements Tag
    Generate gjf From POSCAR With Elements Tag
    Check gjf
#    Clean

Helper For Convert POSCAR To gjf
    Generate v2g Helper 
    Check gjf Helper 
#    Clean

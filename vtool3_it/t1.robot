*** Settings ***
Library     OperatingSystem
Library     diff
Resource    common_keyword/v2g_keyword.robot
Suite Setup  Directory Should Exist  v2g_test_temple  


*** Variables ***
${files_dir}=  v2g_test_temple
${poscar}=  ${files_dir}/13xH2O_CONT
${gjf}=  13xH2O_CONT_py3.gjf
${gjf_temple}=  ${files_dir}/13xH2O_CONT_temple.gjf
${gjf_ABC_temple}=  ${files_dir}/13xH2O_CONT_ABC_temple.gjf
${gjf_diff_result}=   v2g_diff
${helper_temple}=  ${files_dir}/v2g_helper_temple
${hint_temple}=  ${files_dir}/v2g_hint_temple


*** Keywords ***

Generate gjf From POSCAR
    Run v2g  ${poscar}  ${gjf}
    
Generate gjf From POSCAR With Elements Tag
    Run v2g  ${poscar}  ${gjf}  A,B,C
    
Check gjf
    diff_context  ${gjf}  ${gjf_temple}  ${gjf_diff_result}
    ${rc}  ${result}=  Run and Return RC and Output  cat ${gjf_diff_result}
    Should Be Empty  ${result}
    
Check gjf With Elements Tag
    diff_context  ${gjf}  ${gjf_ABC_temple}  ${gjf_diff_result}
    ${rc}  ${result}=  Run and Return RC and Output  cat ${gjf_diff_result}
    Should Be Empty  ${result}
    
Generate v2g Helper  
    Run v2g 

Check v2g Helper
    ${rc}  ${result}=  Run and Return RC and Output  v2g -h
    ${rc}  ${result1}=  Run and Return RC and Output  cat ${helper_temple}
    Should Be Equal  ${result}  ${result1}

Check v2g Hint
    ${rc}  ${result}=  Run and Return RC and Output  v2g
    ${rc}  ${result1}=  Run and Return RC and Output  cat ${helper_temple}
    Should Be Equal  ${result}  ${result1}



*** Test Cases ***
Convert POSCAR To gjf
    Test Setup POSCAR To gjf
    Generate gjf From POSCAR
    Check gjf
    Test Teardown  

Convert POSCAR To gjf With Elements Tag
    Test Setup POSCAR To gjf With Element Tag
    Generate gjf From POSCAR With Elements Tag
    Check gjf With Elements Tag
    Test Teardown

Check v2g Helper
    Test Setup POSCAR To gjf helper
    Run v2g helper
    Check v2g Helper

Check v2g Hint
    Test Setup POSCAR To gjf hint
    Run v2g hint
    Check v2g Hint

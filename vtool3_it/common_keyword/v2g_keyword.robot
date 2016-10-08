*** Keywords ***
Test Setup POSCAR To gjf
    File Should Exist  ${gjf_temple}

Test Setup POSCAR To gjf With Element Tag
    File Should Exist  ${gjf_ABC_temple}

Test Setup POSCAR To gjf hint
    File Should Exist  ${gjf_temple}

Test Setup POSCAR To gjf helper
    File Should Exist  ${gjf_temple}

Run v2g
    [Arguments]  ${input}=${None}  ${output}=${None}  ${element_tag}=${None}
    ${cmd}=  Set Variable If
    ...  "${element_tag}" == "${None}"  v2g -i ${input} -o ${output}
    ...  "${output}" == "${None}"  v2g -i ${input}
#    ...  "${input}" == "${None}"  v2g -h 
    ...  v2g -i ${input} -o ${output} -e ${element_tag}
    ${rc}  ${result}=  Run and Return RC and Output  ${cmd}
    Should Be Equal  ${0}  ${rc}

Run v2g hint
    ${rc}  ${result}=  Run and Return RC and Output  v2g
    Should Be Equal  ${1}  ${rc}

Run v2g helper
    ${rc}  ${result}=  Run and Return RC and Output  v2g -h
    Should Be Equal  ${0}  ${rc}

Test Teardown
    Remove Files  ${gjf}  ${gjf_diff_result}


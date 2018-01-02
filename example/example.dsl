example machine 0pow_n 1pow_n
/*Accepts language L={0^n1^n, n-natural (possible 0)}
q_0 - looking for '0', when found, writes blank ang looking for '1'), accepts empty tape, when found '#', checking by q_c
q_1 - looking for '1' (skipping rest), when not found, reject
q_c - checking, whether there is possibility to go along all tape finding only '#', if yes, then accept
q_b - going back
*/
0 1
q_0
    ; 0           ; 1       ; #       ;
q_0 ; blank q_1 > ; reject  ; # q_c > ; accept
q_1 ; 0 q_1 >     ; # q_b < ; # q_1 > ; reject
q_c ; reject      ; reject  ; # q_c > ; accept
q_b ; 0 q_b <     ; reject  ; # q_b < ; blank q_0 >

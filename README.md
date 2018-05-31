# Flexible-Job-Shop-Scheduling
Optimization of FJSSP using MILP

MILP (May 2018)

1 Problem Formulation-

• Sets and Indices:
1. E: set of jobs
2. i: job i
3. di: due date of job i
4. j: operation number
5. Oi: operations of job i
6. Oij: operation j of job i
7. M = M1 U M2: set of machines
8. M1 = set of teams × stands
9. M2 = set of mechanics × tools

• Decision Variables:
1. Sijk : starting time of operation j on machine k
2. tijk : processing time of operation j on machine k
3. Cijk : completion time of operation j on machine k
4. Ci: completion time of job i (aka full job completed)
5. Xijk = 1 if Oij is assigned to machine k, 0 otherwise
6. Yiji0j0k = 1 if operation Oij precedes operation Oi0j0
on machine k

• Parameters:
1. L a large number (> 0)

Objective function:   minimize δ; δ 2 R

• Constraints:
1. Ci − di ≤ δ; 8i 2 E
2. Pk2Mj Xijk = 1; 8i 2 E; 8j 2 Oi ( = only 1 operation is allowed per machine).
3. Sijk +Cijk ≤ XijkL; 8i; 8j 2 Oi; 8k 2 Mj ( = is operation ij is not assigned to a machine k then starting and completion times are set to 0).
4. Cijk ≥ Sijk + tijk − (1 − Xijk); 8i; 8j 2 Oi; 8k 2 Mj ( = the completion time of an operation of a job is at least as the starting time plus the processing time on that machine).
5. Si0j0k ≥ Cijk − (1 − Yiji0j0k)L8i < i0; 8j 2 Oi; 8j0 2Oi0; 8k 2 Mj \ Mj0 ( = different-job operation precedence on the same machine)
6. Pk2Mj Sijk ≥ Pk2Mj Cij−1k; 8i 2 E; 8j 2 Oi − fO1g ( = precedence of operations of the same job)
7. Ci = Pk2Mj CiOl(i)k = Pk2M(SiOl(i)k + tiOl(i)k; 8i 2 E, where Ol(i) is the last operation of job i. ( = definition of job completion time).
8. jEj = n ≤ 50 (ignore)
9. X a.m. ≤ Sijk; Cijk ≤ Y p.m. (ignore)

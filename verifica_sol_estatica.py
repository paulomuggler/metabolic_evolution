import random as rndm

def produto(r, M):
	res = []
	for re, p in M:
		if re == r:
			res.append(p)
	return res[0]

def findeducts(r, M):
	res = []
	for e, p in M:
		if p == r:
			res.append(e)
	return res

def path_to_target(M, D, F, target):
    react_list = [x + 50 for x in range(50)]
    metab_list = range(50)
    update = True
    react_possible = True

    while update:
        update = False
        for r in react_list:
            if D[r]:
                educts = findeducts(r, M)
                for s in range(len(educts)):
                    react_possible = react_possible and F[educts[s]]
                if react_possible:
                    product = produto(r, M)
                    react_possible = react_possible and F[product]
                    F[product] = True
                    if not react_possible:
                        update = True
                react_possible = True

    return F

F = [True]*20 + [False]*30
M = [(0, 59), (0, 61), (1, 90), (1, 75), (1, 52), (1, 77), (2, 81), (2, 68), (3, 92), (4, 56), (4, 70), (5, 68), (5, 70), (5, 78), (5, 53), (5, 55), (5, 88), (6, 81), (7, 50), (7, 62), (8, 75), (9, 56), (9, 69), (9, 87), (10, 98), (10, 93), (10, 94), (11, 58), (11, 76), (11, 63), (12, 51), (12, 71), (13, 65), (13, 66), (13, 60), (13, 61), (13, 95), (14, 57), (14, 58), (14, 55), (15, 84), (15, 86), (15, 79), (16, 74), (18, 64), (18, 77), (18, 79), (21, 51), (22, 66), (22, 52), (22, 85), (23, 80), (24, 89), (24, 50), (24, 91), (24, 62), (25, 80), (25, 96), (27, 72), (27, 95), (28, 97), (28, 69), (28, 54), (29, 65), (29, 60), (29, 53), (29, 54), (30, 74), (30, 67), (31, 64), (31, 72), (31, 83), (31, 59), (32, 83), (32, 67), (33, 57), (33, 91), (33, 78), (34, 84), (34, 86), (35, 73), (35, 82), (35, 76), (35, 93), (36, 63), (37, 98), (38, 97), (40, 88), (40, 89), (41, 73), (41, 99), (41, 71), (42, 96), (43, 92), (44, 99), (44, 94), (45, 82), (46, 85), (49, 90), (49, 87), (50, 15), (51, 16), (52, 2), (53, 27), (54, 23), (55, 31), (56, 20), (57, 46), (58, 9), (59, 30), (60, 18), (61, 27), (62, 38), (63, 7), (64, 35), (65, 37), (66, 41), (67, 21), (68, 40), (69, 39), (70, 12), (71, 48), (72, 11), (73, 43), (74, 47), (75, 32), (76, 10), (77, 33), (78, 19), (79, 8), (80, 3), (81, 13), (82, 11), (83, 23), (84, 24), (85, 45), (86, 21), (87, 19), (88, 14), (89, 13), (90, 0), (91, 17), (92, 13), (93, 13), (94, 8), (95, 22), (96, 35), (97, 46), (98, 25), (99, 27)]
D = {}
ll = [(True == rndm.randint(0,1)) for i in range(50)]
print 'll = ' + str(ll)

for i in range(50):
	D.update({50+i: ll[i]})

F = path_to_target(M, D, F, 20)
print 'targetproduced: ' + str(F[20])
print 'idade reprodutiva: ' + str(50/((1 if F[20] else 0) - (len([x for x in ll if x == True])/50.0)))

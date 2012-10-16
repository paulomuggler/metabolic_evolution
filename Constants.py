class Constants():
    
    food = 2
    targets = 1
    metabolites = 3
    reactions = 1
    genes = 1
    intermediate = 10
    p = 0.2
    population_size = 100
    division_threshold = 50
    record_size = 10
    rate = 0.0001
    number_environments = 6
    envchg_period = 100
    peso = 1.0/3
    ta = 100
    tb = 10000
    end_step = 5000
    env_dict = {'difficult': [[True]*(food/3) + [False]*(food - food/3),[False]*(food/3) + [True]*(food/3) + [False]*(food - 2*(food/3)), [False]*(2*(food/3))+ [True]*(food - 2*(food/3))], 'periodic2': [[True]*(food/2) + [False]*(food - food/2),[False]*(food/2) + [True]*(food - food/2)], 'minimum':[[True,True], [False, False]], 'minimum2': [[True,True], [False, True], [True,True], [True, False], [True,True], [False, False]], 'minimum_difficult':[[True, True, False, False, False, False],[False, False, True, True, False, False],[False, False, False, False, True, True]]}

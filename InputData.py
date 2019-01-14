
# simulation settings
POP_SIZE = 5000         # cohort population size
SIM_TIME_STEPS = 100    # length of simulation (years)

# transition matrix
TRANS_MATRIX = [
    [1251,  350,    116,    17],   # CD4_200to500
    [0,     731,    512,    15],   # CD4_200
    [0,     0,      1312,   437]   # AIDS
    ]

TRANS_PROB_MATRIX = [
    [0.7215, 0.2018, 0.0669, 0.0098],   # CD4_200to500
    [0.0000, 0.5811, 0.4070, 0.0119],   # CD4_200
    [0.0000, 0.0000, 0.7501, 0.2499]]   # AIDS
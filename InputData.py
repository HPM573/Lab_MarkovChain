
# simulation settings
POP_SIZE = 5000         # cohort population size
SIM_TIME_STEPS = 100    # length of simulation (years)

# transition matrix
TRANS_MATRIX = [
    [1251,  350,    116,    17],   # CD4_200to500
    [0,     731,    512,    15],   # CD4_200
    [0,     0,      1312,   437]   # AIDS
    ]


def get_trans_prob_matrix(trans_matrix):
    """
    :param trans_matrix: transition matrix containing counts of transitions between states
    :return: transition probability matrix
    """

    # initialize transition probability matrix
    trans_prob_matrix = []

    # for each row in the transition matrix
    for row in trans_matrix:
        # calculate the transition probabilities
        sum_row = sum(row)  # sum of counts in this row
        prob_row = []
        for cell in row:
            prob_row.append(cell/sum_row)

        # add this row of transition probabilities to the transition probability matrix
        trans_prob_matrix.append(prob_row)

    return trans_prob_matrix

import SimPy.RandomVariantGenerators as RVGs


class Patient:
    def __init__(self, id, transition_matrix):
        """ initiates a patient
        :param id: ID of the patient
        :param transition_matrix: transition probability matrix
        """
        self.id = id
        self.rng = RVGs.RNG(seed=id)  # random number generator for this patient
        self.tranProbMatrix = transition_matrix  # transition probability matrix


    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """




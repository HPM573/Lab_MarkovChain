import SimPy.RandomVariantGenerators as RVGs


class Patient:
    def __init__(self, id, transition_prob_matrix):
        """ initiates a patient
        :param id: ID of the patient
        :param transition_prob_matrix: transition probability matrix
        """
        self.id = id
        self.tranProbMatrix = transition_prob_matrix  # transition probability matrix


    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """




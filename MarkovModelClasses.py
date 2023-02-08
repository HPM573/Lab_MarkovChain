import numpy as np
from deampy.markov import MarkovJumpProcess

from MarkovInputData import HealthStates


class Patient:
    def __init__(self, id, transition_prob_matrix):
        """ initiates a patient
        :param id: ID of the patient
        :param transition_prob_matrix: transition probability matrix
        """
        self.id = id
        self.transProbMatrix = transition_prob_matrix
        self.stateMonitor = PatientStateMonitor()

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        # random number generator
        rng = np.random.RandomState(seed=self.id)
        # Markov jump process
        markov_jump = MarkovJumpProcess(transition_prob_matrix=self.transProbMatrix)

        k = 0  # simulation time step

        # while the patient is alive and simulation length is not yet reached
        while self.stateMonitor.get_if_alive() and k < n_time_steps:
            # sample from the Markov jump process to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = markov_jump.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # update health state
            self.stateMonitor.update(time_step=k, new_state=HealthStates(new_state_index))

            # increment time
            k += 1


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self):

        self.currentState = HealthStates.CD4_200to500    # current health state
        self.survivalTime = None      # survival time
        self.timeToAIDS = None        # time to develop AIDS

    def update(self, time_step, new_state):
        """
        update the current health state to the new health state
        :param time_step: current time step
        :param new_state: new state
        """

        # update survival time
        if new_state == HealthStates.HIV_DEATH:
            self.survivalTime = time_step + 0.5  # corrected for the half-cycle effect

        # update time until AIDS
        if self.currentState != HealthStates.AIDS and new_state == HealthStates.AIDS:
            self.timeToAIDS = time_step + 0.5  # corrected for the half-cycle effect

        # update current health state
        self.currentState = new_state

    def get_if_alive(self):
        """ returns true if the patient is still alive """
        if self.currentState != HealthStates.HIV_DEATH:
            return True
        else:
            return False

from InputData import HealthState
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
        self.stateMonitor = PatientStateMonitor()  # patient state monitor

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        k = 0  # simulation time step

        # while the patient is alive and simulation length is not yet reached
        while self.stateMonitor.get_if_alive() and k < n_time_steps:

            # find the transition probabilities to future states
            trans_probs = self.tranProbMatrix[self.stateMonitor.currentState.value]

            # create an empirical distribution
            empirical_dist = RVGs.Empirical(probabilities=trans_probs)

            # sample from the empirical distribution to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = empirical_dist.sample(rng=self.rng)

            # update health state
            self.stateMonitor.update(time_step=k, new_state=HealthState(new_state_index))

            # increment time
            k += 1


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self):

        self.currentState = HealthState.CD4_200to500    # current health state
        self.survivalTime = None      # survival time
        self.timeToAIDS = None        # time to develop AIDS
        self.ifDevelopedAIDS = False  # if the patient developed AIDS

    def update(self, time_step, new_state):
        """
        update the current health state to the new health state
        :param time_step: current time step
        :param new_state: new state
        """

        # if the patient has died, do nothing
        if self.currentState == HealthState.HIV_DEATH:
            return

        # update survival time
        if new_state == HealthState.HIV_DEATH:
            self.survivalTime = time_step + 0.5  # corrected for the half-cycle effect

        # update time until AIDS
        if self.currentState != HealthState.AIDS and new_state == HealthState.AIDS:
            self.ifDevelopedAIDS = True
            self.timeToAIDS = time_step + 0.5  # corrected for the half-cycle effect

        # update current health state
        self.currentState = new_state

    def get_if_alive(self):
        """ returns true if the patient is still alive """
        if self.currentState != HealthState.HIV_DEATH:
            return True
        else:
            return False

from InputData import HealthState
import SimPy.RandomVariantGenerators as RVGs
import SimPy.SamplePathClasses as PathCls
import SimPy.MarkovClasses as Markov


class Patient:
    def __init__(self, id, transition_prob_matrix):
        """ initiates a patient
        :param id: ID of the patient
        :param transition_prob_matrix: transition probability matrix
        """
        self.id = id
        self.transitionProbMatrix = transition_prob_matrix
        self.stateMonitor = PatientStateMonitor()

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        # random number generator
        rng = RVGs.RNG(seed=self.id)
        # jump process
        markovJump = Markov.MarkovJumpProcess(transition_prob_matrix=self.transitionProbMatrix)

        k = 0  # simulation time step

        # while the patient is alive and simulation length is not yet reached
        while self.stateMonitor.get_if_alive() and k < n_time_steps:

            # sample from the Markov jump process to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = markovJump.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

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


class Cohort:
    def __init__(self, id, pop_size, transition_prob_matrix):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param transition_prob_matrix: transition probability matrix
        """
        self.id = id
        self.popSize = pop_size
        self.transitionProbMatrix = transition_prob_matrix
        self.cohortOutcomes = CohortOutcomes()  # outcomes of the this simulated cohort

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        """
        # populate the cohort
        patients = []  # list of patients
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              transition_prob_matrix=self.transitionProbMatrix)
            # add the patient to the cohort
            patients.append(patient)

        # simulate all patients
        for patient in patients:
            # simulate
            patient.simulate(n_time_steps)

        # store outputs of this simulation
        self.cohortOutcomes.extract_outcomes(simulated_patients=patients)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []         # patients' survival times
        self.timesToAIDS = []           # patients' times to AIDS
        self.meanSurvivalTime = None    # mean survival times
        self.meanTimeToAIDS = None      # mean time to AIDS
        self.nLivingPatients = None     # survival curve (sample path of number of alive patients over time)

    def extract_outcomes(self, simulated_patients):
        """ extracts outcomes of a simulated cohort
        :param simulated_patients: a list of simulated patients"""

        # record survival time and time until AIDS
        for patient in simulated_patients:
            if not (patient.stateMonitor.survivalTime is None):
                self.survivalTimes.append(patient.stateMonitor.survivalTime)
            if patient.stateMonitor.ifDevelopedAIDS:
                self.timesToAIDS.append(patient.stateMonitor.timeToAIDS)

        # calculate mean survival time
        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)
        # calculate mean time to AIDS
        self.meanTimeToAIDS = sum(self.timesToAIDS)/len(self.timesToAIDS)

        # survival curve
        self.nLivingPatients = PathCls.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )

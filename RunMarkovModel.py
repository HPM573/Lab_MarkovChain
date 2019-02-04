import MarkovModelClasses as Cls
import InputData as D

# create a patient
myPatient = Cls.Patient(id=1,
                        transition_matrix=D.get_trans_prob_matrix(D.TRANS_MATRIX))

# simulate the patient over the specified time steps
myPatient.simulate(n_time_steps=D.SIM_TIME_STEPS)

# print the patient survival time
print('Survival time (years):',
      myPatient.stateMonitor.survivalTime)
# print mean time to AIDS
print('Time until AIDS (years)',
      myPatient.stateMonitor.timeToAIDS)

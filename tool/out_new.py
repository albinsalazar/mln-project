import numpy
import matplotlib.pyplot as plt
from gillespy2.core import (
	Model,
	Species,
	Reaction,
	Parameter)

class Mln_dynamics(Model):
	def __init__(self,parameter_values=None):
		Model.__init__(self, name="MLN")

		delta = Parameter(name='delta ', expression= 1)
		mu = Parameter(name='mu ', expression= 1)
		betaA = Parameter(name='betaA ', expression= 1)
		betaU = Parameter(name='betaU ', expression= 3)
		lamb = Parameter(name='lamb ', expression= 1)
		self.add_parameter([delta, mu, betaA, betaU, lamb])

		AS2 = Species(name='AS2', initial_value=0)
		AS1 = Species(name='AS1', initial_value=0)
		AS3 = Species(name='AS3', initial_value=0)
		AS4 = Species(name='AS4', initial_value=0)
		AI2 = Species(name='AI2', initial_value=1)
		AI1 = Species(name='AI1', initial_value=0)
		AI3 = Species(name='AI3', initial_value=0)
		AI4 = Species(name='AI4', initial_value=1)
		US2 = Species(name='US2', initial_value=0)
		US1 = Species(name='US1', initial_value=1)
		US3 = Species(name='US3', initial_value=1)
		US4 = Species(name='US4', initial_value=0)
		self.add_species([AS2, AS1, AS3, AS4, AI2, AI1, AI3, AI4, US2, US1, US3, US4])

		AS1_to_US1_0 = Reaction(
				name = 'AS1_to_US1_0',
				rate = delta,
				reactants = {AS1: 1},
				products = {US1: 1}
			)

		AS2_to_US2_1 = Reaction(
				name = 'AS2_to_US2_1',
				rate = delta,
				reactants = {AS2: 1},
				products = {US2: 1}
			)

		AS3_to_US3_2 = Reaction(
				name = 'AS3_to_US3_2',
				rate = delta,
				reactants = {AS3: 1},
				products = {US3: 1}
			)

		AS4_to_US4_3 = Reaction(
				name = 'AS4_to_US4_3',
				rate = delta,
				reactants = {AS4: 1},
				products = {US4: 1}
			)

		AI1_to_AS1_4 = Reaction(
				name = 'AI1_to_AS1_4',
				rate = mu,
				reactants = {AI1: 1},
				products = {AS1: 1}
			)

		AI2_to_AS2_5 = Reaction(
				name = 'AI2_to_AS2_5',
				rate = mu,
				reactants = {AI2: 1},
				products = {AS2: 1}
			)

		AI3_to_AS3_6 = Reaction(
				name = 'AI3_to_AS3_6',
				rate = mu,
				reactants = {AI3: 1},
				products = {AS3: 1}
			)

		AI4_to_AS4_7 = Reaction(
				name = 'AI4_to_AS4_7',
				rate = mu,
				reactants = {AI4: 1},
				products = {AS4: 1}
			)

		AS1_AI2_to_AI1_AI2_8 = Reaction(
				name = 'AS1_AI2_to_AI1_AI2_8',
				rate = betaA,
				reactants = {AS1: 1, AI2: 1},
				products = {AI1: 1, AI2: 1}
			)

		AS2_AI1_to_AI2_AI1_9 = Reaction(
				name = 'AS2_AI1_to_AI2_AI1_9',
				rate = betaA,
				reactants = {AS2: 1, AI1: 1},
				products = {AI2: 1, AI1: 1}
			)

		AS1_AI3_to_AI1_AI3_10 = Reaction(
				name = 'AS1_AI3_to_AI1_AI3_10',
				rate = betaA,
				reactants = {AS1: 1, AI3: 1},
				products = {AI1: 1, AI3: 1}
			)

		AS3_AI1_to_AI3_AI1_11 = Reaction(
				name = 'AS3_AI1_to_AI3_AI1_11',
				rate = betaA,
				reactants = {AS3: 1, AI1: 1},
				products = {AI3: 1, AI1: 1}
			)

		AS1_AI4_to_AI1_AI4_12 = Reaction(
				name = 'AS1_AI4_to_AI1_AI4_12',
				rate = betaA,
				reactants = {AS1: 1, AI4: 1},
				products = {AI1: 1, AI4: 1}
			)

		AS4_AI1_to_AI4_AI1_13 = Reaction(
				name = 'AS4_AI1_to_AI4_AI1_13',
				rate = betaA,
				reactants = {AS4: 1, AI1: 1},
				products = {AI4: 1, AI1: 1}
			)

		AS3_AI2_to_AI3_AI2_14 = Reaction(
				name = 'AS3_AI2_to_AI3_AI2_14',
				rate = betaA,
				reactants = {AS3: 1, AI2: 1},
				products = {AI3: 1, AI2: 1}
			)

		AS2_AI3_to_AI2_AI3_15 = Reaction(
				name = 'AS2_AI3_to_AI2_AI3_15',
				rate = betaA,
				reactants = {AS2: 1, AI3: 1},
				products = {AI2: 1, AI3: 1}
			)

		AS3_AI4_to_AI3_AI4_16 = Reaction(
				name = 'AS3_AI4_to_AI3_AI4_16',
				rate = betaA,
				reactants = {AS3: 1, AI4: 1},
				products = {AI3: 1, AI4: 1}
			)

		AS4_AI3_to_AI4_AI3_17 = Reaction(
				name = 'AS4_AI3_to_AI4_AI3_17',
				rate = betaA,
				reactants = {AS4: 1, AI3: 1},
				products = {AI4: 1, AI3: 1}
			)

		AS2_AI4_to_AI2_AI4_18 = Reaction(
				name = 'AS2_AI4_to_AI2_AI4_18',
				rate = betaA,
				reactants = {AS2: 1, AI4: 1},
				products = {AI2: 1, AI4: 1}
			)

		AS4_AI2_to_AI4_AI2_19 = Reaction(
				name = 'AS4_AI2_to_AI4_AI2_19',
				rate = betaA,
				reactants = {AS4: 1, AI2: 1},
				products = {AI4: 1, AI2: 1}
			)

		US1_AI2_to_AI1_AI2_20 = Reaction(
				name = 'US1_AI2_to_AI1_AI2_20',
				rate = betaU,
				reactants = {US1: 1, AI2: 1},
				products = {AI1: 1, AI2: 1}
			)

		US2_AI1_to_AI2_AI1_21 = Reaction(
				name = 'US2_AI1_to_AI2_AI1_21',
				rate = betaU,
				reactants = {US2: 1, AI1: 1},
				products = {AI2: 1, AI1: 1}
			)

		US1_AI3_to_AI1_AI3_22 = Reaction(
				name = 'US1_AI3_to_AI1_AI3_22',
				rate = betaU,
				reactants = {US1: 1, AI3: 1},
				products = {AI1: 1, AI3: 1}
			)

		US3_AI1_to_AI3_AI1_23 = Reaction(
				name = 'US3_AI1_to_AI3_AI1_23',
				rate = betaU,
				reactants = {US3: 1, AI1: 1},
				products = {AI3: 1, AI1: 1}
			)

		US1_AI4_to_AI1_AI4_24 = Reaction(
				name = 'US1_AI4_to_AI1_AI4_24',
				rate = betaU,
				reactants = {US1: 1, AI4: 1},
				products = {AI1: 1, AI4: 1}
			)

		US4_AI1_to_AI4_AI1_25 = Reaction(
				name = 'US4_AI1_to_AI4_AI1_25',
				rate = betaU,
				reactants = {US4: 1, AI1: 1},
				products = {AI4: 1, AI1: 1}
			)

		US3_AI2_to_AI3_AI2_26 = Reaction(
				name = 'US3_AI2_to_AI3_AI2_26',
				rate = betaU,
				reactants = {US3: 1, AI2: 1},
				products = {AI3: 1, AI2: 1}
			)

		US2_AI3_to_AI2_AI3_27 = Reaction(
				name = 'US2_AI3_to_AI2_AI3_27',
				rate = betaU,
				reactants = {US2: 1, AI3: 1},
				products = {AI2: 1, AI3: 1}
			)

		US3_AI4_to_AI3_AI4_28 = Reaction(
				name = 'US3_AI4_to_AI3_AI4_28',
				rate = betaU,
				reactants = {US3: 1, AI4: 1},
				products = {AI3: 1, AI4: 1}
			)

		US4_AI3_to_AI4_AI3_29 = Reaction(
				name = 'US4_AI3_to_AI4_AI3_29',
				rate = betaU,
				reactants = {US4: 1, AI3: 1},
				products = {AI4: 1, AI3: 1}
			)

		US2_AI4_to_AI2_AI4_30 = Reaction(
				name = 'US2_AI4_to_AI2_AI4_30',
				rate = betaU,
				reactants = {US2: 1, AI4: 1},
				products = {AI2: 1, AI4: 1}
			)

		US4_AI2_to_AI4_AI2_31 = Reaction(
				name = 'US4_AI2_to_AI4_AI2_31',
				rate = betaU,
				reactants = {US4: 1, AI2: 1},
				products = {AI4: 1, AI2: 1}
			)

		US1_AI2_to_AS1_AI2_32 = Reaction(
				name = 'US1_AI2_to_AS1_AI2_32',
				rate = lamb,
				reactants = {US1: 1, AI2: 1},
				products = {AS1: 1, AI2: 1}
			)

		US2_AI1_to_AS2_AI1_33 = Reaction(
				name = 'US2_AI1_to_AS2_AI1_33',
				rate = lamb,
				reactants = {US2: 1, AI1: 1},
				products = {AS2: 1, AI1: 1}
			)

		US1_AI3_to_AS1_AI3_34 = Reaction(
				name = 'US1_AI3_to_AS1_AI3_34',
				rate = lamb,
				reactants = {US1: 1, AI3: 1},
				products = {AS1: 1, AI3: 1}
			)

		US3_AI1_to_AS3_AI1_35 = Reaction(
				name = 'US3_AI1_to_AS3_AI1_35',
				rate = lamb,
				reactants = {US3: 1, AI1: 1},
				products = {AS3: 1, AI1: 1}
			)

		US3_AI4_to_AS3_AI4_36 = Reaction(
				name = 'US3_AI4_to_AS3_AI4_36',
				rate = lamb,
				reactants = {US3: 1, AI4: 1},
				products = {AS3: 1, AI4: 1}
			)

		US4_AI3_to_AS4_AI3_37 = Reaction(
				name = 'US4_AI3_to_AS4_AI3_37',
				rate = lamb,
				reactants = {US4: 1, AI3: 1},
				products = {AS4: 1, AI3: 1}
			)

		US1_AS2_to_AS1_AS2_38 = Reaction(
				name = 'US1_AS2_to_AS1_AS2_38',
				rate = lamb,
				reactants = {US1: 1, AS2: 1},
				products = {AS1: 1, AS2: 1}
			)

		US2_AS1_to_AS2_AS1_39 = Reaction(
				name = 'US2_AS1_to_AS2_AS1_39',
				rate = lamb,
				reactants = {US2: 1, AS1: 1},
				products = {AS2: 1, AS1: 1}
			)

		US1_AS3_to_AS1_AS3_40 = Reaction(
				name = 'US1_AS3_to_AS1_AS3_40',
				rate = lamb,
				reactants = {US1: 1, AS3: 1},
				products = {AS1: 1, AS3: 1}
			)

		US3_AS1_to_AS3_AS1_41 = Reaction(
				name = 'US3_AS1_to_AS3_AS1_41',
				rate = lamb,
				reactants = {US3: 1, AS1: 1},
				products = {AS3: 1, AS1: 1}
			)

		US3_AS4_to_AS3_AS4_42 = Reaction(
				name = 'US3_AS4_to_AS3_AS4_42',
				rate = lamb,
				reactants = {US3: 1, AS4: 1},
				products = {AS3: 1, AS4: 1}
			)

		US4_AS3_to_AS4_AS3_43 = Reaction(
				name = 'US4_AS3_to_AS4_AS3_43',
				rate = lamb,
				reactants = {US4: 1, AS3: 1},
				products = {AS4: 1, AS3: 1}
			)

		self.add_reaction([AS1_to_US1_0, AS2_to_US2_1, AS3_to_US3_2, AS4_to_US4_3, AI1_to_AS1_4, AI2_to_AS2_5, AI3_to_AS3_6, AI4_to_AS4_7, AS1_AI2_to_AI1_AI2_8, AS2_AI1_to_AI2_AI1_9, AS1_AI3_to_AI1_AI3_10, AS3_AI1_to_AI3_AI1_11, AS1_AI4_to_AI1_AI4_12, AS4_AI1_to_AI4_AI1_13, AS3_AI2_to_AI3_AI2_14, AS2_AI3_to_AI2_AI3_15, AS3_AI4_to_AI3_AI4_16, AS4_AI3_to_AI4_AI3_17, AS2_AI4_to_AI2_AI4_18, AS4_AI2_to_AI4_AI2_19, US1_AI2_to_AI1_AI2_20, US2_AI1_to_AI2_AI1_21, US1_AI3_to_AI1_AI3_22, US3_AI1_to_AI3_AI1_23, US1_AI4_to_AI1_AI4_24, US4_AI1_to_AI4_AI1_25, US3_AI2_to_AI3_AI2_26, US2_AI3_to_AI2_AI3_27, US3_AI4_to_AI3_AI4_28, US4_AI3_to_AI4_AI3_29, US2_AI4_to_AI2_AI4_30, US4_AI2_to_AI4_AI2_31, US1_AI2_to_AS1_AI2_32, US2_AI1_to_AS2_AI1_33, US1_AI3_to_AS1_AI3_34, US3_AI1_to_AS3_AI1_35, US3_AI4_to_AS3_AI4_36, US4_AI3_to_AS4_AI3_37, US1_AS2_to_AS1_AS2_38, US2_AS1_to_AS2_AS1_39, US1_AS3_to_AS1_AS3_40, US3_AS1_to_AS3_AS1_41, US3_AS4_to_AS3_AS4_42, US4_AS3_to_AS4_AS3_43])

		self.timespan(numpy.linspace(0, 30, 600))

def run_sim(model):
	results = model.run(number_of_trajectories=1000)
	trajectory = results.average_ensemble()
	plt.figure()
	trajectories = [[], [], []]
	for i in range(len(trajectory['AI1'])):
		trajectories[0].append(trajectory['AI2'][i] + trajectory['AI1'][i] + trajectory['AI3'][i] + trajectory['AI4'][i])
		trajectories[1].append(trajectory['AS2'][i] + trajectory['AS1'][i] + trajectory['AS3'][i] + trajectory['AS4'][i])
		trajectories[2].append(trajectory['US2'][i] + trajectory['US1'][i] + trajectory['US3'][i] + trajectory['US4'][i])
	plt.plot(trajectory['time'], trajectories[0], 'b', label='AI')
	plt.plot(trajectory['time'], trajectories[1], 'g', label='AS')
	plt.plot(trajectory['time'], trajectories[2], 'r', label='US')
	plt.legend(loc='upper right')
	plt.annotate(text=f'n = 1000', xy=(0.1, 0.9), xycoords='axes fraction')
	plt.show()
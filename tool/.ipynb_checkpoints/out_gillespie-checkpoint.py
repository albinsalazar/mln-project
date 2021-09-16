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

		AS1 = Species(name='AS1', initial_value=0)
		AS2 = Species(name='AS2', initial_value=0)
		AS3 = Species(name='AS3', initial_value=0)
		AI1 = Species(name='AI1', initial_value=1)
		AI2 = Species(name='AI2', initial_value=0)
		AI3 = Species(name='AI3', initial_value=0)
		US1 = Species(name='US1', initial_value=0)
		US2 = Species(name='US2', initial_value=1)
		US3 = Species(name='US3', initial_value=1)
		self.add_species([AS1, AS2, AS3, AI1, AI2, AI3, US1, US2, US3])

		0_AS1_to_US1 = Reaction(
				name = '0_AS1_to_US1',
				rate = delta,
				reactants = {AS1: 1},
				products = {US1: 1}
			)

		1_AS2_to_US2 = Reaction(
				name = '1_AS2_to_US2',
				rate = delta,
				reactants = {AS2: 1},
				products = {US2: 1}
			)

		2_AS3_to_US3 = Reaction(
				name = '2_AS3_to_US3',
				rate = delta,
				reactants = {AS3: 1},
				products = {US3: 1}
			)

		3_AI1_to_AS1 = Reaction(
				name = '3_AI1_to_AS1',
				rate = mu,
				reactants = {AI1: 1},
				products = {AS1: 1}
			)

		4_AI2_to_AS2 = Reaction(
				name = '4_AI2_to_AS2',
				rate = mu,
				reactants = {AI2: 1},
				products = {AS2: 1}
			)

		5_AI3_to_AS3 = Reaction(
				name = '5_AI3_to_AS3',
				rate = mu,
				reactants = {AI3: 1},
				products = {AS3: 1}
			)

		6_AS1_AI2_to_AI1_AI2 = Reaction(
				name = '6_AS1_AI2_to_AI1_AI2',
				rate = betaA,
				reactants = {AS1: 1, AI2: 1},
				products = {AI1: 1, AI2: 1}
			)

		7_AS2_AI1_to_AI2_AI1 = Reaction(
				name = '7_AS2_AI1_to_AI2_AI1',
				rate = betaA,
				reactants = {AS2: 1, AI1: 1},
				products = {AI2: 1, AI1: 1}
			)

		8_AS1_AI3_to_AI1_AI3 = Reaction(
				name = '8_AS1_AI3_to_AI1_AI3',
				rate = betaA,
				reactants = {AS1: 1, AI3: 1},
				products = {AI1: 1, AI3: 1}
			)

		9_AS3_AI1_to_AI3_AI1 = Reaction(
				name = '9_AS3_AI1_to_AI3_AI1',
				rate = betaA,
				reactants = {AS3: 1, AI1: 1},
				products = {AI3: 1, AI1: 1}
			)

		10_US1_AI2_to_AI1_AI2 = Reaction(
				name = '10_US1_AI2_to_AI1_AI2',
				rate = betaU,
				reactants = {US1: 1, AI2: 1},
				products = {AI1: 1, AI2: 1}
			)

		11_US2_AI1_to_AI2_AI1 = Reaction(
				name = '11_US2_AI1_to_AI2_AI1',
				rate = betaU,
				reactants = {US2: 1, AI1: 1},
				products = {AI2: 1, AI1: 1}
			)

		12_US1_AI3_to_AI1_AI3 = Reaction(
				name = '12_US1_AI3_to_AI1_AI3',
				rate = betaU,
				reactants = {US1: 1, AI3: 1},
				products = {AI1: 1, AI3: 1}
			)

		13_US3_AI1_to_AI3_AI1 = Reaction(
				name = '13_US3_AI1_to_AI3_AI1',
				rate = betaU,
				reactants = {US3: 1, AI1: 1},
				products = {AI3: 1, AI1: 1}
			)

		14_US1_AI2_to_AS1_AI2 = Reaction(
				name = '14_US1_AI2_to_AS1_AI2',
				rate = lamb,
				reactants = {US1: 1, AI2: 1},
				products = {AS1: 1, AI2: 1}
			)

		15_US2_AI1_to_AS2_AI1 = Reaction(
				name = '15_US2_AI1_to_AS2_AI1',
				rate = lamb,
				reactants = {US2: 1, AI1: 1},
				products = {AS2: 1, AI1: 1}
			)

		16_US1_AI3_to_AS1_AI3 = Reaction(
				name = '16_US1_AI3_to_AS1_AI3',
				rate = lamb,
				reactants = {US1: 1, AI3: 1},
				products = {AS1: 1, AI3: 1}
			)

		17_US3_AI1_to_AS3_AI1 = Reaction(
				name = '17_US3_AI1_to_AS3_AI1',
				rate = lamb,
				reactants = {US3: 1, AI1: 1},
				products = {AS3: 1, AI1: 1}
			)

		18_US2_AI3_to_AS2_AI3 = Reaction(
				name = '18_US2_AI3_to_AS2_AI3',
				rate = lamb,
				reactants = {US2: 1, AI3: 1},
				products = {AS2: 1, AI3: 1}
			)

		19_US3_AI2_to_AS3_AI2 = Reaction(
				name = '19_US3_AI2_to_AS3_AI2',
				rate = lamb,
				reactants = {US3: 1, AI2: 1},
				products = {AS3: 1, AI2: 1}
			)

		20_US1_AS2_to_AS1_AS2 = Reaction(
				name = '20_US1_AS2_to_AS1_AS2',
				rate = lamb,
				reactants = {US1: 1, AS2: 1},
				products = {AS1: 1, AS2: 1}
			)

		21_US2_AS1_to_AS2_AS1 = Reaction(
				name = '21_US2_AS1_to_AS2_AS1',
				rate = lamb,
				reactants = {US2: 1, AS1: 1},
				products = {AS2: 1, AS1: 1}
			)

		22_US1_AS3_to_AS1_AS3 = Reaction(
				name = '22_US1_AS3_to_AS1_AS3',
				rate = lamb,
				reactants = {US1: 1, AS3: 1},
				products = {AS1: 1, AS3: 1}
			)

		23_US3_AS1_to_AS3_AS1 = Reaction(
				name = '23_US3_AS1_to_AS3_AS1',
				rate = lamb,
				reactants = {US3: 1, AS1: 1},
				products = {AS3: 1, AS1: 1}
			)

		24_US2_AS3_to_AS2_AS3 = Reaction(
				name = '24_US2_AS3_to_AS2_AS3',
				rate = lamb,
				reactants = {US2: 1, AS3: 1},
				products = {AS2: 1, AS3: 1}
			)

		25_US3_AS2_to_AS3_AS2 = Reaction(
				name = '25_US3_AS2_to_AS3_AS2',
				rate = lamb,
				reactants = {US3: 1, AS2: 1},
				products = {AS3: 1, AS2: 1}
			)

		self.add_reaction([0_AS1_to_US1, 1_AS2_to_US2, 2_AS3_to_US3, 3_AI1_to_AS1, 4_AI2_to_AS2, 5_AI3_to_AS3, 6_AS1_AI2_to_AI1_AI2, 7_AS2_AI1_to_AI2_AI1, 8_AS1_AI3_to_AI1_AI3, 9_AS3_AI1_to_AI3_AI1, 10_US1_AI2_to_AI1_AI2, 11_US2_AI1_to_AI2_AI1, 12_US1_AI3_to_AI1_AI3, 13_US3_AI1_to_AI3_AI1, 14_US1_AI2_to_AS1_AI2, 15_US2_AI1_to_AS2_AI1, 16_US1_AI3_to_AS1_AI3, 17_US3_AI1_to_AS3_AI1, 18_US2_AI3_to_AS2_AI3, 19_US3_AI2_to_AS3_AI2, 20_US1_AS2_to_AS1_AS2, 21_US2_AS1_to_AS2_AS1, 22_US1_AS3_to_AS1_AS3, 23_US3_AS1_to_AS3_AS1, 24_US2_AS3_to_AS2_AS3, 25_US3_AS2_to_AS3_AS2])

		self.timespan(numpy.linspace(0, 30, 600))

def run_sim(model):
	results = model.run(number_of_trajectories=1000)
	trajectory = results.average_ensemble()
	plt.figure()
	trajectories = [[], [], []]
	for i in range(len(trajectory['AI1'])):
		trajectories[0].append(trajectory['AI1'][i] + trajectory['AI2'][i] + trajectory['AI3'][i])
		trajectories[1].append(trajectory['AS1'][i] + trajectory['AS2'][i] + trajectory['AS3'][i])
		trajectories[2].append(trajectory['US1'][i] + trajectory['US2'][i] + trajectory['US3'][i])
	plt.plot(trajectory['time'], trajectories[0], 'b', label='AI'
	plt.plot(trajectory['time'], trajectories[1], 'g', label='AS'
	plt.plot(trajectory['time'], trajectories[2], 'r', label='US'
	plt.legend(loc='upper right')
	plt.annotate(text=f'n = 1000', xy=(0.1, 0.9), xycoords='axes fraction')
plt.show()
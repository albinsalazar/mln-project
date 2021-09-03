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

		delta = Parameter(name="delta", expression = 1)
		mu = Parameter(name="mu", expression = 1)
		betaA = Parameter(name="betaA", expression = 1)
		betaU = Parameter(name="betaU", expression = 3)
		lamb = Parameter(name="lamb", expression = 1)
		self.add_parameter([ delta , mu , betaA , betaU , lamb ] ) 

		AS0 = Species(name="AS0", initial_value=0)
		AS1 = Species(name="AS1", initial_value=0)
		AS2 = Species(name="AS2", initial_value=0)
		AI0 = Species(name="AI0", initial_value=1)
		AI1 = Species(name="AI1", initial_value=0)
		AI2 = Species(name="AI2", initial_value=0)
		US0 = Species(name="US0", initial_value=0)
		US1 = Species(name="US1", initial_value=1)
		US2 = Species(name="US2", initial_value=1)
		self.add_species([AS0 , AS1 , AS2 , AI0 , AI1 , AI2 , US0 , US1 , US2] )

		r_0 = Reaction(
				name = "r_0",
				rate = delta,
				reactants = {AS0: 1},
				products = {US0: 1}
			)

		r_1 = Reaction(
				name = "r_1",
				rate = delta,
				reactants = {AS1: 1},
				products = {US1: 1}
			)

		r_2 = Reaction(
				name = "r_2",
				rate = delta,
				reactants = {AS2: 1},
				products = {US2: 1}
			)

		r_3 = Reaction(
				name = "r_3",
				rate = mu,
				reactants = {AI0: 1},
				products = {AS0: 1}
			)

		r_4 = Reaction(
				name = "r_4",
				rate = mu,
				reactants = {AI1: 1},
				products = {AS1: 1}
			)

		r_5 = Reaction(
				name = "r_5",
				rate = mu,
				reactants = {AI2: 1},
				products = {AS2: 1}
			)

		r_6 = Reaction(
				name = "r_6",
				rate = betaA,
				reactants = {AS0: 1, AI1: 1},
				products = {AI0: 1, AI1: 1}
			)

		r_7 = Reaction(
				name = "r_7",
				rate = betaA,
				reactants = {AS1: 1, AI0: 1},
				products = {AI1: 1, AI0: 1}
			)

		r_8 = Reaction(
				name = "r_8",
				rate = betaA,
				reactants = {AS0: 1, AI2: 1},
				products = {AI0: 1, AI2: 1}
			)

		r_9 = Reaction(
				name = "r_9",
				rate = betaA,
				reactants = {AS2: 1, AI0: 1},
				products = {AI2: 1, AI0: 1}
			)

		r_10 = Reaction(
				name = "r_10",
				rate = betaU,
				reactants = {US0: 1, AI1: 1},
				products = {AI0: 1, AI1: 1}
			)

		r_11 = Reaction(
				name = "r_11",
				rate = betaU,
				reactants = {US1: 1, AI0: 1},
				products = {AI1: 1, AI0: 1}
			)

		r_12 = Reaction(
				name = "r_12",
				rate = betaU,
				reactants = {US0: 1, AI2: 1},
				products = {AI0: 1, AI2: 1}
			)

		r_13 = Reaction(
				name = "r_13",
				rate = betaU,
				reactants = {US2: 1, AI0: 1},
				products = {AI2: 1, AI0: 1}
			)

		r_14 = Reaction(
				name = "r_14",
				rate = lamb,
				reactants = {US0: 1, AI1: 1},
				products = {AS0: 1, AI1: 1}
			)

		r_15 = Reaction(
				name = "r_15",
				rate = lamb,
				reactants = {US1: 1, AI0: 1},
				products = {AS1: 1, AI0: 1}
			)

		r_16 = Reaction(
				name = "r_16",
				rate = lamb,
				reactants = {US0: 1, AI2: 1},
				products = {AS0: 1, AI2: 1}
			)

		r_17 = Reaction(
				name = "r_17",
				rate = lamb,
				reactants = {US2: 1, AI0: 1},
				products = {AS2: 1, AI0: 1}
			)

		r_18 = Reaction(
				name = "r_18",
				rate = lamb,
				reactants = {US1: 1, AI2: 1},
				products = {AS1: 1, AI2: 1}
			)

		r_19 = Reaction(
				name = "r_19",
				rate = lamb,
				reactants = {US2: 1, AI1: 1},
				products = {AS2: 1, AI1: 1}
			)

		r_20 = Reaction(
				name = "r_20",
				rate = lamb,
				reactants = {US0: 1, AS1: 1},
				products = {AS0: 1, AS1: 1}
			)

		r_21 = Reaction(
				name = "r_21",
				rate = lamb,
				reactants = {US1: 1, AS0: 1},
				products = {AS1: 1, AS0: 1}
			)

		r_22 = Reaction(
				name = "r_22",
				rate = lamb,
				reactants = {US0: 1, AS2: 1},
				products = {AS0: 1, AS2: 1}
			)

		r_23 = Reaction(
				name = "r_23",
				rate = lamb,
				reactants = {US2: 1, AS0: 1},
				products = {AS2: 1, AS0: 1}
			)

		r_24 = Reaction(
				name = "r_24",
				rate = lamb,
				reactants = {US1: 1, AS2: 1},
				products = {AS1: 1, AS2: 1}
			)

		r_25 = Reaction(
				name = "r_25",
				rate = lamb,
				reactants = {US2: 1, AS1: 1},
				products = {AS2: 1, AS1: 1}
			)

		self.add_reaction([r_0 , r_1 , r_2 , r_3 , r_4 , r_5 , r_6 , r_7 , r_8 , r_9 , r_10 , r_11 , r_12 , r_13 , r_14 , r_15 , r_16 , r_17 , r_18 , r_19 , r_20 , r_21 , r_22 , r_23 , r_24 , r_25] ) 

		self.timespan(numpy.linspace(0, 5, 100))

def run_sim(model):
	results = model.run(number_of_trajectories=100)
	trajectory = results.average_ensemble()
	plt.figure()
	trajectories = [[], [], []]
	for i in range(len(trajectory["AI0"])):
		trajectories[0].append(trajectory["AI0"][i] + trajectory["AI1"][i] + trajectory["AI2"][i])
		trajectories[1].append(trajectory["AS0"][i] + trajectory["AS1"][i] + trajectory["AS2"][i])
		trajectories[2].append(trajectory["US0"][i] + trajectory["US1"][i] + trajectory["US2"][i])
	plt.plot(trajectory["time"], trajectories[0], "b", label="AI")
	plt.plot(trajectory["time"], trajectories[1], "g", label="AS")
	plt.plot(trajectory["time"], trajectories[2], "r", label="US")
	plt.legend(loc="upper right")
	plt.annotate(text=f"n = 100", xy=(0.1, 0.9), xycoords="axes fraction")
	plt.show()
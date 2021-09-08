import uunet.multinet as ml

def parse_mln(mln_filename):
    print(f'From parser, mln filename:{mln_filename}')
    net = ml.read(mln_filename)
    
    ### Number of actors
    actors = ml.actors(net)
    # N_actors = max(list(map(int, actors)))
    N_actors = len(actors)

    ### Number of layers
    layers = ml.layers(net)
    # N_layers = max(list(map(int, layers)))
    N_layers = len(layers)

    #### Then we extract all the edges we need from the MLN
    #### (here i check if they undirected and take them both, maybe it is best to do this check in
    #### when parsing the rules)

    edges = ml.edges(net)
    edges

    list_split_edges = [] 

    for layer in layers: 
        list_collecting_edges = [] 
        idx_list = [i for i,j in enumerate(edges['from_layer']) if j == layer]
        for i in idx_list : 
            list_collecting_edges.append((edges['from_actor'][i] , edges['to_actor'][i]) )
            if edges['dir'][i] == False: 
                list_collecting_edges.append( (edges['to_actor'][i] , edges['from_actor'][i]) )

        list_split_edges.append(list_collecting_edges)
        
    mln_data = {
        'actors': (actors, N_actors),
        'layers': (layers, N_layers),
        'edges': (edges, list_split_edges)
                }
    
    return mln_data


def parse_language_to_gillespy(STEinFname, OUTFname, mln_data):
    actors, N_actors = mln_data['actors']
    layers, N_layers = mln_data['layers']
    edges, list_split_edges = mln_data['edges']
    
    my_list = []
    tab = '\t'
    
    with open(STEinFname) as f:
        lines = f.readlines()
        columns = [] 

        i = 1
        for line in lines: 
            line = line.strip() # remove leading/trailing white spaces

            if line: 
                if i == 1:
                    columns = [item.strip() for item in line.split(',')]
                    i = i + 1
                else:    
                    d = {}
                    data = [item.strip() for item in line.split(' ')]
                    for index, elem in enumerate(data):
                        d[columns[index]] = data[index]

                    my_list.append(d) # append dictionary to list 
                    
    
    lookingForStates = True
    parsingStates = False
    lookingForParams = False
    parsingParams = False
    lookingForICs = False
    parsingICs = False
    lookingForRules = False
    parsingRules = False
    lookingForViews = False
    parsingViews = False
    lookingForSimOptions = False
    parsingSimOptions = False
    parsingCompleted = False


    N = N_actors ##### NUMBER OF ACTORS IN THE MLN, should be parsed from the MLN file                

    with open(OUTFname, 'w') as out_f:
        list_of_states = []
        list_of_IC = [] 
        rule_counter = 0
        list_of_rules_IDs = []
        list_of_propensities = [] 
        list_of_effects = []         
        list_of_params = [] 
        list_of_views = []

        ### OPTIONS FOR GILLESPIE SIMULATION
        ### number of trajectories/repetitions
        n_rep = 5  ### Default 5
        ### Time horizon
        T_END = 10  ### Default 10

        ##### Manual list of colors for the plot, we can potentially write something else such as a function like the one from the uunet package
        list_of_colors = ['b','g','r','c','m','y','k']
        active_color = 0

        header_string = ('import numpy\n'
                         'import matplotlib.pyplot as plt\n'
                         'from gillespy2.core import (\n'
                         '\tModel,\n'
                         '\tSpecies,\n'
                         '\tReaction,\n'
                         '\tParameter)\n\n'
                         'class Mln_dynamics(Model):\n'
                         '\tdef __init__(self,parameter_values=None):\n'
                         '\t\tModel.__init__(self, name="MLN")\n\n')

        out_f.write(header_string)

        for item in my_list: 
            # parse parameters, species, and reactions
            if lookingForStates == True and item["s1"] == "begin" and item["s2"] == "states": 
                lookingForStates = False
                parsingStates = True

            elif parsingStates == True and item["s1"] != "end":
                #out_f.write(item["s1"]+"\n")
                list_of_states.append(item["s1"])

            elif parsingStates == True and item["s1"] == "end":
                parsingStates = False
                lookingForParams = True

            elif lookingForParams == True and item["s1"] == "begin" and item["s2"] == "parameters":
                parsingParams = True
                lookingForParams = False

            elif parsingParams == True and item["s1"] != "end":
                ### We directly print the paramters into the output file
                #### Desired output: k_c = gillespy2.Parameter(name='k_c',expression=0.05)
                list_of_params.append(item["s1"])
                output = f'\t\t{item["s1"]} = Parameter(name="{item["s1"]}", expression = {item["s3"]})\n'
                out_f.write(output)

            elif parsingParams == True and item["s1"] == "end": 
                parsingParams = False
                lookingForICs = True
                out_f.write("\t\tself.add_parameter([ " )
                for param in list_of_params: 
                    out_f.write( param )
                    if param != list_of_params[-1]:
                        out_f.write(" , ")
                out_f.write(" ] ) \n\n")    

            elif lookingForICs == True and item["s1"] == "begin" and item["s2"] == "IC":
                lookingForICs = False
                parsingICs = True

            elif parsingICs == True and item["s1"] != "end": 
                list_of_IC.append(item["s3"])

            elif parsingICs == True and item["s1"] == "end":
                parsingICs = False
                lookingForRules = True
                #### Printing the species and the ICs 
                #### Desired output: m = gillespy2.Species(name='monomer', initial_value=30)

                for state in list_of_states:
                    for actor in range(N):
                        actor_state = '1' if list_of_IC[actor] == state else '0'
                        output = f'{tab*2}{state}{str(actor)} = Species(name="{state}{str(actor)}", initial_value={actor_state})\n'

                        out_f.write(output)


                ### THERE IS A BETTER WAY TO DO THIS, keep a list of the species names in the generted code i believe can be an option        
                out_f.write("\t\tself.add_species([" )
                for state in list_of_states:
                    for actor in range(N):
                        out_f.write( state+str(actor) )
                        if state == list_of_states[-1] and actor == N-1:
                            continue
                        else:
                            out_f.write( " , ")
                out_f.write("] )\n\n")

            elif lookingForRules == True and item["s1"] == "begin" and item["s2"] == "rules":
                lookingForRules = False
                parsingRules = True    

            elif parsingRules == True and item["s1"] != "end":
                #### PARSING TOWARD REACTIONS
                #### DESIRED RESULT: r_c = gillespy2.Reaction(name="r_creation", rate=k_c, reactants={m:2}, products={d:1})
                #### These first 2 parse rules that talk about layers 1 and 2 with undirected edges
                if item["s2"] == '=1':
    #                 layer_idx = 0 if item["s2"] == '=1' else 1
                    layer_idx = 0
                    for edge in list_split_edges[layer_idx]:
                        output = (f'{tab*2}r_{str(rule_counter)}'
                                  f' = Reaction(\n'
                                  f'{tab*4}name = "r_{str(rule_counter)}",\n'
                                  f'{tab*4}rate = {item["s9"]},\n'
                                  f'{tab*4}reactants = {{{item["s1"]}{str(int(edge[0])-1)}: 1, {item["s3"]}{str(int(edge[1])-1)}: 1}},\n'
                                  f'{tab*4}products = {{{item["s5"]}{str(int(edge[0])-1)}: 1, {item["s7"]}{str(int(edge[1])-1)}: 1}}\n'
                                  f'{tab*3})\n\n')

                        out_f.write(output)
                        rule_counter = rule_counter + 1

                if item["s2"] == '=2':
                    layer_idx = 1
                    for edge in list_split_edges[layer_idx]:
                        output = (f'{tab*2}r_{str(rule_counter)}'
                                  f' = Reaction(\n'
                                  f'{tab*4}name = "r_{str(rule_counter)}",\n'
                                  f'{tab*4}rate = {item["s9"]},\n'
                                  f'{tab*4}reactants = {{{item["s1"]}{str(int(edge[0])-1)}: 1, {item["s3"]}{str(int(edge[1])-1)}: 1}},\n'
                                  f'{tab*4}products = {{{item["s5"]}{str(int(edge[0])-1)}: 1, {item["s7"]}{str(int(edge[1])-1)}: 1}}\n'
                                  f'{tab*3})\n\n')

                        out_f.write(output)
                        rule_counter = rule_counter + 1

                #### Attempt at parsing rules for single nodes
                if item["s2"] == '->': 
                    for actor in actors: 
                        output = (f'{tab*2}r_{str(rule_counter)}'
                                  f' = Reaction(\n'
                                  f'{tab*4}name = "r_{str(rule_counter)}",\n'
                                  f'{tab*4}rate = {item["s5"]},\n'
                                  f'{tab*4}reactants = {{{item["s1"]}{str(int(actor)-1)}: 1}},\n'
                                  f'{tab*4}products = {{{item["s3"]}{str(int(actor)-1)}: 1}}\n'
                                  f'{tab*3})\n\n')

                        out_f.write(output)
                        rule_counter = rule_counter + 1    


            elif parsingRules == True and item["s1"] == "end":
                parsingRules = False
                lookingForViews = True
                out_f.write("\t\tself.add_reaction([")
                for r in range(rule_counter):
                    out_f.write( "r_"+str(r) )
                    if r != rule_counter-1: 
                        out_f.write( " , " )
                out_f.write( "] ) \n\n" )        

            elif lookingForViews == True and item["s1"] == "begin" and item["s2"] == "views":
                lookingForViews = False
                parsingViews = True 

            elif parsingViews == True and item["s1"] != "end":
                list_of_views.append(item["s1"])

            elif parsingViews == True and item["s1"] == "end":
                parsingViews = False
                lookingForSimOptions = True

            elif lookingForSimOptions == True and item["s1"] == "begin" and item["s2"] == "simOptions":
                lookingForSimOptions = False
                parsingSimOptions = True

            elif parsingSimOptions == True and item["s1"] != "end":
                if item["s1"] == "n":
                    n_rep = int(item["s3"])
                if item["s1"] == "t":
                    T_END = int(item["s3"])

            elif parsingSimOptions == True and item["s1"] == "end":
                parsingSimOptions = False
                parsingCompleted = True
                

        footer_string = (f'{tab*2}self.timespan(numpy.linspace(0, {str(T_END)}, {str(T_END*20)}))\n\n'
                         'def run_sim(model):\n'
                         f'{tab}results = model.run(number_of_trajectories={str(n_rep)})\n'
                         f'{tab}trajectory = results.average_ensemble()\n'
                         f'{tab}plt.figure()\n')
        out_f.write(footer_string)
        trajectories = [[] for i in range(len(list_of_views))]
        out_f.write(f'{tab}trajectories = {str(trajectories)}\n')
        out_f.write(f'{tab}for i in range(len(trajectory["{list_of_views[0]}0"])):\n')
        list_of_colors = ['b','g','r','c','m','y','k']
        active_color = 0
        for view in list_of_views:
            idx = list_of_views.index(view)
            s = f'{tab*2}trajectories[{idx}].append('
            for actor in actors:
                s += f'trajectory["{view}{int(actor)-1}"][i]'
                if actor != actors[-1]:
                    s += ' + '
            s += ')\n'
            out_f.write(f'{s}')
        
        for view in list_of_views:
            idx = list_of_views.index(view)
            out_f.write(f'{tab}plt.plot(trajectory["time"], trajectories[{idx}], "{list_of_colors[idx]}", label="{view}")\n')
    
        out_f.write(f'{tab}plt.legend(loc="upper right")\n')
        out_f.write(f'{tab}plt.annotate(text=f"n = {str(n_rep)}", xy=(0.1, 0.9), xycoords="axes fraction")\n')

        out_f.write(f"{tab}plt.show()")


def parse_language_to_kappa(STEinFname, OUTFname, mln_data):
    pass
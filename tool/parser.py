import uunet.multinet as ml

def parse_language_file(language_file):
    print(f'Parsing MLN language file {language_file}')
    language = {
        'states': [],
        'parameters': [],
        'initial conditions': [],
        'rules': [],
        'views': [],
        'simOptions': []
    }
    
    language_file = open(language_file, 'r').readlines()
    
    saving_lines = False
    key = ''
    for line in language_file:
        if 'begin' in line:
            saving_lines = True
            l = line.split()[1:]
            if len(l) > 1:
                l = ' '.join(l)
            else:
                l = l[0]
            key = l
        elif 'end' in line:
            saving_lines = False

        if saving_lines and 'begin' not in line:
            language[key].append(line.strip('\n'))
            
    return language
    

def parse_mln(mln_filename):
    print(f'Parsing network configuration file {mln_filename}')
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


def parse_to_kappa(network_filename, language_filename, out_filename):
    mln_data = parse_mln(network_filename)
    language = parse_language_file(language_filename)
    
    kappa_model = ''
    kappa_model += kappa_parse_signatures(mln_data, language) + '\n\n'
    kappa_model += kappa_parse_rules(mln_data, language) + '\n'
    kappa_model += kappa_parse_variables(language) + '\n\n'
    kappa_model += kappa_parse_observables(mln_data, language) + '\n\n'
    kappa_model += kappa_parse_initial_conditions(mln_data, language)
    
    with open(out_filename, 'w') as f:
        f.write(kappa_model)

    print(f'Successfully exported model into Kappa: {out_filename}')
    

def kappa_parse_signatures(mln_data, language):
    signatures = ['/* Signatures */']
    
    states = '{' + ', '.join(language['states']) + '}'

    for actor in mln_data['actors'][0]:
        sites = []
        for j, layer in enumerate(mln_data['edges'][1]):
            for edge in layer:
                if edge[0] == actor:
                    sites.append(f'l{j+1}v{edge[1]}')
        sites = ', '.join(sites)
                                 
        kappa_signature = f'%agent: V{actor}(state{states}, {sites})'
        signatures.append(kappa_signature)
        
        
    signatures = '\n'.join(signatures)
    
    return signatures


def kappa_parse_variables(language):
    variables = ['/* Variables */']
    
    for param in language['parameters']:
        var_name, var_value = param.split('=')
        var = f"%var: '{var_name.strip()}' {var_value.strip()}"
        variables.append(var)
    variables = '\n'.join(variables)
    
    return variables


def kappa_parse_observables(mln_data, language):
    observables = ['/* Observables */']
    
    for view in language['views']:
        components = []
        for i, actor in enumerate(mln_data['actors'][0]):
            components.append(f'|V{i+1}(state{{{view}}})|')
        obs = f"%obs: '{view}' " + ' + '.join(components)
        observables.append(obs)
    
    observables = '\n'.join(observables)
    
    return observables


def kappa_parse_initial_conditions(mln_data, language):
    n = ''
    for line in language['simOptions']:
        option, value = line.split('=')
        if option.strip() == 'n':
            n = value.strip()
            break
            
    i_c = ['/* Initial conditions */',
           f'%init: {n} (']
    
    initial_states = [x.split('=') for x in language['initial conditions']]

    for i, actor in enumerate(mln_data['actors'][0]):
        sites = []
        site_labels = []
        for j, layer in enumerate(mln_data['edges'][1]):
            for edge in layer:
                if edge[0] == str(i+1):
                    # weird way to keep site labels consistent.
                    # will need a rewrite
                    if i+1 <= int(edge[1]):
                        site_label = f'{j+1}{i+1}{edge[1]}'
                    else:
                        site_label = f'{j+1}{edge[1]}{i+1}'
                        
                    sites.append(f'l{j+1}v{edge[1]}[{site_label}]')
        sites = ', '.join(sites)
        
        initial_state = ''
        for state in initial_states:
            if state[0].strip() == str(i+1):
                initial_state = state[1].strip()
                
        condition = f'V{i+1}(state{{{initial_state}}}, {sites})'
        
        # add a comma unless it's the last entry
        if i + 1 < int(mln_data['actors'][1]):
            condition += ','
        
        i_c.append(condition)
    
    i_c.append(')')
        
    i_c = '\n'.join(i_c)
    
    return i_c


def kappa_parse_rules(mln_data, language):
    kappa_rules = ['/* Rules */']
    
    rules = [x.split('@') for x in language['rules']]
    rules_organised = []
    for ruleset in rules:
        rules_organised.append({'rule': ruleset[0].strip(), 'rate': ruleset[1].strip()})

    for ruleset in rules_organised:
        if '=' not in ruleset['rule']:
            # parse rules not dependant on layers
            rule_states = [state.strip() for state in ruleset['rule'].split('->')]
            kappa_rules.append(f"'{rule_states[0]} to {rule_states[1]}'")
            for i, actor in enumerate(mln_data['actors'][0]):
                kappa_rule = f"V{i+1}(state{{{rule_states[0]}}}) -> V{i+1}(state{{{rule_states[1]}}}) @ '{ruleset['rate']}'"
                kappa_rules.append(kappa_rule)
        else:
            # parse intra-layer rules
            # requires rules in both directions
            rule_sides = [state.strip() for state in ruleset['rule'].split('->')]
            layer = rule_sides[0][rule_sides[0].index('=')+1].strip()

            states = [[x[0].strip(), x[1].strip()] for x in [rule_side.split(f'={layer}') for rule_side in rule_sides]]
            kappa_rules.append(f"'{layer}: {states[0][0]}-{states[0][1]} to {states[1][0]}-{states[1][1]}'")
            for edge in mln_data['edges'][1][int(layer)-1]:
                v1, v2 = edge[0], edge[1]
                kappa_rules.append(f"// V{v1} - V{v2}")
                site_label = f'{layer}{v1}{v2}'
                kappa_rule = (f'V{v1}(state{{{states[0][0]}}}, l{layer}v{v2}[{site_label}]), V{v2}(state{{{states[0][1]}}}, l{layer}v{v1}[{site_label}]) -> '
                    f'V{v1}(state{{{states[1][0]}}}, l{layer}v{v2}[{site_label}]), V{v2}(state{{{states[1][1]}}}, l{layer}v{v1}[{site_label}]) @ '
                    f"'{ruleset['rate']}'")

                kappa_rules.append(kappa_rule)

        kappa_rules.append('')

    kappa_rules = '\n'.join(kappa_rules)

    return kappa_rules


def parse_to_gillespy(network_filename, language_filename, out_filename):
    mln_data = parse_mln(network_filename)
    language = parse_language_file(language_filename)

    tab = '\t'

    header_string = (
        f'import numpy\n'
        f'import matplotlib.pyplot as plt\n'
        f'from gillespy2.core import (\n'
        f'{tab}Model,\n'
        f'{tab}Species,\n'
        f'{tab}Reaction,\n'
        f'{tab}Parameter)\n\n'
        f'class Mln_dynamics(Model):\n'
        f'{tab}def __init__(self,parameter_values=None):\n'
        f'{tab * 2}Model.__init__(self, name="MLN")\n\n'
    )
    
    params = gillespie_parse_parameters(language)
    species = gillespie_parse_species(mln_data, language)
    reactions = gillespie_parse_reactions(mln_data, language)
    timespan = gillespie_parse_timespan(mln_data, language)
    footer = gillespie_parse_sim_options(mln_data, language)
    
    result = (
        header_string +
        params + '\n' +
        species + '\n' +
        reactions + '\n' +
        timespan + '\n' +
        footer
    )
    
    with open(out_filename, 'w') as f:
        f.write(result)
    
#     return result


def gillespie_parse_parameters(language):
    tab = '\t'
    params = []
    param_names = []
    
    for param in language['parameters']:
        name, value = param.split('=')
        param_names.append(name.strip())
        params.append(f"{tab}{tab}{name.strip()} = Parameter(name='{name}', expression={value})")
    
    params.append(f"{tab}{tab}self.add_parameter([{', '.join(param_names)}])\n")
    params = '\n'.join(params)
    
    return params


def gillespie_parse_species(mln_data, language):
    tab = '\t'
    species = []
    species_names = []
    
    for state in language['states']:
        for actor in mln_data['actors'][0]:
            species_names.append(f"{state}{actor}")
            init_value = 0
            for init_conditions in language['initial conditions']:
                name, value = init_conditions.split('=')
                if actor == name.strip() and state == value.strip():
                    init_value = 1
                    break
            species.append(f"{tab}{tab}{state}{actor} = Species(name='{state}{actor}', initial_value={init_value})")
    
    species.append(f"{tab}{tab}self.add_species([{', '.join(species_names)}])\n")
    species = '\n'.join(species)
    
    return species


def gillespie_parse_reactions(mln_data, language):
    tab = '\t'
    reactions = []
    reaction_names = []
    counter = 0
    
    for rule in language['rules']:
        nodes, rate = rule.split('@')
        rate = rate.strip()
        
        if '=' not in nodes:
            # a simple state-to-state rule for a single node
            left_node, right_node = nodes.split('->')
            left_node = left_node.strip()
            right_node = right_node.strip()
            
            for i in range(1, mln_data['actors'][1] + 1):
                name = f"{left_node}{i}_to_{right_node}{i}_{counter}"
                reaction = (
                    f"{tab * 2}{name} = Reaction(\n"
                    f"{tab * 4}name = '{name}',\n"
                    f"{tab * 4}rate = {rate},\n"
                    f"{tab * 4}reactants = {{{left_node}{i}: 1}},\n"
                    f"{tab * 4}products = {{{right_node}{i}: 1}}\n"
                    f"{tab * 3})\n"
                )
                
                reactions.append(reaction)
                reaction_names.append(name)
                counter += 1
        else:
            # two-node rule
            left_side, right_side = nodes.split('->')
            layer_index = int(left_side[left_side.index('=')+1].strip())
            
            left_reactant_1, left_reactant_2 = left_side.split(f"={layer_index}")
            right_reactant_1, right_reactant_2 = right_side.split(f"={layer_index}")
            
            left_reactant_1 = left_reactant_1.strip()
            left_reactant_2 = left_reactant_2.strip()
            right_reactant_1 = right_reactant_1.strip()
            right_reactant_2 = right_reactant_2.strip()
            
            for edge in mln_data['edges'][1][layer_index-1]:
                # note that this list already takes into account directionality of edges
                name = f"{left_reactant_1}{edge[0]}_{left_reactant_2}{edge[1]}_to_{right_reactant_1}{edge[0]}_{right_reactant_2}{edge[1]}_{counter}"
                reaction = (
                    f"{tab * 2}{name} = Reaction(\n"
                    f"{tab * 4}name = '{name}',\n"
                    f"{tab * 4}rate = {rate},\n"
                    f"{tab * 4}reactants = {{{left_reactant_1}{edge[0]}: 1, {left_reactant_2}{edge[1]}: 1}},\n"
                    f"{tab * 4}products = {{{right_reactant_1}{edge[0]}: 1, {right_reactant_2}{edge[1]}: 1}}\n"
                    f"{tab * 3})\n"
                )
                
                reactions.append(reaction)
                reaction_names.append(name)
                counter += 1
                
    
    reactions.append(f"{tab * 2}self.add_reaction([{', '.join(reaction_names)}])\n")
    reactions = '\n'.join(reactions)
    
    return reactions


def gillespie_parse_timespan(mln_data, language):
    tab = '\t'
    t_value = int(language['simOptions'][1].split('=')[1].strip())
    
    # note that below t_value is multiplied by 20 - I don't know why
    timespan = f"{tab * 2}self.timespan(numpy.linspace(0, {t_value}, {t_value * 20}))\n"
    
    return timespan


def gillespie_parse_sim_options(mln_data, language):
    tab = '\t'
    n_value = int(language['simOptions'][0].split('=')[1].strip())
    trajectories = [[] for i in range(len(language['views']))]
    trajectories_loop = []
    plots = []
    
    list_of_colours = ['b','g','r','c','m','y','k']
    active_colour = 0
    for i, view in enumerate(language['views']):
        appends = []
        for actor in mln_data['actors'][0]:
            appends.append(f"trajectory['{view}{actor}'][i]")
        
        appends = ' + '.join(appends)      
        trajectories_loop.append(f"{tab * 2}trajectories[{i}].append({appends})")
        
        plots.append(f"{tab}plt.plot(trajectory['time'], trajectories[{i}], '{list_of_colours[active_colour]}', label='{view}')")
        active_colour += 1
                           
    trajectories_loop = '\n'.join(trajectories_loop)
    plots = '\n'.join(plots)
                           
    footer = (
        f"def run_sim(model):\n"
        f"{tab}results = model.run(number_of_trajectories={n_value})\n"
        f"{tab}trajectory = results.average_ensemble()\n"
        f"{tab}plt.figure()\n"
        f"{tab}trajectories = {trajectories}\n"
        f"{tab}for i in range(len(trajectory['{language['views'][0]}1'])):\n"
        f"{trajectories_loop}\n"
        f"{plots}\n"
        f"{tab}plt.legend(loc='upper right')\n"
        f"{tab}plt.annotate(text=f'n = {n_value}', xy=(0.1, 0.9), xycoords='axes fraction')\n"
        f"{tab}plt.show()"
    )
    
    return footer





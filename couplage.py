import networkx as nx


# implémentation de l'algorithme d'Edmonds ici


def update_matching(matching, alternating_path):
    new_matching = set(matching)
    for edge in alternating_path:
        if edge in matching:
            new_matching.remove(edge)
        else:
            new_matching.add(edge)
   
    # Vérifier si l'arête complémentaire est présente
    for edge in matching:
        if edge not in alternating_path:
            new_matching.add(edge)
   
    return new_matching


def choose_edge(tree, dfs_set):
    for edge in tree.edges:
        if (edge[0] in dfs_set and edge[1] not in dfs_set) or (edge[1] in dfs_set and edge[0] not in dfs_set):
            # Vérifier si l'arête forme un cycle impair
            cycle_nodes = nx.shortest_path(tree, source=edge[0], target=edge[1])
            if len(cycle_nodes) % 2 == 1:
                return edge






def construct_alternating_tree(graph, matching):
    tree = nx.Graph()
    dfs_set = set()
    alternating_path = []


    # Sélectionner un sommet non apparié comme racine
    root = [node for node in graph.nodes if node not in matching][0]


    def dfs(v, parent, in_matching_edge):
        nonlocal alternating_path


        dfs_set.add(v)
        for u in graph.neighbors(v):
            if u == parent:
                continue


            if in_matching_edge and (v, u) in matching:
                # Arête du couplage
                dfs(u, v, not in_matching_edge)
            elif not in_matching_edge and (v, u) not in matching:
                # Arête libre
                dfs(u, v, not in_matching_edge)
                alternating_path.append((v, u))
                dfs_set.add(u)


    dfs(root, None, True)
    tree.add_edges_from(alternating_path)


    return tree, dfs_set, alternating_path


def edmonds_algorithm(graph):
    matching = nx.max_weight_matching(graph, maxcardinality=True)
    return matching


# le graphe de notre problème
G = nx.Graph()
G.add_edges_from([("Mathématiques","Matin"),("Mathématiques",
"après-midi"),("Physique ","après-midi"),("Physique" ,"soir" ),("d’informatique" ,"Matin"),("informatique","soir"),("français","Matin"),("Histoire" ,"après-midi" )
                  ,("Histoire","soir"),("Économie","Matin" ),("Économie","après-midi" ),("Économie" ,"soir")])


# Affichage du graphe initial sous forme de liste d'arêtes
edge_list = list(G.edges)
print("Graphe initial (sous forme de liste d'arêtes):", edge_list)


# Vérifier la bipartition
"""if nx.is_bipartite(G):
    print("Le graphe est biparti.")
else:
    print("Le graphe n'est pas biparti.")"""


# Application de l'algorithme
result = edmonds_algorithm(G)
print("Couplage maximal:", result)
import matplotlib.pyplot as plt
# Création du sous-graphe avec les arêtes du couplage maximal
matching_graph = G.edge_subgraph(result)

# Affichage du sous-graphe avec les arêtes du couplage maximal
pos = nx.spring_layout(G)  # Vous pouvez utiliser une disposition différente selon vos préférences

plt.figure("le graph finale de couplage maximal ")

# Sous-graphe du couplage maximal
nx.draw(matching_graph, pos=pos, with_labels=True, font_weight='bold', node_color='lightblue', node_size=800, edge_color='red', width=2)

plt.title('Sous-graphe du Couplage Maximal')
plt.show()
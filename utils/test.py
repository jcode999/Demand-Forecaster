def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            new_paths = find_all_paths(graph, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths

# graph = {
#     'u': ['v', 'x', 'w'],
#     'v': ['u', 'w', 'x'],
#     'w': ['u', 'v', 'x', 'y', 'z'],
#     'x': ['u', 'v', 'w', 'y'],
#     'y': ['x', 'w', 'z'],
#     'z': ['w', 'y']
# }
# paths = find_all_paths(graph,'z','w')
# for path in paths:
#     print(path)

#Define the cost to get from one node to another
def dijkstra(graph,start,end):
    #keep track of the lowest cost to get to each node
    costs = {}
    #keep track of the parent node of each node
    parents = {}
    #keep track of all the nodes that have been processed
    processed = []
    
    #assign a cost of zero to the start node and an infinite cost to all other nodes
    infinity = float('inf')
    for node in graph:
        costs[node] = infinity
    costs[start] = 0
    
    #find the lowest cost node that has not yet been processed
    node = lowest_cost_node(costs, processed)
    
    #if the lowest cost node is the destination node we are done
    while node is not None and node != end:
        cost = costs[node]
        #go through all the neighbors of this node
        neighbors = graph[node]
        for n in neighbors.keys():
            new_cost = cost + neighbors[n]
            #if it is cheaper to get to this neighbor by going through this node
            if costs[n] > new_cost:
                #update the cost for this node
                costs[n] = new_cost
                #this node becomes the new parent for this neighbor
                parents[n] = node
        #mark the node as processed
        processed.append(node)
        #find the next node to process and loop
        node = lowest_cost_node(costs, processed)
        
    #build the path and return
    path = [end]
    while end != start:
        path.append(parents[end])
        end = parents[end]
    path.reverse()
    return path

#find the node with the lowest cost that has not yet been processed
def lowest_cost_node(costs, processed):
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node

#table of how the algorithm made decisions
graph = {
    'A': {'B': 5, 'C': 1},
    'B': {'A': 5, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 4, 'E': 8},
    'D': {'B': 1, 'C': 4, 'E': 3, 'F': 6},
    'E': {'C': 8, 'D': 3},
    'F': {'D': 6}
}
print('Decision Table:')
print('Node | Cost | Parent')
    #find the path
path = dijkstra(graph, 'A', 'F')
    #print the path and the cost
cost = 0
for i in range(len(path)-1):
    cost += graph[path[i]][path[i+1]]
    print(f'{path[i]} -> {path[i+1]} |  {cost}  | {path[i]}')

# import networkx as nx 
 
# # Create an empty graph 
# G = nx.Graph() 
  
# # Add edges in the graph 
# G.add_weighted_edges_from([('x','z',8),('x','y',6),('x','w',6),('x','v',3), 
#                            ('y','x',6),('y','z',12),('y','t',7),('y','v',8), 
#                            ('z','x',8),('z','y',12),
#                            ('t','y',7),('t','v',4),('t','u',2),
#                            ('u','t',2),('u','v',3),('u','w',3),
#                            ('v','x',3),('v','y',8),('v','t',4),('v','u',3),('v','w',4),
#                            ('w','x',6),('w','u',3),('w','v',4)
#                            ]) 
  
# # Calculate the shortest path using Djikstra's algorithm 
# dest_nodes = ['y','z','t','u','v','w']
# for node in dest_nodes:
#     print('Path from x to ',node)
#     shortest_path = nx.dijkstra_path(G, 'x', node)
#     print(shortest_path)
#     print('\n')



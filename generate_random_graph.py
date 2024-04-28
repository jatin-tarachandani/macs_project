import networkx as nx
import json, random
import sys

#final objective: generate ned file with barabasi albert graph 

def generate_ba_graph(n, m, seed=-1):
    
    if seed == -1:
        seed = random.randint(0, 1000)
    
    G = nx.barabasi_albert_graph(n, m, seed)
    
    return G

def template_ned_file(network_name, num_nodes, num_repos, node_repo_string, num_clients, node_client_string, connection_string):
    # def generate_network_file(package_name, network_name, base_network, num_nodes):
    template = f"""\
package networks;

network {network_name}_network extends base_network {{

    parameters:
        // Number of ccn nodes
        n = {num_nodes};
        
    node_repos={node_repo_string};
    num_repos = {num_repos};
    replicas=1;
    
    num_clients={num_clients};
    node_clients={node_client_string};

connections allowunconnected:
{connection_string}

}}"""

    return template

def generate_connections(graph):
    
    connection_string = ""
    for e in graph.edges:
        i = e[0]
        j = e[1]
        delay = random.uniform(0.5, 5)
        connection=f"node[{i}].face++ <--> {{delay = {delay}ms;}} <--> node[{j}].face++;\n"
        connection_string += connection
    
    return connection_string

def generate_hub_nodes(graph, num_hubs):
    
    nodelist_by_deg = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    
    hubstring = "\""
    
    for elem in nodelist_by_deg[:num_hubs]:
        hubstring+=f"{elem[0]},"
    hubstring+="\""
    return hubstring

def generate_client_nodes(graph, num_clients):
    
    nodelist_by_deg = sorted(graph.degree, key=lambda x: x[1])
    
    clientstring = "\""
    
    for elem in nodelist_by_deg[:num_clients]:
        clientstring += f"{elem[0]},"
    clientstring+="\""
    return clientstring

def generate_ned_file(G, fileprefix, num_hubs, num_clients):
    
    
    
    hubstring = generate_hub_nodes(G, num_hubs)
    
    clientstring = generate_client_nodes(G, num_clients)
    
    connectionstring = generate_connections(G)
    
    filestring = template_ned_file(fileprefix, G.number_of_nodes(), num_hubs, hubstring, num_clients, clientstring, connectionstring)
    
    with open(fileprefix+'.ned', 'w') as f:
        f.write(filestring)
    





if __name__ == "__main__":
    n = (int)(sys.argv[1])
    m = (int)(sys.argv[2])
    fileprefix = sys.argv[3]

    G = generate_ba_graph(n, m, seed = 1)
    #change seed if needed
    generate_ned_file(G, fileprefix, 1, n - 1)


    




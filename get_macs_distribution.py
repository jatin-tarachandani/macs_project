import numpy as np
from tqdm import tqdm
from generate_random_graph import generate_ba_graph
import networkx as nx
import json

def pretty_print_probabilities_(probabilities):
    # Convert probabilities to a numpy array for easy manipulation
    prob_array = np.array(probabilities)
    # Get the shape of the array
    rows, cols = prob_array.shape
    # Find the maximum length of a probability value for formatting
    max_len = len(str(np.max(prob_array)))
    # Define the format string for each probability value
    format_str = "{:." + str(max_len) + "f}"
    
    # Print the 2D array of probabilities
    for row in range(rows):
        for col in range(cols):
            # Format each probability value and print
            print(format_str.format(prob_array[row][col]), end=" ")
        print()  # Move to the next row after printing all columns


def create_zipf_dist(M, alpha):
    '''
    Input: 
    M, size of the content set that follows Zipf law
    alpha, zipf law exponent
    '''
    
    pmf = np.array(M)
    
    
    
    vals = np.array([np.power(float(i), -alpha) for i in range(1, M+1)])
    
    norm_factor = np.sum(vals)
    
    vals = vals/norm_factor
    
    return vals
    

def create_prob_matrix(zipf_prob, N):
    
    
    
    
    pi = np.ones((N+1, R))
    gamma = np.zeros((N+1, R))
    
    pi[0, :] = zipf_prob
    gamma[0, :] = zipf_prob
    
    for i in range(1, N+1):  
        
        
        if(i != N):
            pcsum = np.sum(np.multiply(zipf_prob, np.sum(pi[:i, :], axis=0)))
            removed_terms = np.multiply(zipf_prob, np.sum(pi[:i, :], axis=0))
            gamma[i, :] = pcsum - removed_terms
        else:
            gamma[i, :] = 1 - zipf_prob
        
        
        pi[i, :] = np.multiply(zipf_prob, (1 - zipf_prob))
        for j in range(1, i):
            pi[i, :] = np.multiply(pi[i, :], (1 - zipf_prob - gamma[j, :]))
            pi[i, :] = np.divide(pi[i, :], (1 - gamma[j+1, :]))
        
        pi[i, :] = np.divide(pi[i, :], (1 - gamma[1, :]))
        
    
    return pi, gamma

def compute_out_stream(zipf, pi, network):
    
    
    
    ms = np.multiply(zipf, pi[-1, :])
    
    return ms


def compute_in_stream(R, network, ms):
    
    #content is only located on one node
    nrv = np.zeros((int(network.number_of_nodes()), R))
    
    repo = sorted(network.degree, key=lambda x: x[1], reverse=True)[-1][0]
    
    shortest_paths = nx.single_target_shortest_path(network, repo)
    # print(shortest_paths)
    for v in network.nodes():
        u_set = []
        #construct NH set
        for path in shortest_paths.items():
            
            if len(path[1]) > 1 and path[1][1] == v:
                u_set.append(path[0])
        
        for u in u_set:
            nrv[v, :] += ms * np.float_power(1 - ms, len(u_set) - 1)
    
    return nrv
    
def compute_pprime(R, zipf, nrv):
    
    p_prime = np.zeros((nrv.shape[0], R))
    
    sum_nrv = np.sum(nrv, axis=1).reshape(-1, 1)
    
    
    for v in range(nrv.shape[0]):
        p_prime[v, :] = np.divide(nrv[v, :] + zipf, 1 + sum_nrv[v])
    
    return p_prime #shape is V x R
    


'''
Parameters of the simulation:
N = size of cache
R = size of content set
alpha = Zipf law skew parameter
n = number of nodes in the network
m = number of nodes in seed network for Barabasi Albert graphs
graph_seed = seed for generating the graph
'''
N = 20
R = 2000
alpha = 1

n = 50
m = 3
graph_seed = 1

'''
END PARAMS
'''


zipf = create_zipf_dist(R, alpha)
pi, gam = create_prob_matrix(zipf, N)

network = generate_ba_graph(n, m, seed=graph_seed)
ms = compute_out_stream(zipf, pi, network)
nrv = compute_in_stream(R, network, ms)
p_prime = compute_pprime(R, zipf, nrv)
#this is V x R matrix

pi_nodes = np.zeros((network.number_of_nodes(), N+1, R))
gamma_nodes = np.ones((network.number_of_nodes(), N+1, R))


for v in range(network.number_of_nodes()):
    pi_nodes[v, :, :], gamma_nodes[v, :, :] = create_prob_matrix(p_prime[v, :], N)

#write these matrices to file 

    
np.save(f"pi_{n}_{m}_{graph_seed}_{N}_{R}.npy", pi_nodes)

np.save(f"gamma_{n}_{m}_{graph_seed}_{N}_{R}.npy", gamma_nodes)



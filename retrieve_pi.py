import numpy as np

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

'''
Simulation parameters similar to get_macs_distribution.py
'''
n=50
m=3
graph_seed=1
N=20
R=2000




pi = np.load(f'pi_{n}_{m}_{graph_seed}_{N}_{R}.npy')
zipf = create_zipf_dist(2000, 1)

with open(f'MACS_output_{n}_{m}_{graph_seed}_{N}_{R}.txt', 'w') as f:
    for i in range(50):
        pi_node = pi[i, :]
        p_miss_r = pi_node[-1, :]
        p_hit_r = 1 - p_miss_r
        
        p_hit = np.sum(np.multiply(zipf, p_hit_r))
        
        
        f.write(f"Node {i} hit rate: {p_hit}\n")
            
        print(f"Node {i} hit rate: {p_hit}")

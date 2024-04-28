# Markov Chain Approximations to evaluate CCN caching systems

Presentation given by Taha Adeel Mohammed and Jatin Tarachandani for CS5150: Applications of Markov Chains at IIT Hyderabad.


# Files

* generate_random_graph.py - This file generates the Barabasi-Albert random graph in the form of a ccnSim topology description file. This can be further copied into your ccnSim environment to run simulations.
```
    $ python generate_random_graph.py <total_nodes> <starter_graph_nodes> <filename_prefix>
```
The file will be generated as <filename_prefix>.ned.

* get_macs_distribution.py - This file generates the MACS distribution across all the nodes in the network using the formulas given in (Ben-Ammar et al., [2018](https://doi.org/10.1109/GLOCOM.2018.8648055)). The parameters of the MC-based approximation are marked within the script and can be tweaked as per requirements. It outputs 2 files: one file containing the computed stationary distribution probabilities for each node-state-content_rank combination as pi\_\<n>\_<m\>\_\<graph_seed\>\_\<N\>\_\<R\>.npy, and one containing the computed transition probabilities gamma for each node-state-content_rank combination, in a similar format. 
* retrieve_pi.py - This file gets the per-node overall hit rate from the computed Markov Chain stationary distribution stored in pi\_\<n>\_<m\>\_\<graph_seed\>\_\<N\>\_\<R\>.npy in the same folder. The values of these parameters can be modified from within the script. 
* plotzipf.py - simple file to plot Zipf distributions using scipy.stats

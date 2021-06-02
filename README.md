# A Star Algorithm

Python implementation of the A Star search algorithm for routes of paris subway stations

# Implementation

- Define a Node class to hold the node data of the search tree
- Cost function to calculate the real distance from node child to node parent
- Min value function to get a new node from the frontier, consider the H (estimate distance) + G (distance to initial node)

# Returns

Prints the frontier configuration on each iteration and at the end prints the path (solution) and Total cost in time (considering that the train velocity is 30km/h)

# Dataset

| Station1 (name)        | Station2 (name)           | Estimate Distance (km)  | Real Distance (km) |
| ---------------------- |:-------------------------:|:-----------------------:| ------------------:|
| E1                     | E2                        | 12.0                    | 10.0               |

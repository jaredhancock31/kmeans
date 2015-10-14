#!/usr/bin/env python

# Author: Jared Hancock


import numpy as np
import random
import sys
import itertools as it


def cluster_points(data, centroids):
    clusters = {}
    for coord in data:
        # calc the cluster it belongs to based on euclidean distance from center
        bestCluster = min([(i[0], np.linalg.norm(coord-centroids[i[0]]))for i in enumerate(centroids)], key=lambda t:t[1])[0]

        try:
            clusters[bestCluster].append(coord)
        except KeyError:
            clusters[bestCluster] = [coord]
    return clusters


def update_centers(oldCenter, clusters):
    newCenter = []
    keys = sorted(clusters.keys())
    for k in keys:
        newCenter.append(np.mean(clusters[k], axis = 0))
    return newCenter


def is_converged(nextC, oldC):
    return set([tuple(a) for a in nextC]) == set([tuple(a) for a in oldC])


def find_centers(data, K=3):
    # Initialize to K random centers
    oldC = random.sample(data, K)
    nextC = random.sample(data, K)

    while not is_converged(nextC, oldC):
        oldC = nextC
        # Assign all points in data to clusters
        clusters = cluster_points(data, nextC)
        # Reevaluate centers
        nextC = update_centers(oldC, clusters)
    return nextC, clusters

def get_data(filename):
    data = []
    with open(filename) as f:
        for l in f:
            x = map(int, l.split())
            data.append(x)
    data = np.array(data)
    return data


def main():
    #data = get_data("data.txt")
    #print len(sys.argv)
    #k = 4

    data = get_data(sys.argv[2])
    k = int(sys.argv[1])

    chunk, finalClusters = find_centers(data, k)

    # for key in finalClusters.keys():
    #     for l in it.chain(finalClusters[key]):
    #         print l[0], " ", l[-1], " ", key


    with open("converged.txt", "w") as inf:
        for key in finalClusters.keys():
            for l in it.chain(finalClusters[key]):
                x = str(l[0])
                y = str(l[-1])
                outStr = x + "     " + y + "     " + str(key) + "\n"
                inf.write(outStr)


main()





# line 16 credit to: datasciencelab

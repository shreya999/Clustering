import numpy as np
import os
import math
import time
import sys
from pca_visualization import pca
import ExternalIndex_Computation

global old_centroid
old_centroid = []
count = 0


def euclidean_distance(brr, old_centroid):
    """
    Calculates euclidean distance of the given data.
    .........................................................................................
        Args:
            {Input}: brr, Original Data set containing all attributes.
            {Input}: clusters, All clusters of the data points
        Returns:
            {Output} distance, passes the euclidean distance of every point from clusters to assign_cluster function
    """
    distance = [[0 for i in range(unique_length)] for j in range(len(brr))] # Compute distance of every point from a cluster
    k=0
    for i in range(0, len(brr)):
        for l in range(0, unique_length):
            templist = old_centroid[l]
            for j in range(0, len(brr[0])):
                distance[i][k] += math.pow((brr[i][j] - templist[j]),2)
            distance[i][k] = math.sqrt(distance[i][k])
            k += 1
            if k == unique_length :
                k = 0
    assign_clusters(distance)


def assign_clusters(distance):
    """
    Calculates euclidean distance of the given data.
    .........................................................................................
        Args:
            {Input}: distance, All distances of evey point to every cluster
        Returns:
            {Output}: list_final_pos, Passes the list_final_pos to calculate centroids of the oints contained in the list
    """
    pos = 0
    dict_pos = {}

    for i in range(0,len(distance)):
        min = sys.maxsize
        for j in range(0, len(distance[0])):
            if min > distance[i][j]:
                min = distance[i][j]
                pos = j
                dict_pos[i] = pos

    c = 0
    list_final_pos = []
    for i in range(0, unique_length):
        list_pos = []
        for j in range(len(dict_pos)):
            if dict_pos[j] == c:
               list_pos.append(j)
        c +=1
        list_final_pos.append(list_pos)
    cal_centroid(list_final_pos)



def cal_centroid(new_data):
    """
    Calculates centroid of every cluster
    .........................................................................................
        Args:
            {Input}: new_data, List of data points belonging to every cluster
        Returns:
            {Output}:  final_centroid, Passes the new computed centroids of every cluster to checkConvergence functions
    """
    final_centroid = []
    for i in range(0, len(new_data)):
        currlist_cent = []
        for j in range(0, len(brr[0])):
            sum = 0
            for l in range(0, len(new_data[i])):
                sum += brr[new_data[i][l]][j]
            avg = sum/len(new_data[i])
            currlist_cent.append(avg)
        final_centroid.append(currlist_cent)

    checkConvergence(final_centroid, new_data)



def checkConvergence(final_centroid, list_final_clusters):
    """
    Computes and checks if the new centroids are same as the old centroid. If yes, the algorithm converges; else
    it again iterates over euclidean_distance function
    .........................................................................................
        Args:
            {Input}: final_centroid, Computed new centroids of the data point
            {Input}: list_final_clusters, List containing gene ids of every cluster
        Returns:
            {Output}: Computes the pca graph and passes values to compute external index results if the results
            converges, else iterates from the euclidean distance
    """
    #print("new cent.................",final_centroid)
    #print("old...............", old_centroid)
    answer = np.array_equal(final_centroid, old_centroid)
    global count
    if answer == False and no_of_iterations != count:
        count +=1
        old_centroid.clear()
        for i in range(0, len(final_centroid)):
            old_centroid.append(final_centroid[i])
        final_centroid.clear()
        euclidean_distance(brr, old_centroid)
    else:
        #print(count)
        print("Cluster list: ", list_final_clusters)
        graph_label = "K-means: Result("+ file_name+")"

        j=1
        labels_algo = []
        for i in range(0, len(brr)):
            for j in range(0, len(list_final_clusters)):
                if i in list_final_clusters[j]:
                    labels_algo.append(j+1)

        pca(brr, labels_algo,graph_label, no_of_clusters)
        list_final_clusters1 = []
        for i in range (0, len(list_final_clusters)):
            templist = []
            for j in range(0,len(list_final_clusters[i])):
                templist.append(list_final_clusters[i][j]+1)
            list_final_clusters1.append(templist)

        kmeansClusterValidation(groundtruth_map,brr,list_final_clusters1)


def kmeansClusterValidation(groundTruthMap, geneList, list_final_clusters1):
    """
    Computes and checks if the new centroids are same as the old centroid. If yes, the algorithm converges; else
    it again iterates over euclidean_distance function
    .........................................................................................
        Args:
            {Input}: groundTruthMap, The new centroids of the data point
            {Input}: geneList,
        Returns:
            {Output}: Computes the pca and passes values to compute external index results
        """
    kmeansAlgoClusterMap = {}
    noiseList =[]
    size = len(geneList)
    ExternalIndex_Computation.computeAlgoClusterMap(list_final_clusters1, kmeansAlgoClusterMap,noiseList)
    groundTruthClusterMatrix = np.zeros((size,size), dtype=np.int)
    algoClusterMatrix = np.zeros((size,size), dtype=np.int)
    ExternalIndex_Computation.computeGroundTruthAndAlgoClusterMatrix(groundTruthMap, geneList, groundTruthClusterMatrix, kmeansAlgoClusterMap,algoClusterMatrix)
    ExternalIndex_Computation.computeJaccardCoefficient(groundTruthClusterMatrix,algoClusterMatrix,size)


"""
Main Script
"""
# Read and open the file
file_path = input("Enter the input File Name: ")
file_name = os.path.basename(file_path)
graph_label = "K-means: Original data points("+ file_name+")"
open_file = open(file_path, "r")
file = open_file.readlines()

no_of_iterations = input("Enter the no of iterations: ")
no_of_clusters = input("Enter the no of clusters: ")
no_of_iterations = int(no_of_iterations)
no_of_clusters = int(no_of_clusters)

user_input = input("Enter the initial clusters space separated: ")
input_list = user_input.split(' ')
initial_clusters = [int(x.strip())-1 for x in input_list]
init_list = [initial_clusters[i] for i in range(len(initial_clusters))]

# Append all the data into a list
data = []
for x in file:
    lines = x.split("\n")
    if lines[1] == '' and len(lines[1]) == 0:
        del lines[1]
    for line in lines:
        data.append(line.split("\t"))
data = np.array(data)

# Convert data to float values
global arr
arr = data[:,:]
arr = arr.tolist()
for i in range(0, len(arr)):
    for j in range(0,len(arr[0])):
       arr[i][j] = float(arr[i][j])
arr = np.array(arr)

# Get all the attributes
global brr
brr = arr[:,2:]
brr = brr.tolist()

#Form the initial clusters based on user points
old_centroid = arr[initial_clusters][:,2:]
old_centroid = old_centroid.tolist()

# Get the all ground truth labels
labels = arr[:,1]
labels = labels.astype(np.int64)
global unique_lab
unique_lab = np.unique(labels) # All unique labels

unique_length = len(np.unique(labels))
for i in range(0,len(unique_lab)):
    if unique_lab[i] == -1:
        unique_length = len(unique_lab) -1

# Calculate pca of original data set
pca(brr, labels, graph_label, unique_length)
unique_length = no_of_clusters
#random = np.random.randint(0,arr.shape[0]-1, unique_length) # [378, 55, 51, 35, 237] [464,246,261,397,396,84,67,361,412,247,4], [505,364,145,456,60,41,472,366,460,449,4]

groundtruth_map = {}
k = 1
for i in range(0,len(arr)):
    groundtruth_map[k] = int(arr[i][1])
    k += 1

# Calculate euclidean distance
start_time = time.time()
euclidean_distance(brr, old_centroid)
print("--- %s seconds ---" % (time.time() - start_time))





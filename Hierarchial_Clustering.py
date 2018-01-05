import numpy as np
import math
import time
import copy
import os
import ExternalIndex_Computation
from pca_visualization import pca
import importlib

importlib.reload(ExternalIndex_Computation)
labels = []

'''
{createGeneList}: Reads the file line by line, splits each line using tab, 
creates a list containing the attributes for each object/gene id in the dataset, 
also creates a groundTruthMap containing the ground truth values for the dataset
.........................................................................................
{Input}: file, input file containing the dataset
{Input}: file_name, name of file containing dataset
{Output}: geneList, list containing attributes for each data point
{Output}: groundTruthMap, map containing the ground truth values for dataset
'''
def createGeneList(file, groundTruthMap, geneList, file_name):
    k=1
    for line in iter(file):
        record = line.strip().split("\t")
        groundTruthMap[k] = int(record[1])
        labels.append(int(record[1]))
        k = k+1
        floatRec =[]
        for r in range(2,len(record)):
            num = float(record[r])
            floatRec.append(num)
        geneList.append(floatRec)
    no_of_clusters = int(np.unique(int(record[1])))
    graph_label = "Hierarchical Original (" + file_name + ")"
    pca(geneList, labels, graph_label, no_of_clusters)
    

'''
{createDistanceMatrix}: Create a distance matrix from the given dataset by 
computing the distance between all the attributes between two points/objects in 
the dataset using euclidean measure
..........................................................................................
{Input}: geneList, list containing attributes for each data point
{Output}: clusterMap, stores the clusters formed at each level, 
initially contains all individual points each as a single cluster
{Output}: distanceMatrix, distance matrix for the dataset using euclidean 
'''
def createDistanceMatrix(distanceMatrix, geneList, clusterMap):
    clusterList=[]
    for i in range(0,len(geneList)):
        clusterList.append([i+1])
        for j in range(0,len(geneList)):
            if i == j:
                distanceMatrix[i][j]= 0
            else:
                dist = calculateEuclidean(geneList[i], geneList[j])
                distanceMatrix[i][j] = dist
                distanceMatrix[j][i] = dist
    clusterMap[0] = clusterList


'''
{calculateEuclidean}: Computes the distance between all the attributes between 
two points in the dataset using euclidean measure
..........................................................................................
{Input}: arr1, attributes list of the first data point/object
{Input}: arr2, attributes list of the first second point/object 
{Output}: dist, distance between two objects
'''          
def calculateEuclidean(arr1, arr2): 
    dist =0;
    for i in range(len(arr1)):
        dist = dist+ ((arr1[i]-arr2[i])**2)      
    dist = math.sqrt(dist)
    return dist

'''
{mergeClusters}: Merges two closest clusters and updates the distance matrix- choosing 
to merge two clusters with the minimum distance in the distance matrix 
...............................................................................................
{Input}: distanceMatrix, distance matrix from the previous iteration
{Input}: clusterMap, stores the clusters formed at each level, 
initially contains all individual points each as a single cluster
{Output}: distanceMatrix, updated distance matrix after merging two closest clusters
'''
def mergeClusters(distanceMatrix, clusterMap, k):
    minValue = float('inf')
    minIndex =0
    maxIndex =0
    clusterList = clusterMap[k]
    mergedClusterList = copy.deepcopy(clusterList)
    for i in range(len(distanceMatrix)):
        for j in range( int(len(distanceMatrix) / 2)+1):
            if i != j and distanceMatrix[i][j]<minValue:
                minValue = distanceMatrix[i][j]
                if(i<j):
                    minIndex =i
                    maxIndex =j
                else:
                    minIndex =j
                    maxIndex =i

    maxList = mergedClusterList.pop(maxIndex)
    for i in range(len(maxList)):
        mergedClusterList[minIndex].append(maxList[i])
    clusterMap[k+1] = mergedClusterList
    for i in range(len(distanceMatrix)):
        distanceMatrix[i][minIndex] = min(distanceMatrix[i][minIndex], distanceMatrix[i][maxIndex])
        distanceMatrix[i][maxIndex] = float('inf')
    for j in range(len(distanceMatrix)):
        distanceMatrix[minIndex][j] = min(distanceMatrix[minIndex][j], distanceMatrix[maxIndex][j])
        distanceMatrix[maxIndex][j] = float('inf')
    distanceMatrix = np.delete(distanceMatrix, (maxIndex), 0)
    distanceMatrix = np.delete(distanceMatrix, (maxIndex), 1)
    return distanceMatrix

'''
{agglomerativeClusteringWithSingleLink}: Performs agglomerative clustering repeating 
merging two closest clusters until a single cluster remains
.............................................................................................
{Input}: distanceMatrix, distance matrix for the dataset
{Input}: clusterMap, stores the clusters formed at each level, 
initially contains all individual points each as a single cluster
{Input}: file_name, name of file containing dataset
{Output}: hcaClusters, clusters remaining at the end of the agglomerative clustering
algorithm
'''
def agglomerativeClusteringWithSingleLink(distanceMatrix,clusterMap,hcaClusters, noOfClusters):
    k=0
    while(len(distanceMatrix)>noOfClusters):
        distanceMatrix = mergeClusters(distanceMatrix,clusterMap,k)
        k = k+1
    for currList in clusterMap[k]:
      hcaClusters.append(currList)
    print('HCA Algo Clusters ',clusterMap[k])


'''
{hcaClusterValidation}: Validates the hierarchial agglomerative clustering results 
using external index computation -Rand Index and Jaccard Co-efficient 
...............................................................................................
{Input}: geneList, list containing attributes for each data point
{Input}: groundTruthMap, map containing the ground truth values for dataset
{Output}: hcaClusters, clusters remaining at the end of the agglomerative clustering
algorithm
'''
def hcaClusterValidation(groundTruthMap, geneList, hcaClusters, file_name):
    hcaAlgoClusterMap = {}
    noiseList =[]
    size = len(geneList)
    ExternalIndex_Computation.computeAlgoClusterMap(hcaClusters, hcaAlgoClusterMap,noiseList)
    groundTruthClusterMatrix = np.zeros((size,size), dtype=np.int)
    algoClusterMatrix = np.zeros((size,size), dtype=np.int)
    ExternalIndex_Computation.computeGroundTruthAndAlgoClusterMatrix(groundTruthMap, geneList, groundTruthClusterMatrix, hcaAlgoClusterMap,algoClusterMatrix)
    ExternalIndex_Computation.computeJaccardCoefficient(groundTruthClusterMatrix,algoClusterMatrix,size)

    no_of_clusters = len(hcaClusters)
    graph_label = "Hierarchical Result (" + file_name + ")"
    lab = []
    new_list = []
    for i in range(0, len(hcaClusters)):
        for j in range(0, len(hcaClusters[i])):
            new_list.append(geneList[hcaClusters[i][j] - 1])

    for i in range(0, len(hcaClusters)):
        for j in range(0, len(hcaClusters[i])):
            lab.append(hcaAlgoClusterMap[hcaClusters[i][j]])

    pca(new_list, lab, graph_label, no_of_clusters)

'''
{hierarchialClustering}: main function that runs hierarchial agglomerative clustering algorithm 
on the given dataset computing the clusters using single linkage(min)
................................................................................................
'''    
def hierarchialClustering():
    file_path = input("Enter the file path: ")
    file_name = os.path.basename(file_path)
    file = open(file_path)
    noOfClusters = input("Enter the no of clusters: ")
    noOfClusters = int(noOfClusters)
    groundTruthMap = {}
    geneList = []
    clusterMap = {}
    hcaClusters = []
    createGeneList(file, groundTruthMap, geneList, file_name)
    size = len(geneList)
    distanceMatrix = np.zeros((size,size), dtype=np.float)
    createDistanceMatrix(distanceMatrix, geneList, clusterMap)
    agglomerativeClusteringWithSingleLink(distanceMatrix, clusterMap, hcaClusters, noOfClusters)
    hcaClusterValidation(groundTruthMap, geneList, hcaClusters, file_name)
    
start_time = time.time()    
hierarchialClustering()
print("--- %s seconds ---" % (time.time() - start_time))

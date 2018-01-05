'''
{computeGroundTruthAndAlgoClusterMatrix}: Computes the grouth truth matrix and 
algorithm generated cluster matrix based on which clusters the objects belong.
.........................................................................................
{Input}: geneList, list containing attributes for each data point
{Input}: groundTruthMap, map containing the ground truth values for dataset
{Input}: algoClusterMap, map containing objects grouped into clusters as per 
clustering algorithm
{Output}: groundTruthClusterMatrix, grouth truth matrix
{Output}: algoClusterMatrix,algorithm cluster matrix
'''
def computeGroundTruthAndAlgoClusterMatrix(groundTruthMap,geneList,groundTruthClusterMatrix,algoClusterMap,algoClusterMatrix):
    for i in range(0, len(geneList)):
        for j in range(0, len(geneList)):
            if groundTruthMap[i+1] == groundTruthMap[j+1]:
                groundTruthClusterMatrix[i][j] =1
            else:
                groundTruthClusterMatrix[i][j] =0
                
            if algoClusterMap[i+1] == algoClusterMap[j+1]:
                algoClusterMatrix[i][j] =1
            else:
                algoClusterMatrix[i][j] =0


'''
{computeAlgoClusterMap}: Computes the map containing objects grouped into clusters as per 
clustering algorithm
.........................................................................................
{Input}: noiseList, list containing noise object if present in the dataset
{Input}: algoClusters, list of clusters generated as per the corresponding 
clustering algorithm
{Output}: algoClusterMap, map containing objects grouped into clusters as per 
clustering algorithm
'''
def computeAlgoClusterMap(algoClusters,algoClusterMap,noiseList):
    clNo =1
    for currList in algoClusters:
        for i in currList:
            algoClusterMap[i] = clNo
        clNo = clNo+1
        
    if (len(noiseList)!=0):
        for i in noiseList:
            algoClusterMap[i] =-1
    #print hcaAlgoClusterMap


'''
{computeAlgoClusterMap}: Computes the jaccard coefficient and rand index using the
constructed ground truth matrix and algorithm generated cluster matrix
.........................................................................................
{Input}: groundTruthClusterMatrix, grouth truth matrix
{Input}: algoClusterMatrix,algorithm cluster matrix
{Input}: size, size of the dataset
'''
def computeJaccardCoefficient(groundTruthClusterMatrix,algoClusterMatrix,size):
    M11= M10 = M01= M00 =0
    for i in range(0, size):
        for j in range(0,size):
            if groundTruthClusterMatrix[i][j] == 1 and algoClusterMatrix[i][j] == 1:
                M11 = M11 +1
            elif groundTruthClusterMatrix[i][j] == 1 and algoClusterMatrix[i][j] == 0:
                M01 = M01 +1
            elif groundTruthClusterMatrix[i][j] == 0 and algoClusterMatrix[i][j] == 1:
                M10 = M10 +1
            elif groundTruthClusterMatrix[i][j] == 0 and algoClusterMatrix[i][j] == 0:
                M00 = M00 +1
    jaccard = float(M11)/(M11+M10+M01)
    randIndex = float(M11+M00)/(M11+M10+M01+M00)
    print('Jaccard Coefficient',jaccard)
    print('Rand Index ',randIndex)
    

#Follow the steps below to run K-means Clustering algorithm:
1. Enter the path of the file
2. Enter the number of iterations (i) to be performed
3. Enter the number of clusters (n) to form
4. Enter the corresponding gene id for the (n) cluster numbers
5. PCA vizualization occurs for the original data set
6. Kmeans algorithm runs for the file
7. PCA vizualization occurs after the K-means Clustering Implementation.
8. Cluster list gets displayed.
9. Jacard Coefficient and Rand index are computed and displayed


#Follow the steps below to run Hierarchical Clustering algorithm:
1. Enter the path of file
2. Enter the number of clusters (n) to form
3. PCA vizualization occurs for the original data set
4. HAC algorithm runs for the file
5. PCA vizualization occurs after the HAC Clustering Implementation.
6. Cluster list gets displayed.
7. Jacard Coefficient and Rand index are computed and displayed


#Follow the steps below to run DBScan Clustering algorithm:
1. Enter the path of file
2. Enter the value of epsilon. Eg. 0.8
3. Enter the value of Minpts. Eg. 5
5. PCA vizualization occurs for the original data set
6. DBScan algorithm runs for the file
7. PCA vizualization occurs after the DBScan Clustering Implementation.
8. Cluster list and noiselist get displayed.
9. Jacard Coefficient and Rand index are computed and displayed


#Follow the steps below to run Hadoop algorithm:

After hadoop installation, do the following steps:
Keep the javafile KmeansMapReduce.java in same directory as new_dataset_1.txt or any other text file in local machine. Also keep both these files in your home/hadoop directory from where you are running the commands. Make sure you change the file name on line number 118. Also you can change the numberOfClusters on line 33.

Run the following commands from the hadoop directory.

1. Start Hadoop by running:
	start-hadoop.sh
2. Make a new directory on hdfs for the input files:
	hadoop fs –mkdir –p /input/
3. Copy the local file like cho.txt to the hdfs directory input/:
	hadoop fs –put /home/hadoop/cho.txt /input/
4. Make sure you copied them to the right place:
	hadoop fs –ls /input

Run the code using following commands:
1. hadoop fs -rm -r /output*
2. hadoop com.sun.tools.javac.Main KmeansMapReduce.java
3. jar cf kmr.jar KmeansMapReduce*.class
4. hadoop jar kmr.jar KmeansMapReduce /input/cho.txt /output20

The results of number of iterations required and the clusters formed would be displayed on console.

You can now view the results by running:
	hadoop fs -cat /output20/*
The will be a part-r-00000 file which has the output containing the centroids.

Or if you need the results locally, copy from hdfs then cat:
	hadoop fs –get /output20
cat part-r-00000







 
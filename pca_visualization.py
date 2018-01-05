import numpy as np
import numpy.linalg as np_linalg
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def calculate_mean(brr):
    """
    Calculates mean of the original data.
    .........................................................................................
        Args:
            {Input}: brr: Data points containing all the attributes.
        Returns:
            Returns the mean centric data
    """
    mean_matrix = np.mean(brr, axis=0)
    brr -= mean_matrix
    return brr


def pca(brr, labels, file_name, no_of_clusters):
    """
    Calculates PCA of the given data.
    .........................................................................................
        Args:
            {Input}: arr: Original Data set.
            {Input}: labels: All the class labels
            {Input}: file_name: Name of the file which is to be used for plotting.
            {Input}:
        Returns:
            {Output}: sends the reconstructed data to PCA_plot and calculates pca result having maximum variance to plot
             the graph
    """
    brr = calculate_mean(brr)  # Calculate mean of every column and adjust data by mean
    cov_mat = np.dot(brr.transpose(),brr)/(brr.shape[0]-1) # Calculate the covariance of the data

    eig_value, eig_vector = np_linalg.eig(cov_mat) # Calculate eigen values and eigen vectors of co-variance matrix
    eig_list = []
    for i in range(len(eig_value)):
        eig_list = eig_list + [(np.abs(eig_value[i]), eig_vector[:, i])]

    eig_list.sort()     # Sort the eigen values in descending order
    eig_list.reverse()
    eig_list = eig_list[:2]

    top_eigen_vect=[]
    for i in eig_list:
        top_eigen_vect.append(i[1])
    top_eigen_vect = np.array(top_eigen_vect)
    top_eigen_vect = np.transpose(top_eigen_vect)

    new_data = np.dot(brr, top_eigen_vect)  # Reorganize the data
    plot_title = file_name
    plot_graph(new_data, labels, plot_title, no_of_clusters) #plot the clusters

def pca_calculation(X, labels, file_name, no_of_clusters):
    new_data = PCA(n_components=2).fit_transform(X)
    plot_title = file_name
    plot_graph(new_data, labels, plot_title, no_of_clusters)

def plot_graph(new_data, labels, plot_title, no_of_clusters):
    """
    Plots graphs for PCA
    .........................................................................................
        Args:
            {Input}: new_data, PCA result set
            {Input}: labels, All the class labels/ground truth values
            {Input}: plot_title, Title of the plot.
            {Input}: no_of_clusters, Number of clusters given by the user

    """
    unique_lab = np.unique(labels)

    plt.figure(figsize=(10, 8))
    color = ['#FF0000','#FFA500', '#FFFF00','#008000', '#00FFFF', '#EE82EE','#FF1493', '#8B4513', '#48D1CC', '#000080',
             '#F5D3B3', '#808000', '#0000FF', '#6C3483', '#2ECC71', '#85C1E9', '#AF7AC5', '#229954', '#F0B27A',
             '#E6B0AA', '#D7BDE2', '#EDBB99', '#CCD1D1', '#B9770E', '#FF00FF']
    new_data = np.array(new_data)

    k=0
    for i in range(k, no_of_clusters):
        column1 = []
        column2 = []
        k=0
        for j in range(0, len(new_data)):
            if labels[k] == i+1 or labels[k] == -1:
                column1.append(new_data[j][0])
                column2.append(new_data[j][1])
            k+=1
        plt.scatter(column1, column2, s=45, c = color[i], label = i+1)

    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.title(plot_title)
    plt.legend(scatterpoints=2, loc='upper right')
    plt.show()

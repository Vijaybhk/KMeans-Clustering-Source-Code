# **********************
#       Main Module
# **********************

from mid_kmean_kothapally.libs import MyKmean as Km
import os

# Root path to the project
root_path = os.getcwd()

# output directory path
output_dir_path = os.path.join(root_path, "output")

# create the output directory if it does not exist
if not os.path.exists(output_dir_path):
    os.mkdir(output_dir_path)


def main():
    """
    Main function to run k means clustering for two data sets from aggregation.csv file and s1.txt file
    with separators "," and "\t" respectively.
    """

    filepath = os.path.join(root_path, "data")     # Data directory path by joining root path and data dir
    files = ["aggregation.csv", "s1.txt"]          # List of data files
    separators = [",", "\t"]                       # List of separators

    for k1 in range(5, 10, 2):                              # for k values 5, 7 and 9

        mykmean1 = Km.MyKmeans(k1)                              # MyKmeans class instance with k value from the range
        read_path = os.path.join(filepath, files[0])            # Path to the aggregation.csv file
        mykmean1.read_xy_from_file(read_path, separators[0])    # reading coordinates from the dataset and store points
        mykmean1.assign_random_clust_number()                   # Assigning random clusters to the dataset
        mykmean1.initialize_centroids()                         # Picks initial random centroids

        # Km.plot_clust_points(mykmean1)

        flag_terminate = False                              # Initializes flag_terminate as false to control while loop

        while not flag_terminate:                           # Loop runs when flag terminate is false

            # Assigns points to clusters with the closest centroid
            mykmean1.assign_clust_number()

            # Changes flag to the returned value from the update centroid method
            # Which return True only when there is no change in the updated centroids
            flag_terminate = mykmean1.update_centroid()

            # Km.plot_clust_points(mykmean1)

        # Km.plot_clust_points(mykmean1)

        # Saves csv files with clustered points and centroids to output dir
        Km.save_clust_points_csv(mykmean1, output_dir_path)

        # Saves the k means clusters plot as an image to the output dir
        Km.save_clust_points_img(mykmean1, output_dir_path)

    for k2 in range(10, 21, 5):                     # For k values 10, 15 and 20

        mykmean2 = Km.MyKmeans(k2)
        read_path = os.path.join(filepath, files[1])
        mykmean2.read_xy_from_file(read_path, separators[1])
        mykmean2.assign_random_clust_number()
        mykmean2.initialize_centroids()

        # Km.plot_clust_points(mykmean2)

        flag_terminate = False   # Initializes flag_terminate as false

        while not flag_terminate:
            # Loop runs when flag terminate is false

            mykmean2.assign_clust_number()
            # Assigns points to clusters with the closest centroid

            flag_terminate = mykmean2.update_centroid()
            # Changes flag to the returned value from the update centroid method
            # Which return True only when there is no change in the updated centroids

            # Km.plot_clust_points(mykmean1)

        # Km.plot_clust_points(mykmean1)

        Km.save_clust_points_csv(mykmean2, output_dir_path)
        Km.save_clust_points_img(mykmean2, output_dir_path)


if __name__ == '__main__':
    main()                          # Runs the main function when executed from main module.


"""

Pros of Kmeans Clustering:

1. K-means is suitable for a large number of datasets. It can also produce higher clusters.
2. It is easy to implement k-means and identify unknown groups of data from complex data sets.
3. It is easy to warm the start the position of centroids and then refine further.

Cons of Kmeans Clustering:

1. K-means does not allow optimal number of clusters and we should decide on the clusters before.
2. K-means algorithm can be performed in numerical data only.
3. Centroids are dragged by outliers, or outliers might get their own cluster instead of being ignored 
   which affects the results.


"""
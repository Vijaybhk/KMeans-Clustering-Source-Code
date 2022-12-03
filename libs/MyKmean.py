# *****************************
#     MyKmeans Class Module
# *****************************

from matplotlib import pyplot as plt
import numpy as np
import random
from mid_kmean_kothapally.libs import Point as Pc
import sys
from mid_kmean_kothapally.libs import Utility as Util
import csv
import os


class MyKmeans:
    def __init__(self, k, num_points=10, dimension=2, lower_bound=(0, 0),
                 upper_bound=(10, 10), points=[], centroids={}):
        self.k = k                    # Initiating with zero clusters
        self.num_points = num_points          # Initiating with 10 required number of points
        self.dimension = dimension            # Initiating with 2 dimensions
        self.lower_bound = lower_bound     # Initiating with lower bound (0, 0)
        self.upper_bound = upper_bound   # Initiating with upper bound (10, 10)
        self.points = points              # Initiating an empty list of points
        self.centroids = centroids           # initiating an empty dictionary of centroids

    def set_parameters(self):         # This methods request inputs for MyKmeans properties
        self.k = int(input("\n\nEnter number of k means clusters: "))
        self.num_points = int(input("Enter number of random points required: "))
        self.dimension = int(input("Enter point dimension: "))
        l_bound = input("Enter lower bound with space separation only: ")
        self.lower_bound = tuple(float(x) for x in l_bound.split())
        u_bound = input("Enter upper bound with space separation only: ")
        self.upper_bound = tuple(float(x) for x in u_bound.split())

    def generate_points(self):        # Generate random points of count num_points
        self.points = Util.random_points(self.num_points, self.dimension, self.lower_bound, self.upper_bound)
        return self.points

    def initialize_centroids(self):   # Initialize k number of centroids using random selection from generated points
        """
        Option: 1
        new = random_points(self.k, self.dimension, self.lower_bound, self.upper_bound)
        for i in range(1, self.k+1):
            self.centroids[i] = new[i-1]
            self.centroids[i].clust_id = i
        """
        new = random.sample(self.points, self.k)
        for i in range(1, self.k+1):
            c_p = new[i-1]
            self.centroids[i] = Pc.Point(c_p.x, c_p.y, c_p.z, clust_id=i)
        return self.centroids

    def assign_random_clust_number(self):   # Considering a random cluster id for each of the points
        for i in range(0, len(self.points)):
            r_id = random.randint(1, self.k)
            self.points[i].clust_id = r_id
        return self.points

    def assign_clust_number(self):
        for ii in self.points:
            # initialize with maximum integer value
            # 'sys.maxint' is Python 2.x only. For 3.x, use 'sys.maxsize'
            min_dist = sys.maxsize  # largest Value of a variable
            for jj in self.centroids:
                dist = ii.calc_distance(self.centroids[jj])
                # Calculates distance between centroid and one of self.points

                if min_dist > dist:
                    min_dist = dist
                    ii.clust_id = jj
                # Assigns clust id to the point for which the centroid is the closest.
        return self.points

    def update_centroid(self):    # Updates centroid until there is no change
        flag_all_same_coordinate = True

        for key in self.centroids:   # For every key cluster, value centroid pair in the centroids dictionary
            ref_centroid = self.centroids[key]  # Consider one centroid value from the loop as reference centroid
            ref_clust_id = key                  # Consider respective cluster key as reference cluster id
            cx_sum = 0.0                        # Initialize sum of x coordinate as 0
            cy_sum = 0.0                        # Initialize sum of y coordinate as 0
            cz_sum = 0.0                        # Initialize sum of z coordinate as 0
            cn_sum = 0                          # Initialize number of points as 0

            for each_point in self.points:      # For every point in generated points
                if each_point.clust_id == ref_clust_id:  # When cluster id of the point is same as reference cluster id
                    cx_sum += each_point.x      # Adds x-coordinate to the sum of x coordinates
                    cy_sum += each_point.y      # Adds y-coordinate to the sum of y coordinates
                    cz_sum += each_point.z      # Adds z-coordinate to the sum of z coordinates
                    cn_sum += 1                 # Increments number of points by 1

            if cn_sum != 0:                     # Checks if the number of points is not 0

                self.centroids[ref_clust_id] = Pc.Point(cx_sum/cn_sum, cy_sum/cn_sum, cz_sum/cn_sum, ref_clust_id)

                # Assigning new centroid to the reference cluster id by averaging coordinates from the same cluster

                if not Util.check_same_coordinate(self.centroids[ref_clust_id], ref_centroid):
                    flag_all_same_coordinate = False

                # Compares updated centroid and reference centroid, and changes flag if not same

        return flag_all_same_coordinate

    def read_xy_from_file(self, file_path, seperator):
        """
        reads x and y coordinates from the data set and stores as point objects in a list
        :param file_path: data set path
        :param seperator: seperator used to separate coordinates in each line
        :return: None
        """
        self.points[:] = []                # Removes all elements from self.points
        read_file = open(file_path, 'r')   # Opens file mentioned in read mode
        read_line = read_file.readlines()  # Reads all lines and stores in read_line variable
        x_list = []                        # Empty list of x coordinates
        y_list = []                        # Empty list of y coordinates
        num = 0                            # Initiating number of points as zero

        for line in read_line:             # For every line in read_line
            line_list = list(line.split(seperator))    # Create a list by splitting with input seperator

            # Converts x coordinate from string to float and appends to x_list
            x1 = float(line_list[0])
            x_list.append(x1)

            # Converts y coordinate from string to float and appends to y_list
            y1 = float(line_list[1])
            y_list.append(y1)

            # uses x and y coordinates to create a point class instance and appends to self.points
            self.points.append(Pc.Point(x1, y1))

            # Increments the number of points by 1
            num += 1

        self.lower_bound = (min(x_list), min(y_list))   # Assigning lower bound from the data set
        self.upper_bound = (max(x_list), max(y_list))   # Assigning upper bound from the data set
        self.num_points = num                           # Assigning number of points from data set


def plot_clust_points(mykmean, pt_size=100, centroid_size=200, pt_marker="o", centroid_marker="x"):
    """
    Plots data points and centroids
    :param mykmean: MyKmeans instance (MyKmeans)
    :param pt_size: point size (integer)
    :param centroid_size: centroid point size (integer)
    :param pt_marker: point marker type defined  under matplotlib.markers (string/integer)
    :param centroid_marker: centroid marker type defined  under matplotlib.markers (string/integer)
    :return: None
    """

    cmap = plt.cm.get_cmap('rainbow', mykmean.k)

    idx_sh = list(range(mykmean.k))
    random.shuffle(idx_sh)              # Randomizes the color for clusters

    for i in mykmean.points:
        color = np.array(cmap(idx_sh[i.clust_id-1])).reshape(1, -1)
        plt.scatter(i.x, i.y, c=color, marker=pt_marker, s=pt_size)

    for i in mykmean.centroids:
        pt = mykmean.centroids[i]
        color = np.array(cmap(idx_sh[pt.clust_id-1])).reshape(1, -1)
        plt.scatter(pt.x, pt.y, c=color, marker=centroid_marker, s=centroid_size)
    plt.show()                          # Plots the K means clusters


def save_clust_points_csv(mykmean_inst, out_file_path):
    """
    Saves points and centroids after clustering to csv file with coordinates and cluster ids
    :param mykmean_inst: MyKmeans instance (MyKmeans)
    :param out_file_path: output file path
    :return: None
    """
    if isinstance(mykmean_inst, MyKmeans):
        points_file = os.path.join(out_file_path, "k{}_clustered_points.csv".format(mykmean_inst.k))
        file1 = open(points_file, "w", newline='')
        write_file1 = csv.writer(file1)

        for point in mykmean_inst.points:
            if point.dim == 3:
                write_file1.writerow([point.clust_id, point.x, point.y, point.z])
            elif point.dim == 2:
                write_file1.writerow([point.clust_id, point.x, point.y])

        centroids_file = os.path.join(out_file_path, "k{}_centroids_clusters.csv".format(mykmean_inst.k))
        file2 = open(centroids_file, "w", newline='')
        write_file2 = csv.writer(file2)

        for key in mykmean_inst.centroids:
            if mykmean_inst.centroids[key].dim == 3:
                write_file2.writerow([mykmean_inst.centroids[key].clust_id, mykmean_inst.centroids[key].x,
                                      mykmean_inst.centroids[key].y, mykmean_inst.centroids[key].z])

            elif mykmean_inst.centroids[key].dim == 2:
                write_file2.writerow([mykmean_inst.centroids[key].clust_id, mykmean_inst.centroids[key].x,
                                      mykmean_inst.centroids[key].y])
    else:
        print("Input is not an instance of MyKmeans class")


def save_clust_points_img(mykmean, out_file_path, pt_size=100, centroid_size=200,
                          pt_marker="o", centroid_marker="x", pt_alpha=0.5, centroid_alpha=1):
    """
    saves image with plotted data points and cluster centroids
    :param mykmean: MyKmeans instance (MyKmeans)
    :param out_file_path: output file path
    :param pt_size: point size (integer)
    :param centroid_size: centroid point size (integer)
    :param pt_marker: point marker type defined  under matplotlib.markers (string/integer)
    :param centroid_marker: centroid marker type defined  under matplotlib.markers (string/integer)
    :return: None
    """

    # create a color map object based on a rainbow colormap
    cmap = plt.cm.get_cmap('rainbow', mykmean.k)

    # randomize the color index list
    idx_sh = list(range(mykmean.k))
    random.shuffle(idx_sh)

    # assign a color for the points and a centroid for each cluster
    for i in mykmean.points:
        plt.scatter(i.x, i.y, c=[cmap(idx_sh[i.clust_id - 1])],
                    marker=pt_marker, s=pt_size, alpha=pt_alpha)

        # c = np.array(cmap(idx_sh[pt.clust_id-1])).reshape(1, -1)
        # plt.scatter(pt.x, pt.y, c=c, marker=centroid_marker, s=centroid_size)

    for i in mykmean.centroids:
        pt = mykmean.centroids[i]
        plt.scatter(pt.x, pt.y, c=[cmap(idx_sh[pt.clust_id-1])],
                    marker=centroid_marker, s=centroid_size, alpha=centroid_alpha)

        # c = np.array(cmap(idx_sh[pt.clust_id-1])).reshape(1, -1)
        # plt.scatter(pt.x, pt.y, c=c, marker=centroid_marker, s=centroid_size)
    plt.savefig("{}/k{}_Image".format(out_file_path, mykmean.k))
    plt.clf()
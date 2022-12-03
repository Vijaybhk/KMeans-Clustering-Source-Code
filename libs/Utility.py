# *************************
#       Utility Module
# *************************

import random
from mid_kmean_kothapally.libs import Point as Pc
import sys


def random_points(num_point=10, dimension=2, lower_bound=(0, 0), upper_bound=(10, 10)):
    lst = []
    for j in range(num_point):
        x1 = random.uniform(lower_bound[0], upper_bound[0])
        y1 = random.uniform(lower_bound[1], upper_bound[1])
        if dimension == 2:
            k1 = Pc.Point(x1, y1)
            lst.append(k1)
        elif dimension == 3:
            z1 = random.uniform(lower_bound[2], upper_bound[2])
            k1 = Pc.Point(x1, y1, z1)
            lst.append(k1)
    return lst                  # returns a list of  num_point number of random points between lower and upper bound.


def check_same_coordinate(p1, p2):
    """
    Function to check if two point instances have the same coordinate
    :param p1: the first point instance (Point)
    :param p2: the second point instance (Point)
    :return: a boolean flag (boolean)
    """

    try:
        if isinstance(p1, Pc.Point) and isinstance(p2, Pc.Point):     # Checks if arguments are point class instances
            if p1.x == p2.x and p1.y == p2.y and p1.z == p2.z:  # Comparing Coordinates
                return True
            else:
                return False
        else:
            print("The instances are not point class instances")

    except Exception as e:
        print(type(e), e)
        sys.exit()

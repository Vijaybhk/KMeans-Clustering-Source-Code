# *****************************
#     Point Class Module
# *****************************


class Point:
    def __init__(self, x, y, z=0.0, clust_id=-1):       # attributes x, y and; dim = 2 when z = 0 else dim = 3
        self.x = x
        self.y = y
        self.z = z
        self.dim = 2
        self.clust_id = clust_id
        if z != 0:
            self.dim = 3

    def print_coordinate(self):                 # Method to print the coordinates
        if self.dim == 2:
            return "Point: ({:.3f}, {:.3f}) Cluster: {}".format(self.x, self.y, self.clust_id)

        elif self.dim == 3:
            return "Point: ({:.3f}, {:.3f}, {:.3f}) Cluster: {}".format(self.x, self.y, self.z, self.clust_id)

    def calc_distance(self, object1):           # Method to calculate the distance
        try:
            if isinstance(object1, Point):      # Checks if the argument is instance of the point class or not
                d = ((self.x-object1.x)**2 + (self.y-object1.y)**2 + (self.z-object1.z)**2)**0.5
                return d                        # Calculates and returns distance

            else:
                raise Exception("Not an Instance of Point class")

        except Exception as e:                  # To Handle and raise exception well.
            return "The error is: {}".format(e)
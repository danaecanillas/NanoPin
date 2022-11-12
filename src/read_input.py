import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from numpy import arctan



def input_data(input_file):
    DRIVER_PINS_ID = []
    DRIVER_PINS_COORD = []
    PINS_ID = []
    PINS_COORD = []
    with open (input_file, "r") as def_file:
        for line in def_file:
            if "DIRECTION INPUT" in line:
                DRIVER_PINS_ID.append(line.split(" +")[0].split("- ")[1])
            elif "FIX " in line:
                coord = line.split("( ")[1].split(" )")[0]
                coord_x = int(coord.split(" ")[0])
                coord_y = int(coord.split(" ")[1])
                DRIVER_PINS_COORD.append([coord_x, coord_y])
            elif "FIXED" in line:
                PINS_ID.append(line.split(" +")[0].split(" ")[0])
                coord = line.split("( ")[1].split(" )")[0]
                coord_x = int(coord.split(" ")[0])
                coord_y = int(coord.split(" ")[1])
                PINS_COORD.append([coord_x, coord_y])

    return DRIVER_PINS_ID, DRIVER_PINS_COORD, PINS_ID, PINS_COORD


def plot_coord(points_list):
    colours = ["orange", "blue", "green", "gray", "red"]

    for points_id in range(len(points_list)):
        plt.scatter(
            x = [p[0] for p in points_list[points_id]],
            y = [p[1] for p in points_list[points_id]],
        color = colours[points_id])

    plt.show()


def get_clusters(data, c):
    kmeans = KMeans(n_clusters = c, random_state=0).fit(data)
    return kmeans.cluster_centers_


def net_classification(PINS_COORD, n_nets, p = None):
    #if not p:

    section_size = 180/n_nets

    sections = []
    for x, y in PINS_COORD:
        delta_0 = x - p[0]
        delta_1 = y - p[1]
        tan_ang = delta_1 / delta_0
        ang = arctan(tan_ang)
        section = int(ang/section_size)
        sections.append(section)




input = "input/testcase0.def"

n_nets = 8

DRIVER_PINS_ID, DRIVER_PINS_COORD, PINS_ID, PINS_COORD = input_data(input)

centers = get_clusters(PINS_COORD, 4)

plot_coord((PINS_COORD, DRIVER_PINS_COORD, centers))



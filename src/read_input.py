import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from math import pi



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


DRIVER_INPUT_PINS_ID = DRIVER_PINS_ID[0:16]
DRIVER_INPUT_PINS_COORD = DRIVER_PINS_COORD[0:16]
DRIVER_OUTPUT_PINS_ID = DRIVER_PINS_ID[16:]
DRIVER_OUTPUT_PINS_COORD = DRIVER_PINS_COORD[16:]


def plot_coord(points_list):
    colours = ["orange", "blue", "green", "gray", "red", "purple", "yellow", "pink"]

    for points_id in range(len(points_list)):
        plt.scatter(
            x = [p[0] for p in points_list[points_id]],
            y = [p[1] for p in points_list[points_id]],
        color = colours[points_id])

    plt.show()


def get_clusters(data, c):
    kmeans = KMeans(n_clusters = c, random_state=0).fit(data)
    return kmeans.cluster_centers_


def get_p():
    driver_pins_min_y = np.mean([coord[1] for coord in DRIVER_INPUT_PINS_COORD])
    driver_pins_max_y = np.mean([coord[1] for coord in DRIVER_OUTPUT_PINS_COORD])

    p = np.mean((driver_pins_max_y, driver_pins_min_y))

    return (0, p)


def net_classification(PINS_COORD, n_nets, p = None):
    if not p:
        p = get_p()

    section_size = pi/n_nets
    sections = [[] for i in range(n_nets)]
    print(n_nets, section_size, p)
    for i, (x, y) in enumerate(PINS_COORD):
        delta_0 = x - p[0]
        delta_1 = y - p[1]
        tan_ang = delta_1 / delta_0
        ang = np.arctan(tan_ang)
        print(ang*180/pi)
        section = int((pi/2-ang)/section_size)
        print(section)
        sections[section].append(i)

    return sections



input = "input/testcase0.def"

n_nets = 8

DRIVER_PINS_ID, DRIVER_PINS_COORD, PINS_ID, PINS_COORD = input_data(input)

centers = get_clusters(PINS_COORD, 4)

plot_coord((PINS_COORD, DRIVER_PINS_COORD, centers))


nets = net_classification(PINS_COORD, n_nets)

[len(section) for section in nets]

COLORS = []
for section in nets:
    COLORS.append([PINS_COORD[id] for id in section])



plot_coord(COLORS)


COLORS[0]

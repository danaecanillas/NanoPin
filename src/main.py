import matplotlib.pyplot as plt
#from sklearn.cluster import KMeans
import numpy as np
from math import pi

from read_input import read
from metrics import euclidean, manhattan



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



def get_subsections(p = None):
    if not p:
        p = get_p()

    classification = [[]]*n_nets
    for angle_id, section in enumerate(COLORS):
        upper_points_angle = []
        lower_points_angle = []
        bisectriu = np.mean([pi/n_nets * angle_id, pi/n_nets * (angle_id+1)])
        for id, (x, y) in enumerate(section):
            delta_0 = x - p[0]
            delta_1 = y - p[1]
            tan_ang = delta_1 / delta_0
            ang = np.arctan(tan_ang)
            if ang < bisectriu:
                upper_points_angle.append(nets[angle_id][id])
            else:
                lower_points_angle.append(nets[angle_id][id])

        classification[angle_id] = (upper_points_angle, lower_points_angle)
    return classification



def get_chains(sections, p = None):
    if not p:
        p = get_p()

    net_dists = []

    for up, down in sections:
        section_dist = 0

        pin_aux = p

        if len(up) > 0:
            up_dists = []
            for pin_id in up:
                up_dists.append((PINS_COORD[pin_id], euclidean(PINS_COORD[pin_id], p)))
            up_dists.sort(key = lambda x: x[1])

            section_dist += manhattan(p, up_dists[0][0])

            for pos_id in range(1, len(up_dists)):
                section_dist += manhattan(up_dists[pos_id-1][0], up_dists[pos_id][0])
            
            pin_aux = up_dists[len(up_dists)-1][0]

        if len(down) > 0:
            down_dists = []
            for pin_id in down:
                down_dists.append((PINS_COORD[pin_id], euclidean(PINS_COORD[pin_id], p)))
            down_dists.sort(key = lambda x: x[1], reverse = True)

            section_dist += manhattan(pin_aux, down_dists[0][0])

            for pos_id in range(1, len(down_dists)):
                section_dist += manhattan(down_dists[pos_id-1][0], down_dists[pos_id][0])
            
            pin_aux = down_dists[len(down_dists)-1][0]

        section_dist += manhattan(pin_aux, p)

        net_dists += [section_dist]

    return net_dists



def exec():
    input = "input/testcase0.def"
    n_nets = 8

    DRIVER_PINS_ID, DRIVER_PINS_COORD, PINS_ID, PINS_COORD = read(input)

    #plot_coord((PINS_COORD, DRIVER_PINS_COORD, centers))

    nets = net_classification(PINS_COORD, n_nets)

    COLORS = []
    for section in nets:
        COLORS.append([PINS_COORD[id] for id in section])

    #plot_coord(COLORS)


    subsections = get_subsections()

    net_dists = get_chains(subsections)
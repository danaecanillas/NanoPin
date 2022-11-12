import os
import matplotlib.pyplot as plt
#from sklearn.cluster import KMeans
import numpy as np
from math import pi

#from read_input import read
#from metrics import euclidean, manhattan, final_metrics



def get_p(DRIVER_PINS_COORD):
    driver_pins_min_y = np.mean([coord[1] for coord in DRIVER_PINS_COORD[:16]])
    driver_pins_max_y = np.mean([coord[1] for coord in DRIVER_PINS_COORD[16:]])

    p = np.mean((driver_pins_max_y, driver_pins_min_y))

    return (0, p)



def net_classification(PINS_COORD, n_nets, p):
    section_size = pi/n_nets
    sections = [[] for i in range(n_nets)]
    
    for i, (x, y) in enumerate(PINS_COORD):
        delta_0 = x - p[0]
        delta_1 = y - p[1]
        tan_ang = delta_1 / delta_0
        ang = np.arctan(tan_ang)
        #print(ang*180/pi)
        section = int((pi/2-ang)/section_size)
        #print(section)
        sections[section].append(i)

    return sections



def get_subsections(nets, PINS_COORD, p):
    n_nets = len(nets)
    classification = [[]]*n_nets

    for angle_id, section in enumerate(nets):
        upper_points_angle = []
        lower_points_angle = []
        bisectriu = np.mean([pi/n_nets * angle_id, pi/n_nets * (angle_id+1)])
        for pin in section:
            x, y = PINS_COORD[pin]
            delta_0 = x - p[0]
            delta_1 = y - p[1]
            tan_ang = delta_1 / delta_0
            ang = np.arctan(tan_ang)
            if ang < bisectriu:
                upper_points_angle.append(pin)
            else:
                lower_points_angle.append(pin)

        classification[angle_id] = (upper_points_angle, lower_points_angle)
    return classification



def get_chains(PINS_COORD, DRIVER_PINS_COORD, sections, p):
    net_dists = []

    for section_id, (up, down) in enumerate(sections):
        section_dist = 0

        pin_aux = DRIVER_PINS_COORD[section_id]

        if len(up) > 0:
            up_dists = []
            for pin_id in up:
                up_dists.append((PINS_COORD[pin_id], euclidean(PINS_COORD[pin_id], p)))
            up_dists.sort(key = lambda x: x[1])

            section_dist += manhattan(pin_aux, up_dists[0][0])

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

        section_dist += manhattan(pin_aux, DRIVER_PINS_COORD[section_id+16])

        net_dists += [section_dist]

    return net_dists



def exec():
    os.chdir("src")
    input = "../input/testcase0.def"
    n_nets = 8

    DRIVER_PINS_ID, DRIVER_PINS_COORD, PINS_ID, PINS_COORD = read(input)

    p = get_p(DRIVER_PINS_COORD)

    #plot_coord((PINS_COORD, DRIVER_PINS_COORD, centers))

    nets = net_classification(PINS_COORD, n_nets, p)

    # COLORS = []
    # for section in nets:
    #     COLORS.append([PINS_COORD[id] for id in section])

    #plot_coord(COLORS)


    subsections = get_subsections(nets, PINS_COORD, p)

    net_dists = get_chains(PINS_COORD, DRIVER_PINS_COORD, subsections, p)
    
    print(net_dists)
    print(final_metrics(net_dists))

exec()
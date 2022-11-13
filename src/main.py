import os
import matplotlib.pyplot as plt
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
    # out: list of points for every section
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
    # out: [(section1u, section1d), (section2u, section2d), ...] where every sectionXY is the points in section X up/down
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
            if delta_0 == 0:
                if delta_1 > 0:
                    ang = pi/2
                else:
                    ang = -pi/2
            else:
                tan_ang = delta_1 / delta_0
                ang = np.arctan(tan_ang)
            if ang < bisectriu:
                upper_points_angle.append(pin)
            else:
                lower_points_angle.append(pin)

        classification[angle_id] = (upper_points_angle, lower_points_angle)
    return classification



def get_chains(PINS_COORD, DRIVER_PINS_COORD, sections, p):
    # output: list of [(id1, coord1), (id_2, coord2), ...] for every section
    chains = [[]]*len(sections)
    for section_id, (up, down) in enumerate(sections):
        chain = []
        chain.append((section_id, DRIVER_PINS_COORD[section_id]))

        if len(up) > 0:
            up_dists = []
            for pin_id in up:
                up_dists.append((pin_id, PINS_COORD[pin_id], euclidean(PINS_COORD[pin_id], p)))
            up_dists.sort(key = lambda x: x[2])

            chain += [tuple(up_dists[i][0:2]) for i in range(len(up_dists))]

        if len(down) > 0:
            down_dists = []
            for pin_id in down:
                down_dists.append((pin_id, PINS_COORD[pin_id], euclidean(PINS_COORD[pin_id], p)))
            down_dists.sort(key = lambda x: x[2], reverse = True)

            chain += [tuple(down_dists[i][0:2]) for i in range(len(down_dists))]

        chain.append((section_id, DRIVER_PINS_COORD[section_id+16]))

        chains[section_id] = chain

    return chains



def compute_dists(chains):
    # output: list of distance for every section
    dists = []

    for chain in chains:
        if len(chain) == 2:
            dists.append(0) #empty section
        else:
            dist = 0
            for pin_id in range(1, len(chain)):
                dist += manhattan(chain[pin_id-1][1], chain[pin_id][1])

            dists.append(dist)

    return dists


def get_output(chains, DRIVER_PINS_ID, PINS_ID, output_file, net_name = "Nano_NET"):
    f = open(output_file, "w")
    for ch_id, chain in enumerate(chains):
        if len(chain) > 2:
            f.write("- " + net_name + "\n")
            f.write("  ( " + DRIVER_PINS_ID[chain[0][0]] + " conn_in )"+ "\n")
            f.write("  ( " + PINS_ID[chain[1][0]] + " conn_out )"+ "\n")
            f.write(";"+ "\n")

            for pin_id in range(2, len(chain)-1):
                f.write("- " + net_name+ "\n")
                f.write("  ( " + PINS_ID[chain[pin_id-1][0]] + " conn_in )"+ "\n")
                f.write("  ( " + PINS_ID[chain[pin_id][0]] + " conn_out )"+ "\n")
                f.write(";"+ "\n")
            
            f.write("- " + net_name+ "\n")
            f.write("  ( " + PINS_ID[chain[len(chain)-2][0]] + " conn_in )"+ "\n")
            f.write("  ( " + DRIVER_PINS_ID[chain[len(chain)-1][0]] + " conn_out )"+ "\n")
            f.write(";"+ "\n")
    
    f.close()


def exec(input):
    #os.chdir("src")
    n_nets = 8

    DRIVER_PINS_ID, DRIVER_PINS_COORD, PINS_ID, PINS_COORD = read(input)

    p = get_p(DRIVER_PINS_COORD)

    #plot_coord((PINS_COORD, DRIVER_PINS_COORD, centers))

    nets = net_classification(PINS_COORD, n_nets, p)

    COLORS = []
    for section in nets:
        COLORS.append([PINS_COORD[id] for id in section])

    #plot_coord(COLORS)


    subsections = get_subsections(nets, PINS_COORD, p)

    chains = get_chains(PINS_COORD, DRIVER_PINS_COORD, subsections, p)

    dists = compute_dists(chains)

    print(dists)
    print(final_metrics(dists))

    get_output(chains, DRIVER_PINS_ID, PINS_ID, "xavi_prova.def", net_name = "Nano_NET")





input = "../input/testcase3.def"
exec(input)
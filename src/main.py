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



def get_angle(pin, p):
    # angle between x and p w.r.t. p horizontal
    delta_0 = pin[0] - p[0]
    delta_1 = pin[1] - p[1]
    if delta_0 == 0:
        if delta_1 > 0:
            ang = pi/2
        else:
            ang = -pi/2
    else:
        tan_ang = delta_1 / delta_0
        ang = np.arctan(tan_ang)
    return ang



def net_classification_old(PINS_COORD, n_nets, p):
    # out: list of points for every section
    section_size = pi/n_nets
    sections = [[] for i in range(n_nets)]
    
    for i, pin in enumerate(PINS_COORD):
        ang = get_angle(pin, p)

        section = int((pi/2-ang)/section_size)
        sections[section].append(i)

    return sections


def net_classification(PINS_COORD, n_nets, p):
    # out: list of points for every section
    angles = []
    for i, pin in enumerate(PINS_COORD):
        ang = get_angle(pin, p)
        angles.append((i, ang))
    
    angles.sort(key = lambda x: x[1])
    pins = [pin[0] for pin in angles]

    net_size = len(PINS_COORD) // n_nets

    sections = [pins[i*net_size : (i+1)*net_size] for i in range((len(PINS_COORD) + net_size - 1) // net_size )]

    if len(sections) > n_nets:
        sections[-2] += sections[-1]
        sections.pop()

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
            pin_coord = PINS_COORD[pin]
            ang = get_angle(pin_coord, p)

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
                up_dists.append((pin_id, PINS_COORD[pin_id], euclidean(PINS_COORD[pin_id], p))) #distance can be changed
            up_dists.sort(key = lambda x: x[2])

            chain += [tuple(up_dists[i][0:2]) for i in range(len(up_dists))]

        if len(down) > 0:
            down_dists = []
            for pin_id in down:
                down_dists.append((pin_id, PINS_COORD[pin_id], euclidean(PINS_COORD[pin_id], p))) #distance can be changed
            down_dists.sort(key = lambda x: x[2], reverse = True)

            chain += [tuple(down_dists[i][0:2]) for i in range(len(down_dists))]

        chain.append((section_id+16, DRIVER_PINS_COORD[section_id+16]))

        chains[section_id] = chain

    return chains



def find_loop(chains, PINS_ID):
    visited = [False]*len(PINS_ID)
    found = False

    for ch, chain in enumerate(chains):
        i = 1
        while not found and i < len(chain) - 1:
            pin_id = chain[i][0]
            found = visited[pin_id]
            visited[pin_id] = True
            i += 1
        if found:
            print("Miiiiic a la cadena", ch)
        



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
    # writes output file
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



def exec(in_path, n_nets = 16, out_path = None):
    if not out_path:
        input_name = in_path.split("/")[-1].split(".def")[0]
        out_path = "../output/" + input_name + "_" + str(n_nets) + "_out.def"

    if os.getcwd().split("/")[-1] != "src":
        os.chdir("src")

    DRIVER_PINS_ID, DRIVER_PINS_COORD, PINS_ID, PINS_COORD = read(in_path)

    p = get_p(DRIVER_PINS_COORD)

    #plot_coord((PINS_COORD, DRIVER_PINS_COORD, centers))

    nets = net_classification(PINS_COORD, n_nets, p)

    # print of the map
    COLORS = []
    for section in nets:
        COLORS.append([PINS_COORD[id] for id in section])

    plot_coord(COLORS, DRIVER_PINS_COORD)

    subsections = get_subsections(nets, PINS_COORD, p)

    chains = get_chains(PINS_COORD, DRIVER_PINS_COORD, subsections, p)

    find_loop(chains, PINS_ID)

    dists = compute_dists(chains)

    print(dists)
    print(final_metrics(dists))

    get_output(chains, DRIVER_PINS_ID, PINS_ID, out_path, net_name = "Nano_NET")




in_path = "../input/priv_testcase3.def"
n_nets = 16
out_path = "../output/priv_testcase3_16.def"
exec(in_path, n_nets, out_path)
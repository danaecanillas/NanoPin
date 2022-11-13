def read(input_file):
    DRIVER_PINS_ID = []
    DRIVER_PINS_COORD = []
    PINS_ID = []
    PINS_COORD = []
    with open (input_file, "r") as def_file:
        for line in def_file:
            if "DIRECTION" in line:
                DRIVER_PINS_ID.append(line.split(" +")[0].split("- ")[1])
            elif "FIX " in line:
                coord = line.split("( ")[1].split(" )")[0]
                coord_x = int(coord.split(" ")[0])
                coord_y = int(coord.split(" ")[1])
                DRIVER_PINS_COORD.append((coord_x, coord_y))
            elif "FIXED" in line:
                PINS_ID.append(line.split(" +")[0].split(" ")[0])
                coord = line.split("( ")[1].split(" )")[0]
                coord_x = int(coord.split(" ")[0])
                coord_y = int(coord.split(" ")[1])
                PINS_COORD.append((coord_x, coord_y))

    return DRIVER_PINS_ID, DRIVER_PINS_COORD, PINS_ID, PINS_COORD

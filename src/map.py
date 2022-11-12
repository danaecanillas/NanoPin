

def plot_coord(points_list):
    colours = ["orange", "blue", "green", "gray", "red", "purple", "yellow", "pink"]

    for points_id in range(len(points_list)):
        plt.scatter(
            x = [p[0] for p in points_list[points_id]],
            y = [p[1] for p in points_list[points_id]],
        color = colours[points_id])

    plt.show()
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def plot_coord(points_list, drivers_list):
    colours = ["orange", "blue", "green", "gray", "red", "purple", "yellow", "pink"]
    fig = go.Figure()

    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    for i, points_id in enumerate(range(len(points_list))):
        fig.add_trace(
        go.Scatter(x=[p[0] for p in points_list[points_id]], 
                    y=[p[1] for p in points_list[points_id]], 
                    mode='markers',
                    marker=dict(color=colours[i], size=15)
        ))
    
    fig.add_trace(
    go.Scatter(x=[p[0] for p in drivers_list[0:16]], 
                y=[p[1] for p in drivers_list[0:16]], 
                mode='markers',
                marker=dict(color="black", size=10, symbol="arrow-bar-right")
    ))

    fig.add_trace(
    go.Scatter(x=[p[0] for p in drivers_list[16:]], 
                y=[p[1] for p in drivers_list[16:]], 
                mode='markers',
                marker=dict(color="black", size=10, symbol="arrow-bar-left")
    ))

    fig.show()

plot_coord(COLORS, DRIVER_PINS_COORD)
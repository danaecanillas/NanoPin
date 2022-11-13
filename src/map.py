import matplotlib.pyplot as plt
import plotly.graph_objects as go

def plot_coord(points_list, drivers_list):
    colours = ["orange", "blue", "green", "gray", "red", "purple", "yellow", "pink"]*9
    layout = go.Layout(
    xaxis=dict(
    nticks=300,
    showticklabels=False,
    showgrid=True, # Hide Gridlines
    showline=True, # Hide X-Axis
    ),
    yaxis=dict(
    nticks=300,
    showticklabels=False,
    showgrid=True, # Hide Gridlines
    showline=True, # Hide X-Axis
    ),
    )

    fig = go.Figure(layout=layout)

    for i, points_id in enumerate(range(len(points_list))):
        fig.add_trace(
        go.Scatter(x=[p[0] for p in points_list[points_id]], 
                    y=[p[1] for p in points_list[points_id]], 
                    name="CHAIN " + str(i),
                    mode='markers',
                    marker=dict(color=colours[i])
        ))
    
    fig.add_trace(
    go.Scatter(x=[p[0] for p in drivers_list[0:16]], 
                y=[p[1] for p in drivers_list[0:16]], 
                mode='markers',
                name="DRIVER INPUT",
                marker=dict(color="black", size=10, symbol="arrow-bar-right")
    ))

    fig.add_trace(
    go.Scatter(x=[p[0] for p in drivers_list[16:]], 
                y=[p[1] for p in drivers_list[16:]], 
                mode='markers',
                name="DRIVER OUTPUT",
                marker=dict(color="black", size=10, symbol="arrow-bar-left")
    ))
    
    fig.update_layout(paper_bgcolor="#D3D3D3")
    fig.update_layout(template="simple_white")

    fig.show()

plot_coord(COLORS, DRIVER_PINS_COORD)


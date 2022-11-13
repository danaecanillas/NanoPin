import matplotlib.pyplot as plt
import plotly.graph_objects as go

<<<<<<< HEAD
def plot_coord(points_list):
    colours = ["orange", "blue", "green", "gray", "red", "purple", "yellow", "pink"]*9
    layout = go.Layout(
    xaxis=dict(
    nticks=1000,
    showgrid=True, # Hide Gridlines
    showline=True, # Hide X-Axis
    ),
    yaxis=dict(
    nticks=1000,
    showgrid=True, # Hide Gridlines
    showline=True, # Hide X-Axis
    ),
    )

    fig = go.Figure(layout=layout)
=======
def plot_coord(points_list, drivers_list):
    colours = ["orange", "blue", "green", "gray", "red", "purple", "yellow", "pink"]
    fig = go.Figure()
>>>>>>> b7ecc14dec91c1493a86783db64fb1141a7a3a60

    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    for i, points_id in enumerate(range(len(points_list))):
        fig.add_trace(
        go.Scatter(x=[p[0] for p in points_list[points_id]], 
                    y=[p[1] for p in points_list[points_id]], 
                    name="Chain " + str(i),
                    mode='markers',
                    marker=dict(color=colours[i], size=15)
        ))
    
<<<<<<< HEAD
    fig.update_layout(paper_bgcolor="#D3D3D3")
    fig.update_layout(template="simple_white")

    fig.show()

plot_coord(COLORS)
=======
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
>>>>>>> b7ecc14dec91c1493a86783db64fb1141a7a3a60

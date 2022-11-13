import matplotlib.pyplot as plt
import plotly.graph_objects as go

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

    for i, points_id in enumerate(range(len(points_list))):
        fig.add_trace(
        go.Scatter(x=[p[0] for p in points_list[points_id]], 
                    y=[p[1] for p in points_list[points_id]], 
                    name="Chain " + str(i),
                    mode='markers',
                    marker=dict(color=colours[i])
        ))
    
    fig.update_layout(paper_bgcolor="#D3D3D3")
    fig.update_layout(template="simple_white")

    fig.show()

plot_coord(COLORS)

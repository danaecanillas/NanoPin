import matplotlib.pyplot as plt
import plotly.graph_objects as go

def plot_coord(points_list):
    colours = ["orange", "blue", "green", "gray", "red", "purple", "yellow", "pink"]
    fig = go.Figure()

    for i, points_id in enumerate(range(len(points_list))):
        fig.add_trace(
        go.Scatter(x=[p[0] for p in points_list[points_id]], 
                    y=[p[1] for p in points_list[points_id]], 
                    mode='markers',
                    marker=dict(color=colours[i])
        ))

    fig.add_layout_image(
        dict(
            source="D:\Programació\NanoPin\wallpaper.jpg",
            xref="x",
            yref="y",
            x=0,
            y=3,
            sizex=2,
            sizey=2,
            sizing="stretch",
            opacity=0.2,
            layer="below")
    )

    fig.show()

plot_coord(COLORS)
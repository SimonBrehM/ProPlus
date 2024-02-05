from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
import math

def moyenne_graph(progress):
    progress_percent = progress 
    start_angle = 0
    end_angle = progress_percent / 100 * 2 * math.pi  # Convert progress to radians

    plot = figure(height=300, width=300, title=str(progress), toolbar_location=None, tools="")

    source = ColumnDataSource(data=dict(start=[start_angle], end=[end_angle]))
    plot.wedge(x=0, y=0, start_angle='start', end_angle='end', radius=0.8, color="#ff5b5b", source=source)

    script, div = components(plot)
    return script, div
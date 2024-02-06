from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
import math

def moyenne_graph(progress):
    progress_percent = progress 
    start_angle = math.pi/2
    end_angle = math.pi/2 + progress_percent / 100 * 2 * math.pi  # Convert progress to radians

    p = figure(height=350, width=350, title=None, toolbar_location=None, tools="")
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.yaxis.visible = False 
    p.xaxis.visible = False
    p.outline_line_color = "#FAF9F9"
    p.background_fill_color = "#FAF9F9"

    source = ColumnDataSource(data=dict(start=[start_angle], end=[end_angle]))
    p.wedge(x=0, y=0, start_angle='start', end_angle='end', radius=0.8, color="#ff5b5b", source=source)

    script, div = components(p)
    return script, div
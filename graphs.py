from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
import math

def moyenne_graph(current:float, last:float, suggestive:float=None): 
    if suggestive==None: suggestive = current 
    else: 
        last = suggestive

    #Radian value calculation
    difference = current - last 
    stable_start_angle = math.pi/2
    stable_end_angle = math.pi/2 + current / 100 * 2 * math.pi
    
    if difference > 0:
        stable_end_angle -= difference / 100 * 2 * math.pi
        difference_end_angle = math.pi/2 + current / 100 * 2 * math.pi
        difference_color = "#00BA00"
    else:
        difference_end_angle = math.pi/2 + last / 100 * 2 * math.pi
        difference_color = 'red'
    if suggestive!=current : difference_color = 'lightskyblue'
    difference_start_angle = stable_end_angle

    #Graph settings
    p = figure(height=350, width=350, title=None, toolbar_location=None, tools="")
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.yaxis.visible = False 
    p.xaxis.visible = False
    p.outline_line_color = "#FAF9F9"
    p.background_fill_color = "#FAF9F9"
    p.border_fill_color = "#FAF9F9"

    #Render
    source = ColumnDataSource(data=dict(stable_start=[stable_start_angle], stable_end=[stable_end_angle], difference_start=[difference_start_angle], difference_end=[difference_end_angle]))
    p.wedge(x=0, y=0, start_angle='stable_start', end_angle='stable_end', radius=0.8, color="#ff5b5b", source=source)
    if difference!=0: p.wedge(x=0, y=0, start_angle='difference_start', end_angle='difference_end', radius=0.8, color=difference_color, source=source)

    script, div = components(p)
    return script, div
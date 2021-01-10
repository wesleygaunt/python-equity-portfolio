# -*- coding: utf-8 -*-
"""
Plotting methods, which utilise the Bokeh module to create interactive HTML5 plots. 
"""

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10_10 as palette 
import pandas as pd
import constants
import itertools  

def line(data, show_plot = True, title = 'plot', axis = 'value'):
    """
    

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    show_plot : TYPE, optional
        DESCRIPTION. The default is True.
    title : TYPE, optional
        DESCRIPTION. The default is 'plot'.
    axis : str, 'value' or 'percentage'
        DESCRIPTION. The default is 'value'.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    
    data = data.copy()

    if(type(data) == pd.Series):
        data = pd.DataFrame(data)
        
    output_file(constants.DEFAULT_PLOTS_FOLDER + "\\" + title + ".html")
    
    y_axis_label = ''
    if(axis == 'value'):
        y_axis_label = 'GBP'
    elif(axis == 'percentage'):
        y_axis_label = 'Normalised value'

        
    hover = HoverTool(
    tooltips=[
    ('','$name'),
    ('',   '$x{%F}'),
    ('','$y{0.00}' ), # use @{ } for field names with spaces
    ],
    
    formatters={'$x': 'datetime'}
    
    )
    
    fig = figure(y_axis_label = y_axis_label, x_axis_label='Date',x_axis_type='datetime',sizing_mode="stretch_both",title = title) #tooltips = TOOLTIPS)#,y_axis_label='% change')
    fig.add_tools(hover)
    
    source = ColumnDataSource(data)
    columns = list(data.columns)
    
    colors_cycle = itertools.cycle(palette)
    
    for name,color in zip(columns,colors_cycle):
        fig.line(x = 'index',y = name, source = source, color = color,line_width=2,legend_label = name,name = name,alpha = 1,muted_alpha = 0.2)
    
    fig.legend.location = "top_left"
    fig.legend.click_policy="mute"
    fig.toolbar_location = "above"
    
    # show the results
    if(show_plot):
        show(fig)
    return fig

# def stacked_area(data,plot_file = 'plot', show_plot = True):
#     data = data.copy()
    
#     if 'TOTAL' in data:
#         total = data['TOTAL']
#         del data['TOTAL']
#     else:
#         total = data.sum(axis = 1)

        
#     output_file(constants.DEFAULT_PLOTS_FOLDER + "\\" + plot_file + ".html")
#     #output_file(plot_file + ".html")

#     fig = figure(x_axis_label='Date',x_axis_type='datetime',sizing_mode="stretch_both")#,y_axis_label='% change')
    
#     source = ColumnDataSource(data)
#     columns = list(data.columns)
    
#     fig.varea_stack(stackers=columns, x='index', color=colors[0:len(columns)], legend_label=columns, source=source,muted_alpha = 0.2)
    
#     fig.line(x = total.index,y = total, color = colors[len(columns)],line_width=2,legend_label = 'TOTAL',alpha = 1,muted_alpha = 0.2)

#     fig.legend.location = "top_left"
#     fig.legend.click_policy="mute"
    
#     # show the results
#     if(show_plot):
#         show(fig)
#     return fig

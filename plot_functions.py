
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import os
from rpy2.robjects.conversion import py2rpy

# Set the R_HOME environment variable
#os.environ['R_HOME'] = "/Library/Frameworks/R.framework/Resources"


# import rpy2.robjects as robjects
# from rpy2.robjects import pandas2ri
#
# # Convert the pandas DataFrame to an R data frame
# def compute_mean(df, column_name):
#     # Convert the pandas DataFrame to an R data frame
#     pandas2ri.activate()
#     data = pandas2ri.DataFrame(df)
#
#     # Define the R function code
#     r_code = f'''
#     compute_mean <- function(data) {{
#       # Compute the mean
#       mean_value <- mean(data${column_name})
#
#       # Return the mean
#       return(mean_value)
#     }}
#     '''
#
#     # Load the R function into the R environment
#     robjects.r(r_code)
#
#     # Call the compute_mean function in R
#     mean_value = robjects.r['compute_mean'](data)
#
#     # Return the mean value computed in R
#     return mean_value[0]
#
#
# # Example usage
# data = {'column_name': [1, 2, 3, 4, 5]}
# df = pd.DataFrame(data)
# mean_value = compute_mean(df, 'column_name')
# print(mean_value)
fontsize=14
def plotRt(data_county, cases, pr, ww_arima, ww_trimmed): # log

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    x = data_county.Date +  pd.DateOffset(days=10)

    county = data_county["County"].iloc[0]
    if ww_arima:
        fig.add_trace(go.Scatter(name='WW ARIMA', mode='lines', x=x, y=data_county['Rt_q50_co_Cases_N'],
                                 line=dict(color='rgba(0.121, 0.467, 0.706, 1.0)', width=3)), secondary_y=False, )
        upper_line = data_county['Rt_q90_co_Cases_N']; lower_line = data_county['Rt_q10_co_Cases_N']
        fig.add_trace(go.Scatter(name='95% quantile', mode='lines', x=list(x) + list(x[::-1]),
                                 y=list(upper_line) + list(lower_line[::-1]), fill='tozerox',
                                 fillcolor='rgba(0.121, 0.467, 0.706, 0.5)', line=dict(color='rgba(0.121, 0.467, 0.706, 0.5)'), showlegend=False))

    if ww_trimmed:
        upper_line = data_county['Rt_q90_co_Cases_N_av10']; lower_line = data_county['Rt_q10_co_Cases_N_av10']

        fig.add_trace(go.Scatter(name='WW trimmed', mode='lines', x=x, y=data_county['Rt_q50_co_Cases_N_av10'],
                                 line=dict(color='rgba(0.173, 0.627, 0.173, 1.0)', width=3)), secondary_y=False, )

        fig.add_trace(go.Scatter(name='95% quantile', mode='lines', x=list(x) + list(x[::-1]),
                                 y=list(upper_line) + list(lower_line[::-1]), fill='tozerox',
                                 fillcolor='rgba(0.173, 0.627, 0.173, 0.5)', line=dict(color='rgba(0.173, 0.627, 0.173, 0.5)'), showlegend=False))
    if cases:
        upper_line = data_county['Rt_q90_co_Cases']; lower_line = data_county['Rt_q10_co_Cases']
        fig.add_trace(go.Scatter(name='Cases', mode='lines', x=x, y=data_county['Rt_q50_co_Cases'], line=dict(color='rgba(0.843, 0.153, 0.175, 1.0)', width=3)), secondary_y=False, )
        fig.add_trace(go.Scatter(name='95% quantile', mode='lines', x=list(x) + list(x[::-1]), y=list(upper_line) + list(lower_line[::-1]), fill='tozerox',
                                 fillcolor='rgba(0.843, 0.153, 0.175, 0.5)', line=dict(color='rgba(0.843, 0.153, 0.175, 0.5)'), showlegend=False))
    if pr:
        upper_line = data_county['Rt_q90_co_Cases_pr'];  lower_line = data_county['Rt_q10_co_Cases_pr']
        fig.add_trace(go.Scatter(name='Pos Rate', mode='lines', x=x, y=data_county['Rt_q50_co_Cases_pr'], line=dict(color='rgba(0.584, 0.404, 0.737, 1.0)', width=3)), secondary_y=False, )
        fig.add_trace(go.Scatter(name='95% quantile', mode='lines', x=list(x) + list(x[::-1]), y=list(upper_line) + list(lower_line[::-1]), fill='tozerox',
                                 fillcolor='rgba (0.584, 0.404, 0.737, 0.5)', line=dict(color='rgba (0.584, 0.404, 0.737, 0.5)'), showlegend=False))

    #fig.add_hline(y=q33, line_width=2, line_dash="dash", line_color="green")
    #fig.add_hline(y=q66, line_width=2, line_dash="dash", line_color="green")
    fig.add_hline(y=1, line_width=2, line_dash="dash", line_color="red")

    #fig.update_yaxes(title_text="Cases", secondary_y=True)
    fig.update_layout(font=dict(family="sans-serif", size=fontsize, color="black"), template='plotly_white', xaxis=dict(
        showgrid=True,    # Show grid lines for the x-axis
        showline=True,    # Show the x-axis line
        gridcolor='lightgray',  # Set the color of the grid lines
        zerolinecolor='black'    # Set the color of the x-axis line
    ),
    yaxis=dict(
        showgrid=True,    # Show grid lines for the y-axis
        showline=True,    # Show the y-axis line
        gridcolor='lightgray',  # Set the color of the grid lines
        zerolinecolor='black'    # Set the color of the y-axis line
    ),  legend_font_size=14, legend_title_font_size=fontsize)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=0.8))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    #fig.update_layout(autosize=False, width=450, height=250, margin=dict(l=0, r=0, b=10, t=10, pad=4),
    #                  yaxis=dict(title=ylabel))  # ,xaxis=dict(title="Date"))
    fig.update_layout(font_family="Arial", title_font_family="Arial")
    fig.layout.showlegend = True
    fig.update_layout(title="Rt" )
    #fig.update_layout(font_color='white', title_font_color='white')
    #fig.update_layout(xaxis=dict(domain=[0.3, 0.7]),
    #    yaxis2=dict(title="yaxis2 title", titlefont=dict(color="#ff7f0e"), tickfont=dict(color="#ff7f0e"),
    #                anchor="free", overlaying="y", side="right", position=0.85), )

    return fig


#fig2 = plotNconc(data_county=data_county_, ww_arima=ww_arima, ww_trimmed=ww_trimmed)


def plotNconc(data_county, ww_arima, ww_trimmed): # log

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    x = data_county.Date #+  pd.DateOffset(days=10)

    county = data_county["County"].iloc[0]
    fig.add_trace(go.Scatter(name='N gene/PMMoV', mode='markers', x=x, y=data_county['SC2_N_norm_PMMoV'],
                             line=dict(color='black', width=3)), secondary_y=False, )
    if ww_arima:

        fig.add_trace(go.Scatter(name='WW ARIMA', mode='lines', x=x, y=data_county['mean'],
                                 line=dict(color='rgba(0.121, 0.467, 0.706, 1.0)', width=3)), secondary_y=False, )

        upper_line = data_county['0.975quant']; lower_line = data_county['0.025quant']

        fig.add_trace(go.Scatter(name='95% quantile', mode='lines', x=list(x) + list(x[::-1]),
                                 y=list(upper_line) + list(lower_line[::-1]), fill='tozerox',
                                 fillcolor='rgba(0.121, 0.467, 0.706, 0.5)', line=dict(color='rgba(0.121, 0.467, 0.706, 0.5)'), showlegend=False))

    if ww_trimmed:
        #upper_line = data_county['Rt_q90_co_Cases_N_av10']; lower_line = data_county['Rt_q10_co_Cases_N_av10']

        fig.add_trace(go.Scatter(name='WW trimmed', mode='lines', x=x, y=data_county['N_av10'], line=dict(color='rgba(0.173, 0.627, 0.173, 1.0)', width=3)), secondary_y=False, )

    #fig.add_hline(y=1, line_width=2, line_dash="dash", line_color="red")

    fig.update_yaxes(title_text="Cases", secondary_y=True)
    fig.update_layout(font=dict(family="sans-serif", size=fontsize, color="black"), template='plotly_white',
                      legend_font_size=14, legend_title_font_size=fontsize)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=0.8))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    #fig.update_layout(autosize=False, width=450, height=250, margin=dict(l=0, r=0, b=10, t=10, pad=4),
    #                  yaxis=dict(title=ylabel))  # ,xaxis=dict(title="Date"))
    fig.update_layout(font_family="Arial", title_font_family="Arial")
    fig.layout.showlegend = True
    fig.update_layout(title="Smoothed normalize SARS-CoV-2 concentration")
    #fig.update_layout(font_color='white', title_font_color='white')
    #fig.update_layout(xaxis=dict(domain=[0.3, 0.7]),
    #    yaxis2=dict(title="yaxis2 title", titlefont=dict(color="#ff7f0e"), tickfont=dict(color="#ff7f0e"),
    #                anchor="free", overlaying="y", side="right", position=0.85), )

    return fig


def plotNconc_data(data, ww_arima, ww_trimmed): # log

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    x = data.Date #+  pd.DateOffset(days=10)

    #county = data["County"].iloc[0]
    fig.add_trace(go.Scatter(name='N gene/PMMoV', mode='markers', x=x, y=data['conc'],
                             line=dict(color='black', width=3)), secondary_y=False, )
    #if ww_arima:

        #fig.add_trace(go.Scatter(name='WW ARIMA', mode='lines', x=x, y=data['mean'],
        #                         line=dict(color='rgba(0.121, 0.467, 0.706, 1.0)', width=3)), secondary_y=False, )

        #upper_line = data['0.975quant']; lower_line = data['0.025quant']

        #fig.add_trace(go.Scatter(name='95% quantile', mode='lines', x=list(x) + list(x[::-1]),
        #                         y=list(upper_line) + list(lower_line[::-1]), fill='tozerox',
        #                         fillcolor='rgba(0.121, 0.467, 0.706, 0.5)', line=dict(color='rgba(0.121, 0.467, 0.706, 0.5)'), showlegend=False))

    #if ww_trimmed:
        #upper_line = data_county['Rt_q90_co_Cases_N_av10']; lower_line = data_county['Rt_q10_co_Cases_N_av10']

    #    fig.add_trace(go.Scatter(name='WW trimmed', mode='lines', x=x, y=data['N_av10'], line=dict(color='rgba(0.173, 0.627, 0.173, 1.0)', width=3)), secondary_y=False, )

    #fig.add_hline(y=1, line_width=2, line_dash="dash", line_color="red")

    fig.update_yaxes(title_text="Cases", secondary_y=True)
    fig.update_layout(font=dict(family="sans-serif", size=fontsize, color="black"), template='plotly_white',
                      legend_font_size=14, legend_title_font_size=fontsize)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=0.8))
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
    #fig.update_layout(autosize=False, width=450, height=250, margin=dict(l=0, r=0, b=10, t=10, pad=4),
    #                  yaxis=dict(title=ylabel))  # ,xaxis=dict(title="Date"))
    fig.update_layout(font_family="Arial", title_font_family="Arial")
    fig.layout.showlegend = True
    fig.update_layout(title="Smoothed normalize SARS-CoV-2 concentration")
    #fig.update_layout(font_color='white', title_font_color='white')
    #fig.update_layout(xaxis=dict(domain=[0.3, 0.7]),
    #    yaxis2=dict(title="yaxis2 title", titlefont=dict(color="#ff7f0e"), tickfont=dict(color="#ff7f0e"),
    #                anchor="free", overlaying="y", side="right", position=0.85), )

    return fig
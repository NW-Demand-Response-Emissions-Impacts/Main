"""
make_plots.py

Generates plotly graph objects for displaying on dashbaord.
Functions are separated into tables, bar charts, dropdowns, and callbacks.
"""

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


# ================================================================================ #
# Tables
# ================================================================================ #

def plot_hours_table(potential):
    hours_table = go.Figure(data=[go.Table(
    header=dict(values=list(potential['dr_hours'].columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=potential['dr_hours'].transpose().values.tolist(),
               fill_color='lavender',
               align='left'))
    ])

    hours_table.update_layout(height=200,margin=dict(r=20, l=20, t=20, b=20))

    return hours_table

# ================================================================================ #
# Bar plots
# ================================================================================ #

def plot_impacts_bar(impacts):
    impacts_bar = go.Figure(data=[go.Bar(
        name = 'Winter',
        x = ['Total','DVR','ResTOU Shed'],
        y = [impacts['newbins_Bin_1_Winter_total'], impacts['newbins_Bin_1_Winter_cumulative']['DVR'], impacts['newbins_Bin_1_Winter_cumulative']['ResTOU_shed']]
        ),
        go.Bar(
        name = 'Summer',
        x = ['Total','DVR','ResTOU Shed'],
        y = [impacts['newbins_Bin_1_Summer_total'], impacts['newbins_Bin_1_Summer_cumulative']['DVR'], impacts['newbins_Bin_1_Summer_cumulative']['ResTOU_shed']]
        ),
        go.Bar(
        name = 'Fall',
        x = ['Total','DVR','ResTOU Shed'],
        y = [impacts['newbins_Bin_1_Fall_total'], impacts['newbins_Bin_1_Fall_cumulative']['DVR'], impacts['newbins_Bin_1_Fall_cumulative']['ResTOU_shed']]
        )
    ])

    return impacts_bar

def plot_impacts_bar_moreinfo(impacts):
    impacts_bar_moreinfo = go.Figure(data=[go.Bar(
        name = 'Winter',
        x = ['Old Bin 1','Old Bin 2', 'Old Bin 3', 'Old Bin 4'],
        y = [impacts['newbins_Bin_1_Winter_total'], impacts['oldbins_Bin_1_Winter_total'], impacts['oldbins_Bin_2_Winter_total'], impacts['oldbins_Bin_3_Winter_total'], impacts['oldbins_Bin_4_Winter_total']]
        ),
        go.Bar(
        name = 'Summer',
        x = ['Old Bin 1','Old Bin 2', 'Old Bin 3', 'Old Bin 4'],
        y = [impacts['newbins_Bin_1_Summer_total'], impacts['oldbins_Bin_1_Summer_total'], impacts['oldbins_Bin_2_Summer_total'], impacts['oldbins_Bin_3_Summer_total'], impacts['oldbins_Bin_4_Summer_total']]
        ),
    ])

    return impacts_bar_moreinfo

def plot_potential_bar(potential):
    potential_bar = go.Figure(data=go.Bar(x=potential['comparison_barchart']['DR Plan, Season, and Bin'], y=potential['comparison_barchart']['2041 Potential']))

    return potential_bar

# ================================================================================ #
# Dropdowns
# ================================================================================ #

def plot_rates_dropdown(rates_dd_options):
    rates_dropdown = html.Div([
        dcc.Dropdown(
            id='rates_dropdown',
            options=[{'label': x, 'value': x} for x in rates_dd_options],
            value = 'All Year'
        )])

    rates_plot = html.Div(id = 'rates_plot')

    return rates_dropdown, rates_plot

def plot_potential_dropdown(potential_dd_options):
    potential_dropdown = html.Div([
        dcc.Dropdown(
            id='potential_dropdown',
            options=[{'label': x, 'value': x} for x in potential_dd_options],
            value = 'Winter'
        )])

    potential_plot = html.Div(id = 'potential_plot')

    return potential_dropdown, potential_plot

def plot_rates_dropdown_moreinfo(rates_dd_options_moreinfo):
    rates_dropdown_moreinfo = html.Div([
        dcc.Dropdown(
            id='rates_dropdown_moreinfo',
            options=[{'label': x, 'value': x} for x in rates_dd_options_moreinfo],
            value = 'All Year'
        )])

    rates_plot_moreinfo = html.Div(id = 'rates_plot_moreinfo')

    return rates_dropdown_moreinfo, rates_plot_moreinfo

def plot_impacts_dropdown(impacts_dd_options):
    impacts_dropdown = html.Div([
        dcc.Dropdown(
            id='impacts_dropdown',
            options=[{'label': x, 'value': x} for x in impacts_dd_options],
            value = 'Winter'
        )])

    impacts_plot = html.Div(id = 'impacts_plot')

    return impacts_dropdown, impacts_plot

# ================================================================================ #
# Callbacks
# ================================================================================ #

def rates_callback(rates, rates_dd_choice):
    rates_fig = go.Figure()
    if rates_dd_choice == 'Comparison':
        rates_fig.add_trace(go.Scatter(x=rates['Annual_Baseline']['Report_Hour'], y=rates['Annual_Baseline']['Baseline Emissions Rate Estimate'],name='All Year',marker=dict(color='black')))
        rates_fig.add_trace(go.Scatter(x=rates['Summer_Baseline']['Report_Hour'], y=rates['Summer_Baseline']['Baseline Emissions Rate Estimate'],name='Summer',marker=dict(color='red')))
        rates_fig.add_trace(go.Scatter(x=rates['Winter_Baseline']['Report_Hour'], y=rates['Winter_Baseline']['Baseline Emissions Rate Estimate'],name='Winter',marker=dict(color='blue')))
        rates_fig.add_trace(go.Scatter(x=rates['Fall_Baseline']['Report_Hour'], y=rates['Fall_Baseline']['Baseline Emissions Rate Estimate'],name='Fall',marker=dict(color='orange')))
        rates_fig.add_trace(go.Scatter(x=rates['Spring_Baseline']['Report_Hour'], y=rates['Spring_Baseline']['Baseline Emissions Rate Estimate'],name='Spring',marker=dict(color='pink')))
    elif rates_dd_choice == 'All Year': 
        rates_fig.add_trace(go.Scatter(x=rates['Annual_Baseline']['Report_Hour'], y=rates['Annual_Baseline']['Baseline Emissions Rate Estimate'],name='All Year',marker=dict(color='black')))
    elif rates_dd_choice == 'Summer':
        rates_fig.add_trace(go.Scatter(x=rates['Summer_Baseline']['Report_Hour'], y=rates['Summer_Baseline']['Baseline Emissions Rate Estimate'],name='Summer',marker=dict(color='red')))
    elif rates_dd_choice == 'Winter': 
        rates_fig.add_trace(go.Scatter(x=rates['Winter_Baseline']['Report_Hour'], y=rates['Winter_Baseline']['Baseline Emissions Rate Estimate'],name='Winter',marker=dict(color='blue')))
    elif rates_dd_choice == 'Fall': 
        rates_fig.add_trace(go.Scatter(x=rates['Fall_Baseline']['Report_Hour'], y=rates['Fall_Baseline']['Baseline Emissions Rate Estimate'],name='Fall',marker=dict(color='orange')))
    elif rates_dd_choice == 'Spring': 
        rates_fig.add_trace(go.Scatter(x=rates['Spring_Baseline']['Report_Hour'], y=rates['Spring_Baseline']['Baseline Emissions Rate Estimate'],name='Spring',marker=dict(color='pink')))
        
    rates_fig.update_layout(xaxis_title='Hour', yaxis_title='Emissions Rate')
    
    return dcc.Graph(figure=rates_fig)
    
def potential_callback(potential, potential_dd_choice):
    potential_fig = go.Figure()
    if potential_dd_choice == 'Winter':
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Winter_bin1']['Year'], y=potential['newbins_Winter_bin1']['DVR'], name='DVR',marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Winter_bin1']['Year'], y=potential['newbins_Winter_bin1']['ResTOU'], name='ResTOU',marker=dict(color='red')))
    elif potential_dd_choice == 'Summer':
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Summer_bin1']['Year'], y=potential['newbins_Summer_bin1']['DVR'], name='DVR',marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Winter_bin1']['Year'], y=potential['newbins_Summer_bin1']['ResTOU'], name='ResTOU',marker=dict(color='red')))
    elif potential_dd_choice == 'Fall':
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Fall_bin1']['Year'], y=potential['newbins_Fall_bin1']['DVR'], name='DVR',marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Fall_bin1']['Year'], y=potential['newbins_Fall_bin1']['ResTOU'], name='ResTOU',marker=dict(color='red')))          
        
    potential_fig.update_layout(xaxis_title='Year', yaxis_title='DR Potential (MW)')
    
    return dcc.Graph(figure=potential_fig)

def rates_callback_moreinfo(rates, rates_dd_choice_moreinfo):
    rates_fig_moreinfo = go.Figure()
    if rates_dd_choice_moreinfo == 'Comparison':
        rates_fig_moreinfo.add_trace(go.Scatter(x=rates['newbins_Annual_Baseline']['Report_Hour'], y=rates['newbins_Annual_Baseline']['Baseline Emissions Rate Estimate'],name='All Year',marker=dict(color='black')))
        rates_fig_moreinfo.add_trace(go.Scatter(x=rates['newbins_Summer_Baseline']['Report_Hour'], y=rates['newbins_Summer_Baseline']['Baseline Emissions Rate Estimate'],name='Summer',marker=dict(color='red')))
        rates_fig_moreinfo.add_trace(go.Scatter(x=rates['newbins_Winter_Baseline']['Report_Hour'], y=rates['newbins_Winter_Baseline']['Baseline Emissions Rate Estimate'],name='Winter',marker=dict(color='blue')))
        rates_fig_moreinfo.add_trace(go.Scatter(x=rates['newbins_Fall_Baseline']['Report_Hour'], y=rates['newbins_Fall_Baseline']['Baseline Emissions Rate Estimate'],name='Fall',marker=dict(color='orange')))
    elif rates_dd_choice_moreinfo == 'All Year': 
        rates_fig_moreinfo.add_trace(go.Scatter(x=rates['newbins_Annual_Baseline']['Report_Hour'], y=rates['newbins_Annual_Baseline']['Baseline Emissions Rate Estimate'],name='All Year',marker=dict(color='black')))
    elif rates_dd_choice_moreinfo == 'Summer':
        rates_fig_moreinfo.add_trace(go.Scatter(x=rates['newbins_Summer_Baseline']['Report_Hour'], y=rates['newbins_Summer_Baseline']['Baseline Emissions Rate Estimate'],name='Summer',marker=dict(color='red')))
    elif rates_dd_choice_moreinfo == 'Winter': 
        rates_fig_moreinfo.add_trace(go.Scatter(x=rates['newbins_Winter_Baseline']['Report_Hour'], y=rates['newbins_Winter_Baseline']['Baseline Emissions Rate Estimate'],name='Winter',marker=dict(color='blue')))
    elif rates_dd_choice_moreinfo == 'Fall': 
        rates_fig_moreinfo.add_trace(go.Scatter(x=rates['newbins_Fall_Baseline']['Report_Hour'], y=rates['newbins_Fall_Baseline']['Baseline Emissions Rate Estimate'],name='Fall',marker=dict(color='orange')))
        
    rates_fig_moreinfo.update_layout(xaxis_title='Hour', yaxis_title='Emissions Rate')
    
    return dcc.Graph(figure=rates_fig_moreinfo)

def impacts_callback(impacts, impacts_dd_choice):
    impacts_fig = go.Figure()
    if impacts_dd_choice == 'Winter':
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Bin_1_Winter']['Year'], y=impacts['newbins_Bin_1_Winter']['DVR'], name='DVR',marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Bin_1_Winter']['Year'], y=impacts['newbins_Bin_1_Winter']['ResTOU_shed'], name='ResTOU Shed',marker=dict(color='red')))
    elif impacts_dd_choice == 'Summer':
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Bin_1_Summer']['Year'], y=impacts['newbins_Bin_1_Summer']['DVR'], name='DVR',marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Bin_1_Summer']['Year'], y=impacts['newbins_Bin_1_Summer']['ResTOUS_shed'], name='ResTOU Shed',marker=dict(color='red')))
    elif impacts_dd_choice == 'Fall':
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Bin_1_Fall']['Year'], y=impacts['newbins_Bin_1_Fall']['DVR'], name='DVR',marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Bin_1_Winter']['Year'], y=impacts['newbins_Bin_1_Fall']['ResTOU_shed'], name='ResTOU Shed',marker=dict(color='red')))  
        
    impacts_fig.update_layout(xaxis_title='Year', yaxis_title='Emissions Impacts')
    
    return dcc.Graph(figure=impacts_fig)

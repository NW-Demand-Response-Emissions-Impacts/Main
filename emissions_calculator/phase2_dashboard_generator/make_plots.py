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
    """
    Creates the table of DR hours of implementation.

    Args:
        potential: dictionary of pandas dataframes of potential,
                   which contains the DR hours
    Returns:
        plotly graph object of DR hours table
    """
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
    """
    Plots cumulative emissions reductions as a bar chart.
    For the home page.

    Args:
        impacts: dictionary of pandas dataframes of emissions reductions
    Returns:
        plotly graph object of emissions reductions bar chart
    """
    impacts_bar = go.Figure(data=[go.Bar(
        name = 'Winter',
        x = ['ResTOU Shed','ResTOU Shift'],
        y = [impacts['barchart'].at[0,'newbins_bin1_shed'],
            impacts['barchart'].at[0,'newbins_bin1_shift']]
        ),
        go.Bar(
        name = 'Summer',
        x = ['ResTOU Shed','ResTOU Shift'],
        y = [impacts['barchart'].at[1,'newbins_bin1_shed'],
            impacts['barchart'].at[1,'newbins_bin1_shift']]
        ),
        go.Bar(
        name = 'Fall',
        x = ['ResTOU Shed','ResTOU Shift'],
        y = [impacts['barchart'].at[2,'newbins_bin1_shed'],
            impacts['barchart'].at[2,'newbins_bin1_shift']]
        )
    ])
    impacts_bar.update_layout(
        yaxis_title = 'Metric Tons of CO2 Reduced'
    )

    return impacts_bar

def plot_impacts_bar_moreinfo(impacts):
    """
    Plots cumulative emissions reductions as a bar chart.
    For the more information page.
    Note: a dropdown is currently being used in place of this plot.

    Args:
        impacts: dictionary of pandas dataframes of emissions reductions
    Returns:
        plotly graph object of emissions reductions bar chart
    """
    impacts_bar_moreinfo = go.Figure(data=[go.Bar(
        name = 'Winter',
        x = ['New Bin 1 Shed','New Bin 1 Shift','Old Bin 1','Old Bin 2',
            'Old Bin 3', 'Old Bin 4'],
        y = [impacts['barchart'].at[0, 'newbins_bin1_shed'],
             impacts['barchart'].at[0, 'newbins_bin1_shift'],
             impacts['barchart'].at[0, 'oldbins_bin1'],
             impacts['barchart'].at[0, 'oldbins_bin2'],
             impacts['barchart'].at[0, 'oldbins_bin3'],
             impacts['barchart'].at[0, 'oldbins_bin4']
             ]
        ),
        go.Bar(
        name = 'Summer',
        x = ['New Bin 1 Shed','New Bin 1 Shift','Old Bin 1','Old Bin 2',
            'Old Bin 3', 'Old Bin 4'],
        y = [impacts['barchart'].at[1, 'newbins_bin1_shed'],
             impacts['barchart'].at[1, 'newbins_bin1_shift'],
             impacts['barchart'].at[1, 'oldbins_bin1'],
             impacts['barchart'].at[1, 'oldbins_bin2'],
             impacts['barchart'].at[1, 'oldbins_bin3'],
             impacts['barchart'].at[1, 'oldbins_bin4']
             ]
        ),
        go.Bar(
        name = 'Fall',
        x = ['New Bin 1 Shed','New Bin 1 Shift','Old Bin 1','Old Bin 2',
            'Old Bin 3', 'Old Bin 4'],
        y = [impacts['barchart'].at[2, 'newbins_bin1_shed'],
             impacts['barchart'].at[2, 'newbins_bin1_shift'],
             impacts['barchart'].at[2, 'oldbins_bin1'],
             impacts['barchart'].at[2, 'oldbins_bin2'],
             impacts['barchart'].at[2, 'oldbins_bin3'],
             impacts['barchart'].at[2, 'oldbins_bin4']
             ]
        )
    ])

    impacts_bar_moreinfo.update_layout(
        yaxis_title = 'Metric Tons of CO2 Reduced')

    return impacts_bar_moreinfo

def plot_potential_bar(potential):
    """
    Plots DR potential as a bar chart.

    Args:
        potential: dictionary of pandas dataframes of potential
    Returns:
        plotly graph object of potential bar chart
    """
    potential_bar = go.Figure(data=go.Bar(
        x=potential['comparison_barchart']['DR Plan, Season, and Bin'],
        y=potential['comparison_barchart']['2041 Potential']))

    potential_bar.update_layout(
        yaxis_title = 'DR Potential (MW)')

    return potential_bar

# ================================================================================ #
# Dropdowns
# ================================================================================ #

def plot_rates_dropdown(rates_dd_options):
    """
    Initializes the dropdown menu for hourly emissions rates.
    For the home page.

    Args:
        rates_dd_options: list of dropdowns for emissions rates
    Returns:
        rates_dropdown: HTML division for dropdown menu
        rates_plot: HTML division for plot
    """
    rates_dropdown = html.Div([
        dcc.Dropdown(
            id='rates_dropdown',
            options=[{'label': x, 'value': x} for x in rates_dd_options],
            value = rates_dd_options[0]
        )])

    rates_plot = html.Div(id = 'rates_plot')

    return rates_dropdown, rates_plot

def plot_potential_dropdown(potential_dd_options):
    """
    Initializes the dropdown menu for yearly DR potential.

    Args:
        potential_dd_options: list of dropdowns for potential
    Returns:
        potential_dropdown: HTML division for dropdown menu
        potential_plot: HTML division for plot
    """
    potential_dropdown = html.Div([
        dcc.Dropdown(
            id='potential_dropdown',
            options=[{'label': x, 'value': x} for x in potential_dd_options],
            value = potential_dd_options[0]
        )])

    potential_plot = html.Div(id = 'potential_plot')

    return potential_dropdown, potential_plot

def plot_rates_dropdown_moreinfo(rates_dd_options_moreinfo):
    """
    Initializes the dropdown menu for hourly emissions rates.
    For the more information page.

    Args:
        rates_dd_options_moreinfo: list of dropdowns for emissions rates
    Returns:
        rates_dropdown_moreinfo: HTML division for dropdown menu
        rates_plot_moreinfo: HTML division for plot
    """
    rates_dropdown_moreinfo = html.Div([
        dcc.Dropdown(
            id='rates_dropdown_moreinfo',
            options=[{'label': x, 'value': x} for x in rates_dd_options_moreinfo],
            value = rates_dd_options_moreinfo[0]
        )])

    rates_plot_moreinfo = html.Div(id = 'rates_plot_moreinfo')

    return rates_dropdown_moreinfo, rates_plot_moreinfo

def plot_impacts_dropdown(impacts_dd_options):
    """
    Initializes the dropdown menu for yearly emissions reductions.

    Args:
        impacts_dd_options: list of dropdowns for emissions reductions
    Returns:
        impacts_dropdown: HTML division for dropdown menu
        impacts_plot: HTML division for plot
    """
    impacts_dropdown = html.Div([
        dcc.Dropdown(
            id='impacts_dropdown',
            options=[{'label': x, 'value': x} for x in impacts_dd_options],
            value = impacts_dd_options[0]
        )])

    impacts_plot = html.Div(id = 'impacts_plot')

    return impacts_dropdown, impacts_plot

def plot_total_impacts_dropdown(total_impacts_dd_options):
    """
    Initializes the dropdown menu for cumulative emissions reductions.

    Args:
        total_impacts_dd_options: list of dropdowns for emissions reductions
    Returns:
        total_impacts_dropdown: HTML division for dropdown menu
        total_impacts_plot: HTML division for plot
    """
    total_impacts_dropdown = html.Div([
        dcc.Dropdown(
            id='total_impacts_dropdown',
            options=[{'label': x, 'value': x} for x in total_impacts_dd_options],
            value = total_impacts_dd_options[0]
        )])

    total_impacts_plot = html.Div(id = 'total_impacts_plot')

    return total_impacts_dropdown, total_impacts_plot

# ================================================================================ #
# Callbacks
# ================================================================================ #

def rates_callback(rates, rates_dd_choice):
    """
    Plots hourly emissions rates based on user input.
    Used with @app.callback after setting up HTML layout.
    For the home page.

    Args:
        rates: dictionary of pandas dataframes of emissions rates
        rates_dd_choice: user input
    Returns:
        user-updated dash plot of emissions rates
    """
    rates_fig = go.Figure()
    if rates_dd_choice == 'Comparison':
        rates_fig.add_trace(go.Scatter(x=rates['Annual_Baseline']['Report_Hour'],
            y=rates['Annual_Baseline']['Baseline Emissions Rate Estimate'],
            name='All Year',marker=dict(color='black')))
        rates_fig.add_trace(go.Scatter(x=rates['Summer_Baseline']['Report_Hour'],
            y=rates['Summer_Baseline']['Baseline Emissions Rate Estimate'],
            name='Summer',marker=dict(color='red')))
        rates_fig.add_trace(go.Scatter(x=rates['Winter_Baseline']['Report_Hour'],
            y=rates['Winter_Baseline']['Baseline Emissions Rate Estimate'],
            name='Winter',marker=dict(color='blue')))
        rates_fig.add_trace(go.Scatter(x=rates['Fall_Baseline']['Report_Hour'],
            y=rates['Fall_Baseline']['Baseline Emissions Rate Estimate'],
            name='Fall',marker=dict(color='orange')))
        rates_fig.add_trace(go.Scatter(x=rates['Spring_Baseline']['Report_Hour'],
            y=rates['Spring_Baseline']['Baseline Emissions Rate Estimate'],
            name='Spring',marker=dict(color='pink')))
    elif rates_dd_choice == 'All Year':
        rates_fig.add_trace(go.Scatter(x=rates['Annual_Baseline']['Report_Hour'],
            y=rates['Annual_Baseline']['Baseline Emissions Rate Estimate'],
            name='All Year',marker=dict(color='black')))
    elif rates_dd_choice == 'Summer':
        rates_fig.add_trace(go.Scatter(x=rates['Summer_Baseline']['Report_Hour'],
            y=rates['Summer_Baseline']['Baseline Emissions Rate Estimate'],
            name='Summer',marker=dict(color='red')))
    elif rates_dd_choice == 'Winter':
        rates_fig.add_trace(go.Scatter(x=rates['Winter_Baseline']['Report_Hour'],
            y=rates['Winter_Baseline']['Baseline Emissions Rate Estimate'],
            name='Winter',marker=dict(color='blue')))
    elif rates_dd_choice == 'Fall':
        rates_fig.add_trace(go.Scatter(x=rates['Fall_Baseline']['Report_Hour'],
            y=rates['Fall_Baseline']['Baseline Emissions Rate Estimate'],
            name='Fall',marker=dict(color='orange')))
    elif rates_dd_choice == 'Spring':
        rates_fig.add_trace(go.Scatter(x=rates['Spring_Baseline']['Report_Hour'],
            y=rates['Spring_Baseline']['Baseline Emissions Rate Estimate'],
            name='Spring',marker=dict(color='pink')))

    rates_fig.update_layout(xaxis_title='Hour of the Day',
                            yaxis_title='Avoided Emissions Rate (lb CO2e/kWh)')

    return dcc.Graph(figure=rates_fig)

def potential_callback(potential, potential_dd_choice):
    """
    Plots yearly DR potential based on user input.
    Used with @app.callback after setting up HTML layout.

    Args:
        potential: dictionary of pandas dataframes of potential
        potential_dd_choice: user input
    Returns:
        user-updated dash plot of DR potential
    """
    potential_fig = go.Figure()
    if potential_dd_choice == 'New Bin 1, Winter':
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Winter_bin1']['Year'],
            y=potential['newbins_Winter_bin1']['DVR'], name='DVR',
            marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Winter_bin1']['Year'],
            y=potential['newbins_Winter_bin1']['ResTOU'], name='ResTOU',
            marker=dict(color='red')))
    elif potential_dd_choice == 'New Bin 1, Summer':
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Summer_bin1']['Year'],
            y=potential['newbins_Summer_bin1']['DVR'], name='DVR',
            marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Summer_bin1']['Year'],
            y=potential['newbins_Summer_bin1']['ResTOU'], name='ResTOU',
            marker=dict(color='red')))
    elif potential_dd_choice == 'New Bin 1, Fall':
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Fall_bin1']['Year'],
            y=potential['newbins_Fall_bin1']['DVR'], name='DVR',
            marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['newbins_Fall_bin1']['Year'],
            y=potential['newbins_Fall_bin1']['ResTOU'], name='ResTOU',
            marker=dict(color='red')))
    elif potential_dd_choice == 'Old Bin 1, Summer':
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin1']['Year'],
            y=potential['oldbins_Summer_bin1']['DVR'], name='DVR',
            marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin1']['Year'],
            y=potential['oldbins_Summer_bin1']['IndRTP'], name='InDRTP',
            marker=dict(color='red')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin1']['Year'],
            y=potential['oldbins_Summer_bin1']['ResCPP'], name='ResCPP',
            marker=dict(color='orange')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin1']['Year'],
            y=potential['oldbins_Summer_bin1']['ComCPP'], name='ComCPP',
            marker=dict(color='purple')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin1']['Year'],
            y=potential['oldbins_Summer_bin1']['IndCPP'], name='IndCPP',
            marker=dict(color='black')))
    elif potential_dd_choice == 'Old Bin 1, Winter':
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin1']['Year'],
            y=potential['oldbins_Winter_bin1']['DVR'], name='DVR',
            marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin1']['Year'],
            y=potential['oldbins_Winter_bin1']['IndRTP'], name='InDRTP',
            marker=dict(color='red')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin1']['Year'],
            y=potential['oldbins_Winter_bin1']['ResCPP'], name='ResCPP',
            marker=dict(color='orange')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin1']['Year'],
            y=potential['oldbins_Winter_bin1']['ComCPP'], name='ComCPP',
            marker=dict(color='purple')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin1']['Year'],
            y=potential['oldbins_Winter_bin1']['IndCPP'], name='IndCPP',
            marker=dict(color='black')))
    elif potential_dd_choice == 'Old Bin 2, Summer':
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin2']['Year'],
            y=potential['oldbins_Summer_bin2']['NRCurtailCom'],
            name='NRCurtailCom',marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin2']['Year'],
            y=potential['oldbins_Summer_bin2']['NRCurtailInd'],
            name='NRCurtailInd',marker=dict(color='red')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin2']['Year'],
            y=potential['oldbins_Summer_bin2']['ResTOU'], name='ResTOU',
            marker=dict(color='orange')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin2']['Year'],
            y=potential['oldbins_Summer_bin2']['NRCoolSwchMed'],
            name='NRCoolSwchMed',marker=dict(color='purple')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin2']['Year'],
            y=potential['oldbins_Summer_bin2']['ResBYOT'], name='ResBYOT',
            marker=dict(color='black')))
    elif potential_dd_choice == 'Old Bin 2, Winter':
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin2']['Year'],
            y=potential['oldbins_Winter_bin2']['NRCurtailCom'], name='NRCurtailCom',
            marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin2']['Year'],
            y=potential['oldbins_Winter_bin2']['NRCurtailInd'], name='NRCurtailInd',
            marker=dict(color='red')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin2']['Year'],
            y=potential['oldbins_Winter_bin2']['ResTOU'], name='ResTOU',marker=dict
            (color='orange')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin2']['Year'],
            y=potential['oldbins_Winter_bin2']['NRHeatSwchMed'], name='NRHeatSwchMed',
            marker=dict(color='purple')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin2']['Year'],
            y=potential['oldbins_Winter_bin2']['ResBYOT'], name='ResBYOT',
            marker=dict(color='black')))
    elif potential_dd_choice == 'Old Bin 3, Summer':
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin3']['Year'],
            y=potential['oldbins_Summer_bin3']['NRTstatSm'], name='NRTstatSm',
            marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin3']['Year'],
            y=potential['oldbins_Summer_bin3']['ResERWHDLCSwch'], name='ResERWHDLCSwch',
            marker=dict(color='red')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin3']['Year'],
            y=potential['oldbins_Summer_bin3']['ResERWHDLCGrd'], name='ResERWHDLCGrd',
            marker=dict(color='orange')))
    elif potential_dd_choice == 'Old Bin 3, Winter':
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin3']['Year'],
            y=potential['oldbins_Winter_bin3']['NRTstatSm'], name='NRTstatSm',
            marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin3']['Year'],
            y=potential['oldbins_Winter_bin3']['ResERWHDLCSwch'], name='ResERWHDLCSwch',
            marker=dict(color='red')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin3']['Year'],
            y=potential['oldbins_Winter_bin3']['ResERWHDLCGrd'], name='ResERWHDLCGrd',
            marker=dict(color='orange')))
    elif potential_dd_choice == 'Old Bin 4, Summer':
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin4']['Year'],
            y=potential['oldbins_Summer_bin4']['NRCoolSwchSm'], name='NRCoolSwchSm',
            marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin4']['Year'],
            y=potential['oldbins_Summer_bin4']['ResACSwch'], name='ResACSwch',
            marker=dict(color='red')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin4']['Year'],
            y=potential['oldbins_Summer_bin4']['ResEVSEDLCSwch'], name='ResEVSEDLCSwch',
            marker=dict(color='orange')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin4']['Year'],
            y=potential['oldbins_Summer_bin4']['ResHPWHDLCSwch'], name='ResHPWHDLCSwch',
            marker=dict(color='purple')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Summer_bin4']['Year'],
            y=potential['oldbins_Summer_bin4']['ResHPWHDLCGrd'], name='ResHPWHDLCGrd',
            marker=dict(color='black')))
    elif potential_dd_choice == 'Old Bin 4, Winter':
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin4']['Year'],
            y=potential['oldbins_Winter_bin4']['ResEVSEDLCSwch'], name='ResEVSEDLCSwch',
            marker=dict(color='blue')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin4']['Year'],
            y=potential['oldbins_Winter_bin4']['ResHPWHDLCSwch'], name='ResHPWHDLCSwch',
            marker=dict(color='red')))
        potential_fig.add_trace(go.Scatter(x=potential['oldbins_Winter_bin4']['Year'],
            y=potential['oldbins_Winter_bin4']['ResHPWHDLCGrd'], name='ResHPWHDLCGrd',
            marker=dict(color='orange')))

    potential_fig.update_layout(xaxis_title='Year', yaxis_title='DR Potential (MW)')

    return dcc.Graph(figure=potential_fig)

def rates_callback_moreinfo(rates, rates_dd_choice_moreinfo):
    """
    Plots hourly emissions rates based on user input.
    Used with @app.callback after setting up HTML layout.
    For the more information page.

    Args:
        rates: dictionary of pandas dataframes of emissions rates
        rates_dd_choice: user input
    Returns:
        user-updated dash plot of emissions rates
    """
    rates_fig_moreinfo = go.Figure()
    if rates_dd_choice_moreinfo == 'New Bins, Comparison':
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['newbins_Annual_Baseline']['Report_Hour'],
            y=rates['newbins_Annual_Baseline']['Baseline Emissions Rate Estimate'],
            name='All Year',marker=dict(color='black')))
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['newbins_Summer_Baseline']['Report_Hour'],
            y=rates['newbins_Summer_Baseline']['Baseline Emissions Rate Estimate'],
            name='Summer',marker=dict(color='red')))
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['newbins_Winter_Baseline']['Report_Hour'],
            y=rates['newbins_Winter_Baseline']['Baseline Emissions Rate Estimate'],
            name='Winter',marker=dict(color='blue')))
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['newbins_Fall_Baseline']['Report_Hour'],
            y=rates['newbins_Fall_Baseline']['Baseline Emissions Rate Estimate'],
            name='Fall',marker=dict(color='orange')))
    elif rates_dd_choice_moreinfo == 'New Bins, All Year':
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['newbins_Annual_Baseline']['Report_Hour'],
            y=rates['newbins_Annual_Baseline']['Baseline Emissions Rate Estimate'],
            name='All Year',marker=dict(color='black')))
    elif rates_dd_choice_moreinfo == 'New Bins, Summer':
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['newbins_Summer_Baseline']['Report_Hour'],
            y=rates['newbins_Summer_Baseline']['Baseline Emissions Rate Estimate'],
            name='Summer',marker=dict(color='red')))
    elif rates_dd_choice_moreinfo == 'New Bins, Winter':
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['newbins_Winter_Baseline']['Report_Hour'],
            y=rates['newbins_Winter_Baseline']['Baseline Emissions Rate Estimate'],
            name='Winter',marker=dict(color='blue')))
    elif rates_dd_choice_moreinfo == 'New Bins, Fall':
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['newbins_Fall_Baseline']['Report_Hour'],
            y=rates['newbins_Fall_Baseline']['Baseline Emissions Rate Estimate'],
            name='Fall',marker=dict(color='orange')))
    elif rates_dd_choice_moreinfo == 'Old Bins, Comparison':
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['oldbins_Annual_Baseline']['Report_Hour'],
            y=rates['oldbins_Annual_Baseline']['Baseline Emissions Rate Estimate'],
            name='All Year',marker=dict(color='black')))
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['oldbins_Summer_Baseline']['Report_Hour'],
            y=rates['oldbins_Summer_Baseline']['Baseline Emissions Rate Estimate'],
            name='Summer',marker=dict(color='red')))
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['oldbins_Winter_Baseline']['Report_Hour'],
            y=rates['oldbins_Winter_Baseline']['Baseline Emissions Rate Estimate'],
            name='Winter',marker=dict(color='blue')))
    elif rates_dd_choice_moreinfo == 'Old Bins, All Year':
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['oldbins_Annual_Baseline']['Report_Hour'],
            y=rates['oldbins_Annual_Baseline']['Baseline Emissions Rate Estimate'],
            name='All Year',marker=dict(color='black')))
    elif rates_dd_choice_moreinfo == 'Old Bins, Summer':
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['oldbins_Summer_Baseline']['Report_Hour'],
            y=rates['oldbins_Summer_Baseline']['Baseline Emissions Rate Estimate'],
            name='Summer',marker=dict(color='red')))
    elif rates_dd_choice_moreinfo == 'Old Bins, Winter':
        rates_fig_moreinfo.add_trace(go.Scatter(
            x=rates['oldbins_Winter_Baseline']['Report_Hour'],
            y=rates['oldbins_Winter_Baseline']['Baseline Emissions Rate Estimate'],
            name='Winter',marker=dict(color='blue')))

    rates_fig_moreinfo.update_layout(xaxis_title='Hour of the Day',
                                     yaxis_title='Avoided Emissions Rate (lb CO2e/kWh)')

    return dcc.Graph(figure=rates_fig_moreinfo)

def impacts_callback(impacts, impacts_dd_choice):
    """
    Plots yearly emissions reductions based on user input.
    Used with @app.callback after setting up HTML layout.

    Args:
        impacts: dictionary of pandas dataframes of emissions reductions
        impacts_dd_choice: user input
    Returns:
        user-updated dash plot of emissions reductions
    """
    impacts_fig = go.Figure()
    if impacts_dd_choice == 'New Bin 1, Winter':
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Winter_bin1']['Year'],
            y=impacts['newbins_Winter_bin1']['DVR'], name='DVR',
            marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Winter_bin1']['Year'],
            y=impacts['newbins_Winter_bin1']['ResTOU_shed'], name='ResTOU Shed',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Winter_bin1']['Year'],
            y=impacts['newbins_Winter_bin1']['ResTOU_shift'], name='ResTOU Shift',
            marker=dict(color='orange')))
    elif impacts_dd_choice == 'New Bin 1, Summer':
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Summer_bin1']['Year'],
            y=impacts['newbins_Summer_bin1']['DVR'], name='DVR',
            marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Summer_bin1']['Year'],
            y=impacts['newbins_Summer_bin1']['ResTOU_shed'], name='ResTOU Shed',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Summer_bin1']['Year'],
            y=impacts['newbins_Summer_bin1']['ResTOU_shift'], name='ResTOU Shift',
            marker=dict(color='orange')))
    elif impacts_dd_choice == 'New Bin 1, Fall':
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Fall_bin1']['Year'],
            y=impacts['newbins_Fall_bin1']['DVR'], name='DVR',marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Fall_bin1']['Year'],
            y=impacts['newbins_Fall_bin1']['ResTOU_shed'], name='ResTOU Shed',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['newbins_Fall_bin1']['Year'],
            y=impacts['newbins_Fall_bin1']['ResTOU_shift'], name='ResTOU Shift',
            marker=dict(color='orange')))
    elif impacts_dd_choice == 'Old Bin 1, Summer':
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin1']['Year'],
            y=impacts['oldbins_Summer_bin1']['DVR'], name='DVR',
            marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin1']['Year'],
            y=impacts['oldbins_Summer_bin1']['IndRTP'], name='InDRTP',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin1']['Year'],
            y=impacts['oldbins_Summer_bin1']['ResCPP'], name='ResCPP',
            marker=dict(color='orange')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin1']['Year'],
            y=impacts['oldbins_Summer_bin1']['ComCPP'], name='ComCPP',
            marker=dict(color='purple')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin1']['Year'],
            y=impacts['oldbins_Summer_bin1']['IndCPP'], name='IndCPP',
            marker=dict(color='black')))
    elif impacts_dd_choice == 'Old Bin 1, Winter':
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin1']['Year'],
            y=impacts['oldbins_Winter_bin1']['DVR'], name='DVR',
            marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin1']['Year'],
            y=impacts['oldbins_Winter_bin1']['IndRTP'], name='InDRTP',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin1']['Year'],
            y=impacts['oldbins_Winter_bin1']['ResCPP'], name='ResCPP',
            marker=dict(color='orange')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin1']['Year'],
            y=impacts['oldbins_Winter_bin1']['ComCPP'], name='ComCPP',
            marker=dict(color='purple')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin1']['Year'],
            y=impacts['oldbins_Winter_bin1']['IndCPP'], name='IndCPP',
            marker=dict(color='black')))
    elif impacts_dd_choice == 'Old Bin 2, Summer':
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin2']['Year'],
            y=impacts['oldbins_Summer_bin2']['NRCurtailCom'], name='NRCurtailCom',
            marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin2']['Year'],
            y=impacts['oldbins_Summer_bin2']['NRCurtailInd'], name='NRCurtailInd',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin2']['Year'],
            y=impacts['oldbins_Summer_bin2']['ResTOU'], name='ResTOU',
            marker=dict(color='orange')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin2']['Year'],
            y=impacts['oldbins_Summer_bin2']['NRCoolSwchMed'], name='NRCoolSwchMed',
            marker=dict(color='purple')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin2']['Year'],
            y=impacts['oldbins_Summer_bin2']['ResBYOT'], name='ResBYOT',
            marker=dict(color='black')))
    elif impacts_dd_choice == 'Old Bin 2, Winter':
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin2']['Year'],
            y=impacts['oldbins_Winter_bin2']['NRCurtailCom'], name='NRCurtailCom',
            marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin2']['Year'],
            y=impacts['oldbins_Winter_bin2']['NRCurtailInd'], name='NRCurtailInd',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin2']['Year'],
            y=impacts['oldbins_Winter_bin2']['ResTOU'], name='ResTOU',
            marker=dict(color='orange')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin2']['Year'],
            y=impacts['oldbins_Winter_bin2']['NRHeatSwchMed'], name='NRHeatSwchMed',
            marker=dict(color='purple')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin2']['Year'],
            y=impacts['oldbins_Winter_bin2']['ResBYOT'], name='ResBYOT',
            marker=dict(color='black')))
    elif impacts_dd_choice == 'Old Bin 3, Summer':
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin3']['Year'],
            y=impacts['oldbins_Summer_bin3']['NRTstatSm'], name='NRTstatSm',
            marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin3']['Year'],
            y=impacts['oldbins_Summer_bin3']['ResERWHDLCSwch'], name='ResERWHDLCSwch',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin3']['Year'],
            y=impacts['oldbins_Summer_bin3']['ResERWHDLCGrd'], name='ResERWHDLCGrd',
            marker=dict(color='orange')))
    elif impacts_dd_choice == 'Old Bin 3, Winter':
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin3']['Year'],
            y=impacts['oldbins_Winter_bin3']['NRTstatSm'], name='NRTstatSm',
            marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin3']['Year'],
            y=impacts['oldbins_Winter_bin3']['ResERWHDLCSwch'], name='ResERWHDLCSwch',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin3']['Year'],
            y=impacts['oldbins_Winter_bin3']['ResERWHDLCGrd'], name='ResERWHDLCGrd',
            marker=dict(color='orange')))
    elif impacts_dd_choice == 'Old Bin 4, Summer':
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin4']['Year'],
            y=impacts['oldbins_Summer_bin4']['NRCoolSwchSm'], name='NRCoolSwchSm',
            marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin4']['Year'],
            y=impacts['oldbins_Summer_bin4']['ResACSwch'], name='ResACSwch',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin4']['Year'],
            y=impacts['oldbins_Summer_bin4']['ResEVSEDLCSwch'], name='ResEVSEDLCSwch',
            marker=dict(color='orange')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin4']['Year'],
            y=impacts['oldbins_Summer_bin4']['ResHPWHDLCSwch'], name='ResHPWHDLCSwch',
            marker=dict(color='purple')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Summer_bin4']['Year'],
            y=impacts['oldbins_Summer_bin4']['ResHPWHDLCGrd'], name='ResHPWHDLCGrd',
            marker=dict(color='black')))
    elif impacts_dd_choice == 'Old Bin 4, Winter':
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin4']['Year'],
            y=impacts['oldbins_Winter_bin4']['ResEVSEDLCSwch'], name='ResEVSEDLCSwch',
            marker=dict(color='blue')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin4']['Year'],
            y=impacts['oldbins_Winter_bin4']['ResHPWHDLCSwch'], name='ResHPWHDLCSwch',
            marker=dict(color='red')))
        impacts_fig.add_trace(go.Scatter(x=impacts['oldbins_Winter_bin4']['Year'],
            y=impacts['oldbins_Winter_bin4']['ResHPWHDLCGrd'], name='ResHPWHDLCGrd',
            marker=dict(color='orange')))

    impacts_fig.update_layout(xaxis_title='Year',
                              yaxis_title='Metric Tons of CO2 Reduced')

    return dcc.Graph(figure=impacts_fig)

def total_impacts_callback(total_impacts, total_impacts_dd_choice):
    """
    Plots bar chart of total emissions reductions based on user input.
    Used with @app.callback after setting up HTML layout.

    Args:
        total_impacts: dictionary of pandas dataframes of emissions reductions
        total_impacts_dd_choice: user input
    Returns:
        user-updated dash bar chart of emissions reductions
    """
    if total_impacts_dd_choice == 'New and Old Bins':
        total_impacts_fig = go.Figure(data=[go.Bar(
            name = 'Winter',
            x = ['New Bin 1 Shed','New Bin 1 Shift','Old Bin 1','Old Bin 2',
                'Old Bin 3', 'Old Bin 4'],
            y = [total_impacts['barchart'].at[0, 'newbins_bin1_shed'],
                total_impacts['barchart'].at[0, 'newbins_bin1_shift'],
                total_impacts['barchart'].at[0, 'oldbins_bin1'],
                total_impacts['barchart'].at[0, 'oldbins_bin2'],
                total_impacts['barchart'].at[0, 'oldbins_bin3'],
                total_impacts['barchart'].at[0, 'oldbins_bin4']
                ]
            ),
            go.Bar(
            name = 'Summer',
            x = ['New Bin 1 Shed','New Bin 1 Shift','Old Bin 1','Old Bin 2',
                'Old Bin 3', 'Old Bin 4'],
            y = [total_impacts['barchart'].at[1, 'newbins_bin1_shed'],
                total_impacts['barchart'].at[1, 'newbins_bin1_shift'],
                total_impacts['barchart'].at[1, 'oldbins_bin1'],
                total_impacts['barchart'].at[1, 'oldbins_bin2'],
                total_impacts['barchart'].at[1, 'oldbins_bin3'],
                total_impacts['barchart'].at[1, 'oldbins_bin4']
                ]
            ),
            go.Bar(
            name = 'Fall',
            x = ['New Bin 1 Shed','New Bin 1 Shift','Old Bin 1','Old Bin 2',
                'Old Bin 3', 'Old Bin 4'],
            y = [total_impacts['barchart'].at[2, 'newbins_bin1_shed'],
                total_impacts['barchart'].at[2, 'newbins_bin1_shift'],
                total_impacts['barchart'].at[2, 'oldbins_bin1'],
                total_impacts['barchart'].at[2, 'oldbins_bin2'],
                total_impacts['barchart'].at[2, 'oldbins_bin3'],
                total_impacts['barchart'].at[2, 'oldbins_bin4']
                ]
            )
        ])
    elif total_impacts_dd_choice == 'Old Bins Only':
        total_impacts_fig = go.Figure(data=[go.Bar(
            name = 'Winter',
            x = ['Old Bin 1','Old Bin 2', 'Old Bin 3', 'Old Bin 4'],
            y = [
                total_impacts['barchart'].at[0, 'oldbins_bin1'],
                total_impacts['barchart'].at[0, 'oldbins_bin2'],
                total_impacts['barchart'].at[0, 'oldbins_bin3'],
                total_impacts['barchart'].at[0, 'oldbins_bin4']
                ]
            ),
            go.Bar(
            name = 'Summer',
            x = ['Old Bin 1','Old Bin 2', 'Old Bin 3', 'Old Bin 4'],
            y = [
                total_impacts['barchart'].at[1, 'oldbins_bin1'],
                total_impacts['barchart'].at[1, 'oldbins_bin2'],
                total_impacts['barchart'].at[1, 'oldbins_bin3'],
                total_impacts['barchart'].at[1, 'oldbins_bin4']
                ]
            )
        ])

    total_impacts_fig.update_layout(
        yaxis_title = 'Metric Tons of CO2 Reduced')

    return dcc.Graph(figure=total_impacts_fig)

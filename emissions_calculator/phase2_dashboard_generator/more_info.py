"""
more_info.py

Dashboard layout for the more information page. Calls on read_files and make_plots.
Requires app to be imported to make plotting callbacks for dropdown.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app
from .read_files import get_impacts, get_rates_drdays, get_potential
from .make_plots import plot_potential_bar, plot_potential_dropdown, \
    plot_hours_table, plot_rates_dropdown_moreinfo, plot_impacts_bar_moreinfo, \
    plot_impacts_dropdown, potential_callback, rates_callback_moreinfo, \
    impacts_callback

# Define the parameters
URL = 'https://github.com/NW-Demand-Response-Emissions-Impacts/'+ \
    'emissions_calculator/blob/main/data/processed_data'
seasons_rates = ['Annual','Fall','Winter','Summer']
seasons_impacts = ['Fall','Winter','Summer']
seasons_potential = ['Fall','Winter','Summer']
scenarios = ['Baseline']
bin_types = ['newbins','oldbins']
bin_numbers_impacts = ['Bin_1','Bin_2','Bin_3','Bin_4']
bin_numbers_potential = ['bin1','bin2','bin3','bin4']
rates_dd_options_moreinfo = ['All Year','Fall','Winter','Summer','Comparison']
impacts_dd_options = ['Summer', 'Winter', 'Fall']

# Read in the data
impacts = get_impacts(URL, bin_types, bin_numbers_impacts, seasons_impacts)
rates_moreinfo = get_rates_drdays(URL, bin_types, seasons_rates, scenarios)
potential = get_potential(URL, bin_types, seasons_potential, bin_numbers_potential)

# Make the plots
potential_dropdown, potential_plot = plot_potential_dropdown(seasons_potential)
potential_bar = plot_potential_bar(potential)
hours_table = plot_hours_table(potential)
rates_dropdown_moreinfo, rates_plot_moreinfo = \
    plot_rates_dropdown_moreinfo(rates_dd_options_moreinfo)
impacts_bar_moreinfo = plot_impacts_bar_moreinfo(impacts)
impacts_dropdown, impacts_plot = plot_impacts_dropdown(seasons_potential)

# Set up the HTML layout
layout = html.Div(children=[
    html.H1('Emissions Impacts of Demand Response Programs',
        style={"textAlign": "center"}),
    html.Div(className='row',
             children=[
                 html.Div(className='four columns div-user-controls',
                          children=[html.H2('More Information'),
                                html.P("""The figures on this page offer more
                                    detail into how DR programs impact emissions in
                                    the northwestern US."""
                                ),
                                html.P("""Want to learn more about the data?
                                    All figures in this dashboard are based on
                                    projections of marginal emissions factors for
                                    2022 by the Northwest Power and Conservation
                                    Council. They indicate the emissions benefit of
                                    avoiding one kilowatt-hour of electricity
                                    within the WECC region (Western Electricity
                                    Coordinating Council). Visit our GitHub page to
                                    learn more about how the data is analyzed.
                                    Learn more about avoided emissions factors here.
                                    """
                                )]),
                 html.Div(className='eight columns div-for-charts bg-grey-more',
                          children=[
                                html.H3('Emissions reductions from 2022 to 2041',
                                    style={"textAlign": "center"}
                                ),
                                html.P("""Use the dropdown menu to compare
                                    different seasons!"""
                                ),
                                impacts_dropdown, impacts_plot,
                                html.H3('Emissions impacts bar chart',style=
                                    {"textAlign": "center"}
                                ),
                                html.P("""Which bin leads to the most significant
                                    emissions reduction?"""
                                ),
                                dcc.Graph(id='impacts_bar_moreinfo',
                                    figure=impacts_bar_moreinfo
                                ),
                                html.H3('Emissions rates',style={"textAlign":
                                    "center"}
                                ),
                                html.P("""The plot on the home page shows the
                                    emissions rates for all days of the year. What
                                    about only on days in which DR programs are
                                    implemented? Use the dropdown menu below to
                                    compare these plots for different seasons."""
                                ),
                                rates_dropdown_moreinfo, rates_plot_moreinfo,
                                html.H3("""Table of hours in which DR programs
                                    where implemented""",style={"textAlign":
                                    "center"}
                                ),
                                html.P('Use this table for reference!'),
                                dcc.Graph(id='hours_table', figure=hours_table),
                                html.H3('DR potential',style={"textAlign": "center"}),
                                html.P('DR potential from 2022 to 2041'),
                                potential_dropdown, potential_plot,
                                html.H3('DR potential in 2041',style={"textAlign":
                                    "center"}
                                ),
                                html.P("""Compare different seasons and binning
                                    strategies!"""
                                ),
                                dcc.Graph(id='potential_bar', figure=potential_bar)
                            ])
             ])
    ])

# Use callbacks to make the plots
@app.callback(
dash.dependencies.Output('potential_plot', 'children'),
[dash.dependencies.Input('potential_dropdown', 'value')])
def update_potential(potential_dd_choice):
    """
    Updates the potential plot using dropdown menu

    Args:
        potential: dictionary of pandas dataframes of DR potential
        potential_dd_choice: user's dropdown selection
    Returns:
        dash graph of DR potential
    """
    return potential_callback(potential, potential_dd_choice)

@app.callback(
dash.dependencies.Output('rates_plot_moreinfo', 'children'),
[dash.dependencies.Input('rates_dropdown_moreinfo', 'value')])
def update_rates_moreinfo(rates_dd_choice_moreinfo):
    """
    Updates the emissions rates plot using dropdown

    Args:
        rates_moreinfo: dictionary of pandas dataframes of emissions rates
        rates_dd_choice: user's dropdown selection
    Returns:
        dash graph of emissions rates
    """
    return rates_callback_moreinfo(rates_moreinfo, rates_dd_choice_moreinfo)

@app.callback(
dash.dependencies.Output('impacts_plot', 'children'),
[dash.dependencies.Input('impacts_dropdown', 'value')])
def update_impacts(impacts_dd_choice):
    """
    Updates the emissions impacts plot using dropdown menu

    Args:
        impacts: dictionary of pandas dataframes of emissions impacts
        impacts_dd_choice: user's dropdown selection
    Returns:
        dash graph of emissions impacts
    """
    return impacts_callback(impacts, impacts_dd_choice)

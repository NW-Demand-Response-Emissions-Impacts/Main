"""
home.py

Dashboard layout for the home page. Calls on read_files and make_plots.
Requires app to be imported to make plotting callbacks for dropdown.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app
from .read_files import get_impacts, get_rates_alldays
from .make_plots import plot_impacts_bar, plot_rates_dropdown, rates_callback


# Define the parameters
URL = 'https://github.com/NW-Demand-Response-Emissions-Impacts/'+ \
    'emissions_calculator/blob/main/data/processed_data'
seasons_rates = ['Annual','Fall','Winter','Spring','Summer']
seasons_impacts = ['Fall','Winter','Summer']
scenarios = ['Baseline']
bin_types = ['newbins','oldbins']
bin_numbers = ['Bin_1','Bin_2','Bin_3','Bin_4']
rates_dd_options = ['All Year','Fall','Winter','Spring','Summer','Comparison']

# Read in the data
impacts = get_impacts(URL, bin_types, bin_numbers, seasons_impacts)
rates = get_rates_alldays(URL, seasons_rates, scenarios)

# Make the plots
impacts_bar = plot_impacts_bar(impacts)
rates_dropdown, rates_plot = plot_rates_dropdown(rates_dd_options)

# Set up the HTML layout
layout = html.Div(children=[
    html.H1('Emissions Impacts of Demand Response Programs',style={"textAlign":
        "center"}),
    html.Div(className='row',
             children=[
                 html.Div(className='four columns div-user-controls',
                          children=[html.H2('Home Page'),
                                html.P("""This dashboard displays how demand
                                    response (DR) programs impact on carbon dioxide
                                    emissions in the northwestern United States."""
                                ),
                                html.P("""DR strategies reduce or shift electricity
                                    usage during periods of peak demand. There are
                                    many different ways to do this, including
                                    Demand Voltage Reduction (DVR) and Residential
                                    Time of Use (ResTOU)."""
                                ),
                                html.P("""DVR allows utilities to reduce voltage
                                    during periods of peak demand, which can reduce
                                    resistive energy losses and lead to energy
                                    savings."""
                                ),
                                html.P("""ResTOU programs offer lower electricity
                                    prices during times of day when the demand for
                                    electricity is low, and higher prices when the
                                    demand for electricity is high. This encourages
                                    residents to reduce or shift their electricity
                                    usage away from peak demand hours. “ResTOU -
                                    shed” assumes that consumers reduce their net
                                    electricity consumption, while “ResTOU - shift”
                                    assumes that consumers shift their electricity
                                    consumption to the hours adjacent to the period
                                    of peak demand."""
                                )]),
                 html.Div(className='eight columns div-for-charts bg-grey-home',
                          children=[
                                html.H3('Emissions reductions',style={"textAlign":
                                    "center"}
                                ),
                                html.P("""This bar chart shows the total estimated
                                    emissions reductions due to DR programs from
                                    2022 to 2041."""
                                ),
                                html.P("""Emissions reductions are shown for the
                                    fall, winter, and summer, seasons. Reductions
                                    are also separated into contributions from DVR
                                    and ResTOU programs."""
                                ),
                                html.P("""DVR programs are projected to have the
                                    most significant impact on emissions. ResTOU
                                    programs are projected to be most impactful
                                    during the summer."""
                                ),
                                dcc.Graph(id='impacts_bar', figure=impacts_bar),
                                html.H3('Emissions rates',style={"textAlign":
                                    "center"}
                                ),
                                html.P("""How much could you reduce carbon dioxide
                                    emissions by using less electricity? Well, that
                                    depends on when you reduce your electricity
                                    usage! Electricity is cleanest during daylight
                                    hours, while emissions rates are higher in the
                                    early morning and evening. Reducing electricity
                                    usage in the early morning and evening will
                                    have the biggest impact on reducing
                                    emissions!"""
                                ),
                                html.P("""The plot below shows the avoided
                                    emissions factors during different hours of the
                                    day. This indicates how much emissions would be
                                    reduced by avoiding one kilowatt-hour of
                                    electricity. Use the dropdown menu to compare
                                    seasons!"""
                                ),
                                rates_dropdown, rates_plot
                            ])
             ])
    ])

# Use callback to make plots with dropdown
@app.callback(
dash.dependencies.Output('rates_plot', 'children'),
[dash.dependencies.Input('rates_dropdown', 'value')])
def update_rates(rates_dd_choice):
    """
    Updates the emissions rates plot using dropdown menu.

    Args:
        rates: dictionary of pandas dataframes of emissions rates
        rates_dd_choice: user's dropdown selection
    Returns:
        dash graph of emissions rates
    """
    return rates_callback(rates, rates_dd_choice)

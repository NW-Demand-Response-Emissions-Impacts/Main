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

# Dropdown options
rates_dd_options_moreinfo = ['New Bins, All Year','New Bins, Fall',
                            'New Bins, Winter','New Bins, Summer',
                            'New Bins, Comparison', 'Old Bins, All Year',
                            'Old Bins, Winter','Old Bins, Summer',
                            'Old Bins, Comparison']
impacts_dd_options = ['New Bin 1, Summer', 'New Bin 1, Winter', 'New Bin 1, Fall',
                      'Old Bin 1, Summer', 'Old Bin 1, Winter',
                      'Old Bin 2, Summer', 'Old Bin 2, Winter',
                      'Old Bin 3, Summer', 'Old Bin 3, Winter',
                      'Old Bin 4, Summer', 'Old Bin 4, Winter']
potential_dd_options = impacts_dd_options

# Read in the data
impacts = get_impacts(URL, bin_types, bin_numbers_impacts, seasons_impacts)
rates_moreinfo = get_rates_drdays(URL, bin_types, seasons_rates, scenarios)
potential = get_potential(URL, bin_types, seasons_potential, bin_numbers_potential)

# Make the plots
potential_dropdown, potential_plot = plot_potential_dropdown(potential_dd_options)
potential_bar = plot_potential_bar(potential)
hours_table = plot_hours_table(potential)
rates_dropdown_moreinfo, rates_plot_moreinfo = \
    plot_rates_dropdown_moreinfo(rates_dd_options_moreinfo)
impacts_bar_moreinfo = plot_impacts_bar_moreinfo(impacts)
impacts_dropdown, impacts_plot = plot_impacts_dropdown(impacts_dd_options)

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
                                    the Northwest U.S."""
                                ),
                                html.H3('Learn More About the Data'),
                                html.P("""All figures in this dashboard are based on
                                    projections of DR potential, hours of
                                    implementation, and marginal emissions factors
                                    for 2022-2041 by the Northwest Power and
                                    Conservation Council. Marginal emissions factors
                                    include the emissions benefit of
                                    avoiding one kilowatt-hour of electricity
                                    within the WECC region (Western Electricity
                                    Coordinating Council)."""
                                ),
                                html.H3('Links to Learn More'),
                                html.Div([
                                dcc.Link('Project GitHub Page', 
                                    href='https://github.com/'+
                                    'NW-Demand-Response-Emissions-Impacts', 
                                    style={'font-size':'18px', 'textAlign':
                                    'right', 'text-decoration':'underline'}
                                )],className='row'),
                                html.Div([
                                dcc.Link('Details on Avoided Emissions Factors', 
                                    href='https://www.nwcouncil.org/reports/'+
                                    'avoided-carbon-dioxide-production-rates'+
                                    '-northwest-power-system',
                                    style={'font-size':'18px', 'textAlign':
                                    'right', 'text-decoration':'underline'}
                                )], className='row')
                                ]),
                 html.Div(className='eight columns div-for-charts bg-grey-more',
                          children=[
                                html.H3('Emissions Reductions From 2022 to 2041',
                                    style={"textAlign": "center"}
                                ),
                                html.P("""Use the dropdown menu to compare
                                    different seasons and DR plans!"""
                                ),
                                impacts_dropdown, impacts_plot,
                                html.H3('Cumulative Emissions Reductions',style=
                                    {"textAlign": "center"}
                                ),
                                html.P("""Which bin leads to the most significant
                                    emissions reduction?"""
                                ),
                                dcc.Graph(id='impacts_bar_moreinfo',
                                    figure=impacts_bar_moreinfo
                                ),
                                html.H3('Emissions Rates',style={"textAlign":
                                    "center"}
                                ),
                                html.P("""The plot on the home page shows the
                                    emissions rates for all days of the year in
                                    2022. What about only on days in which DR
                                    programs are implemented? The figure below shows 
                                    the hourly emissions rates for days with DR 
                                    implemented, averaged over the full period from
                                    2022-2041. Note that the emissions rates 
                                    generally decline over time from 2022-2041 (not 
                                    shown). Use the dropdown menu below to compare 
                                    these plots for different DR plans and seasons.
                                    """
                                ),
                                rates_dropdown_moreinfo, rates_plot_moreinfo,
                                html.H3("""DR Hours of Implementation""",
                                    style={"textAlign":"center"}
                                ),
                                html.P("""For the DR plan “oldbins,” DR products 
                                were implemented for 18-20 hours total each season, 
                                with individual DR events during periods of peak 
                                electricity demand. The periods of implementation 
                                differed for Direct Load Control (DLC) products and 
                                non-DLC products as shown below. For the DR plan 
                                “newbins,” the DR products were implemented for 288 
                                hours each season except for spring, always during 
                                the same evening hours."""),
                                html.P("""Comparing these hours with the hourly 
                                emissions rates above illustrates that demand 
                                response is not necessarily implemented during 
                                periods with peak emissions. As a result, the 
                                emissions reductions from DR products that shed load 
                                is only a fraction of the maximum possible emissions 
                                reductions for demand response in the northwestern 
                                US. When demand response is implemented during times 
                                with low emissions rates, products that shift the 
                                load to adjacent hours with higher emissions rates 
                                can actually increase emissions."""
                                ),
                                dcc.Graph(id='hours_table', figure=hours_table),
                                html.H3('DR Potential From 2022 to 2041',
                                    style={"textAlign": "center"}),
                                html.P("""DR potential generally ramps up from 2022 
                                    to 2041. Use the dropdown to explore different 
                                    DR plans, bins of products, and seasons."""),
                                potential_dropdown, potential_plot,
                                html.H3('DR Potential in 2041',style={"textAlign":
                                    "center"}
                                ),
                                html.P("""Compare different DR plans, seasons, and
                                    bins of products!"""
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

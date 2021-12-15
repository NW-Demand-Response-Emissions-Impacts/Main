"""
home.py

Reads in csv files output by the Emissions Calculator.
"""

import pandas as pd


def get_impacts(url, bin_types, seasons, bin_numbers):
    """
    Reads processed csv files containing emissions impacts

    The if/else statements in this function are specific to the default dashboard.
    When uploading new files, check this function to make sure files are being
    read in properly.

    Args:
        url: the GitHub url containing the processed data
        bin_types: list of names of DR binning strategies
        bin_numbers: list of bin numbers
        seasons: list of seasons

    Returns:
        impacts: dictionary of impacts dataframes
    """
    impacts = {}
    impacts['barchart'] = pd.read_csv(url + \
        '/emissions_impacts/emissions_reductions_barchart.csv?raw=True')
    impacts['newbins_barchart'] = pd.read_csv(url + \
        '/emissions_impacts/newbins_barchart.csv?raw=True')
    for name in bin_types:
        for season in seasons:
            for num in bin_numbers:
                if (name == 'newbins' and num != 'bin1') \
                    or (name == 'oldbins' and season == 'Fall'):
                    pass
                else:
                    impacts[name + '_' + season + '_' + num] = \
                        pd.read_csv(url + '/emissions_impacts/' + name + '_' + \
                            season + '_' + num + '.csv?raw=True')

    return impacts

def get_rates_drdays(url, bin_types, seasons, scenarios):
    """
    Reads processed csv files containing emissions rates
    for DR days only.

    The if/else statements in this function are specific to the default dashboard.
    When uploading new files, check this function to make sure files are being
    read in properly.

    Args:
        url: the GitHub url containing the processed data
        bin_types: list of names of DR binning strategies
        seasons: list of seasons
        scenarios: list of emissions scenarios

    Returns:
        rates: dictionary of emissions rates dataframes
    """
    rates = {}
    for name in bin_types:
        for season in seasons:
            for scenario in scenarios:
                if (name == 'oldbins' and season == 'Fall'):
                    pass
                else:
                    rates[name + '_' + season + '_' + scenario] = \
                        pd.read_csv(url + '/emissions_rates/DRdays_allyears_' + \
                        name + '_' + season + '_' + scenario + \
                        '.csv?raw=True')

    return rates

def get_rates_alldays(url, seasons, scenarios):
    """
    Reads processed csv files containing emissions rates
    for all days

    Args:
        url: the GitHub url containing the processed data
        seasons: list of seasons
        scenarios: list of emissions scenarios

    Returns:
        impacts: dictionary of emissions rates dataframes
    """
    rates = {}
    for season in seasons:
        for scenario in scenarios:
            rates[season + '_' + scenario] = pd.read_csv(url + \
                '/emissions_rates/alldays_2022_' + season + '_' + scenario + \
                '.csv?raw=True')

    return rates

def get_potential(url, bin_types, seasons, bin_numbers):
    """
    Reads processed csv files containing DR potential

    The if/else statements in this function are specific to the default dashboard.
    When uploading new files, check this function to make sure files are being
    read in properly.

    Args:
        url: the GitHub url containing the processed data
        bin_types: list of names of DR binning strategies
        seasons: list of seasons
        bin_numbers: list of bin numbers

    Returns:
        potential: dictionary of potential dataframes
    """
    potential = {}
    potential['comparison_barchart'] = pd.read_csv(url + \
        '/dr_potential/comparison_barchart.csv?raw=True')
    potential['dr_hours'] = pd.read_csv(url+'/dr_hours/output_dr_hours.csv?raw=True')
    for name in bin_types:
        for season in seasons:
            for num in bin_numbers:
                if (name == 'newbins' and num != 'bin1') \
                    or (name == 'oldbins' and season == 'Fall'):
                    pass
                else:
                    potential[name + '_' + season + '_' + num] = \
                        pd.read_csv(url + '/dr_potential/' + name + '_' + season + \
                        '_' + num + '.csv?raw=True')

    return potential

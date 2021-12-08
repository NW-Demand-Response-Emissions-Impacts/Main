"""
subcomp_b_process_emissions_factors.py

Read output emissions rates and DR hours from subcomponent a.

For all DR plans (e.g. old bins, new bins),
return seasonal and annual emissions rates averages
only for days with DR, averaged 2022-2041.

Also return seasonal and annual emissions rates averages
for all days in a given year (e.g. 2022),
which will be shown on the general public page.
"""

import pandas as pd

from emissions_parameters import SEASONS_ALLDAYS


def seasonal_ave(dr_name, dr_seasons, emissions_scenario_list,
                 emissions_rates_df_out, dr_hours_df_dict_out):
    """
    Compute seasonal averages of hourly emissions for DR days
    for each DR plan and season and each emissions scenario.

    Args:
        dr_name: list of the names of each DR plan (str)
        dr_seasons: array containing a list of seasons (str) with DR hours
                    for each DR plan
        emissions_scenario_list: list of policy scenarios (str)
                                 with emissions rates files
        emissions_rates_df_out: the emissions rates dataframe
        dr_hours_df_dict_out: dictionary of DR hours dataframes

    Returns:
        df_seasonal_ave: dictionary of seasonal emissions rates averages

    Access output by:
        df_seasonal_ave=seasonal_ave()
    Output example:
        df_seasonal_ave['oldbins_Winter']['Baseline']
    """
    df_seasonal_ave = {}
    for idx, drname in enumerate(dr_name):

        drname = dr_name[idx]
        seasons = dr_seasons[idx]

        for season in seasons:
            dict_key = drname + '_' + season
            df_seasonal_ave[dict_key] = {}

            for scenario_name in emissions_scenario_list:

                column_name = scenario_name + ' Emissions Rate Estimate'
                df_seasonal_ave[dict_key][scenario_name] = get_hour_ave(emissions_rates_df_out,
                                                                        dr_hours_df_dict_out[dict_key], column_name)

    return df_seasonal_ave


def annual_ave(dr_name, dr_seasons, emissions_scenario_list,
               emissions_rates_df_out, dr_hours_df_dict_out):
    """
    Compute annual averages of hourly emissions for DR days
    for each DR plan and each emissions scenario.

    Args:
        dr_name: list of the names of each DR plan (str)
        dr_seasons: array containing a list of seasons (str) with DR hours
                    for each DR plan
        emissions_scenario_list: list of policy scenarios (str)
                                 with emissions rates files
        emissions_rates_df_out: the emissions rates dataframe
        dr_hours_df_dict_out: dictionary of DR hours dataframes

    Returns:
    df_annual_ave: a dictionary of annual emissions rates averages

    Access output by:
    df_annual_ave=annual_ave()

    Output example:
    df_annual_ave['oldbins']['Baseline']
    """
    df_annual_ave = {}

    for idx, drname in enumerate(dr_name):

        drname = dr_name[idx]
        seasons = dr_seasons[idx]
        df_annual_ave[drname] = {}

        # bin_season_name distinguish old/new bins, winter/summer/fall
        bin_season_name = []

        for season in seasons:
            dict_key = drname + '_' + season
            bin_season_name.append(dict_key)

        # For old bins, combine winter & summer
        # For new bins, combine winter, summer & fall
        frames = [dr_hours_df_dict_out[x] for x in bin_season_name]
        dr_hours_df = pd.concat(frames)

        for scenario_name in emissions_scenario_list:
            column_name = scenario_name + ' Emissions Rate Estimate'
            df_annual_ave[drname][scenario_name] = \
                get_hour_ave(emissions_rates_df_out, dr_hours_df, column_name)

    return df_annual_ave


def get_hour_ave(emissions_data, dr_hours, column_name):

    """
    Select DR hour days and return hourly average emissions rates.

    Called in seasonal_ave(), annual_ave()

    Args:
        emissions_data: dataframe with hourly emissions rates
        dr_hours: dataframe with hours of DR implementation
        column_name: name (str) of emissions rates column in emissions_data
    Returns:
        hourly average emissions rates for DR days
    """
    df_cp = emissions_data

    # Group by month and day
    # Sum product column
    # Select (sum>=1), got DR days!
    df_1 = dr_hours.groupby(['Month', 'Day'])['DVR'].sum().reset_index()
    df_1 = df_1[df_1['DVR'] >= 1]

    # Combine month and day together
    df_1['month_day'] = df_1['Month']*100 + df_1['Day']
    df_cp['month_day'] = df_cp['Report_Month']*100 + df_cp['Report_Day']

    # Select DR days in emission rates dataset
    df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]

    # Compute daily average
    return df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()


def alldays_oneyear_seasonal_ave(emissions_scenario_list,
                                 emissions_rates_df_out, year):
    """
    Compute seasonal and annual emissions rates averages
    for all days for one year.

    Args:
        emissions_scenario_list: list of policy scenarios (str)
                                 with emissions rates files
        emissions_rates_df_out: the emissions rates dataframe
        year: the year (int) to average emissions rates over
    Returns:
        df_oneyear_seasonal_ave: dictionary of average emissions rates
                                 for each season and emissions scenario

    Access output by:
    df_oneyear_seasonal_ave=alldays_oneyear_seasonal_ave()

    Output example:
    df_oneyear_seasonal_ave['Winter']['Baseline']
    """
    df_oneyear_seasonal_ave = {}

    for season in SEASONS_ALLDAYS:
        df_oneyear_seasonal_ave[season] = {}

        for scenario_name in emissions_scenario_list:
            column_name = scenario_name + ' Emissions Rate Estimate'
            df_oneyear_seasonal_ave[season][scenario_name] = \
                get_oneyear_hour_ave(emissions_rates_df_out, season, column_name, year)

    return df_oneyear_seasonal_ave


def get_oneyear_hour_ave(emissions_data, season, column_name, year):
    """
    Select all days according to season (including all seasons)
    and return hourly average emissions rates.

    Called in alldays_oneyear_seasonal_ave()

    Args:
        emissions_data: dataframe with hourly emissions rates
        season: season (str) to calculate average over
        column_name: name (str) of emissions rates column in emissions_data
        year: year (int) to calculate average over
    Returns:
        hourly average emissions rates for the given season
    """
    df_cp = emissions_data

    # Month range for different seasons are defined as follows:
    if season == 'Winter':
        month = [1, 2, 3]
    elif season == 'Spring':
        month = [4, 5, 6]
    elif season == 'Summer':
        month = [7, 8, 9]
    elif season == 'Fall':
        month = [10, 11, 12]
    elif season == 'Annual':
        month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    else:
        raise ValueError('Time period unavailable!')

    df_2 = df_cp[df_cp['Report_Month'].isin(month)]
    df_2 = df_2[df_2['Report_Year'] == year]

    return df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()


def subcomp_b_runall(dr_name, dr_seasons, emissions_scenario_list,
                     emissions_rates_df_out, dr_hours_df_dict_out, year):
    """
    Runs through all of the above functions.
    Args:
        dr_name: list of the names of each DR plan (str)
        dr_seasons: array containing a list of seasons (str) with DR hours
                    for each DR plan
        emissions_scenario_list: list of policy scenarios (str)
                                 with emissions rates files
        emissions_rates_df_out: the emissions rates dataframe
        dr_hours_df_dict_out: dictionary of DR hours dataframes
        year: year (int) to output emissions rates averages for all days
              for general info page of dashboard
    Returns:
        df_seasonal_ave: dictionary of seasonally averaged hourly emissions rates
                        for days with DR averaged over full period (2022-2041)
        df_annual_ave: dictionary of annually averaged hourly emissions rates
                        for days with DR averaged over full period (2022-2041)
        df_oneyear_seasonal_ave: dictionary of seasonally, annually averaged hourly
                        emissions rates for all days of a given year
    """
    df_seasonal_ave = seasonal_ave(dr_name, dr_seasons, emissions_scenario_list,
                                   emissions_rates_df_out, dr_hours_df_dict_out)
    df_annual_ave = annual_ave(dr_name, dr_seasons, emissions_scenario_list,
                               emissions_rates_df_out, dr_hours_df_dict_out)
    df_oneyear_seasonal_ave = alldays_oneyear_seasonal_ave(emissions_scenario_list,
                                                           emissions_rates_df_out, year)

    return df_seasonal_ave, df_annual_ave, df_oneyear_seasonal_ave

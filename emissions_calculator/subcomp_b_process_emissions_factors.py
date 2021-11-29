"""
subcomp_b_process_emissions_factors.py

Read output files from sub component a

Return seasonal emissions rates averages for old and new bins,
annual emissions rates averages for old and new bins,
new bin annual emissions rates average of year 2022,
and new bin seasonal emissions rates average of year 2022,
"""

import pandas as pd

from subcomp_a_organize_data import create_emissions_rates_df, create_dr_hours_df_dict

from emissions_parameters import EMISSIONS_SCENARIO_LIST, DR_NAME, DR_SEASONS

EMISSIONS_RATES_DF_OUT = create_emissions_rates_df()
DR_HOURS_DF_DICT_OUT = create_dr_hours_df_dict()


def seasonal_ave():
    """
    Compute seasonal emissions rates averages for old and new bins,

    Access output by:
    df_seasonal_ave=seasonal_ave()

    Output example:
    df_seasonal_ave['oldbins_Winter']['Baseline']
    """
    df_seasonal_ave = {}
    for idx, dr_name in enumerate(DR_NAME):

        dr_name = DR_NAME[idx]
        seasons = DR_SEASONS[idx]

        for season in seasons:
            dict_key = dr_name + '_' + season
            season_ave_key = dict_key + '_ave'
            df_seasonal_ave[season_ave_key] = {}

            for idx_1, scenario_name in enumerate(EMISSIONS_SCENARIO_LIST):

                column_name = scenario_name + ' Emissions Rate Estimate'

                if idx_1 == 0:
                    data = EMISSIONS_RATES_DF_OUT
                    df_seasonal_ave[season_ave_key][scenario_name] = \
                        get_hour_ave(data, DR_HOURS_DF_DICT_OUT[dict_key], column_name)

                else:
                    pass

    return df_seasonal_ave


def annual_ave():
    """
    Compute annual emissions rates averages for old and new bins,

    Access output by:
    df_annual_ave=annual_ave()

    Output example:
    df_annual_ave['oldbins']['Baseline']
    """
    df_annual_ave = {}

    for idx, dr_name in enumerate(DR_NAME):

        dr_name = DR_NAME[idx]
        seasons = DR_SEASONS[idx]
        df_annual_ave[dr_name] = {}

        # bin_season_name distinguish old/new bins, winter/summer/fall
        bin_season_name = []

        for season in seasons:
            dict_key = dr_name + '_' + season
            bin_season_name.append(dict_key)

            # For old bins, combine winter & summer
            # For new bins, combine winter, summer & fall
            frames = [DR_HOURS_DF_DICT_OUT[x] for x in bin_season_name]
            dr_hours_df = pd.concat(frames)

            for idx_1, scenario_name in enumerate(EMISSIONS_SCENARIO_LIST):
                column_name = scenario_name + ' Emissions Rate Estimate'

                if idx_1 == 0:
                    data = EMISSIONS_RATES_DF_OUT

                    df_annual_ave[dr_name][scenario_name] = \
                        get_hour_ave(data, dr_hours_df, column_name)

                else:
                    pass

    return df_annual_ave


def get_hour_ave(data, time_df, column_name):
    """
    Select DR hour days and return hourly average

    Called in seasonal_ave(), annual_ave()
    """
    df_cp = data

    # Group by month and day
    # Sum product column
    # Select (sum>=1), got DR days!
    df_1 = time_df.groupby(['Month', 'Day'])['DVR'].sum().reset_index()
    df_1 = df_1[df_1['DVR'] >= 1]

    # Combine month and day together
    df_1['month_day'] = df_1['Month']*100+df_1['Day']
    df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

    # Select DR days in emission rates dataset
    df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]

    # Compute daily average
    return df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()


def get_2022_hour_ave(data, time, column_name):
    """
    Select days according to season(including all seasons) and return hourly average

    Called in newbins_2022_annual_ave(), newbins_2022_seasonal_ave()
    """
    df_cp = data

    if time == 'Winter':
        month = [1, 2, 3]
    # Spring season average currently unavailable!
    # elif time == 'Spring':
        # month = [4, 5, 6]
    elif time == 'Summer':
        month = [7, 8, 9]
    elif time == 'Fall':
        month = [10, 11, 12]
    elif time == 'Annual':
        month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    else:
        raise ValueError('Time period unavailable!')

    df_2 = df_cp[df_cp['Report_Month'].isin(month)]
    df_2 = df_2[df_2['Report_Year'] == 2022]

    return df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()


def newbins_2022_annual_ave():
    """
    Compute annual emissions rates averages for new bins, year 2022

    Access output by:
    df_2022_annual_ave=newbins_2022_annual_ave()

    Output example:
    df_2022_annual_ave['Baseline']
    """
    df_2022_annual_ave = {}

    for idx, scenario_name in enumerate(EMISSIONS_SCENARIO_LIST):
        column_name = scenario_name + ' Emissions Rate Estimate'

        if idx == 0:
            data = EMISSIONS_RATES_DF_OUT
            df_2022_annual_ave[scenario_name] = get_2022_hour_ave(data, 'Annual', column_name)

        else:
            pass

    return df_2022_annual_ave


def newbins_2022_seasonal_ave():
    """
    Compute seasonal emissions rates averages for new bins, year 2022

    Access output by:
    df_2022_seasonal_ave=newbins_2022_seasonal_ave()

    Output example:
    df_2022_seasonal_ave['Winter']['Baseline']
    """
    df_2022_seasonal_ave = {}

    for season in DR_SEASONS[1]:
        # DR_SEASONS[1] iterate over winter, summer and fall seasons for new bin
        df_2022_seasonal_ave[season] = {}

        for idx, scenario_name in enumerate(EMISSIONS_SCENARIO_LIST):
            column_name = scenario_name + ' Emissions Rate Estimate'

            if idx == 0:
                data = EMISSIONS_RATES_DF_OUT
                df_2022_seasonal_ave[season][scenario_name] = \
                    get_2022_hour_ave(data, season, column_name)

            else:
                pass

    return df_2022_seasonal_ave


def run_all():
    """
    Runs through all of the above functions.
    """
    df_seasonal_ave = seasonal_ave()
    df_annual_ave = annual_ave()
    df_newbins_2022_annual_ave = newbins_2022_annual_ave()
    df_newbins_2022_seasonal_ave = newbins_2022_seasonal_ave()

    return df_seasonal_ave, df_annual_ave, df_newbins_2022_annual_ave, df_newbins_2022_seasonal_ave

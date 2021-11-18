import pandas as pd
import numpy as np

from subcomp_a_organize_data import create_emissions_rates_df, create_DR_hours_df_dict,\
    create_DR_potential_df_dict, create_product_info_df, runall

from emissions_parameters import DIR_EMISSIONS_RATES, \
    DIR_DR_POTENTIAL_HRS, EMISSIONS_SCENARIO_LIST, EMISSIONS_RATES_FILES, \
    DR_NAME, DR_HRS_FILES, DR_POTENTIAL_FILES, SUBSET_PRODUCTS, DR_SEASONS

emissions_rates_df_out, DR_hours_df_dict_out, DR_potential_df_dict_out, DR_product_info_df_dict_out = runall()


def old_bins_winter():

    """
     For DR_hours_df_dict_out['']
     Group by month, day,sum DVR/ResTOU column
     Select (sum>=1), got DR days!
    """

    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['oldbins_Winter'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp = data
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass
    
    return df_3


def old_bins_summer():

    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['oldbins_Summer'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp = data
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass

    return df_3


def new_bins_winter():

    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['newbins_Winter'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp = data
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass

    return df_3


def new_bins_summer():

    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['newbins_Summer'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp = data
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass

    return df_3


def new_bins_fall():

    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['newbins_Fall'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp = data
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass

    return df_3


def runall_b():

    oldbins_winter = old_bins_winter()
    oldbins_summer = old_bins_summer()
    newbins_winter = new_bins_winter()
    newbins_summer = new_bins_summer()
    newbins_fall = new_bins_fall()

    return oldbins_winter, oldbins_summer, newbins_winter, newbins_summer, newbins_fall

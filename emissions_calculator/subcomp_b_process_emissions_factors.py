import pandas as pd
import numpy as np

from subcomp_a_organize_data import create_emissions_rates_df, create_DR_hours_df_dict,\
    create_DR_potential_df_dict, create_product_info_df, runall

from emissions_parameters import DIR_EMISSIONS_RATES, \
    DIR_DR_POTENTIAL_HRS, EMISSIONS_SCENARIO_LIST, EMISSIONS_RATES_FILES, \
    DR_NAME, DR_HRS_FILES, DR_POTENTIAL_FILES, SUBSET_PRODUCTS, DR_SEASONS

emissions_rates_df_out, DR_hours_df_dict_out, DR_potential_df_dict_out, DR_product_info_df_dict_out = runall()

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def old_bins_winter():

    """
     For DR_hours_df_dict_out['']
     Group by month, day,sum DVR/ResTOU column
     Select (sum>=1), got DR days!
    """

    df_2 = {}

    "Get days with DR hours"
    df_1 = DR_hours_df_dict_out['oldbins_Winter'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
    df_1 = df_1[df_1['DVR'] >= 1]

    "Get same, former and latter days with DR hours and put into list"
    days = []
    months = []
    former_days = []
    former_months = []
    latter_days = []
    latter_months = []

    for row in df_1.iterrows():
        month = row[1]['Month']
        day = row[1]['Day']
        days.append(day)
        months.append(month)

        if day-1 > 0:
            former_day = day-1
            former_month = month
        else:
            former_day = days_in_month[month-2]
            former_month = month-1

        if day+1 <= days_in_month[month-1]:
            latter_day = day+1
            latter_month = month
        else:
            latter_day = 1
            latter_month = month+1

        former_days.append(former_day)
        former_months.append(former_month)
        latter_days.append(latter_day)
        latter_months.append(latter_month)

    former_month_day = []
    latter_month_day = []
    dr_month_day = []
    for (month, day) in zip(former_months, former_days):
        former_month_day.append(month*100+day)
    for (month, day) in zip(latter_months, latter_days):
        latter_month_day.append(month*100+day)
    for (month, day) in zip(months, days):
        dr_month_day.append(month*100+day)

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out
            df_cp = data

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_same = df_cp[df_cp['month_day'].isin(dr_month_day)]
            df_former = df_cp[(df_cp['Report_Hour'] >= 12) & (df_cp['month_day'].isin(former_month_day))]
            df_latter = df_cp[(df_cp['Report_Hour'] <= 12) & (df_cp['month_day'].isin(latter_month_day))]

            df_same['new_hourID'] = df_same['Report_Hour']
            df_former['new_hourID'] = df_former['Report_Hour'] - 24
            df_latter['new_hourID'] = df_latter['Report_Hour'] + 24

            frames = [df_same, df_former, df_latter]

            df_all = pd.concat(frames)

            "Compute daily average"
            df_2[idx] = df_all.groupby(['new_hourID'])[column_name].mean().reset_index()

        else:
            pass

    return df_2


def old_bins_summer():

    df_2 = {}

    "Get days with DR hours"
    df_1 = DR_hours_df_dict_out['oldbins_Summer'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
    df_1 = df_1[df_1['DVR'] >= 1]

    "Get same, former and latter days with DR hours and put into list"
    days = []
    months = []
    former_days = []
    former_months = []
    latter_days = []
    latter_months = []

    for row in df_1.iterrows():
        month = row[1]['Month']
        day = row[1]['Day']
        days.append(day)
        months.append(month)

        if day-1 > 0:
            former_day = day-1
            former_month = month
        else:
            former_day = days_in_month[month-2]
            former_month = month-1

        if day+1 <= days_in_month[month-1]:
            latter_day = day+1
            latter_month = month
        else:
            latter_day = 1
            latter_month = month+1

        former_days.append(former_day)
        former_months.append(former_month)
        latter_days.append(latter_day)
        latter_months.append(latter_month)

    former_month_day = []
    latter_month_day = []
    dr_month_day = []
    for (month, day) in zip(former_months, former_days):
        former_month_day.append(month*100+day)
    for (month, day) in zip(latter_months, latter_days):
        latter_month_day.append(month*100+day)
    for (month, day) in zip(months, days):
        dr_month_day.append(month*100+day)

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out
            df_cp = data

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_same = df_cp[df_cp['month_day'].isin(dr_month_day)]
            df_former = df_cp[(df_cp['Report_Hour'] >= 12) & (df_cp['month_day'].isin(former_month_day))]
            df_latter = df_cp[(df_cp['Report_Hour'] <= 12) & (df_cp['month_day'].isin(latter_month_day))]

            df_same['new_hourID'] = df_same['Report_Hour']
            df_former['new_hourID'] = df_former['Report_Hour'] - 24
            df_latter['new_hourID'] = df_latter['Report_Hour'] + 24

            frames = [df_same, df_former, df_latter]

            df_all = pd.concat(frames)

            "Compute daily average"
            df_2[idx] = df_all.groupby(['new_hourID'])[column_name].mean().reset_index()

        else:
            pass

    return df_2


def oldbins_all_year():
    df_2 = {}

    "Get days with DR hours"
    df_temp_winter = \
        DR_hours_df_dict_out['oldbins_Winter'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
    df_temp_winter = df_temp_winter[df_temp_winter['DVR'] >= 1]
    df_temp_summer = \
        DR_hours_df_dict_out['oldbins_Summer'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
    df_temp_summer = df_temp_summer[df_temp_summer['DVR'] >= 1]
    # df_temp_winter['season'] = 'winter'
    # df_temp_summer['season'] = 'summer'
    frames = [df_temp_winter, df_temp_summer]
    df_1 = pd.concat(frames)

    "Get same, former and latter days with DR hours and put into list"
    days = []
    months = []
    former_days = []
    former_months = []
    latter_days = []
    latter_months = []

    for row in df_1.iterrows():
        month = row[1]['Month']
        day = row[1]['Day']
        days.append(day)
        months.append(month)

        if day-1 > 0:
            former_day = day-1
            former_month = month
        else:
            former_day = days_in_month[month-2]
            former_month = month-1

        if day+1 <= days_in_month[month-1]:
            latter_day = day+1
            latter_month = month
        else:
            latter_day = 1
            latter_month = month+1

        former_days.append(former_day)
        former_months.append(former_month)
        latter_days.append(latter_day)
        latter_months.append(latter_month)

    former_month_day = []
    latter_month_day = []
    dr_month_day = []
    for (month, day) in zip(former_months, former_days):
        former_month_day.append(month*100+day)
    for (month, day) in zip(latter_months, latter_days):
        latter_month_day.append(month*100+day)
    for (month, day) in zip(months, days):
        dr_month_day.append(month*100+day)

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out
            df_cp = data

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_same = df_cp[df_cp['month_day'].isin(dr_month_day)]
            df_former = df_cp[(df_cp['Report_Hour'] >= 12) & (df_cp['month_day'].isin(former_month_day))]
            df_latter = df_cp[(df_cp['Report_Hour'] <= 12) & (df_cp['month_day'].isin(latter_month_day))]

            df_same['new_hourID'] = df_same['Report_Hour']
            df_former['new_hourID'] = df_former['Report_Hour'] - 24
            df_latter['new_hourID'] = df_latter['Report_Hour'] + 24

            frames = [df_same, df_former, df_latter]

            df_all = pd.concat(frames)

            "Compute daily average"
            df_2[idx] = df_all.groupby(['new_hourID'])[column_name].mean().reset_index()

        else:
            pass

    return df_2


def new_bins_winter():

    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out
            df_cp = data

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['newbins_Winter'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
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
            df_cp = data

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['newbins_Summer'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
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
            df_cp = data

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['newbins_Fall'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass

    return df_3


def newbins_all_year():
    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):
        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out
            df_cp = data

            "Get days with DR hours"
            df_temp_winter = \
                DR_hours_df_dict_out['newbins_Winter'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_temp_winter = df_temp_winter[df_temp_winter['DVR'] >= 1]
            df_temp_summer = \
                DR_hours_df_dict_out['newbins_Summer'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_temp_summer = df_temp_summer[df_temp_summer['DVR'] >= 1]
            df_temp_fall = \
                DR_hours_df_dict_out['newbins_Fall'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_temp_fall = df_temp_fall[df_temp_fall['DVR'] >= 1]
            # df_temp_winter['season'] = 'winter'
            # df_temp_summer['season'] = 'summer'
            # df_temp_fall['season'] = 'fall'
            frames = [df_temp_winter, df_temp_summer, df_temp_fall]
            df_1 = pd.concat(frames)

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass

    return df_3


def newbins_2022_allyear():
    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):
        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out
            df_cp = data

            "Get days with DR hours"
            df_temp_winter = \
                DR_hours_df_dict_out['newbins_Winter'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_temp_winter = df_temp_winter[df_temp_winter['DVR'] >= 1]
            df_temp_summer = \
                DR_hours_df_dict_out['newbins_Summer'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_temp_summer = df_temp_summer[df_temp_summer['DVR'] >= 1]
            df_temp_fall = \
                DR_hours_df_dict_out['newbins_Fall'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_temp_fall = df_temp_fall[df_temp_fall['DVR'] >= 1]
            # df_temp_winter['season'] = 'winter'
            # df_temp_summer['season'] = 'summer'
            # df_temp_fall['season'] = 'fall'
            frames = [df_temp_winter, df_temp_summer, df_temp_fall]
            df_1 = pd.concat(frames)

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]
            df_2 = df_2[df_2['Report_Year'] == 2022]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass

    return df_3


def newbins_2022_winter():
    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):
        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out
            df_cp = data

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['newbins_Winter'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]
            # df_1['season'] = 'winter'

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]
            df_2 = df_2[df_2['Report_Year'] == 2022]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass

    return df_3


def newbins_2022_summer():
    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):
        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out
            df_cp = data

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['newbins_Summer'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]
            # df_1['season'] = 'summer'

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]
            df_2 = df_2[df_2['Report_Year'] == 2022]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass

    return df_3


def newbins_2022_fall():
    df_3 = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):
        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out
            df_cp = data

            "Get days with DR hours"
            df_1 = DR_hours_df_dict_out['newbins_Fall'].groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
            df_1 = df_1[df_1['DVR'] >= 1]
            # df_1['season'] = 'fall'

            "Combine month and day together"
            df_1['month_day'] = df_1['Month']*100+df_1['Day']
            df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

            "Select DR days in emission rates dataset"
            df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]
            df_2 = df_2[df_2['Report_Year'] == 2022]

            "Compute daily average"
            df_3[idx] = df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()

        else:
            pass

    return df_3


def newbins_2022():
    df_2022_winter = newbins_2022_winter()
    df_2022_summer = newbins_2022_summer()
    df_2022_fall = newbins_2022_fall()
    df_2022_allyear = newbins_2022_allyear()
    return df_2022_winter, df_2022_summer, df_2022_fall, df_2022_allyear


def runall_seasonal():

    oldbins_winter = old_bins_winter()
    oldbins_summer = old_bins_summer()
    newbins_winter = new_bins_winter()
    newbins_summer = new_bins_summer()
    newbins_fall = new_bins_fall()

    return oldbins_winter, oldbins_summer, newbins_winter, newbins_summer, newbins_fall


def runall_allyear():

    oldbins_allyear = oldbins_all_year()
    newbins_allyear = newbins_all_year()

    return oldbins_allyear, newbins_allyear

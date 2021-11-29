import pandas as pd

from subcomp_a_organize_data import create_emissions_rates_df, create_dr_hours_df_dict

from emissions_parameters import EMISSIONS_SCENARIO_LIST, EMISSIONS_RATES_FILES, DAYS_IN_MONTH

emissions_rates_df_out = create_emissions_rates_df()
DR_hours_df_dict_out = create_dr_hours_df_dict()


# This part output results for old bins
def old_bins_winter():

    df_ave = {}

    former_month_day, dr_month_day, latter_month_day = \
        get_former_same_latter_day(DR_hours_df_dict_out['oldbins_Winter'])

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Compute daily average"
            df_ave[idx] = get_new_hour_id_ave(data, former_month_day, dr_month_day, latter_month_day, column_name)

        else:
            pass

    return df_ave


def old_bins_summer():

    df_ave = {}

    former_month_day, dr_month_day, latter_month_day = \
        get_former_same_latter_day(DR_hours_df_dict_out['oldbins_Summer'])

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Compute daily average"
            df_ave[idx] = get_new_hour_id_ave(data, former_month_day, dr_month_day, latter_month_day, column_name)

        else:
            pass

    return df_ave


def oldbins_all_year():

    df_ave = {}

    frames = [DR_hours_df_dict_out['oldbins_Winter'], DR_hours_df_dict_out['oldbins_Summer']]
    dr_hours_df = pd.concat(frames)

    former_month_day, dr_month_day, latter_month_day = get_former_same_latter_day(dr_hours_df)

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Compute daily average"
            df_ave[idx] = get_new_hour_id_ave(data, former_month_day, dr_month_day, latter_month_day, column_name)

        else:
            pass

    return df_ave


# Get days with DR hours
##### delete this function, just use get_hour_ave for all bins
def get_former_same_latter_day(time_df):

    """
     For DR_hours_df_dict_out['']
     Group by month, day,sum DVR/ResTOU column
     Select (sum>=1), got DR days!
    """

    df_1 = time_df.groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
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
            former_day = DAYS_IN_MONTH[month-2]
            former_month = month-1

        if day+1 <= DAYS_IN_MONTH[month-1]:
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

    return former_month_day, dr_month_day, latter_month_day


# Get hourly average by new hour ID
##### delete this function, just use get_hour_ave for all bins
def get_new_hour_id_ave(data, former_month_day, dr_month_day, latter_month_day, column_name):
    df_cp = data

    "Combine month and day together"
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
    return df_all.groupby(['new_hourID'])[column_name].mean().reset_index()


# This part output results for new bins


def get_hour_ave(data, time_df, column_name):
    df_cp = data

    "Get days with DR hours"
##### below, why do you grab both DVR and ResTOU? Think you can just grab DVR:
##### df_1 = time_df.groupby(['Month', 'Day'])['DVR'].sum().reset_index()
    df_1 = time_df.groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
    df_1 = df_1[df_1['DVR'] >= 1]

    "Combine month and day together"
    df_1['month_day'] = df_1['Month']*100+df_1['Day']
    df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

    "Select DR days in emission rates dataset"
    df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]

    "Compute daily average"
    return df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()


def get_2022_hour_ave(data, time_df, column_name):
    df_cp = data

    "Get days with DR hours"
    df_1 = time_df.groupby(['Month', 'Day'])['DVR', 'ResTOU'].sum().reset_index()
    df_1 = df_1[df_1['DVR'] >= 1]
#####for 2022, I'd like to actually grab all days, not just DR days. 
#####the goal is to show the general public emissions factors for all days
    "Combine month and day together"
    df_1['month_day'] = df_1['Month']*100+df_1['Day']
    df_cp['month_day'] = df_cp['Report_Month'] * 100 + df_cp['Report_Day']

    "Select DR days in emission rates dataset"
    df_2 = df_cp[df_cp['month_day'].isin(df_1['month_day'])]
    df_2 = df_2[df_2['Report_Year'] == 2022]

    "Compute daily average"
    return df_2.groupby(['Report_Hour'])[column_name].mean().reset_index()


def new_bins_winter():
#####make a function that looks like new_bins_winter, but has as it's argument dict_key,
#####this will be used for old and new bins, for all seasons
    df_ave = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Compute daily average"
            df_ave[idx] = get_hour_ave(data, DR_hours_df_dict_out['newbins_Winter'], column_name)
#####       df_ave[idx] = get_hour_ave(data, DR_hours_df_dict_out[dict_key], column_name)
        else:
            pass

    return df_ave


def new_bins_summer():

    df_ave = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Compute daily average"
            df_ave[idx] = get_hour_ave(data, DR_hours_df_dict_out['newbins_Summer'], column_name)

        else:
            pass

    return df_ave


def new_bins_fall():

    df_ave = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):

        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Compute daily average"
            df_ave[idx] = get_hour_ave(data, DR_hours_df_dict_out['newbins_Fall'], column_name)

        else:
            pass

    return df_ave

#####if possible, create an allyear function that can be used for both the old and new bins
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

##### try to combine the newbins_2022 functions for the seasons all together 
##### with the argument (dict_key) that will specify the newbins_season 
def newbins_2022_winter():
    df_2022_ave = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):
        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Compute daily average"
            df_2022_ave[idx] = get_2022_hour_ave(data, DR_hours_df_dict_out['newbins_Winter'], column_name)

        else:
            pass

    return df_2022_ave


def newbins_2022_summer():
    df_2022_ave = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):
        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Compute daily average"
            df_2022_ave[idx] = get_2022_hour_ave(data, DR_hours_df_dict_out['newbins_Summer'], column_name)

        else:
            pass

    return df_2022_ave


def newbins_2022_fall():
    df_2022_ave = {}

    for idx, file_name in enumerate(EMISSIONS_RATES_FILES):
        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'

        if idx == 0:
            data = emissions_rates_df_out

            "Compute daily average"
            df_2022_ave[idx] = get_2022_hour_ave(data, DR_hours_df_dict_out['newbins_Fall'], column_name)

        else:
            pass

    return df_2022_ave


def newbins_2022():
    df_2022_winter = newbins_2022_winter()
    df_2022_summer = newbins_2022_summer()
    df_2022_fall = newbins_2022_fall()
    df_2022_allyear = newbins_2022_allyear()
    return df_2022_winter, df_2022_summer, df_2022_fall, df_2022_allyear


def runall_seasonal():

#####suggest combining all five functions below into one function (called average_emissions_rates below),
#####then within runall_seasonal, you can loop through: 
#   emissionsrates_avg = {}
#   for idx, drname in enumerate(DR_NAME):
#       seasons = DR_SEASONS[idx]
#       for season in seasons:
#           dict_key = drname + '_' + season
#           emissionsrates_avg[dict_key] = average_emissions_rates(dict_key)
##### you can just use the get_hour_ave function for both the old and new bins

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

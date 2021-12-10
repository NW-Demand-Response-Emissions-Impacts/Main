"""
subcomp_c_calculate_emissions.py

Reads emissions rates, DR hours, DR potential, and DR product info
from subcomponent a.

Calculates emissions impacts (metric tons CO2e/MWh) as the product of
(a) DR potential (MW) for a given season; 
(b) DR implementation hours (1, 0, or -1; h) for each hour 
in the season, where 1 indicates a load reduction, -1 indicates 
a load increase (due to shifting load), and 0 indicates no DR; 
(c) marginal emissions rates (lbs CO2e/kWh); and 
(d) a unit conversion factor (kWh/MWh)*(metric tons CO2e/lb).

Positive values indicate emissions savings, while negative values
indicate an emissions increase, which can occur if DR shifts the load
to more emission-intensive hours.

We assume that for DR shift products, the load is shifted to adjacent
hours before and after the DR implementation period. For ResTOU
(Residential Time-of-Use), we calculate emissions impacts that would
occur if this were a shed product, and also if this were a shift 
product, as DR pilot studies suggest it can be both. 
"""

import pandas as pd
import numpy as np
from emissions_parameters import EMISSIONS_CHANGEUNITS


def shift_hours(dr_hours, hours_to_shift):
    """
    Outputs an updated dr_hours dataframe that adds -1 values to hours
    in which the load has increased due to a DR shift product. 
    (DR shift products shift load from the time of DR implementation
    to the adjacent hours.)

    Args:
        dr_hours: Dataframe of the hours for a DR plan, season, product

        hours_to_shift: Number of hours by which to shift on either
            side of original hours. (E.g. if shift_hours = 2 and
            dr is implemented 18-21, then hours 16-17 and 22-23 will
            have -1 vals.

    Returns:
        dr_hours_out: dataframe containing hours with DR implemented 
                      to reduce load (+1 value), hours with no DR (0 value)
                      and hours with increased load due to a load shift by DR
                      (-1 value)
    """

    # Get first index in set of 4
    indices_shift = dr_hours.loc[dr_hours==1].index
    firsts = np.array([])
    first = True
    ind_prev = 0
    for ind in indices_shift:
        if first:
            firsts = np.append(firsts, np.array([np.floor(ind)]))
            first = False
            ind_prev = ind
        else:
            first = bool(ind-ind_prev > 1)
            ind_prev = ind
    firsts = firsts.astype(int)

    # Specify indices_shift to insert -1 values for load shift
    # This is where the bug is:
    # need to shift to the two hours before and two hours after
    # needs to also work for a product with six hour period, so maybe you count the consecutive 1s (4 or 6), divide by two, and shift by that much
    shift_inds_down_2 = firsts - hours_to_shift
    shift_inds_down_1 = firsts - (hours_to_shift-1)
    shift_inds_up_1 = firsts + (hours_to_shift-1)
    shift_inds_up_2 = firsts + hours_to_shift
    indices_shift = np.append(shift_inds_down_2,shift_inds_down_1)
    indices_shift = np.append(indices_shift,shift_inds_up_1)
    indices_shift = np.append(indices_shift,shift_inds_up_2)

    # Insert -1 values and output new dr_hours 
    dr_product_shifted = dr_hours.copy()
    dr_product_shifted.loc[indices_shift] = -1
    dr_hours_out = dr_product_shifted.values

    return dr_hours_out


def sort_bins(dr_info, dr_names):
    """
    Args:
        dr_info: DR product information dataframe for a given DR plan
        dr_names: list of DR products (str) for a given DR plan, season 

    Returns:
        out_dict: dictionary with bin number as keys and DR product names
                  as values, for a given DR plan and season.
    """
    out_dict = {}

    for dr_name in dr_names:
        bin_name = dr_info.Bin.loc[dr_info.Product == dr_name].values[0]
        if bin_name in list(out_dict.keys()):
            out_dict[bin_name] = out_dict[bin_name]+[dr_name]
        else:
            out_dict[bin_name] = [dr_name]

    return out_dict


def calc_yearly_avoided_emissions(em_rates, dr_hours, dr_potential, dr_product_info):
    """

    This function uses emissions rates, DR hours, DR potential, 
    and DR product information data to calculate avoided emissions
    each year. It outputs a dictionary of dataframes with emissions 
    impacts for each DR plan, bin, and season. 

    Args:
        em_rates: baseline emissions rates
        dr_hours: 
        dr_potential:
        dr_product_info
        
    Returns:
        output_dictionary: Dictionary containing keys such as ['newbins_Bin_1_summer'], 
                            or ['oldbins_Bin_3_winter']. Each entry contains a dataframe
                            of avoided annual avoided emissions for each DR product
                            in that binning+season combination.
    """

    output_dictionary = {}
    bins = ['oldbins','newbins']
    seasons = [['Winter','Summer'],['Winter','Summer','Fall']]

    em_rates = em_rates.rename({'Report_Month': 'Month', \
                                'Report_Day': 'Day', "Report_Hour": "hourID"}, axis='columns')

    # Get the start and end years and a list of years.
    # These are constant across newbins/oldbins, etc.
    year_start = min(em_rates.Report_Year)
    year_end = max(em_rates.Report_Year)
    years = np.arange(year_start, year_end+1)

    # Loop through DR plan, season, bin, products
    for i in range(len(bins)):
        binning = bins[i]
        dr_info = dr_product_info[binning]

        for season in seasons[i]:
            # Get a "oldbins_summer" type name
            combo_name = binning + "_" + season
            hrs = dr_hours[combo_name]
            pot = dr_potential[combo_name]
            # Grab the names of the DR products that
            # are actually implemented for this season.
            # This assumes we have the same formatted DF everytime
            dr_list = list(hrs.columns.values[3:])
            bin_dict = sort_bins(dr_info, dr_list)

            for bin_num in list(bin_dict.keys()):
                bin_drs = bin_dict[bin_num]

                # Initialize dataframe
                if binning=='newbins':
                    #modify_resTOU_names
                    new_names = ['DVR', 'ResTOU_shift', 'ResTOU_shed']
                    start_matrix = np.zeros((len(years), len(new_names)+1))
                    start_matrix[:, 0] = years.astype(int)
                    yearly_avoided = pd.DataFrame(data = start_matrix, columns=['Year']+new_names)
                else:
                    start_matrix = np.zeros((len(years), len(bin_drs)+1))
                    start_matrix[:, 0] = years.astype(int)
                    yearly_avoided = pd.DataFrame(data = start_matrix, columns=['Year']+bin_drs)

                for dr_name in bin_drs:
                    #rename things so dataframes more easily compared
                    restou_newbins = False
                    #Ok if its new
                    if binning=='newbins':
                        if dr_name == 'ResTOU':
                            restou_newbins = True

                    # Do Shifting if it's a shift product.
                    shift = dr_product_info[binning]['Shift or Shed?'].\
                    loc[dr_product_info[binning].Product==dr_name]
                    shift = shift.iloc[0]

                    if shift == 'Shift':
                        if restou_newbins:
                            dr_season_hours_shed = hrs[dr_name]
                            dr_season_hours_shift = shift_hours(hrs[dr_name], 2)
                        else:
                            dr_season_hours = shift_hours(hrs[dr_name], 2)
                    else:
                        dr_season_hours = hrs[dr_name]

                    for year in range(year_start, year_end+1):
                        dr_pot = pot[dr_name].loc[pot.Year==year]
                        short_df = em_rates.loc[em_rates.Report_Year==year]
                        if year%4==0:
                            #There's no DR implemented on leap years, 
                            #so we can ignore that extra time (last 24 entries)
                            short_df = short_df.iloc[:-24]


                        #Multiply baseline emissions by potential for all hours
                        #This should atomatically work correctly if we have -1 values
                        #due to shifting

                        if restou_newbins:
                            out_arr_shift = short_df["Baseline Emissions Rate Estimate"].\
                            values*dr_season_hours_shift*dr_pot.values * EMISSIONS_CHANGEUNITS
                            out_arr_shed = short_df["Baseline Emissions Rate Estimate"].\
                            values*dr_season_hours_shed*dr_pot.values * EMISSIONS_CHANGEUNITS
                            yearly_avoided["ResTOU_shift"].iloc[year-year_start] = out_arr_shift.sum()
                            yearly_avoided["ResTOU_shed"].iloc[year-year_start] = out_arr_shed.sum()

                        else:
                            out_arr = short_df["Baseline Emissions Rate Estimate"].values*dr_season_hours*dr_pot.values
                            out_arr = out_arr * EMISSIONS_CHANGEUNITS
                            yearly_avoided[dr_name].iloc[year-year_start] = out_arr.sum()

                save_name = binning+"_"+bin_num.split()[0]+"_"+bin_num.split()[1]+"_"+season

                output_dictionary[save_name] = yearly_avoided

    return output_dictionary
                


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


def shift_hours(dr_hours):
    """
    Outputs an updated dr_hours dataframe that adds -1 values to hours
    in which the load has increased due to a DR shift product. 
    (DR shift products shift load from the time of DR implementation
    to the adjacent hours.)

    Args:
        dr_hours: Dataframe of the hours for a DR plan, season, product


    Returns:
        dr_hours_out: dataframe containing hours with DR implemented 
                      to reduce load (+1 value), hours with no DR (0 value)
                      and hours with increased load due to a load shift by DR
                      (-1 value)
    """

    # Get first index in set of hours implemented
    indicies_imp = dr_hours.loc[dr_hours==1].index
    firsts = np.array([])
    first = False
    ind_prev = 0
    num_hours_implemented = 0
    for ind in indicies_imp:
        if first:
            num_hours_implemented = 1
            firsts = np.append(firsts, np.array([np.floor(ind)-1]))
            first = False
            ind_prev = ind
            num_hours_implemented +=1
        else:
            first = bool(ind-ind_prev > 1)
            ind_prev = ind
            num_hours_implemented += 1
        
    firsts = firsts.astype(int)
    # Specify indices_shift to insert -1 values for load shift

    #TO DO: Currently only works for even number of implemented hours
    if num_hours_implemented%2!=0:
        raise ValueError("Number of hours implemented for shifting must be even.")
    hours_to_shift = num_hours_implemented//2
    indicies_shift_down = np.array([]);
    indicies_shift_up = np.array([]);
    for hour in range(1,hours_to_shift+1):
        shift_inds_down = firsts - hour
        shift_inds_up = firsts + (num_hours_implemented-1)+ hour
        indicies_shift_down = np.append(indicies_shift_down, shift_inds_down)
        indicies_shift_up = np.append(indicies_shift_up, shift_inds_up)

    indicies_shift = np.append(indicies_shift_down,indicies_shift_up)

    # Insert -1 values and output new dr_hours 
    dr_product_shifted = dr_hours.copy()
    dr_product_shifted.loc[indicies_shift] = -1
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
        print(dr_name)
        print(dr_info.Product)
        bin_name = dr_info.Bin.loc[dr_info.Product == dr_name].values[0]
        if bin_name in list(out_dict.keys()):
            out_dict[bin_name] = out_dict[bin_name]+[dr_name]
        else:
            out_dict[bin_name] = [dr_name]

    return out_dict


def make_barchart_df(emissions_impacts_dict):
    """
    Args:
        emissions_impacts_dict: The same dictionary that gets returned by 
            calc_yearly_avoided_emissions()

    Returns:
        barchart_dict: dictionary of dataframes formatted such that each  easier plotting 
    """
    
    
    #Let's structure dataframes such that rows are season, columns are dr_procuct
    
    #TO DO: need to specify somewhere earlier as an input that the number of bins is 4
    bin_nums = 4
    #Create 2 dicts, one for oldbins, one for new.
    old_dict = {}
    new_dict = {}
    for n_bin in range(1, bin_nums+1):
        old_dict["bin"+str(n_bin)]=pd.DataFrame(data=[], index = ['Winter', 'Summer'])
        new_dict['bin'+str(n_bin)]=pd.DataFrame(data=[], index = ['Winter', 'Summer', 'Fall'])

    ## Really want to do this in the subcompnent c file...this is getting too messy for here.
    #Sum all years for a barchart and save that separately
    start_condition = True
    for ind, key in enumerate(emissions_impacts_dict.keys()):
        old_bins = bool('oldbins' in key)
        if "bin1" in key:
            bin_num = 1
        elif "bin2" in key:
            bin_num = 2
        elif "bin3" in key:
            bin_num = 3
        else:
            bin_num = 4 

        if "Winter" in key:
            season = "Winter"
        elif "Summer" in key:
            season = "Summer"
        elif "Fall" in key:
            season = "Fall"

        #Check whether the dataframe to put the sums is empty
        if old_bins:
            start_condition = old_dict["bin"+str(bin_num)].empty
        else:
            start_condition = new_dict["bin"+str(bin_num)].empty

        df_temp = emissions_impacts_dict[key]
        df_temp = df_temp.drop(['Year'], axis=1)
        summed_series = df_temp.sum()

        if start_condition:
            cols = list(summed_series.index)
            for col in cols:
                if old_bins:
                    old_dict["bin"+str(bin_num)].loc[season, col] = summed_series.loc[col]
                else:
                    new_dict["bin"+str(bin_num)].loc[season, col] = summed_series.loc[col]
        else:
            cols = list(summed_series.index)
            if old_bins:
                old_dict["bin"+str(bin_num)].loc[season, cols] = summed_series
            else:
                new_dict["bin"+str(bin_num)].loc[season, cols] = summed_series

        #Need to know all the the DR names and get a big list:
    #sum_dict = {}
    #sum_dict["oldbins"] = old_dict
    #sum_dict["newbins"] = new_dict
    out_df = pd.DataFrame(data=[], index = ['Winter', 'Summer', 'Fall'])
    out_df['oldbins_bin1'] = old_dict['bin1'].sum(axis=1)
    out_df['oldbins_bin2'] = old_dict['bin2'].sum(axis=1)
    out_df['oldbins_bin3'] = old_dict['bin3'].sum(axis=1)
    out_df['oldbins_bin4'] = old_dict['bin4'].sum(axis=1)
    
    out_df['newbins_bin1_shed'] = new_dict['bin1'].loc[:, ["DVR", "ResTOU_shed"]].sum(axis=1)
    out_df['newbins_bin1_shift'] = new_dict['bin1'].loc[:, ["DVR", "ResTOU_shift"]].sum(axis=1)


    pure_newbins_df = new_dict['bin1']


    return out_df, pure_newbins_df

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

                    # Do Shifting if it's a shift product.
                    shift = dr_product_info[binning]['Shift or Shed?'].\
                    loc[dr_product_info[binning].Product==dr_name]
                    shift = shift.iloc[0]

                    if shift == 'Shift':
                        dr_season_hours = shift_hours(hrs[dr_name])
                    else:
                        dr_season_hours = hrs[dr_name]

                    for year in range(year_start, year_end+1):
                        dr_pot = pot[dr_name].loc[pot.Year==year]
                        short_df = em_rates.loc[em_rates.Report_Year==year]
                        if year%4==0:
                            
                            #There's no DR implemented on leap days
                            #On Leap years, need to delete february 29
                            truth_array = short_df['Day'].loc[short_df['Month'].values==2]==29
                            leap_inds = truth_array.loc[truth_array==True]
                            delete_inds = short_df.loc[leap_inds.index].index
                            short_df = short_df.drop(delete_inds, axis=0)                     
                            out_arr = short_df["Baseline Emissions Rate Estimate"].values*dr_season_hours*dr_pot.values
                            out_arr = out_arr * EMISSIONS_CHANGEUNITS
                            yearly_avoided[dr_name].iloc[year-year_start] = out_arr.sum()

                        else:
                            out_arr = short_df["Baseline Emissions Rate Estimate"].values*dr_season_hours*dr_pot.values
                            out_arr = out_arr * EMISSIONS_CHANGEUNITS
                            yearly_avoided[dr_name].iloc[year-year_start] = out_arr.sum()

                save_name = binning+"_"+season+"_"+"bin"+bin_num.split()[1]

                output_dictionary[save_name] = yearly_avoided

    return output_dictionary
                
def subcomp_c_runall(em_rates, dr_hours, dr_potential, dr_product_info):
    """
     Args:
        em_rates: baseline emissions rates
        dr_hours: 
        dr_potential:
        dr_product_info
        
    Returns:
        out_dict: the output of calc_yearly_avoided_emissions
        barchart_df: Annual sum of yearly avoided emissions
    
    """
    out_dict = calc_yearly_avoided_emissions(em_rates, dr_hours, dr_potential, dr_product_info)
    barchart_df, newbins_barchart = make_barchart_df(out_dict)
    
    return out_dict, barchart_df, newbins_barchart

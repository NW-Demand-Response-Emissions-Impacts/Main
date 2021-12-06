"""
Subcomponent_c code for calcuating emissions reductions (/increases)

"""


from emissions_parameters import EMISSIONS_CHANGEUNITS
import pandas as pd
import numpy as np


#Function to do ResTOU shifting
def shift_hours(dr_hours, shift_hours):
    """
    
    input: dr_hours: Just the dataframe of the hours for this dr item
            shift_hours: Number of hours to shift on either side of original by
    output: how many hours to shift to shifting window
    
    only shift -2 hrs +2hrs 
    Add -1s to hrs where we want to shift to.
    """
    
    #Baseline hours for newbins is 18-21
    
    #Get first index in set of 4
    indecies = dr_hours.loc[dr_hours==1].index
    firsts = np.array([])
    first = True
    ind_prev = 0
    for ind in (indecies):
        if first:
            firsts = np.append(firsts, np.array([np.floor(ind)]))
            first = False
            ind_prev = ind
        else:
            if ind-ind_prev > 1:
                first = True
            else:
                first = False

            ind_prev = ind

    firsts = firsts.astype(int)
    shift_inds_down_2 = firsts - shift_hours
    shift_inds_down_1 = firsts - (shift_hours-1)
    shift_inds_up_1 = firsts + (shift_hours-1)
    shift_inds_up_2 = firsts + shift_hours
    indecies = np.append(shift_inds_down_2,shift_inds_down_1)
    indecies = np.append(indecies,shift_inds_up_1)
    indecies = np.append(indecies,shift_inds_up_2)

    dr_product_shifted = dr_hours.copy()
    dr_product_shifted.loc[indecies] = -1

    dr_hours_out = dr_product_shifted.values

    return(dr_hours_out)


def sort_bins(dr_info, dr_names):
    """
    make dictionary with bin number as key and names as values
    input:
    output:
    """
    out_dict = {}

    for dr in dr_names:
        bin_name = dr_info.Bin.loc[dr_info.Product == dr].values[0]
        if bin_name in list(out_dict.keys()):
            out_dict[bin_name] = out_dict[bin_name]+[dr]
        else:
            out_dict[bin_name] = [dr]

    return(out_dict)    

#Find the hours where we're doing the resTOU and multiply potential by emissions rate
#by potential

def calc_yearly_avoided_emissions(em_rates, dr_hours, dr_potential, dr_product_info):
    """
    This function uses the loaded data and calculated yearly avoided emissions for the new binning
    Currently only DVR and ResTOU shed 
    """

    output_dictionary = {};
    bins = ['oldbins','newbins']
    seasons = [['Winter','Summer'],['Winter','Summer','Fall']]


    #Get the start and end years and a list of years. 
    #These are constant across newbins/oldbins, etc.
    year_start = min(em_rates.Report_Year)
    year_end = max(em_rates.Report_Year)
    years = np.arange(year_start, year_end+1)

    #Loop over old_bins + new_bins
    for i in range(len(bins)):
        binning = bins[i];
        dr_info = dr_product_info[binning]

        for season in seasons[i]:
            #Get a "olbins_summer" type name
            combo_name = binning + "_" + season
            #print(combo_name)
            hrs = dr_hours[combo_name]
            print("starting hours", min(hrs['ResTOU']))
            pot = dr_potential[combo_name]
            #Grab the names of the DR policies that
            #are actually implemented for this season.
            #This assumes we have the same formatted DF everytime
            DR_list = list(hrs.columns.values[3:])
            
                
            bin_dict = sort_bins(dr_info, DR_list)
            #Loop over every bin number
            for bin_num in list(bin_dict.keys()):
                bin_drs = bin_dict[bin_num]
                start_matrix = np.zeros((len(years), len(bin_drs)+1))
                start_matrix[:, 0] = years.astype(int)
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
                
                for dr in bin_drs:
                    #rename things so dataframes more easily compared
                    em_rates = em_rates.rename({'Report_Month': 'Month', 'Report_Day': 'Day', "Report_Hour": "hourID"}, axis='columns')
                    
                    resTOU_newbins = False
                    #Ok if its new
                    if binning=='newbins':
                        if dr == 'ResTOU':
                            resTOU_newbins = True
                        
                    # Do Shifting if it's a shift product.
                    shift = dr_product_info[binning]['Shift or Shed?'].loc[dr_product_info[binning].Product==dr]
                    shift = shift.iloc[0]
                    #print(hrs[dr])

                    
                    if shift == 'Shift':
                        dr_season_hours = shift_hours(hrs[dr], 2)
                        if resTOU_newbins:
                            dr_season_hours_shed = hrs[dr]
                            dr_season_hours_shift = shift_hours(hrs[dr], 2)
                            #print(min(dr_season_hours_shift))
                            #print(min(dr_season_hours_shed))
                            
                        else:
                            dr_season_hours = shift_hours(hrs[dr], 2)
                    else:
                        dr_season_hours = hrs[dr]
                    
                    
                    for year in range(year_start, year_end+1):
                        dr_pot = pot[dr].loc[pot.Year==year]
                        short_df = em_rates.loc[em_rates.Report_Year==year]
                        #print(dr_hrs)
                        if year%4==0:
                            #Then we've got a leap year, so this math isn't going to work out bc summer_hrs only has 365 days
                            #Looks like there's no DR on leap years, so we can ignore that extra time (last 24 entries)
                            short_df = short_df.iloc[:-24];
                     
                        
                        #Multiply baseline emissions by potential for all hours
                        #This should atomatically work correctly if we have -1 values
                        #due to shifting
                        
                        if resTOU_newbins:
                            out_arr_shift = short_df["Baseline Emissions Rate Estimate"].values*dr_season_hours*dr_pot.values
                            out_arr_shed = short_df["Baseline Emissions Rate Estimate"].values*dr_season_hours_shed*dr_pot.values
                            yearly_sum_shift = out_arr_shift.sum()
                            yearly_sum_shed = out_arr_shed.sum()
                            yearly_avoided["ResTOU_shift"].iloc[year-year_start] = yearly_sum_shift
                            yearly_avoided["ResTOU_shed"].iloc[year-year_start] = yearly_sum_shed

                        else:
                            out_arr = short_df["Baseline Emissions Rate Estimate"].values*dr_season_hours*dr_pot.values
                            out_arr = out_arr * EMISSIONS_CHANGEUNITS
                            yearly_sum = out_arr.sum()
                            yearly_avoided[dr].iloc[year-year_start] = yearly_sum
                            
                save_name = binning+"_"+bin_num.split()[0]+"_"+bin_num.split()[1]+"_"+season;
                print(save_name)
                #Former saving out for Daniel
                #yearly_avoided.to_csv("/Users/jamesstadler/Documents/UW/Courses/CSE583/DR-Emissions-Project/Main/processed_data/subcomp_d_data/"+save_name+".csv")

                output_dictionary[save_name] = yearly_avoided

    return(output_dictionary)
                


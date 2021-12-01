"""
subcomp_d_output_data.py

Outputs csv files for the dashboard to plot,
including emissions factors, DR hours, and DR potential.
"""

import pandas as pd

from emissions_parameters import DIR_DATA_PROC

def output_avg_emissions_rates(df_seasonal_ave, df_annual_ave, df_oneyear_seasonal_ave, year):
    """
    Given subcomp_b output with average hourly emissions rates,
    outputs these into csv files for each DR plan and season. 
    These will be plotted in the default and more info pages.

    Args:
        df_seasonal_ave: dictionary of seasonally averaged hourly emissions rates
                        for days with DR averaged over full period (2022-2041)
        df_annual_ave: dictionary of annually averaged hourly emissions rates 
                        for days with DR averaged over full period (2022-2041)
        df_oneyear_seasonal_ave: dictionary of seasonally, annually averaged hourly
                        emissions rates for all days of a given year
        year: the year for df_oneyear (int)
    """
    DIR_OUT = DIR_DATA_PROC+'emissions_rates/'

    for plan_season_key in df_seasonal_ave_out.keys():
        for scenario_key in df_seasonal_ave_out[plan_season_key].keys():
            fname = DIR_OUT+'DRdays_allyears_'+plan_season_key+'_'+scenario_key+'.csv'
            df_seasonal_ave_out[plan_season_key][scenario_key].to_csv(fname,index=False)
    for plan_key in df_annual_ave_out.keys():
        for scenario_key in df_annual_ave_out[plan_key].keys():
            fname = DIR_OUT+'DRdays_allyears_'+plan_key+'_Annual_'+scenario_key+'.csv'
            df_annual_ave_out[plan_key][scenario_key].to_csv(fname,index=False)
    for season_key in df_oneyear_seasonal_ave_out.keys():
        for scenario_key in df_oneyear_seasonal_ave_out[season_key].keys():
            fname = DIR_OUT+'alldays_'+str(year)+'_'+season_key+'_'+scenario_key+'.csv'
            df_oneyear_seasonal_ave_out[season_key][scenario_key].to_csv(fname,index=False)

def output_dr_hours(dr_hours_dict):
    """
    Given subcomp_a output with hours of DR implementation,
    outputs DR hours for each DR plan and season into one csv.
    This table will be shown on the more info page.

    Args:
        dr_hours_dict: dictionary of 1-or-0 DR hours dataframes 
                             for each DR plan and season
    """
    DIR_OUT = DIR_DATA_PROC+'dr_hours/'

    def list_periods(time_df):
        """
        Outputs lists of DR periods of implementation
        for DLC (direct load control) and non-DLC products,
        where DLC has 6-hour periods and non-DLC has 4-hour periods.
        
        These are the same for all products, so just get periods for
        one non-DLC product ('DVR') and one DLC product ('ResHPWHDLCGrd').
 
        Args: 
            df_hours: a dataframe of DR hours within the dr_hours_dict
        
        Returns:
            period_4hr_nondlc: a list of 4-hour periods for non-DLC products
            period_6hr_dlc: a list of 6-hour periods for DLC products if present
        """
        dvr_on = time_df['DVR']
        hour = time_df['hourID']
        start_4hr = []
        start_6hr = []
        period_4hr_nondlc = []
        period_6hr_dlc = []

        for i in range(1,len(dvr_on)):

            # find start time for 4-hr periods
            if (dvr_on[i] == 1) and (dvr_on[i-1] == 0):
                if not hour[i] in start_4hr:
                    start_4hr.append(hour[i])
                    period_4hr_nondlc.append(str(hour[i]) + " - " + str(hour[i] + 3))

            # find start time for 6-hr periods 
            if 'ResHPWHDLCGrd' in time_df.columns:
                dlc_on = time_df['ResHPWHDLCGrd']
                if (dlc_on[i] == 1) and (dlc_on[i-1] == 0):
                    if not hour[i] in start_6hr:
                        start_6hr.append(hour[i])
                        period_6hr_dlc.append(str(hour[i]) + " - " + str(hour[i] + 5))

        return period_4hr_nondlc, period_6hr_dlc
   
    output_hours_df = pd.DataFrame(columns=['DR Plan', 'Season', 
                                            'DR Hours: Non-DLC Products', 'DR Hours: DLC Products'])
    for idx,key in enumerate(dr_hours_dict.keys()):
        #get DR plan and season
        drplan_season = key.split('_')
        
        #get list of DR hours 
        df_hours = dr_hours_dict[key]
        nondlc_hours, dlc_hours = list_periods(df_hours)

        #add everything to output_hours_df
        output_hours_df.loc[idx] = [drplan_season[0],drplan_season[1],nondlc_hours,dlc_hours]

    output_hours_df.to_csv(DIR_OUT+'output_dr_hours.csv',index=False)

def output_dr_potential(dr_pot_dict,product_info_dict):
    """
    Outputs csv files contain DR potential for each product, 
    where each csv file corresponds to a DR plan and season.

    Args:
        dr_pot_dict: dictionary of DR potential 
                     with each dataframe corresponding to a DR plan and season
        product_info_dict: dictionary of product info including bins
                           with each dataframe corresponding to a DR plan
    """
    DIR_OUT = DIR_DATA_PROC + 'dr_potential/'

    productsum_out = []
    for key in dr_pot_dict.keys():
        df_potential = dr_pot_dict[key]
        
        #get product info to know which products are in which bins
        drplan_season = key.split('_')
        drname = drplan_season[0]
        df_product_info = product_info_dict[drname]

        #loop through bins, output products in each bin
        for idx in range(1,5):
            pdlist = df_product_info[df_product_info['Bin']=='Bin '+str(idx)]['Product'].tolist()
            if pdlist: #only if not empty, excludes empty bins
                pdlist.insert(0,'Year')
                print(pdlist)
                #get potential for these products and output to csv
                df_potential_out = df_potential[df_potential.columns[df_potential.columns.isin(pdlist)]]
                df_potential_out.to_csv(DIR_OUT+key+'_bin'+str(idx)+'.csv',index=False)
                #sum all products within this bin for 2041
                productsum = df_potential_out.iloc[:, 1:].sum(axis=1)
                productsum_out.append([key+'_bin'+str(idx),productsum.iloc[-1]]) 
    product_sum_out_df = pd.DataFrame(productsum_out,columns=['DR Plan, Season, and Bin','2041 Potential'])
    product_sum_out_df.to_csv(DIR_OUT+'comparison_barchart.csv',index=False)

#def output_emissions_impacts(<emissions_impacts_args>):
#    """
#    Given subcomp_c output with DR emissions impacts,
#    outputs this data into csv files for the dashboard. 
#    """
#    DIR_OUT = DIR_DATA_PROC + 'dr_emissions_impacts/'
#    #to be filled out after James finishes subcomp_c

################# Main ####################
#def runall(<emissions_rates_args>,dr_hours_dict,dr_pot_dict,
#            product_info_dict,<emissions_impacts_args>):
#    """
#    Runs through all of the above functions to output all csv files.

#    Args: 
#        dr_hours_dict: dictionary of 1-or-0 DR hours dataframes 
#                       for each DR plan and season
#        dr_pot_dict: dr_pot_dict: dictionary of DR potential 
#                     with each dataframe corresponding to a DR plan and season
#       product_info_dict: dictionary of product info including bins
#                           with each dataframe corresponding to a DR plan    
#    """
#    output_avg_emissions_rates(<emissions_rates_args>)
#    output_dr_hours(dr_hours_dict)
#    output_dr_potential(dr_pot_dict,product_info_dict)
#    output_emissions_impacts(<emissions_impacts_args>)

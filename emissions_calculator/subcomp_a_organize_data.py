"""
subcomp_a_organize_data.py

Reads input files with DR potential, DR implementation hours, and emissions factors, and creates data frames for each of these. 

Also creates a product lookup dataframe that says which bin a product is in, and which DR_hours_label applies to the product. 

This script will run through the old, standard DR bins, and also the new, sensitivity DR bins, both contained in DR_HRS_FILES and DR_POTENTIAL_FILES.
"""
# to do: add timing, exceptions, less hard-coding in the potential function if possible

import pandas as pd
import numpy as np

from emissions_calculator.emissions_parameters import DIR_EMISSIONS_RATES, \
    DIR_DR_POTENTIAL_HRS, EMISSIONS_SCENARIO_LIST, EMISSIONS_RATES_FILES, \
    DR_NAME, DR_HRS_FILES, DR_POTENTIAL_FILES, SUBSET_PRODUCTS, DR_SEASONS
    
def create_emissions_rates_df():
    """
    Given a list of emissions rate files for different policy scenarios, 
    creates a dataframe with 2022-2041 hourly emissions factors for all policy scenarios.
    """
    sheet = 'HourlyAvoidedEmissionsRate'
    columns = ['Report_Year','Report_Month','Report_Day','Report_Hour', \
               'Emissions Rate Estimate']   
    
    for idx,file_name in enumerate(EMISSIONS_RATES_FILES):
        
        xlsx = pd.ExcelFile(DIR_EMISSIONS_RATES+file_name)
        column_name = EMISSIONS_SCENARIO_LIST[idx] + ' Emissions Rate Estimate'
        
        #for first file, read in hours 
        if idx == 0: 
            df = pd.read_excel(xlsx,sheet,usecols=columns[0:3])  
        else:
            pass 

        #for all files, add emissions rates to existing dataframe
        df[column_name] = pd.read_excel(xlsx,sheet,usecols=[columns[4]])
        
    #subset year 2022-2041 #when testing make sure this matches year range for other vars
    emissions_rates_df = df[df['Report_Year']>=2022]
    
    return emissions_rates_df

def create_DR_hours_df_dict():
    """
    Input: Excel files with 1 year of DR hours, where each file contains separate sheets for each season, 
    and each sheet contains columns for the DR products in that season. 
    Output: A dictionary of dataframes where each dataframe gives the DR hours for a given DR plan 
    and season within that plan. 
    """
    DR_hours_df_dict = {} 

    #when testing, should have same number of dr hrs files and dr potential files
    for idx, file_name in enumerate(DR_HRS_FILES):
        
        drname = DR_NAME[idx]
        seasons = DR_SEASONS[idx]
        xlsx = pd.ExcelFile(DIR_DR_POTENTIAL_HRS+file_name)
        
        for season in seasons:
            dict_key = drname + '_' + season
            DR_hours_df_dict[dict_key] = pd.read_excel(xlsx,season)
        
    return DR_hours_df_dict
                           
    #can access each dataframe using
    #dr_hrs_dict = create_DR_hours_df()
    #for key in dr_hrs_dict.keys():
        #df = dr_hrs_dict[key]
        
def create_DR_potential_df_dict():
    """
    Input: Excel files containing DR potential for each year 2022-2041 within each season.
    Output: A dictionary of dataframes where each dataframe gives the potential for a given DR plan 
    and season within that plan.
    """
    DR_potential_df_dict = {}
    
    for idx, file_name in enumerate(DR_POTENTIAL_FILES):
        
        drname = DR_NAME[idx]
        xlsx = pd.ExcelFile(DIR_DR_POTENTIAL_HRS+file_name)
       
        # in these files, summer and winter are in the same sheet, summer first and then winter
        # come back to make less hard-coded
        dict_key = drname + '_Summer'
        DR_potential_df_dict[dict_key] = pd.read_excel(xlsx,'Reporter Outputs', \
                                                       index_col=0,header=None,skiprows=1,nrows=21,usecols=range(21)).T
        DR_potential_df_dict[dict_key] = DR_potential_df_dict[dict_key].rename(columns={'Product': 'Year'})

        dict_key = drname + '_Winter'
        DR_potential_df_dict[dict_key] = pd.read_excel(xlsx,'Reporter Outputs', \
                                                       index_col=0,header=None,skiprows=26,nrows=19,usecols=range(21)).T
        DR_potential_df_dict[dict_key] = DR_potential_df_dict[dict_key].rename(columns={'Product': 'Year'})

        #if only a subset of products is desired, e.g. for new bins just want DVR and ResTOU
        subset = SUBSET_PRODUCTS[idx].copy() #copy because I don't want to change the parameter permanently
        if isinstance(subset[0],str):
            subset.insert(0,'Year')
            DR_potential_df_dict[drname + '_Summer'] = DR_potential_df_dict[drname + '_Summer'][subset]
            DR_potential_df_dict[drname + '_Winter'] = DR_potential_df_dict[drname + '_Winter'][subset]
        else:
            pass
        
        seasons = DR_SEASONS[idx]
        if 'Fall' in seasons: #for new bins, winter potential is also applied to fall
            DR_potential_df_dict[drname + '_Fall'] = DR_potential_df_dict[drname + '_Winter']
        else:
            pass
                    
    return DR_potential_df_dict       

def create_product_info_df():
    """
    Input: Excel files containing DR potential for each year 2022-2041 within each season.
    Output: A dictionary of dataframes for each DR plan, listing products, bins, seasonality, shift or shed 
    """
    DR_product_info_df_dict = {}
    
    for idx, file_name in enumerate(DR_POTENTIAL_FILES):
        
        drname = DR_NAME[idx]
        xlsx = pd.ExcelFile(DIR_DR_POTENTIAL_HRS+file_name)
        column_names = ['Product','Bin','Seasonality','Shift or Shed?']
        DR_product_info_df_dict[drname] = pd.read_excel(xlsx,'EnergyCalcs', \
                                                       skiprows=2,nrows=23,usecols=column_names)  
        
    return DR_product_info_df_dict  

################# Main ####################
def runall():
    """
    Runs through all of the above functions. 
    """
    emissions_rates_df_out = create_emissions_rates_df()
    DR_hours_df_dict_out = create_DR_hours_df_dict()
    DR_potential_df_dict_out = create_DR_potential_df_dict()
    DR_product_info_df_dict_out = create_product_info_df()
    
    return emissions_rates_df_out, DR_hours_df_dict_out, DR_potential_df_dict_out, DR_product_info_df_dict_out            
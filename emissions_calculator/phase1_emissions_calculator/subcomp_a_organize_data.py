"""
subcomp_a_organize_data.py

Reads input files with emissions factors,
DR implementation hours, and DR potential.

Returns dataframe for emissions factors,
and dictionaries of dataframes for DR hours and potential.
Also returns a product lookup dataframe that gives the bin,
seasonality, and shift/shed for each product.
"""
# to do: add timing, exceptions, testing
# less hard-coding in the potential function if possible,
# make so that file names are specified as main function input
# rather than hard-coded into emissions_parameters.py

import pandas as pd

from emissions_parameters import DIR_EMISSIONS_RATES, DIR_DR_POTENTIAL_HRS


def create_emissions_rates_df(emissions_rates_files,
                              emissions_scenario_list):
    """
    Reads in emissions rate files for different policy scenarios
    to create a dataframe with 2022-2041 hourly emissions factors.

    Args:
        emissions_rates_files: list of emissions rates files (str)
                               for each policy scenario
        emissions_scenario_list: list of policy scenarios (str)
                                 with emissions rates files
    Returns:
        emissions_rates_df: the emissions rates dataframe
    """
    sheet = 'HourlyAvoidedEmissionsRate'
    columns = ['Report_Year', 'Report_Month', 'Report_Day', 'Report_Hour',
               'Emissions Rate Estimate']

    for idx, file_name in enumerate(emissions_rates_files):

        xlsx = pd.ExcelFile(DIR_EMISSIONS_RATES+file_name)
        column_name = emissions_scenario_list[idx] + ' ' + columns[4]

        # for first file, read in hours
        if idx == 0:
            df_o = pd.read_excel(xlsx, sheet, usecols=columns[0:4])
        else:
            pass

        # for all files, add emissions rates to existing dataframe
        df_o[column_name] = pd.read_excel(xlsx, sheet, usecols=[columns[4]])

    # subset year 2022-2041 #testing check this matches years for other vars
    emissions_rates_df = df_o[df_o['Report_Year'] >= 2022]

    return emissions_rates_df


def create_dr_hours_df_dict(dr_hrs_files, dr_name, dr_seasons):
    """
    Reads in Excel files with 1 year of DR hours,
    where each file contains separate sheets for each season,
    and each sheet contains columns for the DR products in that season.

    Creates a dictionary of dataframes with each dataframe
    corresponding to a given DR plan and season within that plan.

    Args:
        dr_hrs_files: list of DR hours files (str) for each DR plan
        dr_name: list of the names of each DR plan (str)
        dr_seasons: array containing a list of seasons (str) with DR hours
                    for each DR plan
    Returns:
        dr_hours_df_dict: dictionary of DR hours dataframes
    """
    dr_hours_df_dict = {}

    # when testing, should have same number of dr hrs and pot files
    for idx, file_name in enumerate(dr_hrs_files):

        drname = dr_name[idx]
        seasons = dr_seasons[idx]
        xlsx = pd.ExcelFile(DIR_DR_POTENTIAL_HRS+file_name)

        for season in seasons:
            dict_key = drname + '_' + season
            dr_hours_df_dict[dict_key] = pd.read_excel(xlsx, season)

    return dr_hours_df_dict

    # can access each dataframe using
    # dr_hrs_dict = create_dr_hours_df()
    # for key in dr_hrs_dict.keys():
    # df = dr_hrs_dict[key]


def create_dr_potential_df_dict(dr_potential_files,
                                dr_name, dr_seasons, subset_products):
    """
    Reads in Excel files containing DR potential
    for each year 2022-2041 with all seasons in the same sheet.

    Creates a dictionary of dataframes with each dataframe
    corresponding to a given DR plan and season within that plan.

    Args:
        dr_potential_files: list of DR potential files (str) for each DR plan
        dr_name: list of the names of each DR plan (str)
        dr_seasons: array containing a list of seasons (str) with DR hours
                    for each DR plan
        subset_products: array containing a list of the DR products to subset
                         for each DR plan (str), or a [0] if all DR products are included
    Returns:
        dr_pot_df_dict: dictionary of DR potential dataframes
    """
    dr_pot_df_dict = {}

    for idx, file_name in enumerate(dr_potential_files):

        drname = dr_name[idx]
        xlsx = pd.ExcelFile(DIR_DR_POTENTIAL_HRS+file_name)

        # come back to make less hard-coded
        dict_key = drname + '_Summer'
        dr_pot_df_dict[dict_key] = pd.read_excel(xlsx, 'Reporter Outputs',
                                                 index_col=0, header=None, skiprows=1, nrows=21, usecols=range(21)).T
        dr_pot_df_dict[dict_key] = dr_pot_df_dict[dict_key].rename(columns={'Product': 'Year'})

        dict_key = drname + '_Winter'
        dr_pot_df_dict[dict_key] = pd.read_excel(xlsx, 'Reporter Outputs',
                                                 index_col=0, header=None, skiprows=26, nrows=19, usecols=range(21)).T
        dr_pot_df_dict[dict_key] = dr_pot_df_dict[dict_key].rename(columns={'Product': 'Year'})

        # if only a subset of products is desired, e.g. for new bins
        subset = subset_products[idx].copy()
        if isinstance(subset[0], str):
            subset.insert(0, 'Year')
            dr_pot_df_dict[drname + '_Summer'] = dr_pot_df_dict[drname + '_Summer'][subset]
            dr_pot_df_dict[drname + '_Winter'] = dr_pot_df_dict[drname + '_Winter'][subset]
        else:
            pass

        seasons = dr_seasons[idx]
        if 'Fall' in seasons:  # for new bins, apply winter to fall
            dr_pot_df_dict[drname + '_Fall'] = dr_pot_df_dict[drname + '_Winter']
        else:
            pass

    return dr_pot_df_dict


def create_product_info_df_dict(dr_potential_files, dr_name):
    """
    Reads the DR potential file sheet with product data
    and creates a dictionary of dataframes for each DR plan,
    listing products, bins, seasonality, shift/shed.

    Args:
        dr_potential_files: list of DR potential files (str) for each DR plan
        dr_name: list of the names of each DR plan (str)
    Returns:
        dr_product_info_df_dict: dictionary of DR product info dataframes
    """
    dr_product_info_df_dict = {}

    for idx, file_name in enumerate(dr_potential_files):

        drname = dr_name[idx]
        xlsx = pd.ExcelFile(DIR_DR_POTENTIAL_HRS+file_name)
        column_names = ['Product', 'Bin', 'Seasonality', 'Shift or Shed?']
        dr_product_info_df_dict[drname] = pd.read_excel(xlsx, 'EnergyCalcs',
                                                        skiprows=2, nrows=23, usecols=column_names)
        if drname == 'newbins':
            dr_product_info_df_dict[drname] = \
                dr_product_info_df_dict[drname][dr_product_info_df_dict[drname]['Bin'] == 'Bin 1']

    return dr_product_info_df_dict


################# Main ####################
def subcomp_a_runall(emissions_rates_files, emissions_scenario_list,
                     dr_hrs_files, dr_name, dr_seasons, dr_potential_files, subset_products):
    """
    Runs through all of the above functions to output dataframes or
    dictionaries of dataframes for emissions rates, DR hours, DR potential,
    and DR product information.

    Args:
        emissions_rates_files: list of emissions rates files (str)
                               for each policy scenario
        emissions_scenario_list: list of policy scenarios (str)
                                 with emissions rates files
        dr_hrs_files: list of DR hours files (str) for each DR plan
        dr_name: list of the names of each DR plan (str)
        dr_seasons: array containing a list of seasons (str) with DR hours
                    for each DR plan
        dr_potential_files: list of DR potential files (str) for each DR plan
        subset_products: array containing a list of the DR products to subset
                         for each DR plan (str), or a [0] if all DR products are included
    Returns:
        emissions_rates_df_out: the emissions rates dataframe
        dr_hours_df_dict_out: dictionary of DR hours dataframes
        dr_pot_df_dict_out: dictionary of DR potential dataframes
        dr_product_info_df_dict_out: dictionary of DR product info dataframes
    """
    emissions_rates_df_out = create_emissions_rates_df(emissions_rates_files,
                                                       emissions_scenario_list)
    dr_hours_df_dict_out = create_dr_hours_df_dict(dr_hrs_files, dr_name, dr_seasons)
    dr_potential_df_dict_out = create_dr_potential_df_dict(dr_potential_files,
                                                           dr_name, dr_seasons, subset_products)
    dr_product_info_df_dict_out = create_product_info_df_dict(dr_potential_files,
                                                              dr_name)

    return emissions_rates_df_out, dr_hours_df_dict_out, \
           dr_potential_df_dict_out, dr_product_info_df_dict_out

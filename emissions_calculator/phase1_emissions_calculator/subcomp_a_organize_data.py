"""
subcomp_a_organize_data.py

Reads input files with emissions factors,
DR implementation hours, and DR potential.

Returns dataframe for emissions factors,
and dictionaries of dataframes for DR hours and potential.
Also returns a product lookup dataframe that gives the bin,
seasonality, and shift/shed for each product.
"""
from os import path

import numpy as np
import pandas as pd

def checkarglists(**kwargs):
    """
    Checks if arguments are lists with matching sizes as expected.
    Also checks if items in lists are type str, except for
    subset_products which can have a non-string item.

    Args:
        **kwarg: variable number of function keywords and arguments to check
    """
    for idx, (name,arg) in enumerate(kwargs.items()):
        # check arguments are lists with matching sizes
        if not isinstance(arg,list):
            raise ValueError('Please input a list for the argument: '+ name)
        if idx == 0:
            checklength = len(arg)
            nameo = name
        else:
            if not np.isclose(checklength,len(arg)):
                raise ValueError('The lists for the arguments ' + nameo + \
                                    ' and ' + name + ' are not the same length.')

        # check arguments contain string items
        if name == 'subset_products':
            pass
        else:
            for item in arg:
                if isinstance(item,list):
                    if not all(isinstance(i, str) for i in item):
                        raise ValueError('Argument lists must contain strings')
                else:
                    if not isinstance(item,str):
                        raise ValueError('Argument lists must contain strings')

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

    # check if arguments are lists with matching sizes
    checkarglists(emissions_rates_files = emissions_rates_files, \
                    emissions_scenario_list = emissions_scenario_list)

    for idx, file_name in enumerate(emissions_rates_files):

        # check file exists
        if not path.exists(file_name):
            raise ValueError('Emissions rates file does not exist')

        xlsx = pd.ExcelFile(file_name)
        column_name = emissions_scenario_list[idx] + ' ' + columns[4]

        # check sheet and columns exist, read file
        if not sheet in xlsx.sheet_names:
            raise ValueError('Emissions file does not contain sheet: ' + sheet)
        checkdf = pd.read_excel(xlsx, sheet)
        for column in columns:
            if not column in checkdf.columns:
                raise ValueError('Emissions file does not contain the column: ' + column)

        # for first file, read in hours; check other files match
        if idx == 0:
            df_o = checkdf[columns[0:4]].copy()
        else:
            if not df_o[columns[0:4]].equals(checkdf[columns[0:4]]):
                raise ValueError('Times in emissions files do not match.')

        # for all files, add emissions rates to existing dataframe
        df_o[column_name] = checkdf[columns[4]].copy()

    emissions_rates_df = df_o[df_o['Report_Year'] >= 2022]

    # check emissions_rates_df data makes sense
    if emissions_rates_df.isnull().values.any():
        raise ValueError('Emissions rates or times contain null values')

    for column in emissions_rates_df.columns[0:4]:
        if not emissions_rates_df[column].dtypes == np.int64:
            raise ValueError('Emissions times are not type int')

    for column in emissions_rates_df.columns[4:]:
        if not emissions_rates_df[column].dtypes == np.float64:
            raise ValueError('Emissions rates are not type float')

    years = emissions_rates_df['Report_Year']

    for year in range(years.min(),years.max()+1):
        if year%4==0:
            nhour = 366*24
        else:
            nhour = 365*24
        hrcount = emissions_rates_df[emissions_rates_df['Report_Year']==year]['Report_Hour'].count()
        if not np.isclose(hrcount,nhour):
            raise ValueError('Emissions file contains wrong number of hours in year '+ str(year))

    return emissions_rates_df


def create_dr_hours_df_dict(dr_hrs_files, dr_name, dr_seasons):
    """
    Reads in Excel files with 1 year of DR hours,
    where each file contains separate sheets for each season,
    and each sheet contains columns for the DR products in that season.

    Creates a dictionary of dataframes with each dataframe
    corresponding to a given DR plan and season within that plan.

    Note that subcomp_c will insert values of -1 for hours with shifted
    load for shift products.

    Args:
        dr_hrs_files: list of DR hours files (str) for each DR plan
        dr_name: list of the names of each DR plan (str)
        dr_seasons: array containing a list of seasons (str) with DR hours
                    for each DR plan
    Returns:
        dr_hours_df_dict: dictionary of DR hours dataframes
    """
    dr_hours_df_dict = {}

    # check if arguments are lists with matching sizes
    checkarglists(dr_hrs_files = dr_hrs_files, dr_name = dr_name, \
                    dr_seasons = dr_seasons)

    for idx, file_name in enumerate(dr_hrs_files):

        drname = dr_name[idx]
        seasons = dr_seasons[idx]

        # check file exists and read file
        if not path.exists(file_name):
            raise ValueError('DR hours file does not exist')

        xlsx = pd.ExcelFile(file_name)

        for season in seasons:

            # check sheet exists
            if not season in xlsx.sheet_names:
                raise ValueError('DR hours file does not contain sheet: ' + season)

            dict_key = drname + '_' + season
            dr_hours_df_dict[dict_key] = pd.read_excel(xlsx, season)

            # check dr_hours_df_dict[dict_key] data makes sense
            if dr_hours_df_dict[dict_key].isnull().values.any():
                raise ValueError('DR hours contain null values for '+dict_key)

            for column in dr_hours_df_dict[dict_key].columns:
                if not dr_hours_df_dict[dict_key][column].dtypes == np.int64:
                    raise ValueError('DR hours are not type int for '+dict_key)

            expected_cols = ['hourID','Month','Day']
            for column in expected_cols:
                if not column in dr_hours_df_dict[dict_key].columns:
                    raise ValueError('DR hours are missing column ' + column + ' for ' + dict_key)

            if len(dr_hours_df_dict[dict_key].columns) < (len(expected_cols) + 1):
                raise ValueError('DR hours are missing DR product column for ' + dict_key)

            nhour = 365*24
            hrcount = dr_hours_df_dict[dict_key]['hourID'].count()
            if not np.isclose(hrcount,nhour):
                raise ValueError('DR hours contains wrong number of hours = '+ str(hrcount))

            # for new bins resTOU, copy hours for resTOU_shift and resTOU_shed
            if drname == 'newbins':
                dr_hours_df_dict[dict_key]['ResTOU_shed'] = \
                    dr_hours_df_dict[dict_key]['ResTOU']
                dr_hours_df_dict[dict_key] = \
                    dr_hours_df_dict[dict_key].rename(columns={'ResTOU': 'ResTOU_shift'})
            else:
                pass

    return dr_hours_df_dict


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

    # check if arguments are lists with matching sizes
    checkarglists(dr_potential_files = dr_potential_files, \
                    dr_name = dr_name, dr_seasons = dr_seasons,\
                    subset_products = subset_products)

    for idx, file_name in enumerate(dr_potential_files):

        drname = dr_name[idx]

        # check file and sheet exists and read file
        if not path.exists(file_name):
            raise ValueError('DR potential file does not exist')
        xlsx = pd.ExcelFile(file_name)
        if not 'Reporter Outputs' in xlsx.sheet_names:
            raise ValueError('DR potential file does not contain sheet: Reporter Outputs')

        # note very specific formatting used in NW Power Council files
        dict_key = drname + '_Summer'
        dr_pot_df_dict[dict_key] = pd.read_excel(xlsx, 'Reporter Outputs',\
                            index_col=0, header=None, skiprows=1, nrows=21, usecols=range(21)).T
        dr_pot_df_dict[dict_key] = dr_pot_df_dict[dict_key].rename(columns={'Product': 'Year'})

        dict_key = drname + '_Winter'
        dr_pot_df_dict[dict_key] = pd.read_excel(xlsx, 'Reporter Outputs',\
                            index_col=0, header=None, skiprows=26, nrows=19, usecols=range(21)).T
        dr_pot_df_dict[dict_key] = dr_pot_df_dict[dict_key].rename(columns={'Product': 'Year'})

        # if only a subset of products is desired, e.g. for new bins
        subset = subset_products[idx].copy()
        if isinstance(subset[0], str):
            subset.insert(0, 'Year')
            for season in ['_Summer','_Winter']:
                checklist = all(p in dr_pot_df_dict[drname + season].columns for p in subset)
                if not checklist:
                    raise ValueError('Subset of DR products not found in potential file')
                dr_pot_df_dict[drname + season] = dr_pot_df_dict[drname + season][subset]
        else:
            pass

        # check dr_pot_df_dict[dict_key] data makes sense
        if dr_pot_df_dict[dict_key].isnull().values.any():
            raise ValueError('DR potential contains null values for '+ dict_key)
        for column in dr_pot_df_dict[dict_key].columns:
            if not dr_pot_df_dict[dict_key][column].dtypes == np.float64:
                raise ValueError('DR potential is not type float for '+ dict_key)
        expected_cols = ['Year']
        for column in expected_cols:
            if not column in dr_pot_df_dict[dict_key].columns:
                raise ValueError('DR potential is missing column ' + column + ' for ' + dict_key)
        if len(dr_pot_df_dict[dict_key].columns) < (len(expected_cols) + 1):
            raise ValueError('DR potential is missing DR product column for ' + dict_key)

        # for new bins, apply winter to fall
        seasons = dr_seasons[idx]
        if 'Fall' in seasons:
            dr_pot_df_dict[drname + '_Fall'] = dr_pot_df_dict[drname + '_Winter']
        else:
            pass

        # for new bins resTOU, copy potential for resTOU_shift and resTOU_shed
        if drname == 'newbins':
            for season in dr_seasons[idx]:
                dict_key = drname + '_' + season
                dr_pot_df_dict[dict_key]['ResTOU_shed'] = \
                    dr_pot_df_dict[dict_key]['ResTOU']
                dr_pot_df_dict[dict_key] = \
                    dr_pot_df_dict[dict_key].rename(columns={'ResTOU': 'ResTOU_shift'})
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

    # check if arguments are lists with matching sizes
    checkarglists(dr_potential_files = dr_potential_files, \
                    dr_name = dr_name)

    for idx, file_name in enumerate(dr_potential_files):

        drname = dr_name[idx]

        # check file, sheet, columns exists and read file
        if not path.exists(file_name):
            raise ValueError('DR potential file does not exist')
        xlsx = pd.ExcelFile(file_name)
        if not 'EnergyCalcs' in xlsx.sheet_names:
            raise ValueError('DR potential file does not contain sheet: EnergyCalcs')

        dr_product_info_df_dict[drname] = pd.read_excel(xlsx, 'EnergyCalcs',
                                                        skiprows=2, nrows=23)
        columns = ['Product', 'Bin', 'Seasonality', 'Shift or Shed?']
        for column in columns:
            if not column in dr_product_info_df_dict[drname].columns:
                raise ValueError('DR potential file does not contain the column: ' + column)

        dr_product_info_df_dict[drname] = dr_product_info_df_dict[drname][columns]

        # For 'newbins' plan, only consider bin 1,
        # and look at ResTOU as a shift and a shed product
        if drname == 'newbins':
            dr_product_info_df_dict[drname] = \
                dr_product_info_df_dict[drname][dr_product_info_df_dict[drname]['Bin'] == 'Bin 1'].reset_index(drop=True)
            newrow = dr_product_info_df_dict[drname][dr_product_info_df_dict[drname]['Product'] == 'ResTOU'].copy()
            newrow = newrow.replace('ResTOU','ResTOU_shed')
            newrow = newrow.replace('Shift','Shed')
            dr_product_info_df_dict[drname] = \
                dr_product_info_df_dict[drname].replace('ResTOU','ResTOU_shift')
            dr_product_info_df_dict[drname] = \
                pd.concat([dr_product_info_df_dict[drname], newrow]).reset_index(drop=True)
        else:
            pass
        
        # check dr_product_info_df_dict[drname] data makes sense
        if dr_product_info_df_dict[drname].isnull().values.any():
            raise ValueError('DR product info contains null values for '+ drname)

        for column in dr_product_info_df_dict[drname].columns:
            if not dr_product_info_df_dict[drname][column].dtypes == object:
                raise ValueError('DR product info is not type object for '+ drname)

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

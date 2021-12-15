"""
test_subcomp_a.py

Contains tests for subcomponent_a_organize_data, which reads in excel
files and outputs dataframes and dictionaries of dataframes.
"""

import unittest

import pandas as pd

from subcomp_a_organize_data import create_emissions_rates_df, \
    create_dr_hours_df_dict, create_dr_potential_df_dict, \
    create_product_info_df_dict, subcomp_a_runall
from emissions_parameters import DIR_TESTDATA_IN, DIR_DR_POTENTIAL_HRS

dirdata = DIR_TESTDATA_IN + 'subcomp_a_test_data/'

# inputs
emissions_scenario_list = ['Baseline']
emissions_rates_files = ['AvoidedEmissionsRate' + x + '.xlsx' for x in emissions_scenario_list]
dr_name = ['oldbins','newbins']
dr_hrs_files = [DIR_DR_POTENTIAL_HRS+'DRHours_' + x + '.xlsx' for x in dr_name]
dr_potential_files = ['DR RPM Inputs_071420.xlsx','DR RPM Inputs_021621_newaMWbins.xlsx']
dr_potential_files = [DIR_DR_POTENTIAL_HRS + x for x in dr_potential_files]
dr_seasons = [['Winter','Summer'],['Winter','Summer','Fall']]
subset_products = [[0],['DVR','ResTOU']]


class TestSubCompA(unittest.TestCase):
    """
    Class of unit tests for the subcomponent A
    """

    def test_asmoke(self):
        """
        Smoke test to make sure all functions run.
        """
        create_emissions_rates_df([dirdata + 'subset_20232024.xlsx'],['Baseline'])
        create_dr_hours_df_dict(dr_hrs_files, dr_name, dr_seasons)
        create_dr_potential_df_dict(dr_potential_files,
                    dr_name, dr_seasons, subset_products)
        create_product_info_df_dict(dr_potential_files, dr_name)
        subcomp_a_runall([dirdata + 'subset_20232024.xlsx'],['Baseline'],
                    dr_hrs_files, dr_name, dr_seasons, dr_potential_files, subset_products)

    # Below are one shot tests for all functions
    def test_emissionsrates(self):
        """
        One-shot test to make sure emissions rates output dataframe exists
        with the correct columns.
        """
        emissions_df = \
            create_emissions_rates_df([dirdata + 'subset_20232024.xlsx'],['Baseline'])
        expected_cols = ['Report_Year', 'Report_Month', 'Report_Day', 'Report_Hour',\
                        'Baseline Emissions Rate Estimate']

        self.assertTrue(isinstance(emissions_df, pd.DataFrame))
        self.assertTrue(len(emissions_df) > 0)
        self.assertEqual(set(emissions_df.columns), set(expected_cols))

    def test_drhoursdict(self):
        """
        One-shot test to make sure DR hours output dictionary exists
        with keys tied to dataframes that exist with the correct columns,
        and also check that resTOU_shift and shed have same hours.
        """
        dr_hours_df_dict = create_dr_hours_df_dict(dr_hrs_files,dr_name,dr_seasons)
        expected_cols = ['hourID','Month','Day','DVR','ResTOU_shed','ResTOU_shift']

        self.assertTrue(isinstance(dr_hours_df_dict,dict))
        self.assertTrue(dr_hours_df_dict is not None)
        self.assertTrue(len(dr_hours_df_dict.keys()) > 0)
        self.assertTrue(isinstance(dr_hours_df_dict['newbins_Fall'], pd.DataFrame))
        self.assertTrue(len(dr_hours_df_dict['newbins_Fall']) > 0)
        self.assertEqual(set(dr_hours_df_dict['newbins_Fall'].columns), set(expected_cols))

        sheddf = dr_hours_df_dict['newbins_Fall']['ResTOU_shed']
        shiftdf = dr_hours_df_dict['newbins_Fall']['ResTOU_shift']
        self.assertTrue(sheddf.equals(shiftdf))

    def test_drpotdict(self):
        """
        One-shot test to make sure DR potential output dictionary exists
        with keys tied to dataframes that exist with the correct columns.
        """
        dr_dict = create_dr_potential_df_dict(dr_potential_files,
                                dr_name, dr_seasons, subset_products)
        expected_cols = ['Year']

        self.assertTrue(isinstance(dr_dict,dict))
        self.assertTrue(dr_dict is not None)
        self.assertTrue(len(dr_dict.keys()) > 0)
        usekey = list(dr_dict.keys())[0]
        self.assertTrue(isinstance(dr_dict[usekey], pd.DataFrame))
        self.assertTrue(len(dr_dict[usekey]) > 0)
        self.assertTrue(all(col in dr_dict[usekey].columns for col in expected_cols))

    def test_drinfodict(self):
        """
        One-shot test to make sure DR info output dictionary exists
        with keys tied to dataframes that exist with the correct columns.
        """
        dr_dict = create_product_info_df_dict(dr_potential_files, dr_name)
        expected_cols = ['Product', 'Bin', 'Seasonality', 'Shift or Shed?']

        self.assertTrue(isinstance(dr_dict,dict))
        self.assertTrue(dr_dict is not None)
        self.assertTrue(len(dr_dict.keys()) > 0)
        usekey = list(dr_dict.keys())[0]
        self.assertTrue(isinstance(dr_dict[usekey], pd.DataFrame))
        self.assertTrue(len(dr_dict[usekey]) > 0)
        self.assertEqual(set(dr_dict[usekey].columns), set(expected_cols))


    # Below are edge tests for the checkarglists function, called by all other functions
    def test_listfiles(self):
        """
        Edge test to make sure functions throw a ValueError
        when the input arguments are not lists.
        """
        try:
            create_emissions_rates_df('nonexistentfile.xlsx',['Baseline'])
        except (ValueError) as err:
            print('Edge test succeeded, caught the error: ')
            print(err)

    def test_list_length(self):
        """
        Edge test to make sure functions throw a ValueError
        when the lengths of arguments are not the same.
        """
        try:
            create_emissions_rates_df(['nonexistentfile.xlsx'],['Baseline','toolong'])
        except (ValueError) as err:
            print('Edge test succeeded, caught the error: ')
            print(err)

    def test_nonstring(self):
        """
        Edge test to make sure functions throw a ValueError
        when list arguments contain non-string values.
        """
        try:
            create_emissions_rates_df([42],['Baseline'])
        except (ValueError) as err:
            print('Edge test succeeded, caught the error: ')
            print(err)

    # Below are edge tests for create_emissions_rates_df
    def test_emissionsfile(self):
        """
        Edge test to make sure create_emissions_rates throws a ValueError
        when the input emissions file does not exist.
        """
        try:
            create_emissions_rates_df(['nonexistentfile.xlsx'],['Baseline'])
        except (ValueError) as err:
            print('Emissions edge test succeeded, caught the error: ')
            print(err)

    def test_emissionssheet(self):
        """
        Edge test to make sure create_emissions_rates throws a ValueError
        when the input emissions file does not contain the right sheet.
        """
        try:
            create_emissions_rates_df([dirdata + 'wrongsheet.xlsx'],['Baseline'])
        except (ValueError) as err:
            print('Emissions edge test succeeded, caught the error: ')
            print(err)

    def test_emissionscolumn(self):
        """
        Edge test to make sure create_emissions_rates throws a ValueError
        when the input emissions file does not contain the right columns.
        """
        try:
            create_emissions_rates_df([dirdata + 'wrongcolumns.xlsx'],['Baseline'])
        except (ValueError) as err:
            print('Emissions edge test succeeded, caught the error: ')
            print(err)

    def test_emissionsnull(self):
        """
        Edge test to make sure create_emissions_rates throws a ValueError
        when the emissions data contains null values.
        """
        emfiles = [dirdata + 'emissions_nan.xlsx']
        try:
            create_emissions_rates_df(emfiles,['test'])
        except (ValueError) as err:
            print('Emissions edge test succeeded, caught the error: ')
            print(err)

    def test_emissionsfloat(self):
        """
        Edge test to make sure create_emissions_rates throws a ValueError
        when the emissions rates are not type float.
        """
        emfiles = [dirdata + 'emissions_notfloat.xlsx']
        try:
            create_emissions_rates_df(emfiles,['test'])
        except (ValueError) as err:
            print('Emissions edge test succeeded, caught the error: ')
            print(err)

    def test_emissionsint(self):
        """
        Edge test to make sure create_emissions_rates throws a ValueError
        when the times are not type int.
        """
        emfiles = [dirdata + 'emissions_notint.xlsx']
        try:
            create_emissions_rates_df(emfiles,['test'])
        except (ValueError) as err:
            print('Emissions edge test succeeded, caught the error: ')
            print(err)

    def test_emissionshours(self):
        """
        Edge test to make sure create_emissions_rates throws a ValueError
        when the emissions data contains the wrong number of hours.
        """
        emfiles = [dirdata + 'subset_unmatch.xlsx']
        try:
            create_emissions_rates_df(emfiles,['unmatch'])
        except (ValueError) as err:
            print('Emissions edge test succeeded, caught the error: ')
            print(err)

    def test_scenariotimes(self):
        """
        Edge test to make sure create_emissions_rates throws a ValueError
        when the times for two emissions scenario rates don't match.
        """
        emfiles = [dirdata + 'subset_20232024.xlsx', dirdata + 'subset_unmatch.xlsx']
        try:
            create_emissions_rates_df(emfiles,['Baseline','unmatch'])
        except (ValueError) as err:
            print('Emissions edge test succeeded, caught the error: ')
            print(err)

    # Below are edge tests for dr_hours_df_dict
    def test_hoursfile(self):
        """
        Edge test to make sure dr_hours_df_dict throws a ValueError
        when the input file does not exist.
        """
        try:
            create_dr_hours_df_dict(['nonexistentfile.xlsx'],['oldbins'],[['Fall']])
        except (ValueError) as err:
            print('Hours edge test succeeded, caught the error: ')
            print(err)

    def test_hourssheet(self):
        """
        Edge test to make sure dr_hours_df_dict throws a ValueError
        when the input file does not contain a sheet for the listed season.
        """
        try:
            create_dr_hours_df_dict([dirdata + 'wrongsheet.xlsx'],
                                    ['oldbins'],[['Fall']])
        except (ValueError) as err:
            print('Hours edge test succeeded, caught the error: ')
            print(err)

    def test_hoursnull(self):
        """
        Edge test to make sure dr_hours_df_dict throws a ValueError
        when the hours data contains null values.
        """
        hrfile = [dirdata + 'hours_nan.xlsx']
        try:
            create_dr_hours_df_dict(hrfile,['newbins'],[['Fall']])
        except (ValueError) as err:
            print('Hours edge test succeeded, caught the error: ')
            print(err)

    def test_hoursint(self):
        """
        Edge test to make sure dr_hours_df_dict throws a ValueError
        when the hours data contains non-integer values.
        """
        hrfile = [dirdata + 'hours_notint.xlsx']
        try:
            create_dr_hours_df_dict(hrfile,['newbins'],[['Fall']])
        except (ValueError) as err:
            print('Hours edge test succeeded, caught the error: ')
            print(err)

    def test_hourscols(self):
        """
        Edge test to make sure dr_hours_df_dict throws a ValueError
        when the hours data does not have a necessary time column.
        """
        hrfile = [dirdata + 'hours_columns.xlsx']
        try:
            create_dr_hours_df_dict(hrfile,['newbins'],[['Fall']])
        except (ValueError) as err:
            print('Hours edge test succeeded, caught the error: ')
            print(err)

    def test_hoursproduct(self):
        """
        Edge test to make sure dr_hours_df_dict throws a ValueError
        when the hours data does not have a DR product column.
        """
        hrfile = [dirdata + 'hours_noproduct.xlsx']
        try:
            create_dr_hours_df_dict(hrfile,['newbins'],[['Fall']])
        except (ValueError) as err:
            print('Hours edge test succeeded, caught the error: ')
            print(err)

    def test_hoursrange(self):
        """
        Edge test to make sure dr_hours_df_dict throws a ValueError
        when the hours data has the wrong number of hours.
        """
        hrfile = [dirdata + 'hours_wronghrs.xlsx']
        try:
            create_dr_hours_df_dict(hrfile,['newbins'],[['Fall']])
        except (ValueError) as err:
            print('Hours edge test succeeded, caught the error: ')
            print(err)

    # Below are edge tests for create_dr_potential_df_dict
    def test_potfile(self):
        """
        Edge test to make sure create_dr_potential_df_dict throws
        a ValueError for a missing file.
        """
        try:
            create_dr_potential_df_dict([dirdata + 'nonexistentfile.xlsx'], [dr_name[0]],
                                        [dr_seasons[0]], [subset_products[0]])
        except (ValueError) as err:
            print('Potential edge test succeeded, caught the error: ')
            print(err)

    def test_potsheet(self):
        """
        Edge test to make sure create_dr_potential_df_dict throws a ValueError
        when the input file does not contain expected sheet.
        """
        try:
            create_dr_potential_df_dict([dirdata + 'wrongsheet.xlsx'], [dr_name[0]],
                                        [dr_seasons[0]], [subset_products[0]])
        except (ValueError) as err:
            print('Potential edge test succeeded, caught the error: ')
            print(err)

    def test_potcols(self):
        """
        Edge test to make sure create_dr_potential_df_dict throws a ValueError
        when the input file does not contain expected columns.
        """
        try:
            create_dr_potential_df_dict([dirdata + 'wrongcolumns.xlsx'], [dr_name[0]],
                                        [dr_seasons[0]], [subset_products[0]])
        except (ValueError) as err:
            print('Potential edge test succeeded, caught the error: ')
            print(err)

    def test_potnull(self):
        """
        Edge test to make sure create_dr_potential_df_dict throws a ValueError
        when the data contains null values.
        """
        try:
            create_dr_potential_df_dict([dirdata + 'pot_null.xlsx'], [dr_name[0]],
                                        [dr_seasons[0]], [subset_products[0]])
        except (ValueError) as err:
            print('Potential edge test succeeded, caught the error: ')
            print(err)

    def test_pottype(self):
        """
        Edge test to make sure create_dr_potential_df_dict throws a ValueError
        when the data contains the wrong type of values.
        """
        try:
            create_dr_potential_df_dict([dirdata + 'pot_type.xlsx'], [dr_name[0]],
                                        [dr_seasons[0]], [subset_products[0]])
        except (ValueError) as err:
            print('Potential edge test succeeded, caught the error: ')
            print(err)

    def test_potsubset(self):
        """
        Edge test to make sure create_dr_potential_df_dict throws a ValueError
        when the product subset is not included in the file.
        """
        try:
            create_dr_potential_df_dict([dr_potential_files[0]], [dr_name[0]],
                                        [dr_seasons[0]], [['guacamole']])
        except (ValueError) as err:
            print('Potential edge test succeeded, caught the error: ')
            print(err)

    # Below are edge tests for create_product_info_df_dict
    def test_prodfile(self):
        """
        Edge test to make sure create_product_info_df_dict throws
        a ValueError for a missing file.
        """
        try:
            create_product_info_df_dict([dirdata + 'nonexistentfile.xlsx'], [dr_name[0]])
        except (ValueError) as err:
            print('Product edge test succeeded, caught the error: ')
            print(err)

    def test_prodsheet(self):
        """
        Edge test to make sure create_product_info_df_dict throws a ValueError
        when the input file does not contain expected sheet.
        """
        try:
            create_product_info_df_dict([dirdata + 'wrongsheet.xlsx'], [dr_name[0]])
        except (ValueError) as err:
            print('Product edge test succeeded, caught the error: ')
            print(err)

    def test_prodcols(self):
        """
        Edge test to make sure create_product_info_df_dict throws a ValueError
        when the input file does not contain expected columns.
        """
        try:
            create_product_info_df_dict([dirdata + 'wrongcolumns.xlsx'], [dr_name[0]])
        except (ValueError) as err:
            print('Product edge test succeeded, caught the error: ')
            print(err)

    def test_prodnull(self):
        """
        Edge test to make sure create_product_info_df_dict throws a ValueError
        when the input file contains null values.
        """
        try:
            create_product_info_df_dict([dirdata + 'prod_null.xlsx'], [dr_name[0]])
        except (ValueError) as err:
            print('Product edge test succeeded, caught the error: ')
            print(err)

    def test_prodtype(self):
        """
        Edge test to make sure create_product_info_df_dict throws a ValueError
        when the input file contains non-string values.
        """
        try:
            create_product_info_df_dict([dirdata + 'prod_type.xlsx'], [dr_name[0]])
        except (ValueError) as err:
            print('Product edge test succeeded, caught the error: ')
            print(err)

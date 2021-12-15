"""
test_subcomp_d.py

Contains tests for subcomp_d_output_data, which outputs processed data
into csv files for the dashboard generator to read.
"""

from os import path

import unittest
import pandas as pd

from emissions_parameters import DIR_TESTDATA_IN
from subcomp_d_output_data import output_dr_hours, \
    output_dr_potential, output_avg_emissions_rates, output_emissions_impacts
from emissions_calculator import main

# Using subcomp_d which needs input from earlier subcomps,
# produce csv files in test folder to test
dir_out = DIR_TESTDATA_IN + 'subcomp_d_test_data/'
main(dir_out)

# Expected folders, files, columns for one shot test
# This would need to be modified for different DR plans, bins, seasons
folders = ['dr_hours/','dr_potential/','emissions_rates/','emissions_impacts/']
files = [['output_dr_hours'],['comparison_barchart','newbins_Fall_bin1'],\
         ['alldays_2022_Spring_Baseline','DRdays_allyears_newbins_Winter_Baseline'],\
         ['emissions_reductions_barchart','oldbins_Summer_bin2']]
columns = [[['DR Plan','Season','DR Hours: Non-DLC Products','DR Hours: DLC Products']],\
        [['DR Plan, Season, and Bin','2041 Potential'],\
        ['Year','DVR','ResTOU_shift','ResTOU_shed']],\
        [['Report_Hour','Baseline Emissions Rate Estimate'],\
        ['Report_Hour','Baseline Emissions Rate Estimate']],\
        [['Season','oldbins_bin1','oldbins_bin2','oldbins_bin3','oldbins_bin4',\
        'newbins_bin1_shed','newbins_bin1_shift'],\
        ['Year','NRCurtailCom','NRCurtailInd','ResTOU','NRCoolSwchMed','ResBYOT']]]

# For edge tests
emptydf = pd.DataFrame()
emptydict = {}
dictodd = {}
dictodd['key1'] = 'value1'
emptydictofdf = {}
emptydictofdf['outerkey'] = pd.DataFrame()
emptydictofdict = {}
emptydictofdict['outerkey'] = {}
emptydictofdict['outerkey']['innerkey'] = pd.DataFrame()

class TestSubCompD(unittest.TestCase):
    """
    Class of unit tests for the subcomponent D.
    A smoke test for subcomponent D is in test_emissions_calculator.py.
    Tests below will check on the csvs that are output by subcomponent D.
    """

    def test_csvs(self):
        """
        One-shot test to check that a sample of csvs output by
        subcomponent d exist and match expectations for columns, length.
        """
        for ifolder, folder in enumerate(folders):
            filelist = files[ifolder]
            for ifile, csvfile in enumerate(filelist):
                self.assertTrue(path.exists(dir_out+folder+csvfile+'.csv'))
                checkdf = pd.read_csv(dir_out+folder+csvfile+'.csv')
                expected_cols = columns[ifolder][ifile]
                self.assertEqual(set(checkdf.columns), set(expected_cols))
                self.assertTrue(len(checkdf) > 0)

    def test_df(self):
        """
        Edge test to make sure output_emissions_impacts throws a ValueError
        for inputting a non-dataframe argument.
        """
        try:
            output_emissions_impacts(emptydictofdf, 7, emptydf,dir_out)
        except (ValueError) as err:
            print('Edge test succeeded, caught the error: ')
            print(err)

    def test_dict(self):
        """
        Edge test to make sure output_dr_hours throws a ValueError
        for inputting a non-dict argument.
        """
        try:
            output_dr_hours(emptydf,dir_out)
        except (ValueError) as err:
            print('Edge test succeeded, caught the error: ')
            print(err)

    def test_nokeys(self):
        """
        Edge test to make sure output_dr_potential throws a ValueError
        for inputting a dictionary with no keys.
        """
        try:
            output_dr_potential(emptydict, emptydict,dir_out)
        except (ValueError) as err:
            print('Edge test succeeded, caught the error: ')
            print(err)

    def test_dictofdf(self):
        """
        Edge test to make sure output_dr_potential throws a ValueError
        for inputting a dictionary with no dataframes.
        """
        try:
            output_dr_potential(dictodd, dictodd,dir_out)
        except (ValueError) as err:
            print('Edge test succeeded, caught the error: ')
            print(err)

    def test_dictofdict(self):
        """
        Edge test to make sure output_avg_emissions_rates throws a ValueError
        for inputting something that's not a dictionary of dictionaries.
        """
        try:
            output_avg_emissions_rates(dictodd, dictodd, dictodd, 2022,dir_out)
        except (ValueError) as err:
            print('Edge test succeeded, caught the error: ')
            print(err)


    def test_year(self):
        """
        Edge test to make sure output_avg_emissions_rates throws a ValueError
        for inputting a non-integer year.
        """
        try:
            output_avg_emissions_rates(emptydictofdict, emptydictofdict,
                                        emptydictofdict, [1.0],dir_out)
        except (ValueError) as err:
            print('Edge test succeeded, caught the error: ')
            print(err)

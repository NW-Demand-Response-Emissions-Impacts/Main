"""
test_subcomp_c.py
Contains tests for subcomponent_c_calculate_emissions, which calculates
emissions impacts of demand response products.
"""

import pandas as pd
import numpy as np
import pandas.testing as pdt
import unittest

from subcomp_c_calculate_emissions import shift_hours, sort_bins, make_barchart_df, calc_yearly_avoided_emissions, subcomp_c_runall

from emissions_parameters import EMISSIONS_CHANGEUNITS, DIR_EMISSIONS_RATES, DIR_DR_POTENTIAL_HRS

from subcomp_a_organize_data import subcomp_a_runall

from emissions_parameters import DIR_TESTDATA_IN                   

#Load some test data
dr_hours_5 = pd.read_excel(DIR_TESTDATA_IN+'subcomp_c_test_data/dr_hours_5.xlsx')
dr_hours_4 = pd.read_excel(DIR_TESTDATA_IN+'subcomp_c_test_data/dr_hours_4.xlsx')
emissions_1 = pd.read_excel(DIR_TESTDATA_IN+'subcomp_c_test_data/impacts_1.xlsx')



#Define some parameters for testing
emissions_scenario_list = ['Baseline']  
emissions_rates_files = [DIR_EMISSIONS_RATES+'AvoidedEmissionsRate' + x + '.xlsx' for x in emissions_scenario_list]
EMISSIONS_YEAR = 2022 #year to show emissions rates for gen pub
dr_name = ['oldbins','newbins']
dr_hrs_files = [DIR_DR_POTENTIAL_HRS+'DRHours_' + x + '.xlsx' for x in dr_name]

# For each plan in dr_name, list the DR potential file,
# seasons with DR hours, and the subset of products to include
# (or [0] to include all products).
dr_potential_files = [DIR_DR_POTENTIAL_HRS+'DR RPM Inputs_071420.xlsx',DIR_DR_POTENTIAL_HRS+'DR RPM Inputs_021621_newaMWbins.xlsx']

dr_seasons = [['Winter','Summer'],['Winter','Summer','Fall']]
subset_products = [[0],['DVR','ResTOU']]

#Generate Data from subcomp_a
emissions_rates_df_out, dr_hours_df_dict_out, \
    dr_potential_df_dict_out, dr_product_info_df_dict_out = \
        subcomp_a_runall(emissions_rates_files, emissions_scenario_list, \
            dr_hrs_files, dr_name, dr_seasons, dr_potential_files, subset_products)


class TestSubCompC(unittest.TestCase):
    """
    Tests for the sub component c
    """

    def test_shift_odd_hours(self):
        """
        Edge case test of raise value error if try to shift an odd number of hours.
        """
        try:
            shift_hours(dr_hours_5['ResTOU_shift'])
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_shift(self):
        """
        one shot test that shift is working properly. Input data has
        1's in 6, 7, 8, 9. Result should have same plus -1s
        4, 5, 10, 11.
        """
        shifted_hours = shift_hours(dr_hours_4['ResTOU_shift'])
        if shifted_hours[4] == -1 and shifted_hours[5] == -1\
        and shifted_hours[6]==1 and shifted_hours[7] == 1\
        and shifted_hours[8]==1 and shifted_hours[9]==1 \
        and shifted_hours[10]==-1 and shifted_hours[11]==-1:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_sort_bins_oneshot(self):
        """
        One shot test for the sort_bins helper function
        """
        dr_potential_files = ['DR RPM Inputs_071420.xlsx','DR RPM Inputs_021621_newaMWbins.xlsx']

        dr_product_info = pd.DataFrame(data=[['DVR', 'Bin 1', 'Year-round', 'Shed'],\
                                     ["ResTOU_shift", "Bin 1", "Year-Round", "Shift"],\
                                    ["ResTOU_shed", "Bin 1", "Year-Round", "Shed"],\
                                     ["FakeProduct", "Bin 2", "Year-Round", "Shed"]       ], \
                               columns=['Product', 'Bin', 'Seasonality', 'Shift or Shed?'])
        dr_list = ['DVR', 'ResTOU_shift', 'ResTOU_shed', 'FakeProduct']

        out_dict = sort_bins(dr_product_info, dr_list)

        expected_dict = {'Bin 1': ['DVR', 'ResTOU_shift', 'ResTOU_shed'], 'Bin 2': ['FakeProduct']}
        if out_dict == expected_dict:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    
    def test_smoke(self):
        """
        Smoke test to see if anything crashes when runnign the overall script
        on the full data. Calls every subfunction in subcomp_c except make_barchart.
        Then call make_barchart to also smoke test that.
        """
        
        emissions_impact_dict = calc_yearly_avoided_emissions(emissions_rates_df_out, dr_hours_df_dict_out, 
            dr_potential_df_dict_out, dr_product_info_df_dict_out, dr_name, dr_seasons)
        
        barchart_df, newbins_df = make_barchart_df(emissions_impact_dict)
    
    def test_make_barchart(self):
        """
        one-shot test for the make barchart function.
        The expected dataframes are manually defined and then
        compared against.
        """
        fake_dict = {}
        for i, name in enumerate(dr_name):
            for s_i, season in enumerate(dr_seasons[i]):
                fake_dict[name+"_"+season+"_bin1"] = emissions_1
                fake_dict[name+"_"+season+"_bin2"] = emissions_1
                fake_dict[name+"_"+season+"_bin3"] = emissions_1
                fake_dict[name+"_"+season+"_bin4"] = emissions_1

        barchart, newbins = make_barchart_df(fake_dict)
        
        expected_barchart = pd.DataFrame(data=[[15., 15., 15., 15., 10., 10.],\
                [15., 15., 15., 15., 10., 10.],[np.nan, np.nan, np.nan, np.nan, 10., 10.]],\
                columns = ['oldbins_bin1', 'oldbins_bin2', 'oldbins_bin3',\
                'oldbins_bin4', 'newbins_bin1_shed',\
                'newbins_bin1_shift'], index=['Winter',\
                'Summer', 'Fall'])
        
        expected_newbins = pd.DataFrame(data=[[5., 5., 5.],[5., 5., 5.], [5., 5., 5.]], columns=\
                ['ResTOU_shift', 'DVR', 'ResTOU_shed'], index=\
                ['Winter','Summer', 'Fall'])

        
    def test_runall_bad_input(self):
        """
        Check if handling bad input to runall works
        """
        try:
            subcomp_c_runall(emissions_rates_df_out, emissions_rates_df_out, \
                dr_potential_df_dict_out, dr_product_info_df_dict_out, dr_name, dr_seasons)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
            
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestSubCompC)
_ = unittest.TextTestRunner().run(suite)
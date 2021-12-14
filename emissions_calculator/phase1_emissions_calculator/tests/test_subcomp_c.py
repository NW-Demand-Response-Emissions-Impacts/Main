"""
Tests for sub component c
"""

import pandas as pd
import pandas.testing as pdt
import unittest

from subcomp_c_calculate_emissions import shift_hours, sort_bins, make_barchart_df, calc_yearly_avoided_emissions, subcomp_c_runall

from emissions_parameters import EMISSIONS_CHANGEUNITS

from subcomp_a_organize_data import subcomp_a_runall

from emissions_parameters import DIR_TESTDATA_IN


#Load a bunch of data to breakup and use in tests.
#missions_rates_df_out, dr_hours_df_dict_out, \
#dr_potential_df_dict_out, dr_product_info_df_dict_out = \
#        subcomp_a_runall(emissions_rates_files, emissions_scenario_list, \
#                        dr_hrs_files, dr_name, dr_seasons, dr_potential_files, subset_products
                         

                         
dr_hours_5 = pd.read_excel(DIR_TESTDATA_IN+'subcomp_c_test_data/dr_hours_5.xlsx')
dr_hours_4 = pd.read_excel(DIR_TESTDATA_IN+'subcomp_c_test_data/dr_hours_4.xlsx')


class TestSubCompC(unittest.TestCase):
    """
    Tests for the sub component c
    """
    
    
    def test_shift_odd_hours(self):
        """
        A test of raise value error if try to shift an odd number of hours.
        """
        try:
            shift_hours(dr_hours_5['ResTOU_shift'])
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
            
    def test_shift(self):
        """
        Test that shift is working properly. Input data has 
        1's in 6, 7, 8, 9. Result should have same plus -1s
        4, 5, 10, 11.
        """
        shifted_hours = shift_hours(dr_hours_4['ResTOU_shift'])
        print(shifted_hours[4:12])
        if shifted_hours[4] == -1 and shifted_hours[5] == -1\
        and shifted_hours[6]==1 and shifted_hours[7] == 1\
        and shifted_hours[8]==1 and shifted_hours[9]==1 \
        and shifted_hours[10]==-1 and shifted_hours[11]==-1:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
    
    
    
    
suite = unittest.TestLoader().loadTestsFromTestCase(TestSubCompC)
_ = unittest.TextTestRunner().run(suite)





    

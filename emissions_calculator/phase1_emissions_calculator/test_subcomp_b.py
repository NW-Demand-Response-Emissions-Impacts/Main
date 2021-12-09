"""
Tests for the sub component b
"""

import pandas as pd
import pandas.testing as pdt
import unittest

from subcomp_b_process_emissions_factors import seasonal_ave, annual_ave, \
    get_hour_ave, alldays_oneyear_seasonal_ave, get_oneyear_hour_ave, subcomp_b_runall
from emissions_parameters import DIR_TESTDATA_IN

df_emissions_data = pd.read_excel(DIR_TESTDATA_IN+'subcomp_b_test_data/emissions_data.xlsx')
df_dr_hours_winter = pd.read_excel(DIR_TESTDATA_IN+'subcomp_b_test_data/dr_hours_winter.xlsx')
df_dr_hours_spring = pd.read_excel(DIR_TESTDATA_IN+'subcomp_b_test_data/dr_hours_spring.xlsx')
df_dr_hours_summer = pd.read_excel(DIR_TESTDATA_IN+'subcomp_b_test_data/dr_hours_summer.xlsx')
df_dr_hours_fall = pd.read_excel(DIR_TESTDATA_IN+'subcomp_b_test_data/dr_hours_fall.xlsx')
df_dr_hours_data = pd.read_excel(DIR_TESTDATA_IN+'subcomp_b_test_data/dr_hours_data.xlsx')

# For smoke test, define null input values
# Just to make sure the function could run
dr_name = {}
dr_seasons = {}
emissions_scenario_list = {}
emissions_rates_df_out = {}
dr_hours_df_dict_out = {}
year = 2022


class TestSubCompB(unittest.TestCase):
    """
    Tests for the sub component b
    """

    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        seasonal_ave(dr_name, dr_seasons, emissions_scenario_list,
                     emissions_rates_df_out, dr_hours_df_dict_out)
        annual_ave(dr_name, dr_seasons, emissions_scenario_list,
                   emissions_rates_df_out, dr_hours_df_dict_out)
        get_hour_ave(df_emissions_data, df_dr_hours_winter, 'Test Emissions Rate Estimate')
        alldays_oneyear_seasonal_ave(emissions_scenario_list,
                                     emissions_rates_df_out, year)
        get_oneyear_hour_ave(df_emissions_data, 'Winter', 'Test Emissions Rate Estimate', year)
        subcomp_b_runall(dr_name, dr_seasons, emissions_scenario_list,
                         emissions_rates_df_out, dr_hours_df_dict_out, year)

    def test_get_hour_ave_winter(self):
        """
        One-shot test for get_hour_ave
        Output is winter season average
        """
        df_output_dr_days_ave_winter = pd.read_excel(DIR_TESTDATA_IN+'subcomp_b_test_data/dr_days_ave_winter.xlsx')
        df_dr_days_ave_winter = get_hour_ave(df_emissions_data, df_dr_hours_winter, 'Test Emissions Rate Estimate')
        pdt.assert_frame_equal(df_output_dr_days_ave_winter, df_dr_days_ave_winter)

    def test_get_hour_ave_spring(self):
        """
        One-shot test for get_hour_ave
        Output is spring season average
        """
        df_output_dr_days_ave_spring = pd.read_excel(DIR_TESTDATA_IN+'subcomp_b_test_data/dr_days_ave_spring.xlsx')
        df_dr_days_ave_spring = get_hour_ave(df_emissions_data, df_dr_hours_spring, 'Test Emissions Rate Estimate')
        pdt.assert_frame_equal(df_output_dr_days_ave_spring, df_dr_days_ave_spring)

    def test_get_hour_ave_annual(self):
        """
        One-shot test for get_hour_ave
        Output is annual average
        """
        df_output_dr_days_ave_annual = pd.read_excel(DIR_TESTDATA_IN+'subcomp_b_test_data/dr_days_ave_annual.xlsx')
        df_dr_days_ave_annual = get_hour_ave(df_emissions_data, df_dr_hours_data, 'Test Emissions Rate Estimate')
        pdt.assert_frame_equal(df_output_dr_days_ave_annual, df_dr_days_ave_annual)

    def test_get_oneyear_hour_ave_winter(self):
        """
        One-shot test for get_oneyear_hour_ave
        Output is winter season average
        """
        df_output_all_days_ave_winter_2022 = pd.read_excel(DIR_TESTDATA_IN+'subcomp_b_test_data/all_days_ave_winter_2022.xlsx')
        df_all_days_ave_winter_2022 = get_oneyear_hour_ave(df_emissions_data, 'Winter',
                                                           'Test Emissions Rate Estimate', 2022)
        pdt.assert_frame_equal(df_output_all_days_ave_winter_2022, df_all_days_ave_winter_2022)

    def test_time_period_available(self):
        """
        Edge test to make sure input time period(season) in get_oneyear_hour_ave is defined.
        """
        with self.assertRaises(ValueError):
            get_oneyear_hour_ave(df_emissions_data, 'Autumn', 'Test Emissions Rate Estimate', 2022)
            
    def test_year_available_alldays(self):
        """
        Edge test to make sure input year in alldays_oneyear_seasonal_ave is defined.
        """
        with self.assertRaises(ValueError):
            alldays_oneyear_seasonal_ave(emissions_scenario_list, emissions_rates_df_out, 2020)

    def test_year_available_get_oneyear(self):
        """
        Edge test to make sure input year in get_oneyear_hour_ave is defined.
        """
        with self.assertRaises(ValueError):
            get_oneyear_hour_ave(df_emissions_data, 'Winter',
                                 'Test Emissions Rate Estimate', 2020)

    def test_year_available_runall(self):
        """
        Edge test to make sure input year in subcomp_b_runall is defined.
        """
        with self.assertRaises(ValueError):
            subcomp_b_runall(dr_name, dr_seasons, emissions_scenario_list,
                             emissions_rates_df_out, dr_hours_df_dict_out, 2020)
    
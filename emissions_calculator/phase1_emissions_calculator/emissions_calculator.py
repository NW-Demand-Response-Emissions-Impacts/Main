"""
emissions_calculator.py

Runs all subcomponents to output processed emissions impacts data
for the dashboard.
"""
from emissions_parameters import DIR_EMISSIONS_RATES, DIR_DR_POTENTIAL_HRS
from subcomp_a_organize_data import subcomp_a_runall
from subcomp_b_process_emissions_factors import subcomp_b_runall
from subcomp_c_calculate_emissions import subcomp_c_runall
from subcomp_d_output_data \
    import output_avg_emissions_rates, output_dr_hours, output_dr_potential, \
                output_emissions_impacts

#### DATA ANALYST USERS: UPDATE THIS SECTION ####
# Users can specify any number of scenarios, e.g. ['Baseline','LimitedMarkets']
emissions_scenario_list = ['Baseline']  
emissions_rates_files = [DIR_EMISSIONS_RATES + 'AvoidedEmissionsRate' + x \
                         + '.xlsx' for x in emissions_scenario_list]
EMISSIONS_YEAR = 2022 #year to show emissions rates for gen pub
dr_name = ['oldbins','newbins']
dr_hrs_files = [DIR_DR_POTENTIAL_HRS+'DRHours_' + x + '.xlsx' for x in dr_name]
# The following lists should be the same length as dr_name
# For subset_products, use [0] to include all products.
dr_potential_files = ['DR RPM Inputs_071420.xlsx','DR RPM Inputs_021621_newaMWbins.xlsx']
dr_potential_files = [DIR_DR_POTENTIAL_HRS+ x for x in dr_potential_files]
dr_seasons = [['Winter','Summer'],['Winter','Summer','Fall']]
subset_products = [[0],['DVR','ResTOU']] 
#################################################

def main():
    """
    Runs subcomponents A-D to read, process, and output
    emissions impacts data for the dashboard.
    """

    # Read files and create dataframes
    print('Running subcomponent a')
    emissions_rates_df_out, dr_hours_df_dict_out, \
    dr_potential_df_dict_out, dr_product_info_df_dict_out = \
        subcomp_a_runall(emissions_rates_files, emissions_scenario_list, \
                        dr_hrs_files, dr_name, dr_seasons, dr_potential_files, subset_products)

    print(dr_product_info_df_dict_out)

    # Calculate average hourly emissions rates for dashboard
    print('Running subcomponent b')
    df_seasonal_ave, df_annual_ave, df_oneyear_seasonal_ave = \
        subcomp_b_runall(dr_name, dr_seasons, emissions_scenario_list,\
                        emissions_rates_df_out, dr_hours_df_dict_out, EMISSIONS_YEAR)

    # Calculate emissions impacts
    print('Running subcomponent c')
    emissions_impacts_dict, emissions_annual_df, newbins_barchart_df = \
        subcomp_c_runall(emissions_rates_df_out, dr_hours_df_dict_out, \
                dr_potential_df_dict_out, dr_product_info_df_dict_out)

    # Output csv files for dashboard
    print('Running subcomponent d')
    output_avg_emissions_rates(df_seasonal_ave, df_annual_ave, df_oneyear_seasonal_ave, EMISSIONS_YEAR)
    output_dr_hours(dr_hours_df_dict_out)
    output_dr_potential(dr_potential_df_dict_out, dr_product_info_df_dict_out)
    output_emissions_impacts(emissions_impacts_dict, emissions_annual_df, newbins_barchart_df)

if __name__ == '__main__':
    main()
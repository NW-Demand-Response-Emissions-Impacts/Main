"""
emissions_parameters.py

Defines directories, file names, and constants for use in the emissions_calculator and subcomponents.

"""

# Import the os module
import os

# Get the working directory
# Users should run from the Main project folder
CWD = os.getcwd() #gives .../Main

# Folders within directory
DIR_CALCULATOR = CWD + '/emissions_calculator/'
DIR_DATA_IN = CWD + '/input_data/'
DIR_EMISSIONS_RATES = DIR_DATA_IN + 'AvoidedEmissionsRates/'
DIR_DR_POTENTIAL_HRS = DIR_DATA_IN + 'DRPotentialandHours/'
DIR_DATA_PROC = CWD + '/processed_data/'

# Files to input
# The emissions_calculator will run through the old and new bin data
# Users can modify just the standard data and specify that the emissions calculator only runs through this
# Should move these notes to the user guide
EMISSIONS_SCENARIO_LIST = ['Baseline','EarlyCoalRetirement','LimitedMarkets','NoGasBuildLimits','OrgMarkets','SCC']
EMISSIONS_RATES_FILES = ['AvoidedEmissionsRate' + x + '.xlsx' for x in EMISSIONS_SCENARIO_LIST]  
DR_HRS_FILE_STANDARD = 'DRHours_oldbins.xlsx'
DR_HRS_FILE_SENSITIVITY = 'DRHours_newbins.xlsx'
DR_POTENTIAL_FILE_STANDARD = 'DR RPM Inputs_071420.xlsx'
DR_POTENTIAL_FILE_SENSITIVITY = 'DR RPM Inputs_021621_newaMWbins.xlsx'

# Constants

# multiply emissions rates in lbs CO2e/kWh by this factor to get metric tons CO2e/MWh 
emissions_rate_unit_change = .4536

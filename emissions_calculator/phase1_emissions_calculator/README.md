# Emissions Calculator

This emissions calculator is Component 1 of the Demand Response Emissions Impact project. The emissions calculator processes and outputs data to a processed data directory for Component 2, the dashboard, to access and visualize in a user-friendly webpage.

The emissions_calculator.py script runs through subcomponents A-D in order to A) read and organize the input data into dataframes; B) calculate averages of hourly emissions factors for visualization; C) calculate emissions impacts of demand response implementation; and D) output the resulting arrays into data files in the processed data directory. 

Directories and useful constants are defined in emissions_parameters.py for use in the subcomponents. 

Test scripts for the overarching emissions_calculator and each subcomponent are also included in this directory, and are titled test_(componentname).py  

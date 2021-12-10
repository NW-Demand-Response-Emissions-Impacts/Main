# Avoided Emissions Rates
## Compiled and documented by Lily Hahn
## Data Source: John Ollis, Northwest Power and Conservation Council

This directory contains hourly avoided emissions rates for 2021-2041 under baseline conditions and 5 additional policy scenarios. 

Although these files have a lot of extraneous information, I decided to keep them in their original formatting rather than compiling only the relevant data. This way, if a userdoing data analysis wants to input another Avoided Emissions Rate file in the same format for another policy scenario, our code will work for that file, and they won't need to do data preprocessing.

Hourly avoided emissions rates are found in the HourlyAvoidedEmissionsRate tab in the "Emissions Rate Estimate" column. Relevant columns for time indexing are labeled "Quarter"; "Report_Year"; "Report_Month"; "Report_Day"; and "Report_Hour" and are located in the same sheet.

## Policy Scenarios, Descriptions from John Ollis, and Data Links

Baseline Scenario: https://nwcouncil.app.box.com/s/tb02gilvpeeck166c1mzow457uzninv9

Social Cost of Carbon in power plant dispatch: https://nwcouncil.box.com/s/zfbixu3azvm3849oeaepd7ycb7ftpu36

Early Coal Retirement (early coal retirement throughout WECC): https://nwcouncil.box.com/s/vzlvj2aww757cuxb1qrz0go0f8ud6uzi

Organized Markets (one planning reserve margin throughout WECC, no wheeling costs): https://nwcouncil.box.com/s/1ytj3r5euzlz50ffzpedpu94zcwys0l3

Limited Markets (no planning reserve margins in region outside of NW): https://nwcouncil.box.com/s/yofr4psr6u5x9cvkn77xflebvyhndfud

No Gas Build Limitations (in most of these simulations gas builds were limited per understanding of current regulations, not in this one): https://nwcouncil.box.com/s/7i0k4woptwaghtmivfoa5va34bs8o1ra

## Units and Unit Conversions

Hourly avoided emissions rates are given in lbs CO2 equivalent per kWh energy usage (lbs CO2e/kWh). They will need to be multiplied by 1000 kWh/1MWh to get to units of lbs CO2e/MWh before multiplying by demand response energy reduction in MWh. To get to metric tons CO2e, multiply lb CO2e by 4.536 x 10^-4 metric tons per lb.

## How to Use This Data
Try using pd.read_excel tp read in xlsx format to Pandas dataframe. Otherwise we can convert files to csv files. Since there are multiple worksheets, try something like:
xlsx = pd.ExcelFile('AvoidedEmissionsRateBaseline.xlsx')
df = pd.read_excel(xlsx,'HourlyAvoidedEmissionsRate')

These Hourly Emissions Rates will be multiplied by a dataset with DR potential in each season (MW) and the hours of DR implementation (h) to calculate the amount of avoided CO2equivalent emissions as a result of DR strategies.

We may also want to show plots of emissions rates for different policy scenarios in the Dashboard. For the hours of DR implementation, it will be helpful to look at emissions rates for that day to see how the times of DR implementation compare to the times of maximum emissions reduction potential. For DR shift products, this will also illustrate how our assumptions about what time the load is shifted to can impact emissions.  


# Demand Response Potential and Hours
## Data Provided by Tina Jayaweera, Northwest Power and Conservation Council
## Documentation by Lily Hahn

The original DR product bins ('oldbins') include 4 bins, with bin 1 being the most economically likely bin for implementation. Subsequent modeling discovered that these products were never being acquired by the Regional Portfolio Model, leading to the new binned data ('newbins'). 

For more information on why new bins for DR products were developed, see newbinsrationale.pdf. For newbins, only the DVR and ResTOU products are acquired by the Regional Portfolio Model, so we limit our analysis to this subset of DR products. 

# Navigating the spreadsheet for DR potential: 
('DR RPM Inputs_071420.xlsx' for oldbins and 'DR RPM Inputs_021621_newaMWbins.xlsx' for newbins)
In the "Reporter Outputs" sheet, see "Summer Potential" and "Winter Potential" sections with DR potential for each product in MW for years 2022-2041. In the "EnergyCalcs" sheet, see the breakdown of shift versus shed products and which products are grouped into which bins. 

# Hours of DR implementation
For every hour of the year, a 1 is listed if DR is implemented, or a 0 if not.  

# Shift versus shed
DVR is a shed product, so the load is reduced during hours of implementation. ResTOU is a shift product, so the load is reduced during hours of implementation but must be shifted to other hours of the day. However, TOU pilots suggest that this product often looks more like a shed product, with customers reducing their energy usage rather than shifting it. 

For the ResTOU product, we will try treating this as both a shift or shed product and see how this changes the emissions impacts.  

For all shift products, we will shift the load to the adjacent hours.
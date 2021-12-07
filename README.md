# Northwest DR Impacts: Emissions Calculator

![NW DR Logo](/doc/dr_logo.png "NW DR Logo")

This tool and accompanying dashboard aids in visualization of the projected impacts on carbon emissions of implementation of Demand Response programs in the Pacific Nortwest.
A "Demand Response" is a change in the power consumption by a utility, often in response to times of high power demand by customers, or diminished power supply from power suppliers. Moving forward, utilities in the Northwest are considering implementing demand response strategies to help lessen the load during times of peak demand, such as by giving customers to option to shift their power consumption from a period of high demand to a time of lower demand (e.g. nigh time). The reason we have put together this dashboard is to aid members of the general public, policymakers, journalists, and researchers with visualization and understanding the impacts of these demand response measures on CO2 emissions.


#### Data and Demand Response Products

Modelled data for this project was provided by John Ollis and Tina Jayaweera of the Northwest Power and Conservation Council. CO2 impacts are calculated for 2022-2041 for 4 groupings of Demand Response products (groupings are referred to as "Bins"). For each demand response product, modeled data is provided for the potential of each product to reduce power consumption if applied. Combined with a baseline emissions profile for each day, these inputs are then be used to determine the emissions reduction that results from implementing each demand respone product.


## Directory Structure

```bash
├── LICENSE
├── README.md
├── input_data/
│   ├── AvoidedEmissionsRates/
│   ├── DrPotentialandHours/
├── processed_data/
│   ├── dr_hours/
│   ├── dr_potential/
│   ├── emissions_rates/
│   ├── emissions_impacts/
├── doc/
│   ├── Component_Specification.docx
│   ├── diagramhs.pptx
│   ├── dr_logo.png
│   ├── functional_specification.docx
├── emissions_calculator
│   ├── README.md
│   ├── emissions_calculator.py
│   ├── emissions_parameters.py
│   ├── component_a_organize_data.py
│   ├── component_b_process_emissions_factors.py
│   ├── component_c_calculate_emissions.py
│   ├── component_d_output_data.py
│   ├── test_emissions_calculator.py
│   ├── test_subcomp_a.py
│   ├── test_subcomp_b.py
│   ├── test_subcomp_c.py
│   ├── test_subcomp_d.py
└── requirements.txt
```




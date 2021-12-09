# Northwest Emissions Impacts of Demand Response

![NW DR Logo](/assets/dr_logo.png "NW DR Logo")

## About the Project

This tool and accompanying dashboard calculates and visualizes the projected impacts of demand response (DR) strategies on greenhouse gas emissions in the Northwest U.S. 

Demand response strategies reduce or shift electricity consumption during periods of high demand by electricity consumers. Demand response products that reduce net consumption can reduce emissions, while products that shift the load to different times of day can either increase or decrease emissions depending on the emissions rates at each time of day.

While demand response strategies are typically motivated by resource adequacy and cost concerns, understanding the emissions impacts of demand response can help inform Washington state targets for demand response and motivate broader participation in demand response programs. 

## Visualization
### Click [here](https://demand-response-impacts.herokuapp.com/home) to view the Dashboard!

We created this dashboard for both a general public audience ([home page](https://demand-response-impacts.herokuapp.com/home)) and for those who would like to learn more ([more information page](https://demand-response-impacts.herokuapp.com/more_info)) about DR emissions impacts and the components that produce these impacts. This includes hourly emissions rates, demand response potential for each product, and hours of demand response implementation. 

## Project Design

A high-level component specification is shown below. Please see the [docs](/docs) folder to learn more!

![comp spec](/docs/flow_charts/overall_flow.png)

## Directory Structure
```bash
├── LICENSE
├── Procfile
├── README.md
├── app.py
├── assets/
├── docs/
│   ├── component_specification.pdf
│   ├── flow_charts/
│   └── functional_specification.pdf
├── emissions_calculator/
│   ├── phase1_emissions_calculator/
│   └── phase2_dashboard_generator/
├── examples/
├── index.py
├── input_data/
│   ├── AvoidedEmissionsRates/
│   └── DRPotentialandHours/
├── processed_data/
│   ├── dr_hours/
│   ├── dr_potential/
│   ├── emissions_impacts/
│   └── emissions_rates/
├── requirements.txt
├── runtime.txt
└── test_data/
    ├── AvoidedEmissionsRates/
    ├── DRPotentialandHours/
```

In the emissions_calculator/ directory, phase1_emissions_calculator/ calculates emissions impacts of demand response and outputs processed data for the dashboard. phase2_dashboard_generator/ generates the dashboard webpage that visualizes these emissions impacts.

The directory input_data/ contains subdirectories with the DR potential and hours data and the avoided emissions rates that are processed by the emissions calculator to produce data files within processed_data/. test_data/ contains test input data to test the subcomponents within the emissions calculator.

Documentation includes a Functional Specification, Component Specification, and presentations within the docs/ directory. 

A user guide with examples for running the emissions calculator and interacting with the dashboard can be found in the examples/ directory.

## Installation
-Need to fill this out- confused about how to combine environment.yml, requirements.txt which seems necessary for dashboard, and setup.py, or which of these to include.-

## Future steps
 * Incorporate additional policy scenarios for emissions rates. The emissions calculator will run for a list of policy scenarios, but we currently only use one policy scenario.
 * Contextualize the emissions impacts as a percentage of total Northwest emissions.
 * For comparison with our results, calculate the maximum emissions reduction if DR hours were chosen to optimize emissions reductions.
 
## Contributors
 * @lchahn
 * @lloverasdan
 * @EstherrrrLiu
 * @jjstadler

## Acknowledgments
Marginal emissions rates and demand response product data were provided by John Ollis and Tina Jayaweera of the Northwest Power and Conservation Council. We are grateful for their help in navigating the data and developing methodology to calculate emissions impacts of demand response! 

## Licensing 
[MIT License](https://github.com/NW-Demand-Response-Emissions-Impacts/emissions_calculator/blob/main/LICENSE)



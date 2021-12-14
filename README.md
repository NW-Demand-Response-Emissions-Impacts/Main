# Emissions Impacts of Demand Response in the Northwest U.S.

![NW DR Logo](/assets/dr_logo.png){:height="10%" width="10%"}

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

In the <code>emissions_calculator/</code> directory, <code>phase1_emissions_calculator/</code> calculates emissions impacts of demand response and outputs processed data for the dashboard. <code>phase2_dashboard_generator/</code> generates the dashboard webpage that visualizes these emissions impacts.

The directory <code>input_data/</code> contains subdirectories with the DR potential and hours data and the avoided emissions rates that are processed by the emissions calculator to produce data files within <code>processed_data/</code>. <code>test_data/</code> contains test input data to test the subcomponents within the emissions calculator.

Documentation includes a Functional Specification, Component Specification, and presentations within the <code>docs/</code> directory. 

A user guide with examples for running the emissions calculator and interacting with the dashboard can be found in the <code>examples/</code> directory.

## Installation
Please follow the instructions below to install the emissions calculator, process data, and update the dashboard. For more information, see the user guide within the [examples](/examples) directory.

### Step 1: Clone the Repository
In your terminal, run the following commands to clone the repository and navigate to it:
```bash
git clone https://github.com/NW-Demand-Response-Emissions-Impacts/emissions_calculator.git
cd emissions_calculator
```

### Step 2: Set up your environment
Run the following commands:
```bash
conda create --name emissions_env
conda activate emissions_env
conda install pip
pip install -r requirements.txt
python setup.py install --user
```

### Step 3: Upload new data
If you would like to use different data for the demand response potential and hours, add new excel files to the directory <code>data/input_data/DRPotentialandHours/</code>. To use different marginal emissions rates, add new excel files to the directory <code>data/input_data/AvoidedEmissionsRates/</code>. 

Note that the emissions_calculator has been designed to run for excel files formatted in a particular way, and will raise Value Errors if these formatting expectations are not met.

### Step 4: Update data parameters and run the emissions calculator
1. Navigate to the <code>phase1_emissions_calculator/</code> directory by running:
    <code>cd emissions_calculator/phase1_emissions_calculator/</code>
2. Update data parameters in emissions_calculator.py within the section:
    #### DATA ANALYST USERS: UPDATE THIS SECTION ####
    This includes:
     * a list of DR plan names
     * the seasons in which DR is implemented for each DR plan
     * the subset of DR products to consider for each DR plan
     * a list of policy scenarios with emissions rates (the emissions calculator will determine impacts for each scenario)  
     * file names for the marginal emissions rates, DR potential, and DR hours
     * a year for which the dashboard will display average emissions rates on the main page
3. Run the emissions calculator by running: 
    <code>python emissions_calculator.py</code>

### Step 5: Update and interact with the dashboard
In order to update how the files are read into the dashboard, you must update the data parameters in the modules <code>home.py</code> and <code>more_info.py</code> in <code>emissions_calculator/phase2_dashboard_generator/</code>. These updates are analagous, but not identical, to the parameter updates in <code>emissions_calculator.py</code>. You can the edit the interpretive text and layout of the website by editing <code>home.py</code> and <code>more_info.py</code>. If you would like to edit the plots themselves, you must also edit <code>make_plots.py</code>. Please see the user guide for examples of how to edit the dashboard.   

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



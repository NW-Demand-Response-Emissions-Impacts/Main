## Background

Public utility groups implement demand response (DR) programs to encourage consumers to shift or reduce energy usage during periods of high demand. The primary goal of DR programs is to maintain resource adequacy and reduce costs. However, the impact of these programs on greenhouse gas emissions is not well understood. Knowledge of the emissions impacts of DR programs has the potential to inform state targets and motivate consumer participation.

## User Stories

User 1: Policymakers want to know how DR programs in the Northwest United States impact greenhouse gas emissions. Lacking formal training in data science, policymakers want a simple, easy-to-use interface to visualize the emissions impacts. They want a dashboard, including both figures and brief interpretations, that makes it clear how emissions rates may change under different DR scenarios. They want to use this information when considering DR targets for public utility groups.

User 2: Environmentally conscious members of the general public want to reduce their carbon footprints. They have heard that participating in DR programs might help reduce emissions. These consumers are not necessarily familiar with data science, so they want a simple, user-friendly dashboard that clearly shows how consumer participation in DR programs impacts emissions. They want to use this information to decide whether they want to participate in DR programs.

User 3: Journalists want to tell their audiences how DR programs impact greenhouse gas emissions. They are familiar with DR policies and the utilities groups that implement them. In addition to a simple dashboard, they want information on how the data is collected and analyzed. They want access to the data so that they can be sure the information they communicate to the public is accurate.

User 4: The researchers involved in gathering the data and designing the dashboard want to update the information as new data is collected. They want clear code and documentation that make it easy to update the data and make changes to the dashboard.

## Use Cases

User Action 1: Generate analysis of CO2 emissions for a specific DR plan
* Components
**Dashboard with default choice of DR plan allows for user to specify which plan they would like to analyze from a list
**User chooses from a list of visualization/plotting options how they would like to visualize data
**Data Loader loads data from database
**Plotting module takes user inputs (plotting and DR plan selections) and the loaded data from the Data Loader and generates the figures and analysis
**Dashboard displays visualizations/plots 


User Action 2: Import new, updated data to database
*Components
**Dashboard contains option to allow for user to provide new data to update the database
**User uploads their data file according to specified format
**Data Importer takes user input data and merges it into the existing database. This updated database is now saved as the default database.
**Dashboard auto-updates it's default visualizations/analysis to inlcude the new data that has just been input 

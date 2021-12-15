"""
Setup module for emissions_calculator
"""

from setuptools import setup, find_packages

setup(
    setup_requirements=['setuptools >= 24.2.0'],
    python_requirements='>=3.7',

    name='emissions_calculator',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/NW-Demand-Response-Emissions-Impacts/emissions_calculator',
    license='MIT License',
    author='Lily Hahn',
    author_email='lchahn@uw.edu',
    description=
    """
    This tool and accompanying dashboard calculates and visualizes the 
    projected impacts of demand response (DR) strategies on greenhouse 
    gas emissions in the Northwest U.S.
    
    Demand response strategies reduce or shift electricity consumption 
    during periods of high demand by electricity consumers. Demand 
    response products that reduce net consumption can reduce emissions, 
    while products that shift the load to different times of day can 
    either increase or decrease emissions depending on the emissions 
    rates at each time of day.
    
    While demand response strategies are typically motivated by 
    resource adequacy and cost concerns, understanding the emissions 
    impacts of demand response can help inform Washington state targets 
    for demand response and motivate broader participation in demand 
    response programs.
    
    Owner of tool: Lily Hahn
    Owner email: lchahn@uw.edu
    
    Contributers: Daniel Lloveras, James Stadler, Chang Liu
    """,

    requirements=['certifi==2021.10.8',
                  'numpy==1.21.4',
                  'pandas==1.3.4',
                  'python-dateutil==2.8.2',
                  'pytz==2021.3',
                  'six==1.16.0',
                  'chardet==3.0.4',
                  'Click==7.0',
                  'dash==1.1.1',
                  'dash-core-components==1.1.1',
                  'dash-html-components==1.0.0',
                  'dash-renderer==1.0.0',
                  'dash-table==4.1.0',
                  'dask==2.1.0',
                  'decorator==4.4.0',
                  'Flask==1.1.1',
                  'Flask-Compress==1.4.0',
                  'gunicorn==19.9.0',
                  'html5lib==1.0.1',
                  'idna==2.8',
                  'ipython-genutils==0.2.0',
                  'itsdangerous==1.1.0',
                  'Jinja2==2.11.3',
                  'jupyter-core==4.5.0',
                  'MarkupSafe==1.1.1',
                  'nbformat==4.4.0',
                  'plotly==4.1.0',
                  'traitlets==4.3.2',
                  'Werkzeug==0.15.4',
                  'xlrd==1.0.0',
                  'openpyxl==3.0.9']

)

"""
test_emissions_calculator.py

Contains a test for the emissions_calculator script that runs through
each subcomponent to calculate DR emissions impacts and output data.

Note that this only includes a simple smoke test because
emissions_calculator simply runs through all the subcomponents,
which we test individually in each test_<subcomponent>.py file.

For all tests, we're running from within the
phase1_emissions_calculator/ folder using:
python -m unittest discover -s tests
Or for individual files:
python -m unittest tests/test_<subcompname>.py
"""
import unittest

from emissions_parameters import DIR_DATA_PROC
from emissions_calculator import main

class TestEmissionsCalc(unittest.TestCase):
    """
    Class of one unit test for the emissions calculator.
    """

    def test_calcsmoke(self):
        """
        Smoke test to make sure the emissions calculator runs.
        """
        main(DIR_DATA_PROC)

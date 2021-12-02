"""
Tests for the sub component b
"""

import unittest

from subcomp_b_process_emissions_factors import seasonal_ave, annual_ave, \
    newbins_2022_annual_ave, newbins_2022_seasonal_ave


class TestSubCompB(unittest.TestCase):
    """
    Tests for the sub component b
    """

    def test_smoke(self):
        """
        Simple smoke test to make sure function runs.
        """
        seasonal_ave()
        annual_ave()
        newbins_2022_annual_ave()
        newbins_2022_seasonal_ave()

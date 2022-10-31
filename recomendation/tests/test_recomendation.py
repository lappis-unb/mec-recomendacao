from pandas.testing import assert_frame_equal
import pytest

from recomendation import RecomendationCalculator
from recomendation.blue import BluePercentileCalculator
from recomendation.green import GreenPercentileCalculator
from recomendation.tariff import green_tariff, blue_tariff

from .util import consumption_history, expected_recomendation, expected_current_contract


B_PERCENTILES = BluePercentileCalculator.PERCENTILES
B_PERCENTILE_HEADERS = BluePercentileCalculator.PERCENTILE_HEADERS
B_SUMMARY_HEADERS = BluePercentileCalculator.SUMMARY_HEADERS

G_PERCENTILES = GreenPercentileCalculator.PERCENTILES
G_PERCENTILE_HEADERS = GreenPercentileCalculator.PERCENTILE_HEADERS
G_SUMMARY_HEADERS = GreenPercentileCalculator.SUMMARY_HEADERS


class TestRecomendation:
    ABSOLUTE_TOLERANCE = 0.01

    def setup_class(self):
        self.sut = RecomendationCalculator(
            consumption_history,
            'green',
            blue_tariff,
            green_tariff,
        )
        self.expected_current_contract = expected_current_contract
        self.expected_recomendation = expected_recomendation
        self.result = self.sut.calculate()

    @pytest.mark.order(5)
    def test_current_contract(self):
        assert_frame_equal(
            self.expected_current_contract,
            self.result.current_contract,
            check_exact=False,
            atol=self.ABSOLUTE_TOLERANCE
        )

    @pytest.mark.order(6)
    def test_tariff_type_is_green(self):
        assert 'green' == self.result.best_tariff_type

    @pytest.mark.order(7)
    def test_recomended_contract(self):
        assert_frame_equal(
            self.expected_recomendation,
            self.result.frame,
            check_exact=False,
            atol=self.ABSOLUTE_TOLERANCE
        )

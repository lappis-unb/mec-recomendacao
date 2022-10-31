from pandas import DataFrame
from pandas.testing import assert_frame_equal
import pytest
from pytest import approx

from recomendation.blue import BluePercentileCalculator
from recomendation.tariff import blue_tariff

from .util import consumption_history, b_expected_percentiles, b_expected_summary

PERCENTILES = BluePercentileCalculator.PERCENTILES
PERCENTILE_HEADERS = BluePercentileCalculator.PERCENTILE_HEADERS
SUMMARY_HEADERS = BluePercentileCalculator.SUMMARY_HEADERS

class TestBluePercentileCalculator:
    consumption_history: DataFrame
    sut: BluePercentileCalculator
    ABSOLUTE_TOLERANCE = 0.01

    def setup_class(self):
        self.consumption_history = consumption_history
        self.expected_summary = b_expected_summary
        self.expected_percentiles = b_expected_percentiles
        self.sut = BluePercentileCalculator(self.consumption_history, blue_tariff)
        self.result = self.sut.calculate()

    @pytest.mark.order(1)
    def test_calculates_percentiles(self):
        for p in PERCENTILES:
            p_str = str(p)
            assert_frame_equal(
                # Desconsidera a coluna total_in_reais,
                # que é testada nas asserções seguintes:
                self.result.percentiles[p_str].iloc[:, 0:-2],
                self.expected_percentiles[p_str].iloc[:, 0:-2],
                check_exact=False,
                atol=self.ABSOLUTE_TOLERANCE)

        assert approx(695755.82) == self.result.percentiles['0.1'].total_in_reais
        assert approx(656298.46) == self.result.percentiles['0.2'].total_in_reais
        assert approx(591048.63) == self.result.percentiles['0.3'].total_in_reais
        assert approx(563043.34) == self.result.percentiles['0.4'].total_in_reais
        assert approx(527318.02) == self.result.percentiles['0.5'].total_in_reais
        assert approx(515118.23) == self.result.percentiles['0.6'].total_in_reais
        assert approx(514027.84) == self.result.percentiles['0.7'].total_in_reais
        assert approx(516997.98) == self.result.percentiles['0.8'].total_in_reais
        assert approx(522351.99) == self.result.percentiles['0.9'].total_in_reais
        assert approx(534204.22) == self.result.percentiles['0.95'].total_in_reais
        assert approx(542520.09) == self.result.percentiles['0.98'].total_in_reais

    @pytest.mark.order(2)
    def test_calculates_summary(self):
        assert_frame_equal(
            self.result.summary,
            self.expected_summary,
            check_exact=False,
            atol=self.ABSOLUTE_TOLERANCE)

        assert approx(311.0) == self.result.summary.peak_demand_in_kw
        assert approx(467.0) == self.result.summary.off_peak_demand_in_kw
        assert approx(469740.28) == self.result.summary.total_consumption_value_in_reais
        assert approx(514027.84) == self.result.summary.smallest_total_demand_value_in_reais
        assert approx(983768.11) == self.result.summary.total_total_value_in_reais

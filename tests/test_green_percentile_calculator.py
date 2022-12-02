from pandas import DataFrame
from pandas.testing import assert_frame_equal
import pytest
from pytest import approx

from recommendation.green import GreenPercentileCalculator

from tests.recommendation.readcsv import test_cases

from tests.recommendation.readcsv import consumption_history, g_expected_summary, g_expected_percentiles

PERCENTILES = GreenPercentileCalculator.PERCENTILES
PERCENTILE_HEADERS = GreenPercentileCalculator.PERCENTILE_HEADERS
SUMMARY_HEADERS = GreenPercentileCalculator.SUMMARY_HEADERS

test_data = [(_id) for _id in test_cases.keys()]

ABSOLUTE_TOLERANCE = 0.01

@pytest.mark.parametrize('_id', test_data)
def test_blue_per_calculator(_id: str):
    data = test_cases[_id]
    consumption_history = data.consumption_history
    sut = GreenPercentileCalculator(consumption_history, data.green_tariff)
    result = sut.calculate()

    # teste percentiles
    for p in PERCENTILES:
        p_str = str(p)
        assert_frame_equal(
            # Desconsidera a coluna total_in_reais,
            # que é testada nas asserções seguintes:
            result.percentiles[p_str].iloc[:, 0:-2],
            data.expected_green_percentiles[p_str].iloc[:, 0:-2],
            check_exact=False,
            atol=ABSOLUTE_TOLERANCE)

    # teste resumo
    assert_frame_equal(
        result.summary,
        data.expected_green_summary,
        check_exact=False,
        atol=ABSOLUTE_TOLERANCE)
    
class TestGreenPercentileCalculator:
    consumption_history: DataFrame
    sut: GreenPercentileCalculator
    ABSOLUTE_TOLERANCE = 0.01

    def setup_class(self):
        self.consumption_history = consumption_history
        self.expected_summary = g_expected_summary
        self.expected_percentiles = g_expected_percentiles
        self.sut = GreenPercentileCalculator(self.consumption_history,  test_cases['1011101-5'].green_tariff)
        self.result = self.sut.calculate()

    @pytest.mark.order(3)
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

        assert approx(234371.32) == self.result.percentiles['0.1'].total_in_reais
        assert approx(201889.11) == self.result.percentiles['0.2'].total_in_reais
        assert approx(197693.86) == self.result.percentiles['0.3'].total_in_reais
        assert approx(191019.59) == self.result.percentiles['0.4'].total_in_reais
        assert approx(182700.59) == self.result.percentiles['0.5'].total_in_reais
        assert approx(178676.73) == self.result.percentiles['0.6'].total_in_reais
        assert approx(178536.73) == self.result.percentiles['0.7'].total_in_reais
        assert approx(178536.73) == self.result.percentiles['0.8'].total_in_reais
        assert approx(181325.62) == self.result.percentiles['0.9'].total_in_reais
        assert approx(186140.63) == self.result.percentiles['0.95'].total_in_reais
        assert approx(189444.40) == self.result.percentiles['0.98'].total_in_reais

    @pytest.mark.order(4)
    def test_calculates_summary(self):
        assert approx(178536.73) == self.result.summary.smallest_total_demand_value_in_reais
        assert approx(467.0) == self.result.summary.off_peak_demand_in_kw
        assert approx(745237.65) == self.result.summary.total_consumption_value_in_reais
        assert approx(180833.38) == self.result.summary.total_demand_value_in_reais
        assert approx(926071.02) ==  self.result.summary.total_total_value_in_reais

        assert_frame_equal(
            self.result.summary,
            self.expected_summary,
            check_exact=False,
            atol=self.ABSOLUTE_TOLERANCE)

from tests.recommendation.test_cases import test_cases
from pandas.testing import assert_frame_equal
import pytest
from pytest import approx

from recommendation.blue import BluePercentileCalculator


PERCENTILES = BluePercentileCalculator.PERCENTILES
ABSOLUTE_TOLERANCE = 0.01
test_data = [code for code in test_cases.keys()]

@pytest.mark.parametrize('code', test_data)
def test_blue_per_calculator(code: str):
    data = test_cases[code]
    consumption_history = data.consumption_history
    sut = BluePercentileCalculator(consumption_history, data.blue_tariff)
    result = sut.calculate()

    # teste percentiles
    for p in PERCENTILES:
        p_str = str(p)
        assert_frame_equal(
            # TODO: Desconsidera a coluna "total_in_reais",
            # que é testada na asserção seguinte. "total_in_reais" nem deveria
            # ser uma coluna. Deveria ser um escalar
            result.percentiles[p_str].drop('total_in_reais', axis=1),
            data.expected_blue_percentiles[p_str].drop('total_in_reais', axis=1),
            check_exact=False,
            atol=ABSOLUTE_TOLERANCE)

        assert approx(data.expected_blue_percentiles_total_in_reais[p_str], abs=ABSOLUTE_TOLERANCE) == result.percentiles[p_str].total_in_reais

    # teste resumo
    assert_frame_equal(
        result.summary,
        data.expected_blue_summary,
        check_exact=False,
        atol=ABSOLUTE_TOLERANCE)
    
    assert approx(data.expected_summary_scalar_values['blue']['peak_demand_in_kw'], abs=ABSOLUTE_TOLERANCE) == result.summary.peak_demand_in_kw
    assert approx(data.expected_summary_scalar_values['blue']['off_peak_demand_in_kw'], abs=ABSOLUTE_TOLERANCE) == result.summary.off_peak_demand_in_kw
    assert approx(data.expected_summary_scalar_values['blue']['total_consumption_value_in_reais'], abs=ABSOLUTE_TOLERANCE) == result.summary.total_consumption_value_in_reais
    assert approx(data.expected_summary_scalar_values['blue']['smallest_total_demand_value_in_reais'], abs=ABSOLUTE_TOLERANCE) == result.summary.smallest_total_demand_value_in_reais
    assert approx(data.expected_summary_scalar_values['blue']['total_total_value_in_reais'], abs=ABSOLUTE_TOLERANCE) == result.summary.total_total_value_in_reais

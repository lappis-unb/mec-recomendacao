from pandas.testing import assert_frame_equal
import pytest

from recommendation import RecommendationCalculator
from recommendation.blue import BluePercentileCalculator
from recommendation.green import GreenPercentileCalculator

from recommendation import RecommendationCalculator

from tests.recommendation.readcsv import test_cases

B_PERCENTILES = BluePercentileCalculator.PERCENTILES
B_PERCENTILE_HEADERS = BluePercentileCalculator.PERCENTILE_HEADERS
B_SUMMARY_HEADERS = BluePercentileCalculator.SUMMARY_HEADERS

G_PERCENTILES = GreenPercentileCalculator.PERCENTILES
G_PERCENTILE_HEADERS = GreenPercentileCalculator.PERCENTILE_HEADERS
G_SUMMARY_HEADERS = GreenPercentileCalculator.SUMMARY_HEADERS

test_data = [(_id) for _id in test_cases.keys()]

ABSOLUTE_TOLERANCE = 0.01

@pytest.mark.parametrize('_id', test_data)
def test_recommendation(_id: str):
    data = test_cases[_id]
    sut = RecommendationCalculator(
        data.consumption_history,
        data.current_tariff_flag,
        data.blue_tariff,
        data.green_tariff,
    )

    result = sut.calculate()

    assert_frame_equal(
        data.expected_current_contract,
        result.current_contract,
        check_exact=False,
        atol=ABSOLUTE_TOLERANCE)

    assert data.expected_recommended_tariff_flag == result.tariff_flag

    assert_frame_equal(
        data.expected_recommendation,
        result.frame,
        check_exact=False,
        atol=ABSOLUTE_TOLERANCE)


from pandas import DataFrame
from pandas.testing import assert_frame_equal
import pandas as pd

from recomendation import RecommendationByPercentileCalculator


class TestRecommendation:
    consumption_history: DataFrame
    sut: RecommendationByPercentileCalculator
    absolute_tolerance = 0.01

    def setup_class(self):
        self.consumption_history = pd.read_csv('data/consumption.csv', sep='\t')
        self.expected_percentiles: dict[str, DataFrame] = {}
    
        tariff = {
            'blue_peak_tusd_in_reais_per_kw': 89.29,
            'blue_peak_tusd_in_reais_per_mwh': 117.13,
            'blue_peak_te_in_reais_per_mwh': 413.03,
            'blue_off_peak_tusd_in_reais_per_kw': 31.53,
            'blue_off_peak_tusd_in_reais_per_mwh': 117.13,
            'blue_off_peak_te_in_reais_per_mwh': 260.02,
        }
        self.PERCENTILES = RecommendationByPercentileCalculator.PERCENTILES
        self.sut = RecommendationByPercentileCalculator(
            self.consumption_history,
            tariff
        )
        self.read_expected_percentiles(self)

    def test_calculates_percentiles(self):
        for p in self.PERCENTILES:
            p_str = str(p)
            assert_frame_equal(
                self.sut.percentiles[p_str], 
                self.expected_percentiles[p_str],
                check_exact=False,
                atol=self.absolute_tolerance)
        
    def read_expected_percentiles(self):
        for p in self.PERCENTILES:
            p_str = str(p)
            frame = pd.read_csv(
                f'data/blue_per_{p_str}.csv', 
                sep='\t',
                names=self.sut.PERCENTILE_COLUMNS)
            self.expected_percentiles[p_str] = frame

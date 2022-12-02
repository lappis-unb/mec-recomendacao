import pandas as pd
import json
from os.path import join
from pandas import DataFrame

from recommendation.green import GreenPercentileCalculator, GreenTariff
from recommendation.blue import BluePercentileCalculator, BlueTariff
from recommendation import ContractRecommendationCalculator

HISTORY_HEADERS = ['consumption_peak_in_kwh', 'consumption_off_peak_in_kwh', 'measured_peak_demand_in_kw', 'measured_off_peak_demand_in_kw',
                   'contract_peak_demand_in_kw', 'contract_off_peak_demand_in_kw', 'peak_exceeded_in_kw', 'off_peak_exceeded_in_kw']

B_PERCENTILES = BluePercentileCalculator.PERCENTILES
B_PERCENTILE_HEADERS = BluePercentileCalculator.PERCENTILE_HEADERS
B_SUMMARY_HEADERS = BluePercentileCalculator.SUMMARY_HEADERS

G_PERCENTILES = GreenPercentileCalculator.PERCENTILES
G_PERCENTILE_HEADERS = GreenPercentileCalculator.PERCENTILE_HEADERS
G_SUMMARY_HEADERS = GreenPercentileCalculator.SUMMARY_HEADERS

RECOMENDATION_HEADERS = ContractRecommendationCalculator.HEADERS

CURRENT_CONTRACT_HEADERS = ContractRecommendationCalculator.CURRENT_CONTRACT_HEADERS

SEP = '\t'

class CsvData:
    current_tariff_flag: str
    consumption_history: DataFrame
    blue_tariff: BlueTariff
    green_tariff: GreenTariff
    expected_recommended_tariff_flag: str
    expected_blue_percentiles: dict[str, DataFrame]
    expected_green_percentiles: dict[str, DataFrame]
    expected_blue_summary: DataFrame
    expected_green_summary: DataFrame
    expected_current_contract: DataFrame
    expected_recommendation: DataFrame

class CsvReader:
    def __init__(self, uc_id: str):
        data_path = join('tests', 'recommendation', 'data')
        self.path = join(data_path, f'uc_{uc_id}')
    
    def run(self) -> CsvData:
        data = CsvData()
        data.consumption_history = self._read_consumption_history(HISTORY_HEADERS)
        data.expected_blue_percentiles = self._read_expected_percentiles('blue_per_%s.csv', B_PERCENTILES, B_PERCENTILE_HEADERS)
        data.expected_green_percentiles = self._read_expected_percentiles('green_per_%s.csv', G_PERCENTILES, G_PERCENTILE_HEADERS)
        data.expected_blue_summary = self._read_expected_summary('blue', B_SUMMARY_HEADERS)
        data.expected_green_summary = self._read_expected_summary('green', G_SUMMARY_HEADERS)
        data.expected_recommendation = pd.read_csv(join(self.path, 'recommendation.csv'), names=RECOMENDATION_HEADERS, sep=SEP)
        data.expected_current_contract = pd.read_csv(join(self.path, 'current_contract.csv'), names=CURRENT_CONTRACT_HEADERS, sep=SEP)
        fj = open(join(self.path, 'tariff.json'))
        tariff = json.load(fj)
        data.blue_tariff = BlueTariff(**tariff['blue'])
        data.green_tariff = GreenTariff(**tariff['green'])
        f1 = open(join(self.path, 'recommended_tariff_flag.txt'))
        f2 = open(join(self.path, 'current_tariff_flag.txt'))
        data.expected_recommended_tariff_flag = f1.read().strip()
        data.current_tariff_flag = f2.read().strip()
        f1.close()
        f2.close()
        fj.close()
        return data

    def _read_consumption_history(self, headers: list[str]) -> DataFrame:
        return pd.read_csv(join(self.path, 'consumption.csv'), sep=SEP, names=headers)


    def _read_expected_percentiles(self, 
        filename_template: str,
        percentiles: list[float],
        percentile_headers: list[str]
    ) -> 'dict[str, DataFrame]':
        expected_percentiles = {}
        for p in percentiles:
            p_str = str(p)
            frame = pd.read_csv(
                join(self.path, filename_template % p_str),
                sep='\t',
                names=percentile_headers)
            expected_percentiles[p_str] = frame
        return expected_percentiles


    def _read_expected_summary(self, color: str, summary_headers: list[str]) -> DataFrame:
        return pd.read_csv(
            join(self.path, f'{color}_per_summary.csv'), 
            sep='\t', 
            names=summary_headers)


# Os casos de teste estão em recommendation/tests/data/uc_{id}/**
# Esses id's devem entrar na lista abaixo:
__ucs_ids = [
    '1011101-5',
    # '9006211',
]

def __setup_test_cases():
    readers = [CsvReader(_id) for _id in __ucs_ids]
    datas = [reader.run() for reader in readers]

    test_cases: dict[str, CsvData] = {}
    for _id, data in zip(__ucs_ids, datas):
        test_cases[_id] = data
    
    return test_cases

test_cases = __setup_test_cases()

consumption_history = test_cases['1011101-5'].consumption_history
b_expected_percentiles = test_cases['1011101-5'].expected_blue_percentiles
g_expected_percentiles = test_cases['1011101-5'].expected_green_percentiles
b_expected_summary = test_cases['1011101-5'].expected_blue_summary
g_expected_summary = test_cases['1011101-5'].expected_green_summary
expected_recommendation = test_cases['1011101-5'].expected_recommendation
expected_current_contract = test_cases['1011101-5'].expected_current_contract

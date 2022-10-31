import pandas as pd
from pandas import DataFrame

from recomendation.green import GreenPercentileCalculator, GreenTariff
from recomendation.blue import BluePercentileCalculator, BlueTariff
from recomendation import ContractRecomendationCalculator

B_PERCENTILES = BluePercentileCalculator.PERCENTILES
B_PERCENTILE_HEADERS = BluePercentileCalculator.PERCENTILE_HEADERS
B_SUMMARY_HEADERS = BluePercentileCalculator.SUMMARY_HEADERS

G_PERCENTILES = GreenPercentileCalculator.PERCENTILES
G_PERCENTILE_HEADERS = GreenPercentileCalculator.PERCENTILE_HEADERS
G_SUMMARY_HEADERS = GreenPercentileCalculator.SUMMARY_HEADERS

RECOMENDATION_HEADERS = ContractRecomendationCalculator.COLUMNS

CURRENT_CONTRACT_COLUMNS = ContractRecomendationCalculator.CURRENT_CONTRACT_COLUMNS

def read_consumption_history(headers: list[str]) -> DataFrame:
    return pd.read_csv('data/consumption.csv', sep='\t', names=headers)


def read_expected_percentiles(
    path_template: str,
    percentiles: list[float],
    percentile_headers: list[str]
) -> 'dict[str, DataFrame]':
    expected_percentiles = {}
    for p in percentiles:
        p_str = str(p)
        frame = pd.read_csv(
            path_template % p_str,
            sep='\t',
            names=percentile_headers)
        expected_percentiles[p_str] = frame
    return expected_percentiles


def read_expected_summary(path: str, summary_headers: list[str]) -> DataFrame:
    return pd.read_csv(path, sep='\t', names=summary_headers)


HISTORY_HEADERS = ['consumption_peak_in_kwh', 'consumption_off_peak_in_kwh', 'measured_peak_demand_in_kw', 'measured_off_peak_demand_in_kw', 'contract_peak_demand_in_kw', 'contract_off_peak_demand_in_kw', 'peak_exceeded_in_kw', 'off_peak_exceeded_in_kw']
consumption_history = read_consumption_history(HISTORY_HEADERS)

b_expected_percentiles = read_expected_percentiles('data/blue_per_%s.csv', B_PERCENTILES, B_PERCENTILE_HEADERS)
g_expected_percentiles = read_expected_percentiles('data/green_per_%s.csv', G_PERCENTILES, G_PERCENTILE_HEADERS)

b_expected_summary = read_expected_summary('data/blue_per_summary.csv', B_SUMMARY_HEADERS)
g_expected_summary = read_expected_summary('data/green_per_summary.csv', G_SUMMARY_HEADERS)

expected_recomendation = pd.read_csv('data/recomendation.csv', sep='\t', names=RECOMENDATION_HEADERS)

expected_current_contract = pd.read_csv('data/current_contract.csv', sep='\t', names=CURRENT_CONTRACT_COLUMNS)
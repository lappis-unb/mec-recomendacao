from typing import Literal
from pandas import DataFrame
from recommendation.green import GreenPercentileCalculator, GreenPercentileResult, GreenTariff
from recommendation.blue import BluePercentileCalculator, BluePercentileResult, BlueTariff


class ContractRecommendationResult:
    '''
    Deve refletir a tabela final de Template 2!Tabelas
    '''

    def __init__(self):
        self.frame: DataFrame
        self.current_contract: DataFrame
        self.recommended_tariff_flag = ''
        self.recommended_off_peak_demand_in_kw = .0


class ContractRecommendationCalculator:
    '''
    Não sei se precisa disso tudo como argumento no construtor
    '''
    HEADERS = ['recommended_peak_demand_in_kw', 'recommended_off_peak_demand_in_kw',
               'consumption_value_in_reais', 'demand_value_in_reais',
               'recommended_contract_value_in_reais',
               'percentage_consumption', 'percentage_demand',
               'absolute_difference', 'percentage_difference']

    CURRENT_CONTRACT_HEADERS = ['consumption_value_in_reais', 'demand_value_in_reais',
                                'current_value_in_reais', 'percentage_consumption',
                                'percentage_demand']

    def __init__(
        self,
        consumption_history: DataFrame,
        blue_summary: BluePercentileResult,
        green_summary: GreenPercentileResult,
        current_tariff_flag: Literal['blue', 'green'],
        green_tariff: GreenTariff,
        blue_tariff: BlueTariff,
    ):
        self.green_tariff = green_tariff
        self.blue_tariff = blue_tariff
        self.consumption_history = consumption_history
        self.current_tariff_flag = current_tariff_flag
        self.blue_summary = blue_summary
        self.green_summary = green_summary
        self.frame = DataFrame(columns=self.HEADERS)

        self.current_contract = DataFrame(columns=self.CURRENT_CONTRACT_HEADERS)
        self._calculate_current_contract()

    def calculate(self):
        rec = ContractRecommendationResult()
        rec.current_contract = self.current_contract
        frame = DataFrame(columns=self.HEADERS)

        if self.blue_summary.total_total_value_in_reais < self.green_summary.total_total_value_in_reais:
            rec.recommended_tariff_flag = 'blue'
            frame.recommended_off_peak_demand_in_kw = self.blue_summary.off_peak_demand_in_kw
            frame.consumption_value_in_reais = self.blue_summary.consumption_value_in_reais
            frame.demand_value_in_reais = self.blue_summary.demand_value_in_reais
        else:
            rec.recommended_tariff_flag = 'green'
            frame.recommended_off_peak_demand_in_kw = self.green_summary.off_peak_demand_in_kw
            frame.consumption_value_in_reais = self.green_summary.consumption_value_in_reais
            frame.demand_value_in_reais = self.green_summary.demand_value_in_reais

        frame.recommended_contract_value_in_reais = \
            frame.consumption_value_in_reais + frame.demand_value_in_reais

        frame.percentage_consumption = \
            frame.consumption_value_in_reais / frame.recommended_contract_value_in_reais

        frame.percentage_demand = \
            frame.demand_value_in_reais / frame.recommended_contract_value_in_reais

        frame.absolute_difference = \
            self.current_contract.current_value_in_reais - frame.recommended_contract_value_in_reais
        frame.percentage_difference = \
            1 - frame.recommended_contract_value_in_reais/self.current_contract.current_value_in_reais

        frame.recommended_peak_demand_in_kw = frame.recommended_peak_demand_in_kw.astype('float64')
        rec.frame = frame
        return rec

    def _calculate_current_contract(self):
        if self.current_tariff_flag == 'green':
            self.current_contract.consumption_value_in_reais = \
                self.consumption_history.consumption_peak_in_kwh * \
                (self.green_tariff.peak_tusd_in_reais_per_mwh + self.green_tariff.peak_te_in_reais_per_mwh) \
                / 1000 \
                + self.consumption_history.consumption_off_peak_in_kwh * \
                (self.green_tariff.off_peak_tusd_in_reais_per_mwh + self.green_tariff.off_peak_te_in_reais_per_mwh) \
                / 1000
            self.current_contract.demand_value_in_reais = \
                self.green_tariff.na_tusd_in_reais_per_kw*self.consumption_history.contract_off_peak_demand_in_kw \
                + 3*self.green_tariff.na_tusd_in_reais_per_kw * (self.consumption_history.peak_exceeded_in_kw + self.consumption_history.off_peak_exceeded_in_kw)
        else:
            # FIXME: Esse caminho não foi testado pq o contrato atual é VERDE
            self.current_contract.consumption_value_in_reais = \
                self.consumption_history.consumption_peak_in_kwh * \
                (self.blue_summary.peak_tusd_in_reais_per_mwh + self.blue_tariff.peak_te_in_reais_per_mwh) \
                / 1000 \
                + self.consumption_history.consumption_off_peak_in_kwh * \
                (self.blue_tariff.off_peak_tusd_in_reais_per_mwh + self.blue_tariff.off_peak_te_in_reais_per_mwh) \
                / 1000
            self.current_contract.demand_value_in_reais = \
                self.blue_tariff.peak_tusd_in_reais_per_kw *\
                (self.consumption_history.contract_peak_demand_in_kw + 3*self.consumption_history.peak_exceeded_in_kw) \
                + 3*self.blue_tariff.off_peak_tusd_in_reais_per_kw*self.consumption_history.off_peak_exceeded_in_kw

        self.current_contract.current_value_in_reais = \
            self.current_contract.consumption_value_in_reais + self.current_contract.demand_value_in_reais

        self.current_contract.percentage_consumption = \
            self.current_contract.consumption_value_in_reais / self.current_contract.current_value_in_reais

        self.current_contract.percentage_demand = \
            self.current_contract.demand_value_in_reais / self.current_contract.current_value_in_reais


class RecommendationResult:
    ...

class RecommendationCalculator:
    def __init__(
        self,
        consumption_history: DataFrame,
        current_tariff: str,
        blue_tariff: BlueTariff,
        green_tariff: GreenTariff
    ):
        self.current_tariff = current_tariff
        self.blue_tariff = blue_tariff
        self.green_tariff = green_tariff
        self.consumption_history = consumption_history

        self.blue_calculator = BluePercentileCalculator(consumption_history, blue_tariff)
        self.green_calculator = GreenPercentileCalculator(consumption_history, green_tariff)

    def calculate(self):
        '''
        Essa função ainda deve voltar um RecommendationResult, manipulando
        ou incluindo ContractRecommendationResult
        '''
        b_result = self.blue_calculator.calculate()
        g_result = self.green_calculator.calculate()

        rec_calculator = ContractRecommendationCalculator(
            self.consumption_history,
            b_result.summary,
            g_result.summary,
            self.current_tariff,
            self.green_tariff,
            self.blue_tariff,
        )

        rec = rec_calculator.calculate()

        return rec

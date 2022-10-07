from pandas import DataFrame


class RecommendationByPercentileCalculator():
    PERCENTILES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.98]
    PERCENTILE_COLUMNS = ['demand_peak_in_kw', 'demand_off_peak_in_kw',
                          'overshoot_peak_in_kw', 'overshoot_off_peak_in_kw',
                          'demand_total_value_in_reais']

    def __init__(self, consumption_history: DataFrame, tariff: dict[str, float]) -> None:
        self.consumption_history = consumption_history
        self.history_length = len(consumption_history.index)
        self.tariff = tariff
        self.percentiles: dict[str, DataFrame] = {}
        self.calculate_percentiles()

    def calculate_percentiles(self):
        for p in self.PERCENTILES:
            p_str = str(p)
            self.percentiles[p_str] = DataFrame(
                columns=self.PERCENTILE_COLUMNS)

            # Calcula percentil
            demand_peak_in_kw_percentile = self \
                .consumption_history\
                .measured_demand_peak_in_kw.quantile(p)
            self.percentiles[p_str].demand_peak_in_kw = [demand_peak_in_kw_percentile]*self.history_length

            # Calcula percentil
            demand_off_peak_in_kw_percentile = self\
                .consumption_history\
                .measured_demand_off_peak_in_kw.quantile(p)
            self.percentiles[p_str].demand_off_peak_in_kw = [demand_off_peak_in_kw_percentile]*self.history_length
            
            # Ultrapassagem = max(0, demanda_medidada - demanda_percentil)
            self.percentiles[p_str].overshoot_peak_in_kw = \
                self.consumption_history.measured_demand_peak_in_kw \
                - self.percentiles[p_str].demand_peak_in_kw 
            self.percentiles[p_str].overshoot_peak_in_kw = self.percentiles[p_str] \
                .overshoot_peak_in_kw.map(lambda overshoot: max(0, overshoot))

            # Ultrapassagem = max(0, demanda_medidada - demanda_percentil)
            self.percentiles[p_str].overshoot_off_peak_in_kw = \
                self.consumption_history.measured_demand_off_peak_in_kw \
                - self.percentiles[p_str].demand_off_peak_in_kw 
            self.percentiles[p_str].overshoot_off_peak_in_kw = self.percentiles[p_str] \
                .overshoot_off_peak_in_kw.map(lambda overshoot: max(0, overshoot))

            # Template de relatório: 
            # Seção 4: Metodologia de cálculo: fórmulas (2) e (3)
            # Vdemanda + Vultrapassagem
            self.percentiles[p_str].demand_total_value_in_reais = \
                self.tariff['blue_peak_tusd_in_reais_per_kw']*self.percentiles[p_str].demand_peak_in_kw\
                + 3*self.tariff['blue_peak_tusd_in_reais_per_kw']*self.percentiles[p_str].overshoot_peak_in_kw\
                + self.tariff['blue_off_peak_tusd_in_reais_per_kw']*self.percentiles[p_str].demand_off_peak_in_kw\
                + 3*self.tariff['blue_off_peak_tusd_in_reais_per_kw']*self.percentiles[p_str].overshoot_off_peak_in_kw

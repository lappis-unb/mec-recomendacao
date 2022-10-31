from recomendation.green import GreenTariff
from recomendation.blue import BlueTariff


green_tariff = GreenTariff(
    peak_tusd_in_reais_per_mwh=2280.15,
    peak_te_in_reais_per_mwh=413.03,
    off_peak_tusd_in_reais_per_mwh=117.13,
    off_peak_te_in_reais_per_mwh=260.02,
    na_tusd_in_reais_per_kw=31.53,
)

blue_tariff = BlueTariff(
    peak_tusd_in_reais_per_kw=89.29,
    peak_tusd_in_reais_per_mwh=117.13,
    peak_te_in_reais_per_mwh=413.03,
    off_peak_tusd_in_reais_per_kw=31.53,
    off_peak_tusd_in_reais_per_mwh=117.13,
    off_peak_te_in_reais_per_mwh=260.02,
)

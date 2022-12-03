from dataclasses import dataclass
from enum import Enum

class Tariff:
    BLUE = 'B'
    GREEN = 'G'

@dataclass
class BlueTariff:
    peak_tusd_in_reais_per_kw: float
    peak_tusd_in_reais_per_mwh: float
    peak_te_in_reais_per_mwh: float
    off_peak_tusd_in_reais_per_kw: float
    off_peak_tusd_in_reais_per_mwh: float
    off_peak_te_in_reais_per_mwh: float

@dataclass
class GreenTariff:
    peak_tusd_in_reais_per_mwh: float
    peak_te_in_reais_per_mwh: float
    off_peak_tusd_in_reais_per_mwh: float
    off_peak_te_in_reais_per_mwh: float
    na_tusd_in_reais_per_kw: float


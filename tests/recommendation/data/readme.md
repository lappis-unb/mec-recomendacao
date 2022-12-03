# Breve explicação sobre os dados

## Estrutura de pastas

`data/uc_<id da UC>`:
- entradas:
    - histórico de consumo
    - modalidade tarifa atual
- saídas esperadas:
    - percentis azul/verde `[0.1 -> 0.98]`
    - resumo azul/verde. Com as colunas
        - demanda ponta 
        - demanda fora de ponta 
        - ultrapassagem ponta 
        - ultrapassagem fora de ponta 
        - valor total de demanda
    - recomendação de contrato
    - recomendação de bandeira de tarifa

### Valores escalares
Um `DataFrame` do Pandas não armazena valores escalares, apenas valores do 
tipo lista (Series). Ainda assim, os valores dos arquivos a seguir foram 
armazenados como columas (Series) até ser encontrada uma representação melhor.

`per_total_in_reais.json`: contém os totais de valores em reais de cada 
percentil (0.1 -> 0.98) pra cada modalidade (azul e verde).

`summary_scalar_values.json`: contém os dados:

```json
{
    "blue": {
        "smallest_total_demand_value_in_reais": 0.00,
        "off_peak_demand_in_kw": 0.00,
        "peak_demand_in_kw": 0.00,
        "total_consumption_value_in_reais": 0.00,
        "total_total_value_in_reais": 0.00,
    },
    "green": {
        "smallest_total_demand_value_in_reais": 0.00,
        "off_peak_demand_in_kw": 0.00,
        "total_consumption_value_in_reais": 0.00,
        "total_demand_value_in_reais": 0.00,
        "total_total_value_in_reais": 0.00,
    }
}
```

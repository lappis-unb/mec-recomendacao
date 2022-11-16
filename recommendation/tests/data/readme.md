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

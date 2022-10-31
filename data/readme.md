# Breve explicação sobre esses dados

`blue_per_*.csv` são os cálculos de

- demanda ponta 
- demanda fora de ponta 
- ultrapassagem ponta 
- ultrapassagem fora de ponta 
- valor total de demanda

para cada percentil na planilha Template 2 na modalidade
Azul. Essa lista tbm são as colunas desses arquivos csv.

`blue_per_summary.csv` é o quadro em azul, chamado de "resumo" na planilha.

ROUNDUP(
    SWITCH(
        SMALL(
            {
                'Análise da tarifa azul'!$G$24;
                'Análise da tarifa azul'!$L$24;
                'Análise da tarifa azul'!$Q$24;
                'Análise da tarifa azul'!$V$24;
                'Análise da tarifa azul'!$AA$24;
                'Análise da tarifa azul'!$AF$24;
                'Análise da tarifa azul'!$AA$47;
                'Análise da tarifa azul'!$V$47;
                'Análise da tarifa azul'!$Q$47;
                'Análise da tarifa azul'!$L$47;
                'Análise da tarifa azul'!$G$47
            },
            1
        ),
            'Análise da tarifa azul'!$G$24,
            'Análise da tarifa azul'!C4,
            'Análise da tarifa azul'!$L$24,
            'Análise da tarifa azul'!H4,
            'Análise da tarifa azul'!$Q$24,
            'Análise da tarifa azul'!M4,
            'Análise da tarifa azul'!$V$24,
            'Análise da tarifa azul'!R4,
            'Análise da tarifa azul'!$AA$24,
            'Análise da tarifa azul'!W4,
            'Análise da tarifa azul'!$AF$24,
            'Análise da tarifa azul'!AB4,
            'Análise da tarifa azul'!$G$47,
            'Análise da tarifa azul'!C27,
            'Análise da tarifa azul'!$L$47,
            'Análise da tarifa azul'!H27,
            'Análise da tarifa azul'!$Q$47,
            'Análise da tarifa azul'!M27,
            'Análise da tarifa azul'!$V$47,
            'Análise da tarifa azul'!R27,
            'Análise da tarifa azul'!$AA$47,
            'Análise da tarifa azul'!W27)
            *1.05
        )


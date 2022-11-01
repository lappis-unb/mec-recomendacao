# Módulo de Recomendação de Contrato

Este repositório é um local temporário pra ir 
rascunhando o módulo de recomendação do contrato.

## Visão geral

"Arquitetura" das calculadoras:

    RecomendationCalculator
        BlueCalculator | GreenCalculator
        ContractRecomendationCalculator

    Entrada -> RecomendationCalculator -> Saída

O `|` é pra indicar que não há uma ordem obrigatória entre verde e azul.

**Entrada**
- histórico de consumo
- modalidade tarifa atual
- tarifa azul
- tarifa verde

**Saída**
- tabela do contrato atual
- tabela do contrato recomendado
- e outras coisas a serem definidas

## Setup

Esse repositório foi desenvolvido com Python 3.10.5, mas deve funcionar
com qualquer versão 3.6+.

Instale as dependências

    pip install -r requirements.txt

Pytest é o framework de testes.

## Executar

Rodar todos os testes

    pytest

Rodar um teste específico

    pytest -k 'test_blue_percentile_calculator'

Se `pytest` não for um comando reconhecido na sua máquina, substitua `pytest`
por `python -m pytest`:

    python -m pytest -k 'test_blue_percentile_calculator'

`python` deve ser um comando válido.

Relatório de cobertura:
    
    pytest --cov

Para gerar relatório de cobertura em HTML:

    pytest --cov --cov-report html

Depois abra o arquivo `coverage/index.html` no navegador.

Para mais informações sobre cobertura de testes, leia a 
[documentação](https://pytest-cov.readthedocs.io/en/latest/).

**Note** que testes marcados com `@pytest.mark.order` precisam ser 
executados em uma ordem específica. Em especial, provavelmente apenas o teste 
marcado com `@pytest.mark.order(1)` pode ser executado isoladamente.

Para saber mais sobre como filtrar testes por módulo, classes ou métodos, consulte
a [documentação do Pytest](https://docs.pytest.org/en/4.6.x/example/markers.html#using-k-expr-to-select-tests-based-on-their-name).

## Entrada e saída

Até o momento desta escrita, o arquivo `data/consumption.csv` contém os dados de
entrada do cálculo, enquanto que os arquivos `data/{blue|green}_per_*.csv` são 
respostas esperadas para os testes.

Algumas das respostas esperadas estão hard coded nos casos de teste. Esses valores,
assim como os dos arquivos, foram obtidos diretamente da planilha.

Para ter uma ideia dos dados de entrada e saída e suas formas, dê uma
olhada em [docs/entrada-saida.md](docs/entrada-saida.md).
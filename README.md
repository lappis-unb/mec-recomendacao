# Módulo de Recomendação de Contrato

Este repositório é um local temporário pra ir 
rascunhando o módulo de recomendação do contrato.

**IMPORTANTE**: 
para ter uma ideia melhor sobre como estão organizados os casos de teste
e como são os formatos dos dados de entrada e saída, dê uma olhada 
[aqui](tests/recommendation/data/readme.md).

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

Para saber mais sobre como filtrar testes por módulo, classes ou métodos, consulte
a [documentação do Pytest](https://docs.pytest.org/en/4.6.x/example/markers.html#using-k-expr-to-select-tests-based-on-their-name).

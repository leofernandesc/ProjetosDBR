# DBR Mudanças — Dashboards operacionais

Aplicação em **Python + Streamlit** para visualizar informações operacionais de uma empresa de mudanças e transportes e gerar relatórios de acompanhamento.

## Problema e solução

Dados de operação registrados em planilhas podem dificultar a consulta rápida de status, prazos e indicadores. O projeto reúne visualizações e recursos de relatório em uma interface de consulta, com identidade visual da DBR Mudanças & Transportes.

Funcionalidades presentes no código:
- Importação de planilhas para análise.
- Visualizações e filtros de acompanhamento.
- Tabelas e indicadores operacionais.
- Geração de relatórios em PDF.

O repositório inclui a aplicação principal na raiz e uma versão específica do painel de mudanças em `dashboard_mudancas_2026/`.

## Ferramentas e papel da IA

**Stack:** Streamlit, pandas, Plotly, Altair, openpyxl e ReportLab.

O projeto foi desenvolvido com apoio de ferramentas de IA para acelerar iterações de implementação e apresentação dos dados. A aplicação, entretanto, **não depende de um modelo de IA para funcionar**; seus indicadores são calculados a partir dos dados fornecidos.

Resultados como horas economizadas ou conversões comerciais só devem ser apresentados quando houver medição documentada.

## Rodar localmente

Requer Python 3 e uma planilha no formato esperado pela aplicação.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Para executar a versão separada de acompanhamento de mudanças:

```bash
streamlit run dashboard_mudancas_2026/app.py
```

Consulte o [guia do dashboard de mudanças](dashboard_mudancas_2026/README.md) para o esquema de entrada.

## Privacidade dos dados

**Não publique planilhas reais de clientes, endereços, contatos ou informações financeiras** como exemplos. Demonstrações públicas devem utilizar dados fictícios e devem ocultar quaisquer informações comerciais sensíveis.

Este README descreve o projeto e como executá-lo; não indica que dados operacionais reais estejam disponíveis neste repositório.

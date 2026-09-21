# Dashboard de Mudanças — DBR

Dashboard Streamlit para acompanhar mudanças em aberto da DBR Mudanças & Transportes.

## Uso

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Depois, envie pelo painel lateral a planilha `Dashboard_Mudancas_2026.xlsx`.

O arquivo deve conter uma aba `Base de Dados` com as colunas `Nome`, `Origem`, `Destino`, `Data da Mudança`, `Tipo` e `Status`. As colunas de dias e situação são recalculadas pelo dashboard.

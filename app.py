import os
from io import BytesIO

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Dashboard Entradas e Saidas 2026",
    layout="wide",
)

CAMINHO_REPO = os.path.join(os.path.dirname(__file__), "data", "Entradas e saidas 2026.xlsx")
CAMINHO_LOCAL = os.path.join(
    os.path.expanduser("~"), "Downloads", "Entradas e saidas 2026.xlsx"
)

ORDEM_MESES = {
    "Janeiro": 1, "Fevereiro": 2, "Marco": 3, "Abril": 4,
    "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
    "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12,
}

MESES_ABREV = {
    "jan": "Janeiro", "fev": "Fevereiro", "mar": "Marco",
    "abr": "Abril", "mai": "Maio", "jun": "Junho",
    "jul": "Julho", "ago": "Agosto", "set": "Setembro",
    "out": "Outubro", "nov": "Novembro", "dez": "Dezembro",
}

MESES_EXTENSO = {
    "janeiro": "Janeiro", "fevereiro": "Fevereiro",
    "marco": "Marco", "marça": "Marco", "março": "Marco",
    "abril": "Abril", "maio": "Maio",
    "junho": "Junho", "julho": "Julho", "agosto": "Agosto",
    "setembro": "Setembro", "outubro": "Outubro",
    "novembro": "Novembro", "dezembro": "Dezembro",
}


def normalizar_mes(valor):
    if pd.isna(valor):
        return valor
    texto = str(valor).strip().lower()
    if texto in MESES_ABREV:
        return MESES_ABREV[texto]
    if texto in MESES_EXTENSO:
        return MESES_EXTENSO[texto]
    return str(valor).strip().title()


@st.cache_data
def carregar_dados(arquivo):
    try:
        if isinstance(arquivo, bytes):
            xls = pd.ExcelFile(BytesIO(arquivo))
        else:
            xls = pd.ExcelFile(arquivo)
    except FileNotFoundError:
        st.error("Arquivo nao encontrado: " + str(arquivo))
        st.stop()
    except Exception as e:
        st.error(f"Arquivo corrompido ou invalido: {e}")
        st.stop()

    try:
        df_receitas = pd.read_excel(xls, sheet_name="Base CR")
        df_receitas = df_receitas.drop(columns=["Unnamed: 0"], errors="ignore")
        rename_mes = {
            col: "Mes" for col in df_receitas.columns
            if str(col).lower().strip() in ("mês", "mes")
        }
        df_receitas = df_receitas.rename(columns=rename_mes)
        df_receitas = df_receitas.dropna(subset=["Data", "Valor"])
        df_receitas["Valor"] = pd.to_numeric(df_receitas["Valor"], errors="coerce")
        df_receitas["Data"] = pd.to_datetime(df_receitas["Data"], errors="coerce")
        df_receitas = df_receitas.dropna(subset=["Valor", "Data"])
        for col in ["Mes", "Tipo", "Cliente"]:
            if col in df_receitas.columns and df_receitas[col].dtype == object:
                df_receitas[col] = df_receitas[col].str.strip()
        df_receitas["Mes"] = df_receitas["Mes"].apply(normalizar_mes)
        df_receitas["Mes_num"] = df_receitas["Mes"].map(ORDEM_MESES)
    except Exception as e:
        st.error(f"Erro ao processar receitas: {e}")
        st.stop()

    try:
        df_despesas = pd.read_excel(xls, sheet_name="Base CP", header=1)
        df_despesas.columns = ["Data", "Mes", "Descricao", "Orcado", "Realizado"]
        df_despesas = df_despesas.dropna(subset=["Data", "Descricao"])
        df_despesas["Orcado"] = pd.to_numeric(
            df_despesas["Orcado"], errors="coerce"
        ).fillna(0)
        df_despesas["Realizado"] = pd.to_numeric(
            df_despesas["Realizado"], errors="coerce"
        ).fillna(0)
        df_despesas["Data"] = pd.to_datetime(df_despesas["Data"], errors="coerce")
        df_despesas = df_despesas.dropna(subset=["Data"])
        for col in ["Mes", "Descricao"]:
            if col in df_despesas.columns and df_despesas[col].dtype == object:
                df_despesas[col] = df_despesas[col].str.strip()
        df_despesas["Mes"] = df_despesas["Mes"].apply(normalizar_mes)
        df_despesas["Mes_num"] = df_despesas["Mes"].map(ORDEM_MESES)
    except Exception as e:
        st.error(f"Erro ao processar despesas: {e}")
        st.stop()

    return df_receitas, df_despesas


arquivo_repo_existe = os.path.exists(CAMINHO_REPO)
arquivo_local_existe = os.path.exists(CAMINHO_LOCAL)

uploaded_file = st.sidebar.file_uploader(
    "Atualizar planilha (opcional)",
    type=["xlsx"],
)

if uploaded_file is not None:
    df_receitas, df_despesas = carregar_dados(uploaded_file.getvalue())
elif arquivo_repo_existe:
    df_receitas, df_despesas = carregar_dados(CAMINHO_REPO)
elif arquivo_local_existe:
    df_receitas, df_despesas = carregar_dados(CAMINHO_LOCAL)
else:
    st.info(
        "Nenhuma planilha encontrada. "
        "Use o upload na barra lateral para carregar o arquivo."
    )
    st.stop()

if st.sidebar.button("Atualizar dados"):
    st.cache_data.clear()
    st.rerun()

if df_receitas.empty and df_despesas.empty:
    st.warning("Nenhum dado encontrado na planilha.")
    st.stop()

st.title("Dashboard Entradas e Saidas 2026")

meses_rec = sorted(
    df_receitas["Mes"].dropna().unique(),
    key=lambda x: ORDEM_MESES.get(x, 99),
) if not df_receitas.empty else []

meses_desp = sorted(
    df_despesas["Mes"].dropna().unique(),
    key=lambda x: ORDEM_MESES.get(x, 99),
) if not df_despesas.empty else []

todos_meses = sorted(
    set(meses_rec + meses_desp),
    key=lambda x: ORDEM_MESES.get(x, 99),
)

tipos_receita = sorted(df_receitas["Tipo"].dropna().unique()) if not df_receitas.empty else []
descricoes_despesa = sorted(df_despesas["Descricao"].dropna().unique()) if not df_despesas.empty else []

st.sidebar.header("Filtros")

meses_selecionados = st.sidebar.multiselect(
    "Mes",
    options=todos_meses,
    default=todos_meses,
)

tipos_selecionados = st.sidebar.multiselect(
    "Tipo de Receita",
    options=tipos_receita,
    default=tipos_receita,
)

descricoes_selecionadas = st.sidebar.multiselect(
    "Descricao de Despesa",
    options=descricoes_despesa,
    default=descricoes_despesa,
)

df_rec_filtrado = df_receitas[
    (df_receitas["Mes"].isin(meses_selecionados))
    & (df_receitas["Tipo"].isin(tipos_selecionados))
] if not df_receitas.empty else df_receitas

df_desp_filtrado = df_despesas[
    (df_despesas["Mes"].isin(meses_selecionados))
    & (df_despesas["Descricao"].isin(descricoes_selecionadas))
] if not df_despesas.empty else df_despesas

total_receitas = df_rec_filtrado["Valor"].sum() if not df_rec_filtrado.empty else 0.0
total_orcado = df_desp_filtrado["Orcado"].sum() if not df_desp_filtrado.empty else 0.0
total_realizado = df_desp_filtrado["Realizado"].sum() if not df_desp_filtrado.empty else 0.0
saldo = total_receitas - total_realizado

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Receitas", f"R$ {total_receitas:,.2f}")
col2.metric("Despesas Orcadas", f"R$ {total_orcado:,.2f}")
col3.metric("Despesas Realizadas", f"R$ {total_realizado:,.2f}")
col4.metric("Saldo", f"R$ {saldo:,.2f}")

st.header("Receitas")
st.dataframe(df_rec_filtrado, width="stretch")

st.header("Despesas")
st.dataframe(df_desp_filtrado, width="stretch")

ORDEM_CRONOLOGICA = [m for m in ORDEM_MESES if m in set(meses_rec + meses_desp)]

if not df_rec_filtrado.empty:
    st.header("Receitas por Tipo e Mes")
    receitas_chart = df_rec_filtrado.groupby(["Mes", "Tipo"])["Valor"].sum().reset_index()
    receitas_chart["Mes"] = pd.Categorical(
        receitas_chart["Mes"], categories=ORDEM_CRONOLOGICA, ordered=True
    )
    receitas_chart = receitas_chart.sort_values("Mes")
    fig_receitas = (
        alt.Chart(receitas_chart)
        .mark_bar()
        .encode(
            x=alt.X("Mes", sort=ORDEM_CRONOLOGICA, title="Mes"),
            y=alt.Y("Valor", title="Valor (R$)"),
            color=alt.Color("Tipo", title="Tipo de Receita"),
            tooltip=[
                alt.Tooltip("Mes", title="Mes"),
                alt.Tooltip("Tipo", title="Tipo de Receita"),
                alt.Tooltip("Valor", title="Valor (R$)", format=".2f"),
            ],
        )
    )
    st.altair_chart(fig_receitas, use_container_width=True)

if not df_desp_filtrado.empty:
    st.header("Despesas: Orcado vs Realizado por Mes")
    despesas_agg = (
        df_desp_filtrado.groupby("Mes")
        .agg({"Orcado": "sum", "Realizado": "sum"})
        .reset_index()
    )
    despesas_chart = despesas_agg.melt(
        id_vars="Mes", value_vars=["Orcado", "Realizado"],
        var_name="Categoria", value_name="Valor"
    )
    despesas_chart["Mes"] = pd.Categorical(
        despesas_chart["Mes"], categories=ORDEM_CRONOLOGICA, ordered=True
    )
    despesas_chart = despesas_chart.sort_values("Mes")
    fig_despesas = (
        alt.Chart(despesas_chart)
        .mark_line(point=True)
        .encode(
            x=alt.X("Mes", sort=ORDEM_CRONOLOGICA, title="Mes"),
            y=alt.Y("Valor", title="Valor (R$)"),
            color=alt.Color("Categoria", title="Tipo"),
            tooltip=[
                alt.Tooltip("Mes", title="Mes"),
                alt.Tooltip("Categoria", title="Tipo"),
                alt.Tooltip("Valor", title="Valor (R$)", format=".2f"),
            ],
        )
    )
    st.altair_chart(fig_despesas, use_container_width=True)
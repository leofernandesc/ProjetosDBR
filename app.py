from io import BytesIO
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
LOGO_PATH = APP_DIR / "assets" / "dbr.jpg"
DBR_NAVY = "#17245B"
DBR_BLUE = "#3547A5"
DBR_YELLOW = "#F3C400"
DBR_PALETTE = [DBR_NAVY, DBR_BLUE, "#5263C7", "#7181D8", "#9AA7E8"]
DBR_BACKGROUND = "#FFF9E6"
DBR_SURFACE = "#FFF4C4"
DBR_INPUT = "#FFFBEF"
DBR_CHROME = "#FFF1B8"
DBR_BORDER = "#E6CF72"
DBR_TABLE_BACKGROUND = "#F4F6FF"
DBR_TABLE_ALT = "#EAF0FF"
DBR_TABLE_BORDER = "#B8C4F0"

st.set_page_config(
    page_title="Dashboard Entradas e Saídas | DBR",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
        :root,
        html,
        body,
        #root,
        .stApp {{
            --primary-color: {DBR_BLUE} !important;
            --background-color: {DBR_BACKGROUND} !important;
            --secondary-background-color: {DBR_CHROME} !important;
            --text-color: {DBR_NAVY} !important;
            --dataframe-header-background-color: {DBR_CHROME} !important;
        }}
        html, body, #root,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > div,
        [data-testid="stMain"],
        [data-testid="stMain"] > div,
        [data-testid="stMainBlockContainer"],
        section.main,
        section.main > div,
        .main,
        .block-container {{ background-color: {DBR_BACKGROUND} !important; }}
        [data-testid="stDecoration"],
        [data-testid="stHeader"],
        header[data-testid="stHeader"],
        header[data-testid="stHeader"] > div,
        [data-testid="stToolbar"] {{ background-color: {DBR_CHROME} !important; }}
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] > div:first-child,
        [data-testid="stSidebarContent"],
        [data-testid="stSidebarUserContent"] {{ background-color: {DBR_CHROME} !important; border-right: 1px solid {DBR_BORDER} !important; }}
        #MainMenu,
        [data-testid="stMainMenu"] {{ visibility: hidden !important; pointer-events: none !important; height: 0 !important; }}
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapsedControl"] *,
        button[aria-label*="sidebar" i],
        button[title*="sidebar" i] {{ visibility: visible !important; display: flex !important; pointer-events: auto !important; height: auto !important; }}
        [data-testid="stVerticalBlockBorderWrapper"] {{ background-color: {DBR_SURFACE} !important; border: 1px solid {DBR_BORDER} !important; }}
        [data-testid="stMetric"] {{
            background-color: {DBR_SURFACE} !important;
            border: 1px solid {DBR_BORDER} !important;
            border-top: 4px solid {DBR_YELLOW};
            border-radius: 14px;
            padding: 14px 16px;
            box-shadow: 0 5px 16px rgba(23, 36, 91, 0.06);
        }}
        [data-testid="stFileUploader"],
        [data-testid="stFileUploader"] section,
        [data-testid="stDataFrame"],
        [data-testid="stAlert"],
        [data-testid="stAlert"] > div,
        [data-testid="stExpander"],
        [data-testid="stExpander"] > details {{ background-color: {DBR_SURFACE} !important; border-color: {DBR_BORDER} !important; }}
        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div,
        [data-baseweb="textarea"],
        [data-testid="stTextInput"] input,
        [data-testid="stDateInput"] input {{ background-color: {DBR_INPUT} !important; color: {DBR_NAVY} !important; border-color: {DBR_BORDER} !important; }}
        [data-baseweb="select"] input,
        [data-baseweb="menu"],
        [data-baseweb="popover"],
        [data-baseweb="popover"] > div,
        [data-baseweb="calendar"],
        [role="listbox"],
        [role="option"] {{ background-color: {DBR_INPUT} !important; color: {DBR_NAVY} !important; }}
        [data-baseweb="menu"] *,
        [data-baseweb="popover"] *,
        [data-baseweb="calendar"] *,
        [role="listbox"] *,
        [role="option"] * {{ color: {DBR_NAVY} !important; }}
        [data-baseweb="menu"] [aria-selected="true"],
        [role="option"][aria-selected="true"] {{ background-color: {DBR_CHROME} !important; }}
        [data-baseweb="tag"] {{ background-color: {DBR_CHROME} !important; color: {DBR_NAVY} !important; }}
        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploader"] section > div,
        [data-testid="stFileUploaderDropzone"] {{ background-color: {DBR_INPUT} !important; border-color: {DBR_BORDER} !important; color: {DBR_NAVY} !important; }}
        [data-testid="stAlert"] *,
        [data-testid="stFileUploader"] * {{ color: {DBR_NAVY} !important; }}
        .dbr-table-wrap {{
            background: {DBR_TABLE_BACKGROUND};
            border: 1px solid {DBR_TABLE_BORDER};
            border-radius: 14px;
            overflow-x: auto;
            margin: 0 0 18px;
        }}
        .dbr-data-table {{
            border-collapse: collapse;
            color: {DBR_NAVY};
            font-size: 0.92rem;
            min-width: 100%;
            background: {DBR_TABLE_BACKGROUND};
        }}
        .dbr-data-table th {{ background: {DBR_BLUE}; color: white; font-weight: 800; padding: 10px 12px; text-align: left; white-space: nowrap; }}
        .dbr-data-table td {{ background: {DBR_TABLE_BACKGROUND}; border-top: 1px solid {DBR_TABLE_BORDER}; padding: 9px 12px; white-space: nowrap; }}
        .dbr-data-table tr:nth-child(even) td {{ background: {DBR_TABLE_ALT}; }}
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {{ color: {DBR_NAVY}; }}
        [data-testid="stMetricLabel"] {{ color: #667085; }}
        [data-testid="stMetricValue"] {{ color: {DBR_NAVY}; }}
        .dbr-hero {{
            background: linear-gradient(115deg, {DBR_NAVY} 0%, {DBR_BLUE} 100%);
            color: white;
            border-radius: 18px;
            padding: 22px 26px;
            margin: 4px 0 22px;
            box-shadow: 0 10px 26px rgba(23, 36, 91, 0.18);
        }}
        .dbr-kicker {{ color: {DBR_YELLOW}; font-size: 0.78rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; }}
        .dbr-title {{ font-size: 2rem; font-weight: 800; line-height: 1.1; margin: 4px 0; }}
        .dbr-subtitle {{ color: #E8ECFF; margin: 0; }}
        .stButton > button {{ border-color: {DBR_BLUE}; color: {DBR_NAVY}; }}
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    st.markdown("### Fonte de dados")
    uploaded_file = st.file_uploader(
        "Selecione a planilha Entradas e Saidas 2026 (.xlsx)",
        type=["xlsx"],
        help="A planilha precisa conter as abas Base CR e Base CP.",
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


def render_table(dataframe):
    table_html = dataframe.to_html(index=False, border=0, na_rep="")
    st.markdown(
        f'<div class="dbr-table-wrap"><table class="dbr-data-table">'
        + table_html.split("<table", 1)[1].split(">", 1)[1].rsplit("</table>", 1)[0]
        + "</table></div>",
        unsafe_allow_html=True,
    )


@st.cache_data
def carregar_dados(arquivo):
    try:
        xls = pd.ExcelFile(BytesIO(arquivo))
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
        for col in ["Mes", "Tipo"]:
            if col in df_receitas.columns and df_receitas[col].dtype == object:
                df_receitas[col] = df_receitas[col].str.strip()
        df_receitas["Mes"] = df_receitas["Mes"].apply(normalizar_mes)
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
    except Exception as e:
        st.error(f"Erro ao processar despesas: {e}")
        st.stop()

    return df_receitas, df_despesas


hero_logo, hero_text = st.columns([1.15, 5])
with hero_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=190)
with hero_text:
    st.markdown(
        """
        <div class="dbr-hero">
            <div class="dbr-kicker">DBR Mudanças & Transportes</div>
            <div class="dbr-title">Dashboard de Entradas e Saídas</div>
            <p class="dbr-subtitle">Visão financeira de receitas, despesas orçadas, despesas realizadas e saldo.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if uploaded_file is None:
    st.info("Carregue a planilha acima para visualizar o dashboard.")
    st.stop()

df_receitas, df_despesas = carregar_dados(uploaded_file.getvalue())

if st.sidebar.button("Atualizar dados"):
    st.cache_data.clear()
    st.rerun()

if df_receitas.empty and df_despesas.empty:
    st.warning("Nenhum dado encontrado na planilha.")
    st.stop()

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
render_table(df_rec_filtrado)

st.header("Despesas")
render_table(df_desp_filtrado)

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
            color=alt.Color(
                "Tipo",
                title="Tipo de Receita",
                scale=alt.Scale(range=DBR_PALETTE),
            ),
            tooltip=[
                alt.Tooltip("Mes", title="Mes"),
                alt.Tooltip("Tipo", title="Tipo de Receita"),
                alt.Tooltip("Valor", title="Valor (R$)", format=".2f"),
            ],
        )
        .properties(background=DBR_SURFACE)
        .configure_axis(labelColor=DBR_NAVY, titleColor=DBR_NAVY, gridColor=DBR_BORDER)
        .configure_legend(labelColor=DBR_NAVY, titleColor=DBR_NAVY)
        .configure_view(stroke=None)
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
            color=alt.Color(
                "Categoria",
                title="Tipo",
                scale=alt.Scale(range=[DBR_NAVY, DBR_BLUE]),
            ),
            tooltip=[
                alt.Tooltip("Mes", title="Mes"),
                alt.Tooltip("Categoria", title="Tipo"),
                alt.Tooltip("Valor", title="Valor (R$)", format=".2f"),
            ],
        )
        .properties(background=DBR_SURFACE)
        .configure_axis(labelColor=DBR_NAVY, titleColor=DBR_NAVY, gridColor=DBR_BORDER)
        .configure_legend(labelColor=DBR_NAVY, titleColor=DBR_NAVY)
        .configure_view(stroke=None)
    )
    st.altair_chart(fig_despesas, use_container_width=True)

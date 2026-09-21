from __future__ import annotations

import unicodedata
from io import BytesIO
from pathlib import Path

import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
LOGO_PATH = APP_DIR / "assets" / "dbr.jpg"

DBR_NAVY = "#17245B"
DBR_BLUE = "#3547A5"
DBR_YELLOW = "#F3C400"
DBR_MUTED = "#667085"
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
    page_title="Dashboards DBR",
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
        [data-testid="stMetricLabel"] {{ color: {DBR_MUTED}; }}
        [data-testid="stMetricValue"] {{ color: {DBR_NAVY}; }}
        .dbr-hero {{
            display: flex;
            align-items: center;
            gap: 18px;
            background: linear-gradient(115deg, {DBR_NAVY} 0%, {DBR_BLUE} 100%);
            color: white;
            border-radius: 18px;
            padding: 22px 26px;
            margin: 4px 0 22px;
            box-shadow: 0 10px 26px rgba(23, 36, 91, 0.18);
        }}
        .dbr-hero-kicker, .dbr-kicker {{ color: {DBR_YELLOW}; font-size: 0.78rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; }}
        .dbr-hero-title, .dbr-title {{ font-size: 2rem; font-weight: 800; line-height: 1.1; margin: 4px 0; }}
        .dbr-hero-subtitle, .dbr-subtitle {{ color: #E8ECFF; margin: 0; }}
        .dbr-section {{ color: {DBR_NAVY}; font-size: 1.22rem; font-weight: 800; margin: 24px 0 10px; }}
        .dbr-subsection {{ color: {DBR_NAVY}; font-size: 1rem; font-weight: 800; margin: 16px 0 8px; }}
        .dbr-alert {{
            background: {DBR_SURFACE};
            border: 1px solid {DBR_BORDER};
            border-left: 6px solid {DBR_YELLOW};
            border-radius: 12px;
            color: #614700;
            padding: 12px 16px;
            margin: 12px 0 18px;
        }}
        .dbr-small {{ color: {DBR_MUTED}; font-size: 0.9rem; }}
        .stButton > button {{ border-color: {DBR_BLUE}; color: {DBR_NAVY}; }}
        .stDownloadButton > button {{ background: {DBR_NAVY}; color: white; border: 0; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def render_table(dataframe: pd.DataFrame) -> None:
    table_html = dataframe.to_html(index=False, border=0, na_rep="")
    st.markdown(
        f'<div class="dbr-table-wrap"><table class="dbr-data-table">'
        + table_html.split("<table", 1)[1].split(">", 1)[1].rsplit("</table>", 1)[0]
        + "</table></div>",
        unsafe_allow_html=True,
    )


# Dashboard 1: Entradas e Saídas
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
    "janeiro": "Janeiro", "fevereiro": "Fevereiro", "marco": "Marco",
    "marça": "Marco", "março": "Marco", "abril": "Abril", "maio": "Maio",
    "junho": "Junho", "julho": "Julho", "agosto": "Agosto",
    "setembro": "Setembro", "outubro": "Outubro", "novembro": "Novembro",
    "dezembro": "Dezembro",
}


def normalizar_mes(valor: object) -> object:
    if pd.isna(valor):
        return valor
    texto = str(valor).strip().lower()
    if texto in MESES_ABREV:
        return MESES_ABREV[texto]
    if texto in MESES_EXTENSO:
        return MESES_EXTENSO[texto]
    return str(valor).strip().title()


@st.cache_data(show_spinner=False)
def carregar_dados(arquivo: bytes) -> tuple[pd.DataFrame, pd.DataFrame]:
    xls = pd.ExcelFile(BytesIO(arquivo))
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

    df_despesas = pd.read_excel(xls, sheet_name="Base CP", header=1)
    df_despesas.columns = ["Data", "Mes", "Descricao", "Orcado", "Realizado"]
    df_despesas = df_despesas.dropna(subset=["Data", "Descricao"])
    df_despesas["Orcado"] = pd.to_numeric(df_despesas["Orcado"], errors="coerce").fillna(0)
    df_despesas["Realizado"] = pd.to_numeric(df_despesas["Realizado"], errors="coerce").fillna(0)
    df_despesas["Data"] = pd.to_datetime(df_despesas["Data"], errors="coerce")
    df_despesas = df_despesas.dropna(subset=["Data"])
    for col in ["Mes", "Descricao"]:
        if col in df_despesas.columns and df_despesas[col].dtype == object:
            df_despesas[col] = df_despesas[col].str.strip()
    df_despesas["Mes"] = df_despesas["Mes"].apply(normalizar_mes)
    return df_receitas, df_despesas


def render_entradas_dashboard(arquivo: bytes) -> None:
    try:
        df_receitas, df_despesas = carregar_dados(arquivo)
    except Exception as exc:
        st.error(f"Não foi possível ler a planilha de Entradas e Saídas: {exc}")
        st.stop()

    if df_receitas.empty and df_despesas.empty:
        st.warning("Nenhum dado encontrado na planilha.")
        st.stop()

    meses_rec = sorted(df_receitas["Mes"].dropna().unique(), key=lambda x: ORDEM_MESES.get(x, 99)) if not df_receitas.empty else []
    meses_desp = sorted(df_despesas["Mes"].dropna().unique(), key=lambda x: ORDEM_MESES.get(x, 99)) if not df_despesas.empty else []
    todos_meses = sorted(set(meses_rec + meses_desp), key=lambda x: ORDEM_MESES.get(x, 99))
    tipos_receita = sorted(df_receitas["Tipo"].dropna().unique()) if not df_receitas.empty else []
    descricoes_despesa = sorted(df_despesas["Descricao"].dropna().unique()) if not df_despesas.empty else []

    with st.sidebar:
        st.markdown("### Filtros de Entradas e Saídas")
        meses_selecionados = st.multiselect("Mês", todos_meses, default=todos_meses, key="entradas_meses")
        tipos_selecionados = st.multiselect("Tipo de Receita", tipos_receita, default=tipos_receita, key="entradas_tipos")
        descricoes_selecionadas = st.multiselect("Descrição de Despesa", descricoes_despesa, default=descricoes_despesa, key="entradas_descricoes")

    df_rec_filtrado = df_receitas[
        (df_receitas["Mes"].isin(meses_selecionados)) & (df_receitas["Tipo"].isin(tipos_selecionados))
    ] if not df_receitas.empty else df_receitas
    df_desp_filtrado = df_despesas[
        (df_despesas["Mes"].isin(meses_selecionados)) & (df_despesas["Descricao"].isin(descricoes_selecionadas))
    ] if not df_despesas.empty else df_despesas

    st.markdown('<div class="dbr-section">Dashboard de Entradas e Saídas</div>', unsafe_allow_html=True)
    total_receitas = df_rec_filtrado["Valor"].sum() if not df_rec_filtrado.empty else 0.0
    total_orcado = df_desp_filtrado["Orcado"].sum() if not df_desp_filtrado.empty else 0.0
    total_realizado = df_desp_filtrado["Realizado"].sum() if not df_desp_filtrado.empty else 0.0
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Receitas", f"R$ {total_receitas:,.2f}")
    col2.metric("Despesas Orçadas", f"R$ {total_orcado:,.2f}")
    col3.metric("Despesas Realizadas", f"R$ {total_realizado:,.2f}")
    col4.metric("Saldo", f"R$ {total_receitas - total_realizado:,.2f}")

    st.markdown("### Receitas")
    render_table(df_rec_filtrado)
    st.markdown("### Despesas")
    render_table(df_desp_filtrado)

    ordem_cronologica = [mes for mes in ORDEM_MESES if mes in set(meses_rec + meses_desp)]
    if not df_rec_filtrado.empty:
        st.markdown("### Receitas por Tipo e Mês")
        receitas_chart = df_rec_filtrado.groupby(["Mes", "Tipo"])["Valor"].sum().reset_index()
        receitas_chart["Mes"] = pd.Categorical(receitas_chart["Mes"], categories=ordem_cronologica, ordered=True)
        fig_receitas = (
            alt.Chart(receitas_chart.sort_values("Mes"))
            .mark_bar()
            .encode(
                x=alt.X("Mes", sort=ordem_cronologica, title="Mês"),
                y=alt.Y("Valor", title="Valor (R$)"),
                color=alt.Color("Tipo", title="Tipo de Receita", scale=alt.Scale(range=DBR_PALETTE)),
                tooltip=[alt.Tooltip("Mes", title="Mês"), alt.Tooltip("Tipo", title="Tipo de Receita"), alt.Tooltip("Valor", title="Valor (R$)", format=".2f")],
            )
            .properties(background=DBR_SURFACE)
            .configure_axis(labelColor=DBR_NAVY, titleColor=DBR_NAVY, gridColor=DBR_BORDER)
            .configure_legend(labelColor=DBR_NAVY, titleColor=DBR_NAVY)
            .configure_view(stroke=None)
        )
        st.altair_chart(fig_receitas, use_container_width=True)

    if not df_desp_filtrado.empty:
        st.markdown("### Despesas: Orçado vs Realizado por Mês")
        despesas_agg = df_desp_filtrado.groupby("Mes").agg({"Orcado": "sum", "Realizado": "sum"}).reset_index()
        despesas_chart = despesas_agg.melt(id_vars="Mes", value_vars=["Orcado", "Realizado"], var_name="Categoria", value_name="Valor")
        despesas_chart["Mes"] = pd.Categorical(despesas_chart["Mes"], categories=ordem_cronologica, ordered=True)
        fig_despesas = (
            alt.Chart(despesas_chart.sort_values("Mes"))
            .mark_line(point=True)
            .encode(
                x=alt.X("Mes", sort=ordem_cronologica, title="Mês"),
                y=alt.Y("Valor", title="Valor (R$)"),
                color=alt.Color("Categoria", title="Tipo", scale=alt.Scale(range=[DBR_NAVY, DBR_BLUE])),
                tooltip=[alt.Tooltip("Mes", title="Mês"), alt.Tooltip("Categoria", title="Tipo"), alt.Tooltip("Valor", title="Valor (R$)", format=".2f")],
            )
            .properties(background=DBR_SURFACE)
            .configure_axis(labelColor=DBR_NAVY, titleColor=DBR_NAVY, gridColor=DBR_BORDER)
            .configure_legend(labelColor=DBR_NAVY, titleColor=DBR_NAVY)
            .configure_view(stroke=None)
        )
        st.altair_chart(fig_despesas, use_container_width=True)


# Dashboard 2: Mudanças 2026
def normalize_key(value: object) -> str:
    text = "" if value is None else str(value).strip()
    text = unicodedata.normalize("NFKD", text)
    return "".join(char for char in text if not unicodedata.combining(char)).upper()


def normalize_text(value: object, fallback: str = "Não informado") -> str:
    if pd.isna(value):
        return fallback
    text = str(value).strip()
    return text or fallback


def normalize_status(value: object) -> str:
    labels = {
        "AGUARDANDO PAGTO": "Aguardando Pagto",
        "AGUARDANDO PAGAMENTO": "Aguardando Pagto",
        "AGUARDANDO TRANSPORTE": "Aguardando Transporte",
        "AGUARDANDO DATA": "Aguardando DATA",
        "DEPOSITO - DBR": "Depósito - DBR",
    }
    text = normalize_text(value, "Não informado")
    return labels.get(normalize_key(text), text)


def find_base_sheet(excel_file: pd.ExcelFile) -> str:
    for sheet in excel_file.sheet_names:
        if normalize_key(sheet) == "BASE DE DADOS":
            return sheet
    expected = {"NOME", "ORIGEM", "DESTINO", "DATA DA MUDANCA", "TIPO", "STATUS"}
    for sheet in excel_file.sheet_names:
        for header_row in range(6):
            preview = pd.read_excel(excel_file, sheet_name=sheet, header=header_row, nrows=2)
            if expected.issubset({normalize_key(column) for column in preview.columns}):
                return sheet
    raise ValueError("Não encontrei uma aba 'Base de Dados' com as colunas esperadas.")


def find_header_row(excel_file: pd.ExcelFile, sheet_name: str) -> int:
    expected = {"NOME", "ORIGEM", "DESTINO", "DATA DA MUDANCA", "TIPO", "STATUS"}
    for header_row in range(6):
        preview = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_row, nrows=2)
        if expected.issubset({normalize_key(column) for column in preview.columns}):
            return header_row
    raise ValueError("Não encontrei a linha de cabeçalho da aba Base de Dados.")


@st.cache_data(show_spinner=False)
def load_mudancas_data(file_bytes: bytes) -> pd.DataFrame:
    excel_file = pd.ExcelFile(BytesIO(file_bytes))
    sheet_name = find_base_sheet(excel_file)
    header_row = find_header_row(excel_file, sheet_name)
    raw = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_row)
    aliases = {"NOME": "Nome", "ORIGEM": "Origem", "DESTINO": "Destino", "DATA DA MUDANCA": "Data da Mudança", "TIPO": "Tipo", "STATUS": "Status"}
    rename_map = {column: aliases[normalize_key(column)] for column in raw.columns if normalize_key(column) in aliases}
    data = raw.rename(columns=rename_map).copy()
    required = ["Nome", "Origem", "Destino", "Data da Mudança", "Tipo", "Status"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError("Colunas ausentes: " + ", ".join(missing))
    data = data[required].copy()
    data["Data da Mudança"] = pd.to_datetime(data["Data da Mudança"], errors="coerce", dayfirst=True)
    for column in ["Nome", "Origem", "Destino", "Tipo"]:
        data[column] = data[column].map(normalize_text)
    data["Status"] = data["Status"].map(normalize_status)
    meaningful = data[required].astype("string").fillna("").apply(lambda column: column.str.strip().ne(""))
    data = data[meaningful.any(axis=1)].copy()
    today = pd.Timestamp.now().normalize()
    data["Dias"] = (data["Data da Mudança"] - today).dt.days
    situation = pd.Series("PROGRAMADA", index=data.index, dtype="string")
    situation.loc[data["Data da Mudança"].isna()] = "SEM DATA"
    situation.loc[data["Data da Mudança"] < today] = "ATRASADA"
    situation.loc[data["Data da Mudança"] == today] = "HOJE"
    situation.loc[data["Data da Mudança"].notna() & (data["Data da Mudança"] > today) & (data["Data da Mudança"] <= today + pd.Timedelta(days=7))] = "PRÓXIMA"
    data["Situação"] = situation
    return data.sort_values(["Data da Mudança", "Nome"], na_position="last").reset_index(drop=True)


def make_bar_chart(data: pd.DataFrame, x: str, y: str, title: str, color: str | None = None):
    fig = px.bar(data, x=x, y=y, title=title, color=color, text_auto=True)
    fig.update_layout(title_font_color=DBR_NAVY, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=DBR_SURFACE, margin=dict(l=10, r=10, t=48, b=10), showlegend=False, font=dict(color=DBR_NAVY), xaxis=dict(color=DBR_NAVY, gridcolor=DBR_BORDER), yaxis=dict(color=DBR_NAVY, gridcolor=DBR_BORDER))
    return fig


def render_mudancas_dashboard(arquivo: bytes) -> None:
    try:
        data = load_mudancas_data(arquivo)
    except Exception as exc:
        st.error(f"Não foi possível ler a planilha de Mudanças: {exc}")
        st.stop()
    if data.empty:
        st.warning("A planilha não possui mudanças preenchidas.")
        st.stop()

    with st.sidebar:
        st.markdown("### Filtros de Mudanças")
        search = st.text_input("Buscar mudança", placeholder="Nome, cidade ou rota", key="mudancas_search")
        status_options = sorted(data["Status"].dropna().unique())
        selected_status = st.multiselect("Status", status_options, default=status_options, key="mudancas_status")
        type_options = sorted(data["Tipo"].dropna().unique())
        selected_types = st.multiselect("Tipo", type_options, default=type_options, key="mudancas_tipos")
        situation_options = [situation for situation in ["ATRASADA", "HOJE", "PRÓXIMA", "PROGRAMADA", "SEM DATA"] if situation in set(data["Situação"])]
        selected_situations = st.multiselect("Situação", situation_options, default=situation_options, key="mudancas_situacoes")
        valid_dates = data["Data da Mudança"].dropna()
        date_range = None
        if not valid_dates.empty:
            date_range = st.date_input("Período", value=(valid_dates.min().date(), valid_dates.max().date()), key="mudancas_periodo")

    filtered = data.copy()
    if search.strip():
        query = search.strip().casefold()
        searchable = filtered[["Nome", "Origem", "Destino", "Tipo", "Status"]].astype(str).agg(" ".join, axis=1)
        filtered = filtered[searchable.str.casefold().str.contains(query, na=False)]
    if selected_status:
        filtered = filtered[filtered["Status"].isin(selected_status)]
    if selected_types:
        filtered = filtered[filtered["Tipo"].isin(selected_types)]
    if selected_situations:
        filtered = filtered[filtered["Situação"].isin(selected_situations)]
    if date_range and len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = filtered[filtered["Data da Mudança"].isna() | filtered["Data da Mudança"].between(start_date, end_date)]

    total = len(filtered)
    today_count = int((filtered["Situação"] == "HOJE").sum())
    next_seven = int((filtered["Situação"] == "PRÓXIMA").sum())
    without_date = int((filtered["Situação"] == "SEM DATA").sum())
    deposit = int((filtered["Status"] == "Depósito - DBR").sum())
    status_counts = filtered["Status"].value_counts().rename_axis("Status").reset_index(name="Mudanças")

    st.markdown('<div class="dbr-section">Resumo operacional</div>', unsafe_allow_html=True)
    metric_cols = st.columns(5)
    metric_cols[0].metric("Mudanças", total)
    metric_cols[1].metric("Para hoje", today_count)
    metric_cols[2].metric("Próximos 7 dias", next_seven)
    metric_cols[3].metric("Sem data", without_date)
    metric_cols[4].metric("Depósito DBR", deposit)
    if today_count or without_date:
        messages = []
        if today_count:
            messages.append(f"{today_count} para hoje")
        if without_date:
            messages.append(f"{without_date} sem data")
        st.markdown('<div class="dbr-alert"><strong>Atenção operacional:</strong> ' + " • ".join(messages) + "</div>", unsafe_allow_html=True)
    if filtered.empty:
        st.warning("Nenhuma mudança corresponde aos filtros selecionados.")
        st.stop()

    st.markdown('<div class="dbr-subsection">Mudanças por status</div>', unsafe_allow_html=True)
    status_columns = st.columns(len(status_counts))
    for status_column, (status, count) in zip(status_columns, status_counts.itertuples(index=False, name=None)):
        status_column.metric(status, int(count))
    st.markdown('<div class="dbr-subsection">Tabela geral</div>', unsafe_allow_html=True)
    table = filtered[["Nome", "Origem", "Destino", "Data da Mudança", "Tipo", "Status", "Dias", "Situação"]].copy()
    table["Data da Mudança"] = table["Data da Mudança"].dt.strftime("%d/%m/%Y")
    table["Dias"] = table["Dias"].astype("Int64")
    render_table(table)
    st.download_button("Baixar lista filtrada (CSV)", data=table.to_csv(index=False).encode("utf-8-sig"), file_name="mudancas_filtradas.csv", mime="text/csv", key="mudancas_download")

    fig = make_bar_chart(status_counts, "Mudanças", "Status", "Mudanças por status", "Status")
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    fig.update_traces(marker_color=DBR_BLUE)
    st.plotly_chart(fig, use_container_width=True)
    left, right = st.columns([1, 1])
    with left:
        by_type = filtered["Tipo"].value_counts().rename_axis("Tipo").reset_index(name="Mudanças")
        fig = make_bar_chart(by_type, "Mudanças", "Tipo", "Mudanças por tipo", "Tipo")
        fig.update_layout(yaxis=dict(categoryorder="total ascending"))
        fig.update_traces(marker_color=DBR_BLUE)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        route_data = filtered.assign(Rota=filtered["Origem"] + " → " + filtered["Destino"])
        route_counts = route_data["Rota"].value_counts().head(10).rename_axis("Rota").reset_index(name="Mudanças")
        fig = make_bar_chart(route_counts, "Mudanças", "Rota", "Principais rotas", "Rota")
        fig.update_layout(yaxis=dict(categoryorder="total ascending"))
        fig.update_traces(marker_color=DBR_BLUE)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="dbr-section">Agenda de mudanças</div>', unsafe_allow_html=True)
    schedule = filtered.dropna(subset=["Data da Mudança"]).copy()
    if not schedule.empty:
        schedule_by_date = schedule.groupby("Data da Mudança", as_index=False).size().rename(columns={"size": "Mudanças"})
        fig = px.bar(schedule_by_date, x="Data da Mudança", y="Mudanças", title="Quantidade de mudanças por data", color_discrete_sequence=[DBR_BLUE], text_auto=True)
        fig.update_layout(title_font_color=DBR_NAVY, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=DBR_SURFACE, margin=dict(l=10, r=10, t=48, b=10), font=dict(color=DBR_NAVY), xaxis=dict(color=DBR_NAVY, gridcolor=DBR_BORDER), yaxis=dict(color=DBR_NAVY, gridcolor=DBR_BORDER))
        st.plotly_chart(fig, use_container_width=True)


# Interface única: escolha do dashboard e upload no conteúdo principal.
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    st.markdown("### Aplicação DBR")
    st.caption("Escolha o dashboard e faça o upload da planilha no painel principal.")

hero_logo, hero_text = st.columns([1.15, 5])
with hero_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=190)
with hero_text:
    st.markdown(
        """
        <div class="dbr-hero">
            <div>
                <div class="dbr-hero-kicker">DBR Mudanças & Transportes</div>
                <div class="dbr-hero-title">Central de Dashboards</div>
                <p class="dbr-hero-subtitle">Escolha o painel e carregue a planilha correspondente.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="dbr-section">Escolha o dashboard</div>', unsafe_allow_html=True)
selected_dashboard = st.radio(
    "Tipo de dashboard",
    ["Entradas e Saídas", "Mudanças 2026"],
    horizontal=True,
    label_visibility="collapsed",
    key="dashboard_selector",
)

if selected_dashboard == "Entradas e Saídas":
    uploaded_file = st.file_uploader(
        "Envie a planilha de Entradas e Saídas (.xlsx)",
        type=["xlsx"],
        help="A planilha precisa conter as abas Base CR e Base CP.",
        key="upload_entradas",
    )
    expected_structure = "Abas esperadas: Base CR e Base CP."
else:
    uploaded_file = st.file_uploader(
        "Envie a planilha de Mudanças 2026 (.xlsx)",
        type=["xlsx"],
        help="A planilha precisa conter a aba Base de Dados.",
        key="upload_mudancas",
    )
    expected_structure = "Aba esperada: Base de Dados, com nome, origem, destino, data, tipo e status."

st.caption(expected_structure)
if uploaded_file is None:
    st.info("Faça o upload da planilha selecionada para abrir o dashboard.")
    st.stop()

if selected_dashboard == "Entradas e Saídas":
    render_entradas_dashboard(uploaded_file.getvalue())
else:
    render_mudancas_dashboard(uploaded_file.getvalue())

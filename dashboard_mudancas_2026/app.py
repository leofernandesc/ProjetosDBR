from __future__ import annotations

import unicodedata
from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
LOGO_PATH = APP_DIR / "assets" / "dbr.jpg"

DBR_NAVY = "#17245B"
DBR_BLUE = "#3547A5"
DBR_YELLOW = "#F3C400"
DBR_INK = "#172033"
DBR_MUTED = "#667085"
DBR_BACKGROUND = "#FFF9E6"
DBR_SURFACE = "#FFF4C4"
DBR_INPUT = "#FFFBEF"
DBR_CHROME = "#FFF1B8"
DBR_BORDER = "#E6CF72"

STATUS_COLORS = {
    "Aguardando Pagto": DBR_YELLOW,
    "Aguardando Transporte": DBR_BLUE,
    "Aguardando DATA": "#8B5CF6",
    "Depósito - DBR": DBR_NAVY,
}

CSS = f"""
<style>
    :root {{
        --dbr-navy: {DBR_NAVY};
        --dbr-blue: {DBR_BLUE};
        --dbr-yellow: {DBR_YELLOW};
        --dbr-ink: {DBR_INK};
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
    [data-testid="stMainMenu"],
    [data-testid="stToolbar"] {{ visibility: hidden !important; pointer-events: none !important; height: 0 !important; }}
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
        background: {DBR_SURFACE};
        border: 1px solid {DBR_BORDER};
        border-radius: 14px;
        overflow-x: auto;
        margin: 0 0 18px;
    }}
    .dbr-data-table {{
        border-collapse: collapse;
        color: {DBR_NAVY};
        font-size: 0.92rem;
        min-width: 100%;
        background: {DBR_SURFACE};
    }}
    .dbr-data-table th {{ background: {DBR_CHROME}; color: {DBR_NAVY}; font-weight: 800; padding: 10px 12px; text-align: left; white-space: nowrap; }}
    .dbr-data-table td {{ background: {DBR_INPUT}; border-top: 1px solid {DBR_BORDER}; padding: 9px 12px; white-space: nowrap; }}
    .dbr-data-table tr:nth-child(even) td {{ background: #FFF7D6; }}
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
    .dbr-hero-kicker {{ color: {DBR_YELLOW}; font-size: 0.78rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; }}
    .dbr-hero-title {{ font-size: 2rem; font-weight: 800; line-height: 1.1; margin: 4px 0; }}
    .dbr-hero-subtitle {{ color: #E8ECFF; margin: 0; }}
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
"""


st.set_page_config(
    page_title="Dashboard de Mudanças | DBR",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "📦",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CSS, unsafe_allow_html=True)


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
            preview = pd.read_excel(
                excel_file, sheet_name=sheet, header=header_row, nrows=2
            )
            columns = {normalize_key(column) for column in preview.columns}
            if expected.issubset(columns):
                return sheet

    raise ValueError("Não encontrei uma aba 'Base de Dados' com as colunas esperadas.")


def find_header_row(excel_file: pd.ExcelFile, sheet_name: str) -> int:
    expected = {"NOME", "ORIGEM", "DESTINO", "DATA DA MUDANCA", "TIPO", "STATUS"}
    for header_row in range(6):
        preview = pd.read_excel(
            excel_file, sheet_name=sheet_name, header=header_row, nrows=2
        )
        columns = {normalize_key(column) for column in preview.columns}
        if expected.issubset(columns):
            return header_row
    raise ValueError("Não encontrei a linha de cabeçalho da aba Base de Dados.")


@st.cache_data(show_spinner=False)
def load_data(file_bytes: bytes) -> pd.DataFrame:
    excel_file = pd.ExcelFile(BytesIO(file_bytes))
    sheet_name = find_base_sheet(excel_file)
    header_row = find_header_row(excel_file, sheet_name)
    raw = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_row)

    rename_map = {}
    for column in raw.columns:
        normalized = normalize_key(column)
        aliases = {
            "NOME": "Nome",
            "ORIGEM": "Origem",
            "DESTINO": "Destino",
            "DATA DA MUDANCA": "Data da Mudança",
            "TIPO": "Tipo",
            "STATUS": "Status",
        }
        if normalized in aliases:
            rename_map[column] = aliases[normalized]
    data = raw.rename(columns=rename_map).copy()

    required = ["Nome", "Origem", "Destino", "Data da Mudança", "Tipo", "Status"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError("Colunas ausentes: " + ", ".join(missing))

    data = data[required].copy()
    data["Data da Mudança"] = pd.to_datetime(
        data["Data da Mudança"], errors="coerce", dayfirst=True
    )
    data["Nome"] = data["Nome"].map(normalize_text)
    data["Origem"] = data["Origem"].map(normalize_text)
    data["Destino"] = data["Destino"].map(normalize_text)
    data["Tipo"] = data["Tipo"].map(normalize_text)
    data["Status"] = data["Status"].map(normalize_status)

    # Remove linhas totalmente vazias sem descartar mudanças que ainda não têm data.
    meaningful = data[required].astype("string").fillna("").apply(
        lambda column: column.str.strip().ne("")
    )
    data = data[meaningful.any(axis=1)].copy()

    today = pd.Timestamp.now().normalize()
    data["Dias"] = (data["Data da Mudança"] - today).dt.days
    situation = pd.Series("PROGRAMADA", index=data.index, dtype="string")
    has_no_date = data["Data da Mudança"].isna()
    situation.loc[has_no_date] = "SEM DATA"
    situation.loc[data["Data da Mudança"] < today] = "ATRASADA"
    situation.loc[data["Data da Mudança"] == today] = "HOJE"
    situation.loc[
        data["Data da Mudança"].notna()
        & (data["Data da Mudança"] > today)
        & (data["Data da Mudança"] <= today + pd.Timedelta(days=7))
    ] = "PRÓXIMA"
    data["Situação"] = situation

    return data.sort_values(
        ["Data da Mudança", "Nome"], na_position="last"
    ).reset_index(drop=True)


def make_bar_chart(data: pd.DataFrame, x: str, y: str, title: str, color: str | None = None):
    fig = px.bar(data, x=x, y=y, title=title, color=color, text_auto=True)
    fig.update_layout(
        title_font_color=DBR_NAVY,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=DBR_SURFACE,
        margin=dict(l=10, r=10, t=48, b=10),
        showlegend=False,
        font=dict(color=DBR_NAVY),
        xaxis=dict(color=DBR_NAVY, gridcolor=DBR_BORDER),
        yaxis=dict(color=DBR_NAVY, gridcolor=DBR_BORDER),
    )
    return fig


def render_table(dataframe: pd.DataFrame) -> None:
    table_html = dataframe.to_html(index=False, border=0, na_rep="")
    st.markdown(
        f'<div class="dbr-table-wrap"><table class="dbr-data-table">'
        + table_html.split("<table", 1)[1].split(">", 1)[1].rsplit("</table>", 1)[0]
        + "</table></div>",
        unsafe_allow_html=True,
    )


with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    st.markdown("### Fonte de dados")
    uploaded_file = st.file_uploader(
        "Envie Dashboard_Mudancas_2026.xlsx",
        type=["xlsx"],
        help="A planilha deve conter a aba Base de Dados.",
    )
    st.caption("Os dados ficam apenas nesta sessão do dashboard.")


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
                <div class="dbr-hero-title">Dashboard de Mudanças</div>
                <p class="dbr-hero-subtitle">Acompanhamento das mudanças em aberto, prazos e status operacionais.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if uploaded_file is None:
    st.info("Envie a planilha pela barra lateral para visualizar o dashboard.")
    st.markdown(
        """
        **Estrutura esperada:** a planilha deve conter uma aba `Base de Dados` com
        nome, origem, destino, data da mudança, tipo e status.
        """
    )
    st.stop()


try:
    data = load_data(uploaded_file.getvalue())
except Exception as exc:
    st.error(f"Não foi possível ler a planilha: {exc}")
    st.stop()


if data.empty:
    st.warning("A planilha não possui mudanças preenchidas.")
    st.stop()


with st.sidebar:
    st.markdown("### Filtros")
    search = st.text_input("Buscar mudança", placeholder="Nome, cidade ou rota")
    status_options = sorted(data["Status"].dropna().unique())
    selected_status = st.multiselect("Status", status_options, default=status_options)
    type_options = sorted(data["Tipo"].dropna().unique())
    selected_types = st.multiselect("Tipo", type_options, default=type_options)
    situation_options = [
        situation for situation in ["ATRASADA", "HOJE", "PRÓXIMA", "PROGRAMADA", "SEM DATA"]
        if situation in set(data["Situação"])
    ]
    selected_situations = st.multiselect(
        "Situação", situation_options, default=situation_options
    )

    valid_dates = data["Data da Mudança"].dropna()
    date_range = None
    if not valid_dates.empty:
        date_range = st.date_input(
            "Período",
            value=(valid_dates.min().date(), valid_dates.max().date()),
        )


filtered = data.copy()
if search.strip():
    query = search.strip().casefold()
    searchable = filtered[["Nome", "Origem", "Destino", "Tipo", "Status"]].astype(str).agg(
        " ".join, axis=1
    )
    filtered = filtered[searchable.str.casefold().str.contains(query, na=False)]
if selected_status:
    filtered = filtered[filtered["Status"].isin(selected_status)]
if selected_types:
    filtered = filtered[filtered["Tipo"].isin(selected_types)]
if selected_situations:
    filtered = filtered[filtered["Situação"].isin(selected_situations)]
if date_range and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[
        filtered["Data da Mudança"].isna()
        | filtered["Data da Mudança"].between(start_date, end_date)
    ]


total = len(filtered)
late = int((filtered["Situação"] == "ATRASADA").sum())
today_count = int((filtered["Situação"] == "HOJE").sum())
next_seven = int((filtered["Situação"] == "PRÓXIMA").sum())
without_date = int((filtered["Situação"] == "SEM DATA").sum())
deposit = int((filtered["Status"] == "Depósito - DBR").sum())

st.markdown('<div class="dbr-section">Resumo operacional</div>', unsafe_allow_html=True)
metric_cols = st.columns(6)
metric_cols[0].metric("Mudanças", total)
metric_cols[1].metric("Atrasadas", late)
metric_cols[2].metric("Para hoje", today_count)
metric_cols[3].metric("Próximos 7 dias", next_seven)
metric_cols[4].metric("Sem data", without_date)
metric_cols[5].metric("Depósito DBR", deposit)

if late or today_count or without_date:
    messages = []
    if late:
        messages.append(f"{late} atrasada(s)")
    if today_count:
        messages.append(f"{today_count} para hoje")
    if without_date:
        messages.append(f"{without_date} sem data")
    st.markdown(
        '<div class="dbr-alert"><strong>Atenção operacional:</strong> '
        + " • ".join(messages)
        + "</div>",
        unsafe_allow_html=True,
    )

if filtered.empty:
    st.warning("Nenhuma mudança corresponde aos filtros selecionados.")
    st.stop()


st.markdown('<div class="dbr-subsection">Tabela geral</div>', unsafe_allow_html=True)
table = filtered[
    ["Nome", "Origem", "Destino", "Data da Mudança", "Tipo", "Status", "Dias", "Situação"]
].copy()
table["Data da Mudança"] = table["Data da Mudança"].dt.strftime("%d/%m/%Y")
table["Dias"] = table["Dias"].astype("Int64")
render_table(table)
st.download_button(
    "Baixar lista filtrada (CSV)",
    data=table.to_csv(index=False).encode("utf-8-sig"),
    file_name="mudancas_filtradas.csv",
    mime="text/csv",
)


st.markdown('<div class="dbr-subsection">Mudanças por status</div>', unsafe_allow_html=True)
status_counts = filtered["Status"].value_counts().rename_axis("Status").reset_index(name="Mudanças")
fig = make_bar_chart(status_counts, "Mudanças", "Status", "Mudanças por status", "Status")
fig.update_layout(yaxis=dict(categoryorder="total ascending"))
fig.update_traces(marker_color=[STATUS_COLORS.get(value, DBR_BLUE) for value in status_counts["Status"]])
st.plotly_chart(fig, use_container_width=True)


left, right = st.columns([1, 1])
with left:
    by_type = filtered["Tipo"].value_counts().rename_axis("Tipo").reset_index(name="Mudanças")
    fig = make_bar_chart(by_type, "Mudanças", "Tipo", "Mudanças por tipo", "Tipo")
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    fig.update_traces(marker_color=DBR_NAVY)
    st.plotly_chart(fig, use_container_width=True)
with right:
    route_data = filtered.assign(
        Rota=filtered["Origem"] + " → " + filtered["Destino"]
    )
    route_counts = route_data["Rota"].value_counts().head(10).rename_axis("Rota").reset_index(name="Mudanças")
    fig = make_bar_chart(route_counts, "Mudanças", "Rota", "Principais rotas", "Rota")
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    fig.update_traces(marker_color=DBR_BLUE)
    st.plotly_chart(fig, use_container_width=True)


st.markdown('<div class="dbr-section">Agenda de mudanças</div>', unsafe_allow_html=True)
schedule = filtered.dropna(subset=["Data da Mudança"]).copy()
if not schedule.empty:
    schedule_by_date = (
        schedule.groupby("Data da Mudança", as_index=False)
        .size()
        .rename(columns={"size": "Mudanças"})
    )
    fig = px.bar(
        schedule_by_date,
        x="Data da Mudança",
        y="Mudanças",
        title="Quantidade de mudanças por data",
        color_discrete_sequence=[DBR_BLUE],
        text_auto=True,
    )
    fig.update_layout(
        title_font_color=DBR_NAVY,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=DBR_SURFACE,
        margin=dict(l=10, r=10, t=48, b=10),
        font=dict(color=DBR_NAVY),
        xaxis=dict(color=DBR_NAVY, gridcolor=DBR_BORDER),
        yaxis=dict(color=DBR_NAVY, gridcolor=DBR_BORDER),
    )
    st.plotly_chart(fig, use_container_width=True)

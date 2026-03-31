import streamlit as st


def aplicar_estilo():
    st.markdown("""
    <style>
    /* Fundo geral */
    .stApp {
        background-color: #F4F7FB;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #132A63;
    }

    /* Tudo da sidebar */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Página ativa no menu */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #7EDC12 !important;
        color: #132A63 !important;
        border-radius: 10px;
        font-weight: bold;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #132A63 !important;
    }

    /* Alertas */
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Botões */
    .stButton > button {
        background-color: #7EDC12;
        color: #132A63;
        border: none;
        border-radius: 10px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #6BC50F;
        color: #132A63;
    }

    /* Inputs */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


def mostrar_logo():
    st.image("assets/logo/logo_govplan.jpg", width=220)
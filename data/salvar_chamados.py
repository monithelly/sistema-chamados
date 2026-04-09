import os
import streamlit as st
import gspread
from datetime import datetime
from zoneinfo import ZoneInfo

SPREADSHEET_ID = "1huNRk11OX11ae-lv4NQX-OED3qgTzVHSTxTVV_dPI9o"


def get_sheet():
    if "gcp_service_account" not in st.secrets:
        raise KeyError("A chave 'gcp_service_account' não foi encontrada no secrets.toml")

    creds_info = dict(st.secrets["gcp_service_account"])
    client = gspread.service_account_from_dict(creds_info)
    return client.open_by_key(SPREADSHEET_ID).sheet1


def salvar_anexo(arquivo):
    if arquivo is None:
        return ""

    pasta_uploads = "uploads"
    os.makedirs(pasta_uploads, exist_ok=True)

    agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo"))
    timestamp = agora_brasil.strftime("%Y%m%d_%H%M%S")

    nome_original = arquivo.name
    nome_limpo = nome_original.replace(" ", "_")
    nome_arquivo = f"{timestamp}_{nome_limpo}"

    caminho_arquivo = os.path.join(pasta_uploads, nome_arquivo)

    with open(caminho_arquivo, "wb") as f:
        f.write(arquivo.getbuffer())

    return caminho_arquivo


def salvar_chamado(dados):
    agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo"))

    caminho_anexo = salvar_anexo(dados.get("anexo"))

    nova_linha = [
        agora_brasil.strftime("%d/%m/%Y %H:%M:%S"),  # data_hora
        dados.get("solicitante", ""),
        dados.get("categoria", ""),
        dados.get("orgao", ""),
        dados.get("login", ""),
        dados.get("url", ""),
        dados.get("link_gravacao", ""),
        dados.get("descricao", ""),
        caminho_anexo,
        dados.get("criticidade", ""),   # nova coluna
        "Aguardando abertura",          # status
        "",
        "",
        ""
    ]

    sheet = get_sheet()
    sheet.append_row(nova_linha)

    return True
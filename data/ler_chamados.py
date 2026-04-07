import streamlit as st
import pandas as pd
import gspread

SPREADSHEET_ID = "1huNRk11OX11ae-lv4NQX-OED3qgTzVHSTxTVV_dPI9o"


def get_sheet():
    creds_info = dict(st.secrets["gcp_service_account"])
    client = gspread.service_account_from_dict(creds_info)
    return client.open_by_key(SPREADSHEET_ID).sheet1


def ler_chamados():
    sheet = get_sheet()
    dados = sheet.get_all_records()
    df = pd.DataFrame(dados)

    if "data_abertura" in df.columns:
        df["data_abertura"] = pd.to_datetime(
            df["data_abertura"],
            format="%d/%m/%Y %H:%M:%S",
            errors="coerce"
        )

    return df


def atualizar_chamado(indice_linha, status, numero, observacao, data_fechamento):
    sheet = get_sheet()
    linha = indice_linha + 2
    colunas = {
        "status": 10,
        "numero_chamado_externo": 11,
        "observacao_interna": 12,
        "data_fechamento": 13
    }
    sheet.update_cell(linha, colunas["status"], status)
    sheet.update_cell(linha, colunas["numero_chamado_externo"], numero)
    sheet.update_cell(linha, colunas["observacao_interna"], observacao)
    sheet.update_cell(linha, colunas["data_fechamento"], data_fechamento)
import os
import pandas as pd
from datetime import datetime

CAMINHO_ARQUIVO = "data/chamados.csv"


def salvar_chamado(dados):
    novo_registro = {
        "data_abertura": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "solicitante": dados["solicitante"],
        "categoria": dados["categoria"],
        "orgao": dados["orgao"],
        "login": dados["login"],
        "url": dados["url"],
        "link_gravacao": dados["link_gravacao"],
        "descricao": dados["descricao"],
        "anexo": dados["anexo"],
        "status": "Aguardando abertura",
        "numero_chamado_externo": "",
        "observacao_interna": "",
        "data_fechamento": ""
    }

    if os.path.exists(CAMINHO_ARQUIVO):
        df_existente = pd.read_csv(CAMINHO_ARQUIVO)
        df_novo = pd.concat([df_existente, pd.DataFrame([novo_registro])], ignore_index=True)
    else:
        df_novo = pd.DataFrame([novo_registro])

    df_novo.to_csv(CAMINHO_ARQUIVO, index=False, encoding="utf-8-sig")
import os
import pandas as pd

CAMINHO_HISTORICO = "data/historico_chamados.xlsx"
CAMINHO_ATUAL = "data/chamados.csv"
CAMINHO_BACKUP = "data/chamados_backup.csv"


def padronizar_colunas(df):
    return df.rename(columns={
        "Carimbo de data/hora": "data_abertura",
        "Solicitante": "solicitante",
        "Login": "login",
        "Órgão": "orgao",
        "URL": "url",
        "Descrição": "descricao",
        "Anexo (se necessário)": "anexo",
        "Categoria": "categoria",
        "Categoria ": "categoria",
        "Link gravação": "link_gravacao",
        "Status": "status",
        "N° Chamado": "numero_chamado_externo",
        "Nº Chamado": "numero_chamado_externo",
    })


def garantir_colunas(df):
    colunas_necessarias = [
        "data_abertura",
        "solicitante",
        "categoria",
        "orgao",
        "login",
        "url",
        "link_gravacao",
        "descricao",
        "anexo",
        "status",
        "numero_chamado_externo",
        "observacao_interna",
        "data_fechamento",
    ]

    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            df[coluna] = ""

    return df[colunas_necessarias]


if not os.path.exists(CAMINHO_HISTORICO):
    print("ERRO: não encontrei o arquivo data/historico_chamados.xlsx")
    raise SystemExit

# lê histórico
df_historico = pd.read_excel(CAMINHO_HISTORICO)
df_historico = padronizar_colunas(df_historico)
df_historico = garantir_colunas(df_historico)

# lê base atual, se existir
if os.path.exists(CAMINHO_ATUAL):
    df_atual = pd.read_csv(CAMINHO_ATUAL, encoding="utf-8-sig")
    df_atual = garantir_colunas(df_atual)

    # backup da base atual
    df_atual.to_csv(CAMINHO_BACKUP, index=False, encoding="utf-8-sig")
else:
    df_atual = pd.DataFrame(columns=df_historico.columns)

# junta tudo
df_final = pd.concat([df_historico, df_atual], ignore_index=True)

# remove duplicados básicos
df_final = df_final.drop_duplicates(
    subset=["data_abertura", "solicitante", "descricao"],
    keep="first"
)

# salva base final oficial
df_final.to_csv(CAMINHO_ATUAL, index=False, encoding="utf-8-sig")

print("Pronto! Base unificada salva em data/chamados.csv")
print(f"Total de registros: {len(df_final)}")
print("Backup salvo em data/chamados_backup.csv")
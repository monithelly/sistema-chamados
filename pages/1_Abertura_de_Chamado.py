import streamlit as st
from data.salvar_chamados import salvar_chamado
from utils.styles import aplicar_estilo, mostrar_logo

aplicar_estilo()
mostrar_logo()

st.title("Abertura de Chamado")
st.write("Preencha as informações abaixo para abrir um chamado.")
st.divider()

mensagem = st.empty()

with st.form("form_chamado", clear_on_submit=True):
    solicitante = st.text_input("Solicitante")
    categoria = st.selectbox(
        "Categoria",
        ["Bug", "Sugestão de melhoria", "Robô de fontes"]
    )
    orgao = st.text_input("Órgão")
    login = st.text_input("Login")
    url = st.text_input("URL")
    link_gravacao = st.text_input("Link da gravação")
    descricao = st.text_area("Descrição")
    anexo = st.file_uploader("Anexo (opcional)")
    enviar = st.form_submit_button("Abrir chamado")

if enviar:
    if not solicitante or not orgao or not descricao:
        mensagem.error("Preencha pelo menos: Solicitante, Órgão e Descrição.")
    else:
        nome_anexo = anexo.name if anexo else ""

        dados = {
            "solicitante": solicitante,
            "categoria": categoria,
            "orgao": orgao,
            "login": login,
            "url": url,
            "link_gravacao": link_gravacao,
            "descricao": descricao,
            "anexo": nome_anexo
        }

        try:
            salvar_chamado(dados)
            mensagem.success("Chamado salvo com sucesso!")
        except Exception as e:
            mensagem.error(f"Erro ao salvar o chamado: {e}")
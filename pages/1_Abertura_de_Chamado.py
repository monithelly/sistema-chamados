import streamlit as st
from data.salvar_chamados import salvar_chamado
from data.enviar_email import enviar_email_novo_chamado
from utils.styles import aplicar_estilo, mostrar_logo

st.set_page_config(page_title="Abertura de Chamado", layout="centered")

aplicar_estilo()
mostrar_logo()

st.title("Abertura de Chamado")
st.write("Preencha as informações abaixo para abrir um chamado.")
st.divider()

# Placeholder fixo no topo para a mensagem
banner = st.empty()

with st.form("form_chamado", clear_on_submit=False):
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
        banner.error("Preencha pelo menos: Solicitante, Órgão e Descrição.")
        st.stop()

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
        resultado = salvar_chamado(dados)

        try:
            enviar_email_novo_chamado(dados)
        except Exception:
            pass

        if resultado:
            banner.success("Chamado aberto com sucesso!")
            st.toast("Chamado aberto com sucesso!")
        else:
            banner.error("O chamado não foi salvo.")
            st.toast("O chamado não foi salvo.")

    except Exception as e:
        banner.error(f"Erro ao salvar o chamado: {e}")
        st.toast(f"Erro ao salvar o chamado: {e}")
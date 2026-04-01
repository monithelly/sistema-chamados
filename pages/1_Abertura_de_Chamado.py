import html
import streamlit as st
from data.salvar_chamados import salvar_chamado
from data.enviar_email import enviar_email_novo_chamado
from utils.styles import aplicar_estilo, mostrar_logo

st.set_page_config(page_title="Abertura de Chamado", layout="centered")

aplicar_estilo()
mostrar_logo()


def set_banner_params(mensagem: str, tipo: str):
    try:
        st.query_params["msg"] = mensagem
        st.query_params["tipo"] = tipo
    except Exception:
        st.experimental_set_query_params(msg=mensagem, tipo=tipo)


def get_banner_params():
    try:
        msg = st.query_params.get("msg", "")
        tipo = st.query_params.get("tipo", "")
    except Exception:
        params = st.experimental_get_query_params()
        msg = params.get("msg", [""])
        tipo = params.get("tipo", [""])
        msg = msg[0] if isinstance(msg, list) else msg
        tipo = tipo[0] if isinstance(tipo, list) else tipo
    return msg, tipo


st.title("Abertura de Chamado")
st.write("Preencha as informações abaixo para abrir um chamado.")
st.divider()

msg, tipo = get_banner_params()

if msg:
    cor_fundo = "#d1fae5" if tipo == "sucesso" else "#fee2e2"
    cor_texto = "#065f46" if tipo == "sucesso" else "#991b1b"
    cor_borda = "#a7f3d0" if tipo == "sucesso" else "#fecaca"

    st.markdown(
        f"""
        <div style="
            background-color:{cor_fundo};
            color:{cor_texto};
            padding:14px 16px;
            border-radius:10px;
            border:1px solid {cor_borda};
            font-weight:600;
            margin-top:16px;
            margin-bottom:16px;
        ">
            {html.escape(msg)}
        </div>
        """,
        unsafe_allow_html=True
    )

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
        set_banner_params(
            "Preencha pelo menos: Solicitante, Órgão e Descrição.",
            "erro"
        )
        st.rerun()

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
            set_banner_params("Chamado aberto com sucesso!", "sucesso")
        else:
            set_banner_params("O chamado não foi salvo.", "erro")

        st.rerun()

    except Exception as e:
        set_banner_params(f"Erro ao salvar o chamado: {e}", "erro")
        st.rerun()
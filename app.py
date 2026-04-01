import streamlit as st
from utils.styles import aplicar_estilo, mostrar_logo

st.set_page_config(
    page_title="Central de Chamados",
    page_icon="📞",
    layout="wide"
)

aplicar_estilo()
mostrar_logo()

st.title("Central de Chamados")

st.subheader("Sistema interno para abertura e acompanhamento de chamados")

st.divider()

st.write("""
Bem-vindo ao sistema de chamados.

Aqui você pode:
- Abrir um novo chamado
- Acompanhar seus chamados
- Visualizar o dashboard geral

Use o menu lateral à esquerda para navegar.
""")

st.info("💡 Dica: Utilize seu nome para conseguir acompanhar seus chamados depois.")
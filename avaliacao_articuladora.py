import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def gerar_pdf(avaliacao, grupo, pontos, pesos, notas, nota_final):
    # Seleção de pasta para salvar o PDF
    pasta_destino = st.text_input("Digite o caminho onde deseja salvar o PDF:")
    if not pasta_destino:
        st.warning("⚠ Por favor, insira um caminho válido para salvar o PDF.")
        return

    nome_arquivo = st.text_input("Digite o nome do arquivo PDF (sem extensão):").strip()
    if not nome_arquivo:
        st.warning("⚠ Por favor, insira um nome válido para o arquivo.")
        return

    caminho_arquivo = os.path.join(pasta_destino, f"{nome_arquivo}.pdf")

    pdf = canvas.Canvas(caminho_arquivo, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Boletim de Avaliação")

    # Informações gerais
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 720, f"Avaliação: {avaliacao}")
    pdf.drawString(100, 700, f"Grupo: {grupo}")
    pdf.drawString(100, 680, f"Peso da avaliação: {pontos} pontos")

    # Critérios avaliados
    y = 650
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y, "Critérios Avaliados:")
    y -= 20

    pdf.setFont("Helvetica", 12)
    for criterio, peso in pesos.items():
        nota_atribuida = notas[criterio]
        pontos_recebidos = (nota_atribuida / 100) * (peso / 100) * pontos
        pdf.drawString(100, y, f"{criterio}: {nota_atribuida}% ({pontos_recebidos:.1f} pontos)")
        y -= 20

    # Nota final
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, y - 30, f"Nota final: {nota_final:.2f} pontos.")
    pdf.save()
    st.success(f"✅ Arquivo '{caminho_arquivo}' salvo com sucesso!")

st.title("Boletim de Avaliação Articuladora")
st.write("Bem-vindo ao Avaliador de Atividade Articuladora por Rodrigo Noronha de Mello")

avaliacao = st.text_input("Qual o nome da avaliação?").strip()
grupo = st.text_input("Qual o nome do grupo?").strip()

pontos = st.number_input("Qual o peso da avaliação? (em pontos)", min_value=0.0, step=1.0)

criterios_avaliacao = {
    "Profissionalismo": "Trabalho colaborativo, entrega dentro do prazo, ortografia e gramática adequadas.",
    "Orientações de entrega": "O trabalho atende as orientações e instruções de entrega.",
    "Qualidade das informações": "As informações apresentadas são relevantes e bem estruturadas.",
    "Cobertura do caso": "Todas as informações solicitadas para o caso foram contempladas.",
    "Formatação ABNT": "O documento postado atende à formatação conforme as normas da ABNT.",
    "Referências": "As referências estão no formato da ABNT, são atualizadas e confiáveis."
}

st.subheader("Critérios de Avaliação")
for criterio, definicao in criterios_avaliacao.items():
    st.write(f"**{criterio}:** {definicao}")

# Inserir pesos para os critérios
pesos = {}
st.subheader("Pesos dos Critérios (em %)")
for criterio in criterios_avaliacao:
    pesos[criterio] = st.number_input(f"{criterio} (peso %):", min_value=0.0, max_value=100.0, step=1.0)

if sum(pesos.values()) != 100:
    st.warning("⚠ A soma dos pesos deve ser exatamente 100%. Ajuste os valores.")

# Inserir notas dos critérios
notas = {}
st.subheader("Notas dos Critérios")
for criterio in criterios_avaliacao:
    notas[criterio] = st.selectbox(
        f"Nota para {criterio}:", 
        options=[100, 50, 0], 
        format_func=lambda x: f"{x}%"
    )

nota_final = sum((notas[criterio] / 100) * (pesos[criterio] / 100) * pontos for criterio in criterios_avaliacao)
st.metric("Nota Final da Avaliação", f"{nota_final:.2f} pontos")

if st.button("Gerar PDF"):
    gerar_pdf(avaliacao, grupo, pontos, pesos, notas, nota_final)
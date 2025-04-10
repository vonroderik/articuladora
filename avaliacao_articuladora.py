"""
Created on Apr 10 2025

@author: Rodrigo Noronha de Mello
GitHub: https://github.com/vonroderik
"""

import tkinter as tk
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def gerar_pdf(avaliacao, grupo, pontos, pesos, notas, nota_final):
    # Criar janela para selecionar pasta de destino
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    pasta_destino = filedialog.askdirectory(title="Selecione onde deseja salvar o PDF")

    if not pasta_destino:
        print("\n⚠ Nenhuma pasta selecionada! O arquivo não será salvo.")
        return  # Sai da função sem salvar o arquivo

    nome_arquivo = input("\nDigite um nome para o arquivo PDF (sem extensão): ").strip()
    caminho_arquivo = f"{pasta_destino}/{nome_arquivo}.pdf"

    pdf = canvas.Canvas(caminho_arquivo, pagesize=letter)
    
    # Título
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
    print(f"\n✅ Arquivo '{caminho_arquivo}' salvo com sucesso!")

while True:
    print("\nBEM-VINDO AO AVALIADOR DE ATIVIDADE ARTICULADORA")
    print("por Rodrigo Noronha de Mello")

    avaliacao = input("\nQual o nome da avaliação? ").strip()
    grupo = input("Qual o nome do grupo? ").strip()

    while True:
        nota_avaliacao = input("\nQual o peso da avaliação? Digite apenas números: ").replace(",", ".")
        try:
            pontos = float(nota_avaliacao)
            break
        except ValueError:
            print("⚠ Erro! Você deve digitar um número válido. Tente novamente.")

    criterios_avaliacao = {
        "Profissionalismo": "Trabalho colaborativo, entrega dentro do prazo, ortografia e gramática adequadas.",
        "Orientações de entrega": "O trabalho atende as orientações e instruções de entrega.",
        "Qualidade das informações": "As informações apresentadas são relevantes e bem estruturadas.",
        "Cobertura do caso": "Todas as informações solicitadas para o caso foram contempladas.",
        "Formatação ABNT": "O documento postado atende à formatação conforme as normas da ABNT.",
        "Referências": "As referências estão no formato da ABNT, são atualizadas e confiáveis."
    }

    print("\nCritérios de avaliação:\n")
    for criterio, definicao in criterios_avaliacao.items():
        print(f"{criterio}: {definicao}\n")

    while True:
        pesos = {}
        print("\nAgora, digite o peso (em percentual) para cada critério:")
        for criterio in criterios_avaliacao:
            while True:
                peso = input(f"{criterio}: ").replace(",", ".").replace("%", "")
                try:
                    peso = float(peso)
                    pesos[criterio] = peso
                    break
                except ValueError:
                    print("⚠ Erro! Você deve digitar um número válido. Tente novamente.")

        soma_pesos = sum(pesos.values())

        if soma_pesos == 100:
            print("\n✅ Os pesos foram inseridos corretamente!")
            for criterio, peso in pesos.items():
                print(f"{criterio}: {peso}%")
            break
        else:
            print(f"\n⚠ Atenção! A soma dos pesos inseridos é {soma_pesos:.2f}%, mas deveria ser 100%. Tente novamente.")

    notas = {}
    print("\nAgora, digite a nota do aluno para cada critério:")
    print("1 - Atende plenamente (100%)")
    print("2 - Atende parcialmente (50%)")
    print("3 - Não atende (0%)\n")

    for criterio in criterios_avaliacao:
        while True:
            nota = input(f"{criterio}: ")
            if nota == "1":
                notas[criterio] = 100
                break
            elif nota == "2":
                notas[criterio] = 50
                break
            elif nota == "3":
                notas[criterio] = 0
                break
            else:
                print("⚠ Erro! Digite apenas '1', '2' ou '3'.")

    nota_final = sum((notas[criterio] / 100) * (pesos[criterio] / 100) * pontos for criterio in criterios_avaliacao)

    print(f"\n🔎 Nota final da avaliação: {nota_final:.2f} pontos.")

    while True:
        print("\nOpções:")
        print("1 - Avaliar outro grupo (mantendo os critérios)")
        print("2 - Iniciar nova avaliação do zero")
        print("3 - Gerar PDF")
        print("4 - Sair")

        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            grupo = input("\nDigite o nome do novo grupo: ").strip()

            # Pedir novamente as notas para o novo grupo
            notas = {}
            print("\nAgora, digite a nota do aluno para cada critério:")
            print("1 - Atende plenamente (100%)")
            print("2 - Atende parcialmente (50%)")
            print("3 - Não atende (0%)\n")

            for criterio in criterios_avaliacao:
                while True:
                    nota = input(f"{criterio}: ")
                    if nota == "1":
                        notas[criterio] = 100
                        break
                    elif nota == "2":
                        notas[criterio] = 50
                        break
                    elif nota == "3":
                        notas[criterio] = 0
                        break
                    else:
                        print("Erro! Digite apenas '1', '2' ou '3'.")

            # Recalcular nota final
            nota_final = sum((notas[criterio] / 100) * (pesos[criterio] / 100) * pontos for criterio in criterios_avaliacao)

            print(f"\nNota final da avaliação: {nota_final:.2f} pontos.")
            continue  # Retorna ao menu após avaliar o novo grupo

        elif opcao == "2":
            print("\nIniciando uma nova avaliação do zero...\n")
            break

        elif opcao == "3":
            gerar_pdf(avaliacao, grupo, pontos, pesos, notas, nota_final)
            continue    

        elif opcao == "4":
            print("\nSaindo do programa...")
            exit()

        else:
            print("\nOpção inválida! Escolha entre 1, 2, 3 ou 4.")

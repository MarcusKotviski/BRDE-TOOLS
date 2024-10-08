from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from functions_for_windows import show_popup
from selenium.webdriver.common.by import By
from datetime import datetime
from tkinter import filedialog
from selenium import webdriver
import tkinter as tk
import pandas as pd

TIMER = 120

def registrar_ocorrencia_da_data(data):
    # Dia de ontem
    dia_digitado = int(data[0:2])
    mes_digitado = int(data[3:5])
    ano_digitado = int(data[6:10])
    dia_formatado = datetime(ano_digitado, mes_digitado, dia_digitado, 0, 0)

    dia_formatado_preencher = data

    # Abrindo Excel
    root = tk.Tk()
    root.withdraw()

    # Caminho Excel e nome planilha
    CAMINHO_ARQUIVO = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo", filetypes=(("Arquivos do Excel", "*.xlsx"), ("Todos os arquivos", "*.*")))
    df = pd.read_excel(CAMINHO_ARQUIVO, sheet_name='Planilha1')

    # Logando
    driver = webdriver.Chrome()
    driver.get(f"https://brbank.brde.com.br/Pessoas/Buscar")

    # Pegando valores do excel e adicionando a lista
    for i, mutuario in enumerate(df['MUTUÁRIO']):
        cobranca = '13'
        if dia_formatado == df.loc[i, 'DATA']:
            # Valores
            descricao = df.loc[i, 'OBSERVAÇÃO']
            nome = df.loc[i, 'NOME']

            # Nome do mutuario
            print(mutuario)

            # Acessando o site
            driver.get(f"https://brbank.brde.com.br/Pessoas/Buscar")

            # Encontrando e preenchendo barra de pesquisa
            encontrando_barra_pesquisa = WebDriverWait(driver, TIMER).until(EC.presence_of_element_located((By.ID, 'NomeCnpjCpf')))
            encontrando_barra_pesquisa.clear()
            encontrando_barra_pesquisa.send_keys(mutuario)
            encontrando_barra_pesquisa.send_keys(Keys.ENTER)

            # Entrando nas "Ocorrência"
            entrando_ocorrencias = WebDriverWait(driver, TIMER).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div[3]/table/tbody/tr/td[6]/a/span')))
            entrando_ocorrencias.click()

            # Entrando em "Incluir Ocorrência"
            entrando_incluir = WebDriverWait(driver, TIMER).until(EC.presence_of_element_located((By.ID, 'addOcorrenciaBtn')))
            entrando_incluir.send_keys(Keys.ENTER)

            # Seleciona assunto e preenche "13 - Cobrança"
            preenchendo_assunto_1 = WebDriverWait(driver, TIMER).until(EC.presence_of_element_located((By.ID, 'select2-AssuntoOcorrenciaId-container')))
            preenchendo_assunto_1.click()
            preenchendo_assunto_2 = WebDriverWait(driver, TIMER).until(EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input')))
            preenchendo_assunto_2.send_keys(cobranca)
            preenchendo_assunto_2.send_keys(Keys.ENTER)

            # Inserindo data
            inserindo_data = WebDriverWait(driver, TIMER).until(EC.presence_of_element_located((By.ID, 'Data')))
            inserindo_data.clear()
            inserindo_data.send_keys(str(dia_formatado_preencher))

            # Inserindo "Descrição"
            inserindo_descricao = WebDriverWait(driver, TIMER).until(EC.presence_of_element_located((By.NAME, 'Descricao')))
            inserindo_descricao.send_keys(f'{nome}: {descricao}')

            # Encontra o "Incluir Ocorrência"
            incluindo = WebDriverWait(driver, TIMER).until(EC.presence_of_element_located((By.ID, 'createBtn')))
            incluindo.send_keys(Keys.ENTER)

            finalizando = WebDriverWait(driver, TIMER).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pagination"]/ul/li[3]/a')))
            finalizando.click()
    
    show_popup('Ocorrencias', f"Ocorrencias registradas com sucesso")
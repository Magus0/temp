import PySimpleGUI as sg
import os
import fitz
from tinydb import TinyDB, Query
from subprocess import call
import time

def Obter_eqString_da_variavel_global(variavel):
    return [k for k, v in globals().items() if v is variavel][0]

def add_to_metadados(var):
    db_absolute_path = 'C:\\Users\\luizm\\Documents\\Python\\Projetos\\Livraria_pdf\\tinydb\\metadados.json'
    db = TinyDB(db_absolute_path)

    # verifica se a chave já existe na base de dados
    if db.contains(Query().key == Obter_eqString_da_variavel_global(var)):
        # atualiza o registro correspondente
        db.update({'value': var}, Query().key == Obter_eqString_da_variavel_global(var))
    else:
        # insere um novo registro
        db.insert({'key': Obter_eqString_da_variavel_global(var), 'value': var})

    db.close()

# o path precisa ser absoluto e conter a extensão .py no final.
def executar_py(path):
    call(['python', path])

# atualizar para que 'status' retorne o log da gui
def atualizar_log(text=None, cor=None):
    if text is None:
        text = ''
    if cor is None:
        cor = '#008000'
    window['status'].update(text, text_color=cor)

# Definindo o layout da janela
layout = [[sg.Text('Arquivo:', size=(11,1)), sg.InputText(key='path_pdf', size=(40, 1)), sg.FileBrowse('Procurar', size=(10,1)), sg.Button('Visualizar', size=(10, 1))],
          [sg.Text('Título', size=(11,1)), sg.InputText(key='caixa1', size=(30, 1))],
          [sg.Text('Autor', size=(11,1)), sg.InputText(key='caixa2', size=(30, 1))],
          [sg.Text('Editora', size=(11,1)), sg.InputText(key='caixa3', size=(30, 1))],
          [sg.Text('Ano', size=(11,1)), sg.InputText(key='caixa4', size=(30, 1))],
          [sg.Text('Idioma', size=(11,1)), sg.InputText(key='caixa5', size=(30, 1))],
          [sg.Text('ISBN', size=(11,1)), sg.InputText(key='caixa6', size=(30, 1))],
          [sg.Text('Assunto', size=(11,1)), sg.InputText(key='caixa7', size=(30, 1))],
          [sg.Text('Palavras chave', size=(11,1)), sg.InputText(key='caixa8', size=(30, 1))],
          [sg.Button('Limpar campos', size=(15, 1), button_color=('white', 'red'), font=('Helvetica', 12)), sg.Button('Editar', size=(12, 1), button_color=('white', 'green'), font=('Helvetica', 12))],
          [sg.Text(key='status', size=(40,1), font=('Helvetica bold', 10))]]

# Criando a janela
window = sg.Window('Editor de metadados de pdf', layout)

# Loop para manter a janela aberta e receber entradas do usuário
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Limpar campos':
        atualizar_log()
        # Limpar todos os campos de entrada
        for i in range(1, 9):
            window[f'caixa{i}'].update('')
        window['path_pdf'].update('')
    elif event == 'Editar':
        atualizar_log()
        # Obtendo o path do arquivo
        caminho_pdf = values['path_pdf']
        if caminho_pdf == '':
            continue
        # Obtendo os valores das caixas de texto
        input_usuario = [values[f'caixa{i}'] for i in range(1, 9)]
        # atualizando o .json e executando o editor de pdf
        atualizar_log('Editando metadados...')
        add_to_metadados(caminho_pdf)
        add_to_metadados(input_usuario)
        executar_py('C:\\Users\\luizm\\Documents\\Python\\Projetos\\Livraria_pdf\\Gerenciador_pdf\\Editor_metadados.py')
    elif event == 'Procurar':
        # Abrir uma janela para procurar um arquivo
        file_path = sg.popup_get_file('Procurar arquivo', no_window=True)
        if file_path:
            window['status'].update(f'Arquivo selecionado: {file_path}')
            # Atualizar a caixa de texto com o path do arquivo selecionado
            window['path_pdf'].update(file_path)
            window.refresh()
            #atualizar_log('Caminho adicionado')
    elif event == 'Visualizar':
        filepath = values['path_pdf']
        # verificar se o arquivo é .pdf
        atualizar_log()
        if filepath:
            # Carregar o arquivo PDF e gerar a imagem em miniatura
            with fitz.open(filepath) as pdf:
                first_page = pdf[0]
                image = first_page.get_pixmap(alpha=False, matrix=fitz.Matrix(0.5, 0.5)).tobytes()
            # Abrir uma nova janela para exibir a imagem em miniatura
            thumbnail_layout = [[sg.Image(data=image, size=(300, 400))]]
            thumbnail_window = sg.Window('Miniatura', thumbnail_layout)

            # Loop da janela de miniatura
            while True:
                thumbnail_event, thumbnail_values = thumbnail_window.read()
                if thumbnail_event == sg.WIN_CLOSED:
                    break

            # Fechar a janela de miniatura
            thumbnail_window.close()
        else:
            atualizar_log('Não há nenhum arquivo selecionado','#FF0000')


# Fechando a janela
window.close()

from os import replace
import tkinter as tk
from datetime import date
from seleniumbase import Driver
from tkinter import ttk
from tkinter import messagebox
from selenium import webdriver
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para carregar os nomes das empresas a partir do arquivo "empresas.txt"
def carregar_empresas():
    empresas = []
    try:
        with open("empresas.txt", "r", encoding="utf-8") as file:
            for linha in file:
                dados = linha.strip().split("|")
                empresa = {
                    "nome": dados[0],
                    "cpf": dados[1],
                    "datanasc": dados[2],
                    "cnpj": dados[3],
                    "var": dados[4],
                    "senha_gov": dados[5],
                }
                empresas.append(empresa)    
    except FileNotFoundError:
        with open("empresas.txt", "w", encoding="utf-8") as file:
            pass
    return empresas

# Função para emitir nota de produto na empresa selecionada
def nota_produto():
    item_selecionado = tabela.focus()
    if item_selecionado:
        nome_empresa = tabela.item(item_selecionado)['values'][0]
        print("Empresa selecionada:", nome_empresa)
        
        # Encontrar os dados da empresa selecionada na lista de empresas
        lista_empresas = carregar_empresas()
        dados_empresa = None
        for empresa in lista_empresas:
            print(empresa["nome"])
            if empresa["nome"] == nome_empresa:
                dados_empresa = empresa
                print(dados_empresa)
                break

        if dados_empresa:
            navegador= Driver(uc=True)
            cnpj = dados_empresa["cnpj"]
            datanasc = dados_empresa["datanasc"]
            cpf = dados_empresa["cpf"]
            var = dados_empresa["var"]
            navegador.get('https://www.sefaz.rs.gov.br/nfa/nfe-nfa-mei.aspx')
            iframe_xpath = '//*[@id="iframeConteudo"]'
            frame = WebDriverWait(navegador, 1).until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
            print('waiting 1 sec')
            navegador.switch_to.frame(frame)
            navegador.find_element(By.XPATH, '/html/body/table/tbody/tr/td/form/table[4]/tbody/tr[1]/td[2]/input').send_keys(cpf)
            navegador.find_element(By.XPATH, '/html/body/table/tbody/tr/td/form/table[4]/tbody/tr[2]/td[2]/input').send_keys(datanasc)
            navegador.find_element(By.XPATH, '//*[@id="cnpj"]').send_keys(cnpj)
            if var.isdigit():
                navegador.find_element(By.XPATH, '/html/body/table/tbody/tr/td/form/table[4]/tbody/tr[5]/td[2]/input').send_keys(var)
            else:
                WebDriverWait(navegador, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rdNomeMae"]')))
                navegador.find_element(By.XPATH, '//*[@id="rdNomeMae"]').click()
                navegador.find_element(By.XPATH, '/html/body/table/tbody/tr/td/form/table[4]/tbody/tr[6]/td[2]/input').send_keys(var)
                navegador.find_element(By.XPATH, '/html/body/table/tbody/tr/td/form/table[4]/tbody/tr[7]/td/input').click()

# Funcao para emitir nota de servico na empresa selecionada            
def nota_gov():
    item_selecionado = tabela.focus()
    if item_selecionado:
        nome_empresa = tabela.item(item_selecionado)['values'][0]
        print("Empresa selecionada:", nome_empresa)
        lista_empresas = carregar_empresas()
        dados_empresa = None
        for empresa in lista_empresas:
            if empresa["nome"] == nome_empresa:
                dados_empresa = empresa
                break

        if dados_empresa:
            cpf = dados_empresa["cpf"]
            senha_gov = dados_empresa["senha_gov"]
            if senha_gov == "":
                messagebox.showerror("Erro", "Nenhuma senha encontrada para o CPF cadastrado!\nCadastre uma utilizando o botão 'Editar Empresa'")
                raise ValueError("Nenhuma senha encontrada para o CPF cadastrado!")
            navegador= Driver(uc=True)
            data = date.today()
            data = data.strftime('%d%m%Y')
            navegador.implicitly_wait(10)
            navegador.get('https://www.nfse.gov.br/EmissorNacional/Login?ReturnUrl=%2fEmissorNacional')
            navegador.find_element(By.XPATH, '/html/body/section/div/div/div[2]/div[2]/div[3]/div/a').click()
            navegador.find_element(By.XPATH, '//*[@id="accountId"]').send_keys(cpf)
            navegador.find_element(By.XPATH, '//*[@id="enter-account-id"]').click()
            navegador.find_element(By.XPATH, '//*[@id="password"]').send_keys(senha_gov)
            navegador.find_element(By.XPATH, '//*[@id="submit-button"]').click()
            navegador.get('https://www.nfse.gov.br/EmissorNacional/DPS/Pessoas')
            navegador.find_element(By.XPATH, '//*[@id="DataCompetencia"]').send_keys(data)

# Funcao para atualizar a lista apos inserir ou alterar empresas           
def atualizar_lista_empresas():
    lista_empresas = carregar_empresas()
    tabela.delete(*tabela.get_children())
    for empresa in lista_empresas:
        tabela.insert("", "end", values=(empresa["nome"],))

# Funcao para limitar os caracteres na GUI
def validate_input(P, limit):
    if len(P) > limit:
        return False
    return P.isdigit() or P == ""

# Função para abrir a janela de adicionar empresa
def abrir_interface_adicionar_empresa(dados_empresa=None):
    def salvar_nova_empresa():
        nova_empresa = {
            "nome": entry_nome.get().upper(),
            "cpf": entry_cpf.get()[:11],
            "datanasc": entry_datanasc.get()[:8],
            "cnpj": entry_cnpj.get()[:14],
            "nire_mae": entry_nire_mae.get(),
            "senha_gov": entry_senha_gov.get()    
        }

        if dados_empresa:
            arquivo_temp = "empresas_temp.txt"
            with open("empresas.txt", "r") as arquivo_original, open(arquivo_temp, "w") as arquivo_novo:
                for linha in arquivo_original:
                    dados = linha.strip().split("|")
                    if dados[0] == dados_empresa["nome"]:
                        linha_editada = f"{nova_empresa['nome']}|{nova_empresa['cpf']}|{nova_empresa['datanasc']}|{nova_empresa['cnpj']}|{nova_empresa['nire_mae']}|{nova_empresa['senha_gov']}\n"
                        arquivo_novo.write(linha_editada)
                    else:
                        arquivo_novo.write(linha)
            replace(arquivo_temp, "empresas.txt")
        else:
            with open("empresas.txt", "a") as file:
                file.write(f"{nova_empresa['nome']}|{nova_empresa['cpf']}|{nova_empresa['datanasc']}|{nova_empresa['cnpj']}|{nova_empresa['nire_mae']}|{nova_empresa['senha_gov']}\n")

        janela_adicionar.destroy()
        atualizar_lista_empresas()
        carregar_empresas()

    # Criar a janela de adicionar empresa
    janela_adicionar = tk.Toplevel()
    janela_adicionar.title("Adicionar Empresa" if not dados_empresa else "Editar Empresa")
    janela_adicionar.resizable(False, False)
    validate_cpf = janela_adicionar.register(lambda P: validate_input(P, 11))
    validate_cnpj = janela_adicionar.register(lambda P: validate_input(P, 14))
    validate_datanasc = janela_adicionar.register(lambda P: validate_input(P, 8))

    # Campos de entrada para adicionar os dados da empresa
    tk.Label(janela_adicionar, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entry_nome = tk.Entry(janela_adicionar, width=50)
    entry_nome.focus_set()
    entry_nome.grid(row=0, column=1, padx=5, pady=5)
    if dados_empresa:
        entry_nome.insert(0, dados_empresa["nome"])

    tk.Label(janela_adicionar, text="CPF:").grid(row=1, column=0, padx=5, pady=5)
    entry_cpf = tk.Entry(janela_adicionar, width=50, validate="key", validatecommand=(validate_cpf, '%P'))
    entry_cpf.grid(row=1, column=1, padx=5, pady=5, )
    if dados_empresa:
        entry_cpf.insert(0, dados_empresa["cpf"])

    tk.Label(janela_adicionar, text="Data de Nascimento:").grid(row=2, column=0, padx=5, pady=5)
    entry_datanasc = tk.Entry(janela_adicionar, width=50, validate="key", validatecommand=(validate_datanasc, '%P'))
    entry_datanasc.grid(row=2, column=1, padx=5, pady=5)
    if dados_empresa:
        entry_datanasc.insert(0, dados_empresa["datanasc"])

    tk.Label(janela_adicionar, text="CNPJ:").grid(row=3, column=0, padx=5, pady=5)
    entry_cnpj = tk.Entry(janela_adicionar, width=50, validate="key", validatecommand=(validate_cnpj, '%P'))
    entry_cnpj.grid(row=3, column=1, padx=5, pady=5)
    if dados_empresa:
        entry_cnpj.insert(0, dados_empresa["cnpj"])
    
    tk.Label(janela_adicionar, text="NIRE / Nome da mãe:").grid(row=4, column=0, padx=5, pady=5)
    entry_nire_mae = tk.Entry(janela_adicionar, width=50)
    entry_nire_mae.grid(row=4, column=1, padx=5, pady=5)
    if dados_empresa:
        entry_nire_mae.insert(0, dados_empresa["var"])

    tk.Label(janela_adicionar, text="Senha GOV.BR:").grid(row=5, column=0, padx=5, pady=5)
    entry_senha_gov = tk.Entry(janela_adicionar, width=50)
    entry_senha_gov.grid(row=5, column=1, padx=5, pady=5)
    if dados_empresa:
        entry_senha_gov.insert(0, dados_empresa["senha_gov"])

    # Botão para confirmar e salvar os dados
    botao_salvar = tk.Button(janela_adicionar, text="Salvar", command=salvar_nova_empresa, width=20)
    botao_salvar.grid(row=6, columnspan=2, padx=5, pady=10)

# Carregar os dados das empresas do arquivo
lista_empresas = carregar_empresas()

# Funcao para editar empresas
def edit_emp():
    item_selec = tabela.focus()
    if item_selec:
        nome_empresa = tabela.item(item_selec)['values'][0]
        print("Empresa selecionada:", nome_empresa)
        
        # Carregar os dados das empresas do arquivo
        lista_empresas = carregar_empresas()
        
        # Encontrar a empresa selecionada
        dados_empresa = None
        for empresa in lista_empresas:
            if empresa["nome"] == nome_empresa:
                dados_empresa = empresa
                break
        
        if dados_empresa:
            abrir_interface_adicionar_empresa(dados_empresa)

# Funcao para excluir empresas
def exc_emp():
    item_selec = tabela.focus()
    if item_selec:
        nome_empresa = tabela.item(item_selec)['values'][0]
        print("Empresa selecionada:", nome_empresa)
        # Carregar todas as empresas do arquivo
        lista_empresas = carregar_empresas()

        # Filtrar a lista removendo a empresa selecionada
        lista_empresas = [empresa for empresa in lista_empresas if empresa["nome"] != nome_empresa]

        # Reescrever o arquivo com as empresas restantes
        with open("empresas.txt", "w", encoding="utf-8") as file:
            for empresa in lista_empresas:
                file.write(f"{empresa['nome']}|{empresa['cpf']}|{empresa['datanasc']}|{empresa['cnpj']}|{empresa['var']}|{empresa['senha_gov']}\n")
        
        # Atualizar a lista na interface
        atualizar_lista_empresas()

# Criar a interface gráfica principal
root = tk.Tk()
root.geometry('520x273')
root.minsize(width=520, height=273)
root.iconbitmap("icone.ico")
root.title("Programa Gerador de NF e NFS-e")

# Criar um frame para a tabela e a scrollbar
frame_tabela = tk.Frame(root)
frame_tabela.pack(padx=10, pady=1, fill=tk.BOTH, expand=True)

# Criar a tabela para exibir os nomes das empresas
tabela = ttk.Treeview(frame_tabela, columns=("Nome"), show="headings")
tabela.heading("#1", text="Nome da Empresa")
tabela.column("#1", width=300)

# Adicionar uma scrollbar à tabela
scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scrollbar.set)

# Posicionar a tabela e a scrollbar dentro do frame
tabela.pack(side="left", fill=tk.BOTH, expand=True)
scrollbar.pack(side="right", fill="y")


# Inserir os nomes das empresas na tabela
for empresa in lista_empresas:
    tabela.insert("", "end", values=(empresa["nome"],))

# Botão para fazer nota de produtos
botao_mostrar_detalhes = tk.Button(root, text="Nota Produto", command=nota_produto)
botao_mostrar_detalhes.pack(side=tk.LEFT, padx=5, pady=5, fill=None)

# Botão para fazer notas de serviços
botao_mostrar_detalhes = tk.Button(root, text="Nota Serviço", command=nota_gov)
botao_mostrar_detalhes.pack(side=tk.LEFT, padx=5, pady=5, fill=None)

# Botão para abrir a janela de adicionar empresa
botao_adicionar_empresa = tk.Button(root, text="Adicionar Empresa", command=abrir_interface_adicionar_empresa)
botao_adicionar_empresa.pack(side=tk.LEFT, padx=5, pady=5, fill=None)

# Botao para abrir a janela de editar empresa
botao_adicionar_empresa = tk.Button(root, text="Editar Empresa", command=edit_emp)
botao_adicionar_empresa.pack(side=tk.LEFT, padx=5, pady=5, fill=None)

# Botao para abrir a janela de editar empresa
botao_adicionar_empresa = tk.Button(root, text="Excluir Empresa", command=exc_emp)
botao_adicionar_empresa.pack(side=tk.LEFT, padx=5, pady=5, fill=None)

# Executar a interface
root.mainloop()


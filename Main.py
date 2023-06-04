#Primeiro projeto estruturado em Python

#Desenvolvido por Lucas Stallbaum

#Data de Criação 06/06/2022

#TCC Curso Sintec

#DESCRIÇÃO;

#   -Cópia do layout da NuBank(Mobile),
#       programa realiza conexão com o MySQL, e usa a interface gráfica já integrada com o PY o TKinter, usado em praticamente toda sua estrutura, 
#       biblioteca Pandas no backend, escolhida para fazer inserts, updates etc, e as funções em python.
#


#Instruções para usar;

#Instalar Python, e MySQL(se preferir, escrever diretamente o usuário e senha no código, excluindo as conexões com o banco)
# realizar o Pip Install das seguintes bibliotecas: PyoDbc, pandas, ttkthemes, pil;


# ------------------------------------------------------------Versão BETA, ainda há ajustes de layout.------------------------------------------------------


import tkinter as tk
from   tkinter import LEFT, PhotoImage, StringVar, ttk
import pyodbc as odbc
import pandas as pd
from   ttkthemes import ThemedTk
from   PIL import ImageTk, Image


def login():
    global numero_conta
    global nome_colaborador
    try:
        conta_get   = int(account.get())
        senha_get   = int(psw.get())
        agencia_get = str(agency.get())

        query = f'''SELECT *
         FROM conta 
         WHERE conta = {conta_get} AND agencia = {agencia_get}'''
        execute = pd.read_sql_query(query, connection)

        for index, row in execute.iterrows():
            if row.senha == senha_get and row.agencia == agencia_get:         
                main_frame_1.destroy()
                main_frame_2.pack(fill=tk.BOTH, 
                                            expand = True, 
                                                anchor = tk.CENTER
) 
                numero_conta = row.conta
                nome()
                saldo()
            else:
                error_message.pack(pady = (20, 0))
                error_message.config(fg = 'white')
    except:
        error_message.pack(pady = (20, 0))
        error_message.config(fg = 'white')

#Função feita registra os numeros clicados com o mouse no mouse numerico na Entry
def visorentry(num):
    global equacao_texto
     
    equacao_texto = equacao_texto + str(num)
    equacao_label.set(equacao_texto)

#Função que apaga o ultimo numero registrado na Entry
def apagar():
    global equacao_texto
    equacao_texto = equacao_texto[:-1]
    equacao_label.set(equacao_texto)

#Função que destrói a tela principal e mostra a tela de transferir
def transferir_def(event):
    main_frame_2.destroy()
    root.geometry('350x660')
    main_frame_5.pack(fill=tk.BOTH, 
                                expand = True, 
                                    anchor = tk.CENTER
)

#Função criada para recolher as credenciais da pessoa favorecida, e fazer a transferencia de uma conta a outra

def credenciais_transferencias():
    global valor_transferencia

    agencia_get    = str(agency_transferir.get())
    conta_get      = int(account_transferir.get())       
    senha_get      = int(psw_transferir.get())
    id_conta_trans = None
    id_conta       = None
    
    query = f'SELECT id_conta FROM conta WHERE conta = {conta_get} AND agencia = {agencia_get}'
    execute = pd.read_sql_query(query, connection)
    for index, row in execute.iterrows():
        if row.id_conta != '':
            id_conta_trans = row.id_conta

    query = f'SELECT id_conta, senha, saldo FROM conta WHERE conta = {numero_conta}'
    execute = pd.read_sql_query(query, connection)
    for index, row in execute.iterrows():
        id_conta = row.id_conta
        if row.senha == senha_get:
            if int(row.saldo) >= int(valor_transferencia):
                query = 'UPDATE conta SET saldo = saldo - (?) WHERE id_conta = (?)'
                cursor.execute(query, (str(valor_transferencia), str(id_conta)))
                connection.commit()

                query = 'UPDATE conta SET saldo = saldo + (?) WHERE id_conta = (?)'
                cursor.execute(query, (str(valor_transferencia), str(id_conta_trans)))
                connection.commit()
            else:
                print('saldo insuficiente')
        else:
            print('senha incorreta') 

#Função para recolher o valor a ser enviado
def envio_transferencia(event):
    global valor_transferencia
    valor_transferencia = str(entry_transferir.get())
    main_frame_5.destroy()
    main_frame_6.pack(fill=tk.BOTH, 
                                expand = True, 
                                    anchor = tk.CENTER
)
    root.geometry('350x550')
#Função que destroi 
def deposito_def(event):
    main_frame_2.destroy()
    root.geometry('350x660')
    main_frame_4.pack(fill=tk.BOTH, 
                                expand = True, 
                                        anchor = tk.CENTER
)

#Função que faz o deposito na conta 
def envio_deposito_def(event):
    global cursor
    global numero_conta

    deposito_get = str(entry_deposito.get())
    query = """
    UPDATE conta
    SET saldo = saldo + (?)
    WHERE conta = (?)
    """
    cursor.execute(query, (deposito_get, numero_conta))
    connection.commit()

#Função em construcao kkkk
def back_def(event):
    main_frame_4.destroy()
    main_frame_2.pack(fill=tk.BOTH, 
                            expand = True, 
                                anchor = tk.CENTER
)


#Função que puxa do banco de dados o nome de quem esta acessando a conta
def nome():
    query = f'''
        SELECT nome
        FROM colaborador cr
        JOIN conta co ON co.id_colaborador = cr.id_colaborador
        WHERE conta = {numero_conta}'''

    execute = pd.read_sql_query(query, connection)

    for index, row in execute.iterrows():
        nome_txt.config(text = f'Olá, {row.nome}')


#Função que puxa do banco de dados o saldo da pessoa que esta acessando a conta
def saldo():
    query = f'''
        SELECT saldo
        FROM conta ca
        JOIN colaborador cr ON ca.id_colaborador = cr.id_colaborador
        WHERE conta = {numero_conta}'''

    execute = pd.read_sql_query(query, connection)

    for index, row in execute.iterrows():
        saldo_int.config(text = f'R${row.saldo}')


################################

# CONEXÃO MYSQL
connection_string = '''
DRIVER={MySQL ODBC 8.0 ANSI Driver}; 
SERVER=localhost;DATABASE=banco_digital; 
UID=root; PASSWORD=$C418; OPTION=3;Trusted_connection = yes'''
connection = odbc.connect(connection_string)
cursor     = connection.cursor()
################################

# CONSTANTES

background_color = '#8a05be'
numero_conta     = None
numero_conta_destinatario = None
sizesBx          = 8       
sizesBy          = 4
color            = 'white'
activebg         = '#262626'
valor_transferencia = None

################################

# TELA PROGRAMA

root = ThemedTk (theme = "breeze")
root.geometry   ('350x600')
style           = ttk.Style(root)
root.resizable  (False, False)
root.title      ('NUbank App')
root.tk.call ('wm', 'iconphoto', root._w, tk.PhotoImage(file=r'_img\ico.png'))
equacao_texto   = ''
equacao_label   = StringVar()

################################
# FRAMES
  
main_frame_1         = tk.Frame(root)
login_frame          = tk.Frame(main_frame_1)

main_frame_2         = tk.Frame(root)
nome_frame           = tk.Frame(main_frame_2, width=350, height=100)
saldo_frame          = tk.Frame(main_frame_2, width=350, height=300)
fatura_frame         = tk.Frame(main_frame_2, width=350, height=200)

main_frame_4         = tk.Frame(root)
deposito_frame       = tk.Frame(main_frame_4, width=350,  height=300)
deposito_num_frame   = tk.Frame(main_frame_4, width=350,  height=370)

main_frame_5         = tk.Frame(root)
transferir_frame     = tk.Frame(main_frame_5, width=350,  height=300)
transferir_num_frame = tk.Frame(main_frame_5, width=350,  height=370) 

main_frame_6                   = tk.Frame(root)
credencial_transferencia_frame = tk.Frame(main_frame_6,  width=350,  height=200)

################################
# TELA DE LOGIN

main_frame_1.pack(fill = tk.BOTH, 
                            expand = True, 
                                    anchor = tk.CENTER
)

login_frame.pack(fill = tk.BOTH,  
                            expand = True
)
login_frame.config(bg = background_color
)

# LOGO IMG
logo = ImageTk.PhotoImage(Image.open(r"_img\icon2.png")
)
logo_img = tk.Label(
                    login_frame, 
                    image = logo, 
                    width=150, 
                height=150
)
logo_img.pack(pady = (40, 0)
)

# AGENCIA
agency_txt = tk.Label(
                    login_frame, 
                    text = 'Agência',
                    bg = background_color, 
                    fg = 'white', 
                    font = ('Arial', 12, 'bold')
)
agency_txt.pack(pady = (25, 5)
)
agency = ttk.Entry(login_frame, 
                    width = 25
)
agency.pack(pady = (5, 0)
)

# CONTA
account_txt = tk.Label(
                    login_frame, 
                    text = 'Conta',       
                    bg = background_color, 
                    fg = 'white', 
                    font = ('Arial', 12, 'bold'), 
)
account_txt.pack(pady = (15, 5)
)
account = ttk.Entry(login_frame, 
                    width = 25
)
account.pack()

# SENHA
psw_txt = tk.Label(
                    login_frame, 
                    text = 'Senha', 
                    bg = background_color, 
                    fg = 'white', 
                    font = ('Arial', 12, 'bold')
)
psw_txt.pack(pady = (10, 5)
)
psw = ttk.Entry(
                login_frame,
                width = 25
)
psw.pack()

# BOTAO ENTRAR
proceed_button = ttk.Button(
                            login_frame, 
                            text = 'Entrar', 
                            command= lambda: login() 
)
proceed_button.pack(pady = (20, 0)
)

# MENSAGEM DE ERRO
error_message = tk.Label(login_frame, 
                        text = 'Credenciais incorretas. Tente novamente.',
                        bg = background_color)

######################################################################################################
# TELA INICIAL
nome_frame.grid(row = 0, 
                column = 0, 
                columnspan = 5, 
                sticky = tk.N
)
nome_frame.grid_propagate(0)
nome_frame.config(bg = background_color)

saldo_frame.grid(row        = 1, 
                 column     = 0, 
                 columnspan = 5
)
saldo_frame.grid_propagate(0
)
saldo_frame.config(bg = 'white'
)

fatura_frame.grid(row        = 2, 
                  column     = 0, 
                  columnspan = 5
)
fatura_frame.grid_propagate(0
)
fatura_frame.config(bg = 'white'
)

# NOME
nome_txt = tk.Label(nome_frame, 
                    font = ('Arial 13 bold'),
                    fg   = 'white', 
                    bg   = background_color
)
nome_txt.grid(row    = 0, 
              column = 0, 
              pady   = (40, 0), 
              padx   = (20, 0)
)

# SALDO
saldo_txt = tk.Label(saldo_frame, 
                     text = 'Saldo', 
                     font = ('Arial 15 '),
                     fg   = 'black', 
                     bg   = 'white'
)
saldo_txt.grid( row    = 0, 
                column = 0, 
                pady   = (15, 5), 
                padx   = (20, 0), 
                sticky = tk.W
)

saldo_int = tk.Label(
                    saldo_frame, 
                    font = ('Arial 17 bold'), 
                    fg   = 'black', 
                    bg   = 'white'
)
saldo_int.grid(row = 1, 
                    column = 0, 
                    pady   = (0, 10), 
                    padx   = (20, 0), 
                    sticky = tk.W
)

# BOTÕES
transferir = ImageTk.PhotoImage(Image.open(r"_img\transferir.png"))

deposito   = ImageTk.PhotoImage(Image.open(r"_img\deposito.png"))

pagar      = ImageTk.PhotoImage(Image.open(r"_img\pagar.png"))

transferir_btn = tk.Label(
                        saldo_frame,    
                        image = transferir, 
                        borderwidth=0
)
transferir_btn.grid(row    = 2, 
                    column = 0, 
                    padx   = (45,1), 
                    pady   = (30,10), 
                    sticky = tk.W
)
transferir_btn.bind('<Button-1>', transferir_def
)

deposito_btn = tk.Label(
                        saldo_frame, 
                        image = deposito, 
                        borderwidth = 0
)
deposito_btn.grid(row = 2, 
                    column = 1, 
                    padx   = (50,1), 
                    pady   = (30,10), 
                    sticky = tk.W
)
deposito_btn.bind('<Button-1>', deposito_def
)
 
# LABELS
label_transferir = tk.Label(saldo_frame, 
                    text = 'Transferir', 
                    font = ('Arial 10 bold'), 
                    bg   = 'white', 
                    fg   = 'black'
)
label_transferir.grid(row = 3, 
                      column = 0,
                      sticky = tk.E
)

label_deposito = tk.Label(saldo_frame, 
                          text = 'Depósito', 
                          font = ('Arial 10 bold'), 
                          bg   = 'white', 
                          fg   = 'black'
)
label_deposito.grid(row = 3,
                    column = 1, 
                    sticky = tk.E
)

separator = ttk.Separator(saldo_frame, orient = 'horizontal').place(x = 0, y = 299, relwidth = 3
)

# TELA DE TRANSFERENCIA #############################################################

#FRAME 
img_back = ImageTk.PhotoImage(Image.open(r"_img\back.jpeg")
)

credencial_transferencia_frame.pack(fill = tk.BOTH, expand = True)

credencial_transferencia_frame.config(bg = background_color)

#LABEL
credencial_transferencia_label = tk.Label(credencial_transferencia_frame, 
                                            text = 'Digite as seguintes informações para seguir com a transferência.', 
                                            font = ('Arial 10 bold'), 
                                            bg   = 'white', 
                                            fg   = 'black'
)

# AGENCIA TRANS
agency_txt_transferir = tk.Label(
                                credencial_transferencia_frame, 
                                text = 'Agência', 
                                bg = background_color, 
                                fg = 'white', 
                                font = ('Arial', 12, 'bold')
)
agency_txt_transferir.pack(pady = (25, 5))

agency_transferir = ttk.Entry(credencial_transferencia_frame, width = 25)

agency_transferir.pack(pady = (5, 0))

# CONTA DE TRANSFERENCIA
account_txt_transferir = tk.Label(
                                credencial_transferencia_frame, 
                                text = 'Conta', 
                                bg = background_color, 
                                fg = 'white', 
                                font = ('Arial', 12, 'bold'), 
)
account_txt_transferir.pack(pady = (15, 5))

account_transferir = ttk.Entry(credencial_transferencia_frame, width = 25)

account_transferir.pack()

# SENHA TRANSFERENCIA
psw_txt_transferir = tk.Label(credencial_transferencia_frame, 
                                text = 'Senha',  
                                bg = background_color, 
                                fg = 'white', 
                                font = ('Arial', 12, 'bold')
)
psw_txt_transferir.pack(pady = (10, 5)
)
psw_transferir = ttk.Entry(
                        credencial_transferencia_frame, 
                        width = 25
)
psw_transferir.pack()

# BOTAO DE TRANSFERENCIA
button_transferir = ttk.Button(
                            credencial_transferencia_frame, 
                            text = 'Enviar.', 
                            command = credenciais_transferencias
)
button_transferir.pack(pady = (20, 0)
)

# MENSAGEM DE ERRO
error_message_transferir = tk.Label(credencial_transferencia_frame, 
                    text = 'Credenciais incorretas. Tente novamente.', 
                        bg = background_color
)

#FRAME 
transferir_frame.config(bg = 'white'
)
transferir_frame.grid(row = 0, 
                        column = 0, 
                        columnspan = 5, 
                        sticky = tk.N
)
transferir_frame.grid_propagate(0
)
transferir_frame.config(bg = 'white'
)

transferir_num_frame.grid(row = 1, 
                        column = 0, 
                        columnspan = 5, 
                        sticky = tk.N
)
transferir_num_frame.grid_propagate(0)

transferir_num_frame.config(bg = 'white')

# BOTAO DE BACK

back_btn1 = tk.Label(transferir_frame, 
                        image = img_back, 
                        borderwidth=0
)
back_btn1.grid(row = 0, 
               column = 0, 
               sticky = tk.W
)
back_btn1.bind('<Button-1>', back_def
)

# LABELS

label_transferencia1 = tk.Label(transferir_frame, 
                                text = 'Qual a quantia ', 
                                font = ('Arial 17 bold'), 
                                bg = 'white',  
                                fg = 'black'
)
label_transferencia1.grid(row = 1, 
                            column = 0, 
                            padx = 42, 
                            pady = (20,0), 
                            columnspan = 5, 
                            sticky = tk.N
)
label_transferencia1.grid_propagate(0
)

label_transferencia2 = tk.Label(transferir_frame, 
                                text = 'você deseja Transferir?', 
                                font = ('Arial 17 bold'), 
                                bg = 'white', 
                                fg = 'black'
)
label_transferencia2.grid(row = 2, 
                        column = 0, 
                        padx = 42,  
                        pady = (0,40), 
                        columnspan = 5,
                        sticky = tk.N
)

label_transferencia2.grid_propagate(0
)

label_transferencia3 = tk.Label(transferir_frame, 
                                text = 'Digite um valor entre R$1,00 e', 
                                font = ('Arial 10 bold'), 
                                bg = 'white', 
                                fg = 'gray'
)
label_transferencia3.grid(row = 4, 
                        column = 0, 
                        padx = 42, 
                        columnspan = 5, 
                        sticky = tk.N
)
label_transferencia3.grid_propagate(0
)

label_transferencia4 = tk.Label(transferir_frame, 
                                text = 'R$6.000,00', 
                                font = ('Arial 10 bold'), 
                                bg = 'white', 
                                fg = 'gray'
)
label_transferencia4.grid(row = 5, 
                        column = 0, 
                        padx = 42,  
                        pady = (0,10), 
                        columnspan = 5, 
                        sticky = tk.N                                   
)
label_transferencia4.grid_propagate(0
)

separtor1 = ttk.Separator(transferir_frame, 
                        orient = 'horizontal').place(x = 0, y = 299, 
                                                        relwidth = 3
)
# ENTRY 

entry_transferir = ttk.Entry(transferir_frame, 
                            width = 25,
                            textvariable = equacao_label
)
entry_transferir.grid(row = 3, 
                        column = 0, 
                        padx = (75,0), 
                        pady = (1,20)
)

# BOTAO DE TRANSFERIR

btn_transferir = tk.Label(transferir_frame, 
                    text = 'Transferir', 
                    bg = 'white', 
                    fg = 'black'
)
 
btn_transferir.grid(row = 6,
                     column = 0, 
                    padx = (80,1)
)

btn_transferir.bind('<Button-1>', envio_transferencia
)

# BOTOES NUMERICOS DO DEPOSITO
 
button10 = tk.Button(transferir_num_frame,
            text = 1,
            bg = color,
            font = 'Arial',
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(1)
)
button10.grid(row = 0, 
            column = 0
)

button20 = tk.Button(transferir_num_frame, 
            text = 2,
            font = 'Arial',
            bg = color,
            activebackground = activebg, 
                width = sizesBx,  
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(2)
)
button20.grid(row = 0, column = 1
)

button30 = tk.Button(transferir_num_frame,
            text = 3, 
            font = 'Arial',
            bg = color,
            activebackground = activebg, 
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(3)
)
button30.grid(row = 0, column = 2
)

button40 = tk.Button(transferir_num_frame, 
            text = 4,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(4)
)
button40.grid(row = 1, 
            column = 0            
)

button50 = tk.Button(transferir_num_frame, 
            text = 5,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(5)
)
button50.grid(row = 1, 
            column = 1
)

button60 = tk.Button(transferir_num_frame, 
            text = 6,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(6)
)
button60.grid(row = 1, 
            column = 2
)

button70 = tk.Button(transferir_num_frame, 
            text = 7,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(7)
)
button70.grid(row = 2, 
            column = 0
)

button80 = tk.Button(transferir_num_frame, 
            text = 8,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(8)
)
button80.grid(row = 2, 
            column = 1
)

button90 = tk.Button(transferir_num_frame, 
            text = 9,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(9)
)
button90.grid(row = 2, 
            column = 2
)

button00 = tk.Button(transferir_num_frame, 
            text = 0,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0, 
                command = lambda:visorentry(0)
)
button00.grid(row = 3, 
            column = 1
)

button_ponto0 = tk.Button(transferir_num_frame, 
            font = 'Arial',
            bg = color,
            text = '.',
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(".")
)
button_ponto0.grid(row = 1,
            padx = (6,6),
            pady = (5,5),
            column = 3
)

button_virgula0 = tk.Button(transferir_num_frame, 
            font = 'Arial',
            bg = color,
            text = ',',
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(",")
)
button_virgula0.grid(row = 2,
            padx = (6,6),
            pady = (5,5),
            column = 3
)


button_apagar0 = tk.Button(transferir_num_frame, 
            text = '⌫',     
            bg = color,
            activebackground = activebg,
            width = 8,
            height = 4,
            borderwidth = 0,
            command = apagar
)
button_apagar0.grid(row = 0, 
            column = 3
)

# TELA DE DEPOSITO ################################################################################################

#IMAGEM
img_back = ImageTk.PhotoImage(Image.open(r"_img\back.jpeg"))

#FRAME d
deposito_frame.grid(row = 0, 
                    column = 0, 
                    columnspan = 5, 
                    sticky = tk.N
)
deposito_frame.grid_propagate(0
)
deposito_frame.config(bg = 'white'
)

deposito_num_frame.grid(row = 1, 
                    column = 0, 
                    columnspan = 5, 
                    sticky = tk.N
)
deposito_num_frame.grid_propagate(0
)
deposito_num_frame.config(bg = 'white'
)
# BOTAO DE BACK

back_btn = tk.Label(deposito_frame, 
                    image = img_back, 
                    borderwidth=0
)
back_btn.grid(row = 0, 
                column = 0, 
                sticky = tk.W                     
)
back_btn.bind('<Button-1>', back_def
)

# LABELS

label_deposito1 = tk.Label(deposito_frame, 
                            text = 'Qual a quantia ', 
                            font = ('Arial 17 bold'), 
                            bg   = 'white', 
                            fg   = 'black'
)
label_deposito1.grid(row = 1, 
                    column = 0, 
                    padx   = 42, 
                    pady   = (20,0),  
                    columnspan = 5, 
                    sticky = tk.N
)
label_deposito1.grid_propagate(0
)

label_deposito2 = tk.Label(deposito_frame, 
                            text = 'você deseja depositar?', 
                            font = ('Arial 17 bold'), 
                            bg = 'white', 
                            fg = 'black'
)
label_deposito2.grid(row = 2, 
                    column = 0, 
                    padx = 42,  
                    pady = (0,40), 
                    columnspan = 5, 
                    sticky = tk.N
)
label_deposito2.grid_propagate(0
)

label_deposito3 = tk.Label(deposito_frame, 
                    text = 'Digite um valor entre R$20,00 e', 
                    font = ('Arial 10 bold'), 
                    bg = 'white', 
                    fg = 'gray'
)
label_deposito3.grid(row = 4, 
                column = 0, 
                padx = 42, 
                columnspan = 5, 
                sticky = tk.N)

label_deposito3.grid_propagate(0
)

label_deposito4 = tk.Label(deposito_frame, 
                            text = 'R$15.000,00', 
                            font = ('Arial 10 bold'), 
                            bg = 'white', 
                            fg = 'gray'
)
label_deposito4.grid(row = 5, 
                    column = 0, 
                    padx = 42,  
                    pady = (0,10), 
                    columnspan = 5, 
                    sticky = tk.N
)
label_deposito4.grid_propagate(0
)

separtor1 = ttk.Separator(deposito_frame, 
                          orient = 'horizontal').place(x = 0, y = 299, relwidth = 3
)
# ENTRY 

entry_deposito = ttk.Entry(deposito_frame, 
                            width = 25, 
                            textvariable = equacao_label
)
entry_deposito.grid(row = 3, 
                    column = 0, 
                    padx = (75,0),
                    pady = (1,20)
)

# BOTAO DE DEPOSITAR

envio_deposito = tk.Label(deposito_frame, 
                    text = 'Depositar', 
                    bg = 'white', 
                    fg = 'black'
)
 
envio_deposito.grid(row = 6, 
                    column = 0, 
                    padx = (80,1)
)

envio_deposito.bind('<Button-1>', envio_deposito_def
)

# BOTOES NUMERICOS DO DEPOSITO
 
button1 = tk.Button(deposito_num_frame,
            text = 1,
            bg = color,
            font = 'Arial',
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(1)
)
button1.grid(row = 0, 
            column = 0            
)

button2 = tk.Button(deposito_num_frame, 
            text = 2,
            font = 'Arial',
            bg = color,
            activebackground = activebg, 
                width = sizesBx,  
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(2)
)
button2.grid(row = 0, column = 1
)

button3 = tk.Button(deposito_num_frame,
            text = 3, 
            font = 'Arial',
            bg = color,
            activebackground = activebg, 
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(3)
)
button3.grid(row = 0, column = 2
)

button4 = tk.Button(deposito_num_frame, 
            text = 4,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(4)
)
button4.grid(row = 1, 
            column = 0
)

button5 = tk.Button(deposito_num_frame, 
            text = 5,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(5)
)
            
button5.grid(row = 1, 
            column = 1
)

button6 = tk.Button(deposito_num_frame, 
            text = 6,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(6)
)
            
button6.grid(row = 1, 
            column = 2
)

button7 = tk.Button(deposito_num_frame, 
            text = 7,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(7)
)
            
button7.grid(row = 2, 
            column = 0
)

button8 = tk.Button(deposito_num_frame, 
            text = 8,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(8)
)
button8.grid(row = 2, 
            column = 1
)

button9 = tk.Button(deposito_num_frame, 
            text = 9,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(9)
)
button9.grid(row = 2, 
            column = 2
)

button0 = tk.Button(deposito_num_frame, 
            text = 0,
            font = 'Arial',
            bg = color,
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0, 
                command = lambda:visorentry(0)
)
button0.grid(row = 3, 
            column = 1
)

button_ponto = tk.Button(deposito_num_frame, 
            font = 'Arial',
            bg = color,
            text = '.',
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(".")
)
button_ponto.grid(row = 1,
            padx = (6,6),
            pady = (5,5),
            column = 3
)

button_virgula = tk.Button(deposito_num_frame, 
            font = 'Arial',
            bg = color,
            text = ',',
            activebackground = activebg,
                width = sizesBx, 
                height = sizesBy,
                borderwidth = 0,
                command = lambda:visorentry(",")
)
button_virgula.grid(row = 2,
            padx = (6,6),
            pady = (5,5),
            column = 3,
)


button_apagar = tk.Button(deposito_num_frame, 
            text = '⌫',     
            bg = color,
            activebackground = activebg,
                width = 8,
                height = 4,
                borderwidth = 0,
                command = apagar
)
button_apagar.grid(row = 0, 
            column = 3
)

# FATURA

#IMAGEM
img_cartao = ImageTk.PhotoImage(Image.open(r"_img\cartao.png")
)

#LABELS
img_label = tk.Label(fatura_frame, 
                    image = img_cartao, 
                        borderwidth=0
)
img_label.grid(row = 0, 
                column = 0, 
                padx = (10,1), 
                pady = (10,2), 
                sticky = tk.W
)


fatura = tk.Label(fatura_frame, 
                    text = 'Cartão de crédito',
                    font = ('Arial 14 bold'), 
                    bg = 'white', 
                    fg = 'black'
)
fatura.grid(row = 1, 
            column = 0, 
            padx = (20,1), 
            pady = (2,5), 
            sticky = tk.W
)
fatura_atual = tk.Label(fatura_frame, 
                        text = 'Fatura atual',
                        font = ('Arial 12 bold'), 
                        bg = 'white', 
                        fg = 'darkgray'
)
fatura_atual.grid(row = 2, 
                column = 0, 
                padx = (20,1), 
                pady = (2,5), 
                sticky = tk.W
)
fatura_valor = tk.Label(
                        fatura_frame, 
                        text = 'R$0,00',
                        font = ('Arial 17 bold'),
                        fg = 'black', 
                        bg = 'white'
)
fatura_valor.grid(
                row = 3, 
                column = 0, 
                padx = (20,1), 
                pady = (10,5), 
                sticky = tk.W)

root.mainloop()

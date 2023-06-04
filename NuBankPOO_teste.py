import tkinter as tk
from tkinter import LEFT, PhotoImage, StringVar, ttk
import pyodbc as odbc
import pandas as pd
from PIL import ImageTk, Image
from ttkthemes import ThemedTk
import messagebox

class NUbankClass:
    def __init__(self):
        self.root            = ThemedTk (theme = "breeze")
        self.root.geometry   ('350x600')
        self.style           = ttk.Style(self.root)
        self.root.resizable  (False, False)
        self.root.title      ('NUbank App')
        self.root.tk.call    ('wm', 'iconphoto', self.root._w, tk.PhotoImage(file='_img\iconn.ico.png'))
        self.equacao_texto   = ''
        self.equacao_label   = StringVar()
        
        self.background_color = '#8a05be'
        self.numero_conta     = None
        self.numero_conta_destinatario = None
        self.sizesBx          = 8       
        self.sizesBy          = 4
        self.color            = 'white'
        self.activebg         = '#262626'
        self.valor_transferencia = None

        self.Tela_login()

        self.root.mainloop()

    def conn(self):     
        self.connection_string = '''
        DRIVER={MySQL ODBC 8.0 ANSI Driver}; 
        SERVER=localhost;DATABASE=banco_digital; 
        UID=root; PASSWORD=lucas04095489;OPTION=3;"
        Trusted_connection = yes'''
        self.connection   = odbc.connect(self.connection_string)
        self.cursor       = self.connection.cursor()
        self.agency       = "3333"
        self.numero_conta = "4444"
        self.psw          = "5555"

    def login(self):
        try:
            self.conta_get   = int(self.account.get())
            self.senha_get   = int(self.psw.get())
            self.agencia_get = str(self.agency.get())
    
            self.query = f'''SELECT *
             FROM conta 
             WHERE conta = {self.conta_get} AND agencia = {self.agencia_get}'''
            self.execute = pd.read_sql_query(self.query, self.connection)
    
            for index, row in self.execute.iterrows():
                if row.senha == self.senha_get and row.agencia == self.agencia_get:         
                    self.main_frame_1.destroy()
                    self.main_frame_2.pack(fill=tk.BOTH, 
                                                expand = True, 
                                                    anchor = tk.CENTER
        ) 
                    self.numero_conta = self.row.conta
                    self.nome()
                    self.saldo()
                else:
                    self.error_message.pack(pady = (20, 0))
                    self.error_message.config(fg = 'white')
        except:
            self.error_message.pack(pady = (20, 0))
            self.error_message.config(fg = 'white')

    #DEF que registra os numeros clicados com o mouse no mouse numerico na Entry
    def visorentry(self, num):
        self.equacao_texto = self.equacao_texto + str(num)
        self.equacao_label.set(self.equacao_texto)

    #DEF que apaga o ultimo numero registrado na Entry
    def apagar(self):
        self.equacao_texto = self.equacao_texto[:-1]
        self.equacao_label.set(self.equacao_texto)

    def envio_transferencia(self, event):
        self.valor_transferencia = str(self.entry_transferir.get())
        self.main_frame_5.destroy()
        self.main_frame_6.pack(fill=tk.BOTH, 
                               expand = True, 
                                    anchor = tk.CENTER
        )
        self.root.geometry('350x550')

    def credenciais_transferencias(self):
        self.agencia_get    = str(self.agency_transferir.get())
        self.conta_get      = int(self.account_transferir.get())       
        self.senha_get      = int(self.psw_transferir.get())
        self.id_conta_trans = None
        self.id_conta       = None
        
        self.query = f'SELECT id_conta FROM conta WHERE conta = {self.conta_get} AND agencia = {self.agencia_get}'
        self.execute = pd.read_sql_query(self.query, self.connection)
        for index, row in self.execute.iterrows():
            if self.row.id_conta != '':
                self.id_conta_trans = self.row.id_conta

        self.query = f'SELECT id_conta, senha, saldo FROM conta WHERE conta = {self.numero_conta}'
        self.execute = pd.read_sql_query(self.query, self.connection)
        for index, row in self.execute.iterrows():
            self.id_conta = self.row.id_conta
            if self.row.senha == self.senha_get:
                if int(self.row.saldo) >= int(self.valor_transferencia):
                    self.query = 'UPDATE conta SET saldo = saldo - (?) WHERE id_conta = (?)'
                    self.cursor.execute(self.query, (str(self.valor_transferencia), str(self.id_conta)))
                    self.connection.commit()

                    self.query = 'UPDATE conta SET saldo = saldo + (?) WHERE id_conta = (?)'
                    self.cursor.execute(self.query, (str(self.valor_transferencia), str(self.id_conta_trans)))
                    self.connection.commit()
                else:
                    print('saldo insuficiente')
            else:
                print('senha incorreta') 

    #DEF que faz o deposito na conta 
    def envio_deposito_def(self, event):
        self.deposito_get = str(self.entry_deposito.get())
        self.query = """
        UPDATE conta
        SET saldo = saldo + (?)
        WHERE conta = (?)
        """
        self.cursor.execute(self.query, (self.deposito_get, self.numero_conta))
        self.connection.commit()

    #DEF que puxa do banco de dados o nome de quem esta acessando a conta
    def nome(self):
        self.query = f'''
            SELECT nome
            FROM colaborador cr
            JOIN conta co ON co.id_colaborador = cr.id_colaborador
            WHERE conta = {self.numero_conta}'''

        self.execute = pd.read_sql_query(self.query, self.connection)

        for index, row in self.execute.iterrows():
            self.nome_txt.config(text = f'Olá, {self.row.nome}')

    #DEF que puxa do banco de dados o saldo da pessoa que esta acessando a conta
    def saldo(self):
        self.query = f'''
            SELECT saldo
            FROM conta ca
            JOIN colaborador cr ON ca.id_colaborador = cr.id_colaborador
            WHERE conta = {self.numero_conta}'''

        self.execute = pd.read_sql_query(self.query, self.connection)

        for index, row in self.execute.iterrows():
            self.saldo_int.config(text = f'R${self.row.saldo}')


    def Tela_login(self):
        self.main_frame_1    = tk.Frame(self.root)
        self.main_frame_1.pack(fill = tk.BOTH, 
                                    expand = True, 
                                    anchor = tk.CENTER
        )

        self.login_frame     = tk.Frame(self.main_frame_1)
        self.login_frame.pack(fill = tk.BOTH,  
                                    expand = True
        )
        self.login_frame.config(bg = self.background_color
        )
        
        self.logo = ImageTk.PhotoImage(Image.open(r"C:\Users\SWA-Sistemas\Desktop\NUBANK\_img\icon2.png")
        )
        self.logo_img = tk.Label(
                            self.login_frame, 
                                image = self.logo, 
                                    width=150, 
                                        height=150
        )
        self.logo_img.pack(pady = (40, 0)
        )

      
        self.agency_txt = tk.Label(
                            self.login_frame, 
                                text = 'Agência',
                                    bg = self.background_color, 
                                        fg = 'white', 
                                            font = ('Arial', 12, 'bold')
        )
        self.agency_txt.pack(pady = (25, 5)
        )
        self.agency = ttk.Entry(self.login_frame, 
                                        width = 25
        )
        self.agency.pack(pady = (5, 0)
        )

        
        self.account_txt = tk.Label(
                            self.login_frame, 
                                    text = 'Conta', 
                                            bg = self.background_color, 
                                                    fg = 'white', 
                                                            font = ('Arial', 12, 'bold'), 
        )
        self.account_txt.pack(pady = (15, 5)
        )
        self.account = ttk.Entry(self.login_frame, 
                                width = 25
        )
        self.account.pack()


        self.psw_txt = tk.Label(
                            self.login_frame, 
                                    text = 'Senha', 
                                            bg = self.background_color, 
                                                    fg = 'white', 
                                                            font = ('Arial', 12, 'bold'),
        )
        self.psw_txt.pack(pady = (10, 5)
        )
        self.psw = ttk.Entry(
                    self.login_frame,
                        width = 25,
                        show = "*"
        )
        self.psw.pack()

       
        self.proceed_button = ttk.Button(
                            self.login_frame, 
                                text = 'Entrar',
                                command = self.Pagina_Principal()
       
        )
        self.proceed_button.pack(pady = (20, 0)
        )

        self.error_message = tk.Label(self.login_frame, 
                            text = 'Credenciais incorretas. Tente novamente.',
                                    bg = self.background_color) 
        # MENSAGEM DE ERRO
        error_message = tk.Label(self.login_frame, 
                    text = 'Credenciais incorretas. Tente novamente.',
                            bg = self.background_color)

        #pagina principal #########################################################################################

    def Pagina_Principal(self):
        self.main_frame_2         = tk.Frame(self.root)
        self.nome_frame           = tk.Frame(self.main_frame_2, width=350, height=100)
        self.saldo_frame          = tk.Frame(self.main_frame_2, width=350, height=300)
        self.fatura_frame         = tk.Frame(self.main_frame_2, width=350, height=200)

        self.nome_frame.grid(row   = 0, 
                                    column = 0, 
                                        columnspan = 5, 
                                            sticky = tk.N
        )
        self.nome_frame.grid_propagate(0)
        self.nome_frame.config(bg = self.background_color)

        self.saldo_frame.grid(row      = 1, 
                                column = 0, 
                                        columnspan = 5
        )
        self.saldo_frame.grid_propagate(0
        )
        self.saldo_frame.config(bg = 'white'
        )

        self.fatura_frame.grid(row = 2, 
                                    column = 0, 
                                            columnspan = 5
        )
        self.fatura_frame.grid_propagate(0
        )
        self.fatura_frame.config(bg = 'white'
        )

        # NOME
        self.nome_txt = tk.Label(self.nome_frame, 
                            font = ('Arial 13 bold'),
                                fg = 'white', 
                                    bg = self.background_color
        )
        self.nome_txt.grid(row = 0, 
                            column = 0, 
                                pady = (40, 0), 
                                    padx = (20, 0)
        )

        # SALDO
        self.saldo_txt = tk.Label(self.saldo_frame, 
                            text = 'Saldo', 
                                font = ('Arial 15 '),
                                    fg = 'black', 
                                        bg = 'white'
        )
        self.saldo_txt.grid(row = 0, 
                            column = 0, 
                                pady = (15, 5), 
                                    padx = (20, 0), 
                                        sticky = tk.W
        )

        self.saldo_int = tk.Label(
                            self.saldo_frame, 
                                font = ('Arial 17 bold'), 
                                    fg = 'black', 
                                        bg = 'white'
        )
        self.saldo_int.grid(row = 1, 
                            column = 0, 
                                pady = (0, 10), 
                                    padx = (20, 0), 
                                        sticky = tk.W
        )

        # BOTÕES
        self.transferir = ImageTk.PhotoImage(Image.open(r"C:\Users\SWA-Sistemas\Desktop\NUBANK\_img\transferir.png")
        )
        self.deposito = ImageTk.PhotoImage(Image.open(r"C:\Users\SWA-Sistemas\Desktop\NUBANK\_img\deposito.png")
        )
        self.pagar = ImageTk.PhotoImage(Image.open(r"C:\Users\SWA-Sistemas\Desktop\NUBANK\_img\pagar.png")
        )

        self.transferir_btn = tk.Label(
                            self.saldo_frame,    
                                image = self.transferir, 
                                    borderwidth=0
        )
        self.transferir_btn.grid(row = 2, 
                            column = 0, 
                                padx = (45,1), 
                                    pady = (30,10), 
                                        sticky = tk.W
        )
        self.transferir_btn.bind('<Button-1>', self.Main_Valor_transferencia()
        )

        self.deposito_btn = tk.Label(
                            self.saldo_frame, 
                                image = self.deposito, 
                                    borderwidth = 0
        )
        self.deposito_btn.grid(row = 2, 
                            column = 1, 
                                padx = (50,1), 
                                    pady = (30,10), 
                                        sticky = tk.W
        )
        self.deposito_btn.bind('<Button-1>', self.deposito_def()
        )

        # LABELS
        self.label_transferir = tk.Label(self.saldo_frame, 
                            text = 'Transferir', 
                                font = ('Arial 10 bold'), 
                                    bg = 'white', 
                                        fg = 'black'
        )
        self.label_transferir.grid(row = 3, 
                            column = 0,
                                    sticky = tk.E
        )

        self.label_deposito = tk.Label(self.saldo_frame, 
                            text = 'Depósito', 
                                font = ('Arial 10 bold'), 
                                    bg = 'white', 
                                        fg = 'black'
        )
        self.label_deposito.grid(row = 3, column = 1, sticky = tk.E
        )

        self.separator0 = ttk.Separator(self.saldo_frame, 
                            orient = 'horizontal').place(x = 0, y = 299, 
                                                                        relwidth = 3
        )
# TELA DE TRANSFERENCIA #############################################################
    def transferir_def(self, event):  
        self.valor_transferencia = str(self.entry_transferir.get())
        self.main_frame_5.destroy()
        self.main_frame_6.pack(fill=tk.BOTH, 
                               expand = True, 
                                    anchor = tk.CENTER
        )
        self.root.geometry('350x550')
        #FRAME 
        self.img_back = ImageTk.PhotoImage(Image.open(r"C:\Users\SWA-Sistemas\Desktop\NUBANK\_img\back.jpeg")
        )

        self.credencial_transferencia_frame.pack(fill = tk.BOTH, expand = True
        )
        self.credencial_transferencia_frame.config(bg = self.background_color
        )

        #LABEL
        self.credencial_transferencia_label = tk.Label(self.credencial_transferencia_frame, 
                            text = 'Digite as seguintes informações para seguir com a transferência.', 
                                font = ('Arial 10 bold'), 
                                    bg = 'white', 
                                        fg = 'black'
        )

        # AGENCIA TRANS
        self.agency_txt_transferir = tk.Label(
                            self.credencial_transferencia_frame, 
                                text = 'Agência', 
                                    bg = self.background_color, 
                                        fg = 'white', 
                                            font = ('Arial', 12, 'bold')
        )
        self.agency_txt_transferir.pack(pady = (25, 5)
        )
        self.agency_transferir = ttk.Entry(self.credencial_transferencia_frame, 
                            width = 25
        )
        self.agency_transferir.pack(pady = (5, 0)
        )

        # CONTA TRANS
        self.account_txt_transferir = tk.Label(
                            self.credencial_transferencia_frame, 
                                text = 'Conta', 
                                    bg = self.background_color, 
                                        fg = 'white', 
                                            font = ('Arial', 12, 'bold'), 
        )
        self.account_txt_transferir.pack(pady = (15, 5)
        )
        self.account_transferir = ttk.Entry(self.credencial_transferencia_frame, 
                            width = 25
        )
        self.account_transferir.pack()

        # SENHA TRANS
        self.psw_txt_transferir = tk.Label(
                            self.credencial_transferencia_frame, 
                                text = 'Senha',  
                                    bg = self.background_color, 
                                        fg = 'white', 
                                            font = ('Arial', 12, 'bold')
        )
        self.psw_txt_transferir.pack(pady = (10, 5)
        )
        self.psw_transferir = ttk.Entry(
                            self.self.credencial_transferencia_frame, 
                                width = 25
        )
        self.psw_transferir.pack()

        # BOTAO DE TRANSFERENCIA
        self.button_transferir = ttk.Button(
                            self.self.credencial_transferencia_frame, 
                                text = 'Enviar.', 
                                    command = self.credenciais_transferencias()
        )
        self.button_transferir.pack(pady = (20, 0)
        )

        # MENSAGEM DE ERRO
        self.error_message_transferir = tk.Label(self.self.credencial_transfecia_frame, 
                            text = 'Credenciais incorretas. Tente novamente.', 
                                bg = self.background_color
        )
        
        #################################################################################################### 
    def Main_Valor_transferencia(self):
        #FRAME 
        self.valor_transferencia = str(self.entry_transferir.get())
        self.transferir_frame.config(bg = 'white'
        )
        self.transferir_frame.grid(row = 0, 
                            column = 0, 
                                columnspan = 5, 
                                    sticky = tk.N
        )
        self.transferir_frame.grid_propagate(0
        )
        self.transferir_frame.config(bg = 'white'
        )

        self.transferir_num_frame.grid(row = 1, 
                            column = 0, 
                                columnspan = 5, 
                                    sticky = tk.N
        )
        self.transferir_num_frame.grid_propagate(0
        )
        self.transferir_num_frame.config(bg = 'white'
        )

        # BOTAO DE BACK

        self.back_btn1 = tk.Label(self.transferir_frame, 
                            image = self.img_back, 
                                borderwidth=0
        )
        self.back_btn1.grid(row = 0, 
                            column = 0, 
                                sticky = tk.W
        )
        self.back_btn1.bind('<Button-1>', self.back_def()
        )

        # LABELS

        self.label_transferencia1 = tk.Label(self.transferir_frame, 
                            text = 'Qual a quantia ', 
                                font = ('Arial 17 bold'), 
                                    bg = 'white',  
                                        fg = 'black'
        )
        self.label_transferencia1.grid(row = 1, 
                            column = 0, 
                                padx = 42, 
                                    pady = (20,0), 
                                        columnspan = 5, 
                                            sticky = tk.N
        )
        self.label_transferencia1.grid_propagate(0
        )

        self.label_transferencia2 = tk.Label(self.transferir_frame, 
                            text = 'você deseja Transferir?', 
                                font = ('Arial 17 bold'), 
                                    bg = 'white', 
                                        fg = 'black'
        )
        self.label_transferencia2.grid(row = 2, 
                            column = 0, 
                                padx = 42,  
                                    pady = (0,40), 
                                        columnspan = 5,
                                                sticky = tk.N
        )

        self.label_transferencia2.grid_propagate(0
        )

        self.label_transferencia3 = tk.Label(self.transferir_frame, 
                            text = 'Digite um valor entre R$1,00 e', 
                                font = ('Arial 10 bold'), 
                                    bg = 'white', 
                                        fg = 'gray'
        )
        self.label_transferencia3.grid(row = 4, 
                            column = 0, 
                                padx = 42, 
                                    columnspan = 5, 
                                        sticky = tk.N
        )
        self.label_transferencia3.grid_propagate(0
        )

        self.label_transferencia4 = tk.Label(self.transferir_frame, 
                            text = 'R$6.000,00', 
                                font = ('Arial 10 bold'), 
                                    bg = 'white', 
                                        fg = 'gray'
        )
        self.label_transferencia4.grid(row = 5, 
                            column = 0, 
                                padx = 42,  
                                    pady = (0,10), 
                                        columnspan = 5, 
                                            sticky = tk.N                                   
        )
        self.label_transferencia4.grid_propagate(0
        )

        self.separator1 = ttk.Separator(self.transferir_frame, 
                                orient = 'horizontal').place(x = 0, y = 299, 
                                                                        relwidth = 3
        )
        # ENTRY 

        self.entry_transferir = ttk.Entry(self.transferir_frame, 
                                width = 25,
                                    textvariable = self.equacao_label
        )
        self.entry_transferir.grid(row = 3, 
                                column = 0, 
                                    padx = (75,0), 
                                        pady = (1,20)
        )

        # BOTAO DE TRANSFERIR

        self.btn_transferir = tk.Label(self.transferir_frame, 
                            text = 'Transferir', 
                                bg = 'white', 
                                    fg = 'black'
        )

        self.btn_transferir.grid(row = 6,
                                column = 0, 
                                padx = (80,1)
        )

        self.btn_transferir.bind('<Button-1>', self.transferir_def()
        )
        
        # BOTOES NUMERICOS DO DEPOSITO

        self.button10 = tk.Button(self.transferir_num_frame,
                    text = 1,
                    bg = self.color,
                    font = 'Arial',
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(1)
        )
        self.button10.grid(row = 0, 
                    column = 0
        )

        self.button20 = tk.Button(self.transferir_num_frame, 
                    text = 2,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg, 
                        width = self.sizesBx,  
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(2)
        )
        self.button20.grid(row = 0, column = 1
        )

        self.button30 = tk.Button(self.transferir_num_frame,
                    text = 3, 
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg, 
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(3)
        )
        self.button30.grid(row = 0, column = 2
        )

        self.button40 = tk.Button(self.transferir_num_frame, 
                    text = 4,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(4)
        )
        self.button40.grid(row = 1, 
                    column = 0            
        )

        self.button50 = tk.Button(self.transferir_num_frame, 
                    text = 5,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(5)
        )
        self.button50.grid(row = 1, 
                    column = 1
        )

        self.button60 = tk.Button(self.transferir_num_frame, 
                    text = 6,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(6)
        )
        self.button60.grid(row = 1, 
                    column = 2
        )

        self.button70 = tk.Button(self.transferir_num_frame, 
                    text = 7,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(7)
        )
        self.button70.grid(row = 2, 
                    column = 0
        )

        self.button80 = tk.Button(self.transferir_num_frame, 
                    text = 8,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(8)
        )
        self.button80.grid(row = 2, 
                    column = 1
        )

        self.button90 = tk.Button(self.transferir_num_frame, 
                    text = 9,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(9)
        )
        self.button90.grid(row = 2, 
                    column = 2
        )

        self.button00 = tk.Button(self.transferir_num_frame, 
                    text = 0,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0, 
                        command = self.visorentry(0)
        )
        self.button00.grid(row = 3, 
                    column = 1
        )

        self.button_ponto0 = tk.Button(self.transferir_num_frame, 
                    font = 'Arial',
                    bg = self.color,
                    text = '.',
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(".")
        )
        self.button_ponto0.grid(row = 1,
                    padx = (6,6),
                    pady = (5,5),
                    column = 3
        )

        self.button_virgula0 = tk.Button(self.transferir_num_frame, 
                    font = 'Arial',
                    bg = self.color,
                    text = ',',
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(",")
        )
        self.button_virgula0.grid(row = 2,
                    padx = (6,6),
                    pady = (5,5),
                    column = 3
        )


        self.button_apagar0 = tk.Button(self.transferir_num_frame, 
                    text = '⌫',     
                    bg = self.color,
                    activebackground = self.activebg,
                        width = 8,
                        height = 4,
                        borderwidth = 0,
                        command = self.apagar()
        )
        self.button_self.apagar0.grid(row = 0, 
                    column = 3
        )

# TELA DE DEPOSITO ################################################################################################

    def deposito_def(self):
        self.main_frame_2.destroy()
        self.root.geometry('350x660')
        self.main_frame_4.pack(fill=tk.BOTH, 
                                expand = True, 
                                    anchor = tk.CENTER
        )
        #IMAGEM


        #FRAME d
        self.deposito_frame.grid(row = 0, 
                        column = 0, 
                            columnspan = 5, 
                                sticky = tk.N
        )
        self.deposito_frame.grid_propagate(0
        )
        self.deposito_frame.config(bg = 'white'
        )

        self.deposito_num_frame.grid(row = 1, 
                        column = 0, 
                            columnspan = 5, 
                                sticky = tk.N
        )
        self.deposito_num_frame.grid_propagate(0
        )
        self.deposito_num_frame.config(bg = 'white'
        )
        # BOTAO DE BACK

        self.back_btn = tk.Label(self.deposito_frame, 
                        image = self.img_back, 
                            borderwidth=0
        )
        self.back_btn.grid(row = 0, 
                        column = 0, 
                            sticky = tk.W                     
        )
        self.back_btn.bind('<Button-1>', self.back_def()
        )

        # LABELS

        self.label_deposito1 = tk.Label(self.deposito_frame, 
                        text = 'Qual a quantia ', 
                            font = ('Arial 17 bold'), 
                                bg = 'white', 
                                    fg = 'black'
        )
        self.label_deposito1.grid(row = 1, 
                        column = 0, 
                            padx = 42, 
                                pady = (20,0),  
                                    columnspan = 5, 
                                        sticky = tk.N
        )
        self.label_deposito1.grid_propagate(0
        )

        self.label_deposito2 = tk.Label(self.deposito_frame, 
                        text = 'você deseja depositar?', 
                            font = ('Arial 17 bold'), 
                                bg = 'white', 
                                    fg = 'black'
        )
        self.label_deposito2.grid(row = 2, 
                        column = 0, 
                            padx = 42,  
                                pady = (0,40), 
                                    columnspan = 5, 
                                        sticky = tk.N
        )
        self.label_deposito2.grid_propagate(0
        )

        self.label_deposito3 = tk.Label(self.deposito_frame, 
                        text = 'Digite um valor entre R$20,00 e', 
                            font = ('Arial 10 bold'), 
                                    bg = 'white', 
                                        fg = 'gray'
        )
        self.label_deposito3.grid(row = 4, 
                        column = 0, 
                            padx = 42, 
                                columnspan = 5, 
                                    sticky = tk.N)
        self.label_deposito3.grid_propagate(0
        )

        self.label_deposito4 = tk.Label(self.deposito_frame, 
                            text = 'R$15.000,00', 
                                font = ('Arial 10 bold'), 
                                    bg = 'white', 
                                        fg = 'gray'
        )
        self.label_deposito4.grid(row = 5, 
                             column = 0, 
                                padx = 42,  
                                  pady = (0,10), 
                                      columnspan = 5, 
                                         sticky = tk.N
        )
        self.label_deposito4.grid_propagate(0
        )

        self.separator2 = ttk.Separator(self.deposito_frame, 
                                    orient = 'horizontal').place(x = 0, y = 299, relwidth = 3
        )
        # ENTRY 

        self.entry_deposito = ttk.Entry(self.deposito_frame, 
                            width = 25, 
                                textvariable = self.equacao_label
        )
        self.entry_deposito.grid(row = 3, 
                            column = 0, 
                                padx = (75,0),
                                    pady = (1,20)
        )

        # BOTAO DE DEPOSITAR

        self.envio_deposito = tk.Label(self.deposito_frame, 
                            text = 'Depositar', 
                                bg = 'white', 
                                    fg = 'black'
        )

        self.envio_deposito.grid(row = 6, 
                            column = 0, 
                                padx = (80,1)
        )

        self.envio_deposito.bind('<Button-1>', self.envio_deposito_def()
        )

        # BOTOES NUMERICOS DO DEPOSITO

        self.button1 = tk.Button(self.deposito_num_frame,
                    text = 1,
                    bg = self.color,
                    font = 'Arial',
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(1)
        )
        self.button1.grid(row = 0, 
                    column = 0            
        )

        self.button2 = tk.Button(self.deposito_num_frame, 
                    text = 2,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg, 
                        width = self.sizesBx,  
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(2)
        )
        self.button2.grid(row = 0, column = 1
        )

        self.button3 = tk.Button(self.deposito_num_frame,
                    text = 3, 
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg, 
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(3)
        )
        self.button3.grid(row = 0, column = 2
        )

        self.button4 = tk.Button(self.deposito_num_frame, 
                    text = 4,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(4)
        )
        self.button4.grid(row = 1, 
                    column = 0
        )

        self.button5 = tk.Button(self.deposito_num_frame, 
                    text = 5,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(5)
        )

        self.button5.grid(row = 1, 
                    column = 1
        )

        self.button6 = tk.Button(self.deposito_num_frame, 
                    text = 6,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(6)
        )

        self.button6.grid(row = 1, 
                    column = 2
        )

        self.button7 = tk.Button(self.deposito_num_frame, 
                    text = 7,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(7)
        )

        self.button7.grid(row = 2, 
                    column = 0
        )

        self.button8 = tk.Button(self.deposito_num_frame, 
                    text = 8,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(8)
        )
        self.button8.grid(row = 2, 
                    column = 1
        )

        self.button9 = tk.Button(self.deposito_num_frame, 
                    text = 9,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(9)
        )
        self.button9.grid(row = 2, 
                    column = 2
        )

        self.button0 = tk.Button(self.deposito_num_frame, 
                    text = 0,
                    font = 'Arial',
                    bg = self.color,
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0, 
                        command = self.visorentry(0)
        )
        self.button0.grid(row = 3, 
                    column = 1
        )

        self.button_ponto = tk.Button(self.deposito_num_frame, 
                    font = 'Arial',
                    bg = self.color,
                    text = '.',
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(".")
        )
        self.button_ponto.grid(row = 1,
                    padx = (6,6),
                    pady = (5,5),
                    column = 3
        )

        self.button_virgula = tk.Button(self.deposito_num_frame, 
                    font = 'Arial',
                    bg = self.color,
                    text = ',',
                    activebackground = self.activebg,
                        width = self.sizesBx, 
                        height = self.sizesBy,
                        borderwidth = 0,
                        command = self.visorentry(",")
        )
        self.button_virgula.grid(row = 2,
                    padx = (6,6),
                    pady = (5,5),
                    column = 3,
        )


        self.button_apagar = tk.Button(self.deposito_num_frame, 
                    text = '⌫',     
                    bg = self.color,
                    activebackground = self.activebg,
                        width = 8,
                        height = 4,
                        borderwidth = 0,
                        command = self.apagar()
        )
        self.button_apagar.grid(row = 0, 
                    column = 3
        )

        # FATURA

        #IMAGEM
        self.img_cartao = ImageTk.PhotoImage(Image.open(r"C:\Users\SWA-Sistemas\Desktop\NUBANK\_img\cartao.png")
        )

        #LABELS
        self.img_label = tk.Label(self.fatura_frame, 
                            image = self.img_cartao, 
                                borderwidth=0
        )
        self.img_label.grid(row = 0, 
                            column = 0, 
                                padx = (10,1), 
                                    pady = (10,2), 
                                        sticky = tk.W
        )


        self.fatura = tk.Label(self.fatura_frame, 
                            text = 'Cartão de crédito',
                                font = ('Arial 14 bold'), 
                                    bg = 'white', 
                                        fg = 'black'
        )
        self.fatura.grid(row = 1, 
                            column = 0, 
                                padx = (20,1), 
                                    pady = (2,5), 
                                        sticky = tk.W
        )
        self.fatura_atual = tk.Label(self.fatura_frame, 
                            text = 'Fatura atual',
                                font = ('Arial 12 bold'), 
                                    bg = 'white', 
                                        fg = 'darkgray'
        )
        self.fatura_atual.grid(row = 2, 
                            column = 0, 
                                padx = (20,1), 
                                    pady = (2,5), 
                                        sticky = tk.W
        )
        self.accountfatura_valor = tk.Label(self.fatura_frame, 
                            text = 'R$0,00',
                                font = ('Arial 17 bold'),
                                    fg = 'black', 
                                        bg = 'white'
        )
        self.fatura_valor.grid(row = 3, 
                            column = 0, 
                                padx = (20,1), 
                                    pady = (10,5), 
                                        sticky = tk.W)



NUbankClass()                                                                     
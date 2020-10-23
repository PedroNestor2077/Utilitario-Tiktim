from tkinter import *
from tkinter import scrolledtext
from time import strftime
from datetime import date
from tkinter import ttk  		       			 			
import sqlite3
import winsound
erro=False
try:
    connect=sqlite3.connect('db/estoque.db')
    cursor=connect.cursor()
except:
    erro=True
#---------------------------------#
#==================================ESTOQUE================================================#
estoque_auto=False
nome_buscar=[]
quantidade_buscar=[]
ultimo_update_buscar=[]
medida_buscar=[]
alerta_buscar=[]
preço_buscar=[]
fornecedores_buscar_nome=[]
fornecedores_buscar_telefone=[]
fornecedores_itens_buscar_nome_iten=[]
alerta_list=[]
nome_tabela=""
nome_item=""
len_id=0
tabela=""
tabela2=""
nome_buscar_check=[]
nome_buscar_historico=[]
quantidade_buscar_historico=[]
data_buscar_historico=[]
preço_buscar_historico=[]
operaçao_buscar_historico=[]
medida_buscar_historico=[]
id_check=1600
text=["","","","","C","R","E","A","T","E","D"," ","B","Y"," ","P","E","D","R","O"," ","N","E","S","T","O","R",".","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
c=0
text_animação=""
fonte_botoes="Cambria 11 bold"
#==================================ESTOQUE================================================#
data_atual = date.today()
data_em_texto = data_atual.strftime("%d/%m")
hora_atual=strftime("%H:%M:%S")
#---------------------------------#
tempero_quantity,sabores,ingredientes_quantidade,ingredientes_nome,ingredientes_medida,ingredientes=[],[],[],[],[],[]
save=0
restante=0
tipo_porco_frango=''
divide=1
apaga=False
iniciado=False
calcula=False
save_nome=""
#------------------------------------------------CLASS---------------------------------------------------------------#
class DataBase:
    def __create__(self,name,itens):
        cursor.execute(f"CREATE TABLE  IF NOT EXISTS  [{name}] ({itens})")
        connect.commit()
    def __find__(self,table, iten, list):
        global tempero_name, tempero_quantity, sabores, ingredientes
        # ------------------------------#
        cursor.execute(f"SELECT * FROM [{table}]")
        len_id = len(cursor.fetchall())
        # ------------------------------#
        y = 1
        while y <= len_id:
            cursor.execute(f"SELECT {iten} FROM '{table}' WHERE id={y}")
            list.append(cursor.fetchone()[0])
            y += 1
    def __update__(self,table,iten,value,id):
        try:
            cursor.execute(f"UPDATE [{table}] SET {iten} = '{value}' WHERE id ={id}")
            connect.commit()
        except:
            print("erro no update",table,iten,value)
    def __insert__(self,table,iten,values):
        cursor.execute(f"INSERT INTO [{table}] ({iten}) VALUES ({values})")
        connect.commit()
    def __delete_table__(self,table):
        cursor.execute(f"DROP TABLE [{table}]")
        connect.commit()
class color:
    botao_confirmar_on="blue"
    botao_confirmar_off="#4682B4"
    botao_limpar_on="#6959CD"
    botao_limpar_off="#8B0000"
    lb_botao_confirmar_on="black"
    lb_botao_confirmar_off="black"
    botao_confirmar_active="red"
    lb_botao_limpar_on="black"
    lb_botao_limpar_off="#778899"
class font:
    titulo="impact 17 underline"
    botoes="Cambria 11 bold"
    lb='gothic 10 bold'
class Cleaner:
    def zerar_historico_estoque(self):
        operador.__delete_table__('historico_entrada')
        operador.__create__('historico_entrada','id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT,quantidade REAL,preço REAL,data TEXT,operaçao TEXT')
    def zerar_tabela_ingredientes_frango(self):
        sabores = []
        try:
            operador.__find__("sabor_frango", "nome", sabores)
        except:
            print('sabores frango nao encontrado')
        if len(sabores)>1:
            y = 0
            try:
                while y < len(sabores):
                    tabela = "sabores_frango_" + str(sabores[y])
                    tabela_historico="historico_ingredientes_frango_"+str(sabores[y])
                    operador.__delete_table__(tabela)
                    operador.__delete_table__(tabela_historico)
                    y += 1
                operador.__delete_table__("sabor_frango")
                operador.__create__("sabor_frango", "id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT")
                operador.__insert__("sabor_frango", "nome", "'frango pura'")
                operador.__create__("sabores_frango_frango pura",
                                    "id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade REAL, medida TEXT")
                operador.__create__(f"historico_ingredientes_frango_frango pura",
                                "'id' INTEGER PRIMARY KEY AUTOINCREMENT,'data' TEXT ,'massa' TEXT")
                operador.__insert__("sabores_frango_frango pura", "nome, quantidade, medida", "'massa','1','KG'")
                print('zerei frango')
            except:
                print("erro ao zerar frango")
    def zerar_tabela_ingredientes_porco(self):
        sabores = []
        try:
            operador.__find__("sabor_porco", "nome", sabores)
        except:
            print('sabores porco nao encontrado')
        if len(sabores)>1:
            y = 0
            try:
                while y < len(sabores):
                    tabela = "sabores_porco_" + sabores[y]
                    tabela_historico="historico_ingredientes_porco_"+str(sabores[y])
                    operador.__delete_table__(tabela_historico)
                    operador.__delete_table__(tabela)
                    y += 1
                operador.__delete_table__("sabor_porco")
                operador.__create__("sabor_porco", "id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT")
                operador.__insert__("sabor_porco", "nome", "'porco pura'")
                operador.__create__("sabores_porco_porco pura",
                                    "id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade REAL, medida TEXT")
                operador.__create__(f"historico_ingredientes_porco_porco pura",
                                "'id' INTEGER PRIMARY KEY AUTOINCREMENT,'data' TEXT ,'massa' TEXT")
                operador.__insert__("sabores_porco_porco pura", "nome, quantidade, medida", "'massa','1','KG'")
                print('zerei porco')
            except:
                print("erro ao zerar porco")
    def zerar_tabela_funcionarios(self):
        try:
            operador.__delete_table__("funcionarios")
            operador.__create__("funcionarios",
                                "id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, telefone TEXT, cpf TEXT")
            inserir_funcionarios_select()
        except:
            print("erro ao zerar")
    def clean_calcular(self):
        sons('botao')
        global restante,apaga,calcula
        lb_restante_r["text"] = "0KG"
        restante = 0
        create_table("calcular")
        create_table("ingredientes")
        lb_erro_calcular_carne.place(x=1000, y=1000)
        lb_erro_calcular_limpeza.place(x=1000, y=1000)
        ed_carne.delete(0, END)
        ed_limpeza.delete(0, END)
        check_frango.deselect()
        check_porco.deselect()
        apaga=True
        calcula=False
    def clean_ingredientes(self):
        sons('botao')
        global total, restante, tipo_porco_frango
        lb_restante_r["text"] = f"{total:.0f}KG"
        restante = total
        slide1["to"] = restante
        slide1.set(0)
        create_table("ingredientes")
        if tipo_porco_frango == "porco":
            inserir_sabores_tabela("porco")
        if tipo_porco_frango == "frango":
            inserir_sabores_tabela("frango")
    def zerar_tabela_historico_calcular(self):
        sabores=[]
        operador.__find__("sabor_porco","nome",sabores)
        print(sabores,'zerar historico,porco')
        y=0
        while y<len(sabores):
            nome_tabela="historico_ingredientes_porco_"+str(sabores[y].lower())
            operador.__delete_table__(f"{nome_tabela}")
            operador.__create__(f"{nome_tabela}",
                                "'id' INTEGER PRIMARY KEY AUTOINCREMENT,'data' TEXT ,'massa' TEXT")
            y += 1
        sabores=[]
        operador.__find__("sabor_frango","nome",sabores)
        print(sabores,'zerar historico,frango')
        y=0
        while y<len(sabores):
            nome_tabela="historico_ingredientes_frango_"+str(sabores[y].lower())
            operador.__delete_table__(f"{nome_tabela}")
            operador.__create__(f"{nome_tabela}",
                                "'id' INTEGER PRIMARY KEY AUTOINCREMENT,'data' TEXT ,'massa' TEXT")
            y += 1
            print(nome_tabela)
        operador.__delete_table__("historico_calcular")
        operador.__delete_table__("historico_comentarios")
        operador.__delete_table__("historico_produzido_por")
        operador.__create__("historico_calcular","'id' INTEGER PRIMARY KEY AUTOINCREMENT,'data' TEXT ,'carne' TEXT,'peito' TEXT,'limpeza' TEXT,'bacon' TEXT,'toucinho' TEXT,'alho' TEXT,'sal' TEXT,'total' TEXT,'tipo' TEXT")
        operador.__create__('historico_comentarios',"'id' INTEGER PRIMARY KEY AUTOINCREMENT, 'data' TEXT, 'comentario' TEXT")
        operador.__create__('historico_produzido_por',"'id' INTEGER PRIMARY KEY AUTOINCREMENT, 'data' TEXT, 'nome' TEXT")
        #operador.__create__("historico_ingredientes_porco_porco pura","'id' INTEGER PRIMARY KEY AUTOINCREMENT,'data' TEXT ,'massa' TEXT")
    def sair(self):
        janela.destroy()
    def close_janela_historico(self):
        sons('botao')
        global janela_salvar_historico
        janela_salvar_historico.destroy()
    def close_coment(self):
        sons('botao')
        global frame_comentario
        frame_comentario.place(x=1000,y=1000)
class New:
    def adicionar_sabor(self):
        operador.__find__("ingredientes", "nome", ingredientes)
        tipo = ""
        ingredientes_adicionar = []
        ingredientes_adicionar_quantidade = []
        ingredientes_adicionar_medida = []
        # -----------------------------------------------------------------------------------------------------------------------------------------#
        def limpar():
            global ingredientes_adicionar, ingredientes_quantidade, ingredientes_adicionar_medida, medida, tipo
            select_ver.delete(0, END)
            tipo = ""
            medida = ""
            ingredientes_adicionar, ingredientes_quantidade, ingredientes_adicionar_medida = [], [], []
            check_kg.deselect()
            check_g.deselect()
            check_porco.deselect()
            check_frango.deselect()
            ed_nome.delete(0, END)
            combo.set("")
            ed_preço.delete(0, END)
        def checar():
            check = 0
            try:
                nome = str(ed_nome.get())
                check += 1
            except:
                pass
            try:
                a = float(ed_preço.get())
                check += 1
            except:
                pass
            try:
                a = (str(medida))
                check += 1
            except:
                pass
            try:
                a = (combo.get())
                if a == "":
                    check -= 1
                else:
                    check += 1
            except:
                pass
            a=0
            igual=False
            while a<len(ingredientes_adicionar):
                if str(combo.get())==str(ingredientes_adicionar[a]):
                    igual=True
                a+=1
            if check == 4 and igual==False:
                bt_salvar["command"] = adicionar
                bt_confirmar["command"] = salvar
                bt_salvar["bg"] = "blue"
            else:
                bt_salvar["command"] = ""
                bt_salvar["bg"] = "white"
        def atualizar_atualizar():
            checar()
            janela_adicionar_sabor.after(200, atualizar_atualizar)
        def check_porco_adicionar():
            global tipo
            tipo = "porco"
            check_frango.deselect()
        def check_frango_adicionar():
            global tipo
            tipo = "frango"
            check_porco.deselect()
        def check_kg():
            global medida
            medida = "KG"
            check_g.deselect()
        def check_g():
            global medida
            medida = "g"
            check_kg.deselect()
        def close():
            sons('botao')
            janela_adicionar_sabor.destroy()
        def adicionar():
            global medida, tipo, nome_sabor,save_nome
            select_ver.delete(0, END)
            nome_sabor = str(ed_nome.get())
            ingredientes_adicionar_quantidade.append(float(ed_preço.get()))
            ingredientes_adicionar_medida.append(str(medida))
            ingredientes_adicionar.append(str(combo.get()))
            print(medida,ed_preço.get())
            select_ver.insert(END, "NOVO SABOR")
            select_ver.insert(END, f" NOME:{nome_sabor.upper()}")
            select_ver.insert(END, f" TIPO:{tipo.upper()}")
            select_ver.insert(END, f"INGREDIENTES:")
            y = 0
            while y < len(ingredientes_adicionar):
                select_ver.insert(END,
                 f"    {ingredientes_adicionar[y].upper()}-{ingredientes_adicionar_quantidade[y]}{ingredientes_adicionar_medida[y]}/KG")
                y += 1
        def salvar():
            global medida, tipo, nome_sabor
            # -------------------------#
            tabela = "sabor_" + tipo
            buscar = []
            operador.__find__(tabela, "nome", buscar)
            igual = False
            y = 0
            while y < len(buscar):
                if nome_sabor == buscar[y]:
                    igual = True
                    break
                y += 1
            # -------------------------#
            if igual == False:
                operador.__insert__(f'{tabela}', "nome", f"'{nome_sabor}'")
                # -------------------------#
                tabela = "sabores_" + tipo + "_" + f"{nome_sabor}"
                operador.__create__(f'{tabela}',"id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade REAL, medida TEXT")
                #--------CRIANDO TABELA PARA HISTORICO---------#
                ingredientes_criar_historico ="'id' INTEGER PRIMARY KEY AUTOINCREMENT, 'data' TEXT, 'massa' TEXT,"
                y=0
                while y<len(ingredientes_adicionar):
                    ingredientes_criar_historico+="'"+ingredientes_adicionar[y].lower()+"'"+" TEXT, "
                    y+=1
                len_str=int(len(ingredientes_criar_historico))
                len_str=len_str-2
                ingredientes_criar_historico=str(ingredientes_criar_historico[0:len_str])
                print(ingredientes_criar_historico)
                operador.__create__(f'historico_ingredientes_{tipo}_{nome_sabor}',f"{ingredientes_criar_historico}")
                #--------CRIANDO TABELA PARA HISTORICO---------#
                y = 0
                operador.__insert__(f'{tabela}', "nome,quantidade,medida", f"'massa','1','KG'")
                while y < len(ingredientes_adicionar):
                    operador.__insert__(f'{tabela}', "nome,quantidade,medida",f"'{ingredientes_adicionar[y]}','{ingredientes_adicionar_quantidade[y]}','{ingredientes_adicionar_medida[y]}'")
                    y += 1
            else:
                print("igual!")
        # -----------------------------------------------------------------------------------------------------------------------------------------#
        janela_adicionar_sabor = Toplevel()
        janela_adicionar_sabor.geometry("600x256+530+200")
        janela_adicionar_sabor["bg"] = "black"
        janela_adicionar_sabor.title("ATUALIZAR PREÇO>")
        janela_adicionar_sabor.resizable(width=False, height=False)
        janela_adicionar_sabor.transient()
        janela_adicionar_sabor.focus_force()
        janela_adicionar_sabor.grab_set()
        # ------------------------------------------------FRAME--------------------------------------------#
        frame_main_main = Frame(janela_adicionar_sabor, width=605, height=250, highlightbackground="grey",
                                highlightthickness=10, bg="#363636")
        frame_main_main.place(x=2, y=2)
        frame_funçoes = Frame(frame_main_main, highlightbackground="grey", highlightthickness=5, height=150, width=280,
                              bg="#363636")
        frame_funçoes.place(x=15, y=45)
        frame_main = Frame(frame_funçoes, highlightbackground="grey", highlightthickness=3, height=100, width=200,
                           bg="#363636")
        frame_main.place(x=10, y=70)
        # -------------------------------------------------FRAME--------------------------------------------#
        combo = ttk.Combobox(frame_main)
        combo.pack(side=BOTTOM, fill=BOTH)
        combo['values'] = ingredientes
        # -------------------------------------------------LABEL--------------------------------------------#
        lb_titulo = Label(frame_main_main, bg="#363636", text="ADICIONAR NOVO SABOR", font="impact 17 bold",foreground="green")
        lb_titulo.place(x=80, y=5)
        lb_nome_iten = Label(frame_funçoes, bg="#363636", foreground="white", font='gothic 10 bold', text="NOME:")
        lb_nome_iten.place(x=10, y=10)
        lb_preço_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="QUANTIDADE:")
        lb_preço_iten.pack(side=LEFT)
        lb_erro = Label(frame_main, bg="#363636", foreground="red", font='gothic 10 bold', text="Valores inválidos.")
        # -------------------------------------------------LABEL--------------------------------------------#
        # -------------------------------------------------ENTRY--------------------------------------------#
        ed_preço = Entry(frame_main, width=8)
        ed_preço.pack(side=LEFT)
        ed_nome = Entry(frame_funçoes, width=20)
        ed_nome.place(x=70, y=12)
        # -------------------------------------------------ENTRY--------------------------------------------#
        check_kg = Checkbutton(frame_funçoes, text="KG", font="Cambria 10", command=check_kg)
        check_kg.place(x=110, y=45)
        check_g = Checkbutton(frame_funçoes, text="G", font="Cambria 10", command=check_g)
        check_g.place(x=165, y=45)
        check_porco = Checkbutton(frame_funçoes, text="PORCO", font="Cambria 10", command=check_porco_adicionar)
        check_porco.place(x=10, y=45)
        check_frango = Checkbutton(frame_funçoes, text="FRANGO", font="Cambria 10", command=check_frango_adicionar)
        check_frango.place(x=50, y=45)
        select_ver = Listbox(frame_main_main, bg="#1C1C1C", foreground="#B22222", height=10, width=25,
                             font='gothic 13 bold')
        select_ver.place(x=300, y=40)
        select_ver.insert(END, "NOVO SABOR:")
        select_ver.insert(END, "NOME:")
        select_ver.insert(END, "TIPO:")
        select_ver.insert(END, "INGREDIENTES:")

        # -------------------------------------------------BOTOES--------------------------------------------#
        bt_salvar = Button(frame_main, text="ADICIONAR", bg=cor.botao_confirmar_off, font=font.botoes,
                           activebackground=cor.botao_confirmar_active)
        bt_salvar.pack(side=BOTTOM)
        bt_confirmar = Button(frame_main_main, text="SALVAR", bg=cor.botao_confirmar_off, font=font.botoes, width=28,
                              activebackground=cor.botao_confirmar_active, foreground=color.lb_botao_confirmar_off)
        bt_confirmar.place(x=16, y=198)
        bt_sair = Button(frame_main_main, text="x", bg=cor.botao_limpar_off, font=font.botoes, command=close,
                         foreground=color.lb_botao_limpar_off, activebackground=cor.botao_confirmar_active)
        bt_sair.place(x=2, y=2)
        bt_limpar = Button(frame_main_main, text="x", bg=cor.botao_limpar_off, font=font.botoes, command=limpar,
                           activebackground=cor.botao_confirmar_active, foreground=color.lb_botao_limpar_off)
        bt_limpar.place(x=400, y=10)
        atualizar_atualizar()
    def adicionar_novo_funcionário(self):
        def close():
            sons('botao')
            janela_adicionar_novo_funcionario.destroy()

        def add():
            try:
                nome = str(ed_nome_funcionario.get())
                telefone = str(ed_numero_funcionario.get())
                cpf = str(ed_cpf_funcionario.get())
                operador.__insert__("funcionarios", "nome,telefone,cpf", f"'{nome}','{telefone}','{cpf}'")
                janela_adicionar_novo_funcionario.destroy()
                inserir_funcionarios_select()
            except:
                lb_erro.place(x=80, y=150)

        global len_id, tabela, medida, hora_atual, ed_numero_funcionario
        try:
            janela_adicionar_novo_funcionario = Toplevel()
            janela_adicionar_novo_funcionario.geometry("325x195+570+200")
            janela_adicionar_novo_funcionario["bg"] = "black"
            janela_adicionar_novo_funcionario.title("ADICIONAR NOVO>")
            janela_adicionar_novo_funcionario.resizable(width=False, height=False)
            janela_adicionar_novo_funcionario.transient()
            janela_adicionar_novo_funcionario.focus_force()
            janela_adicionar_novo_funcionario.grab_set()
            # -------------------------------------------------FRAME--------------------------------------------#
            frame_main = Frame(janela_adicionar_novo_funcionario, width=320, height=190, bg="#363636",
                               highlightbackground="grey", highlightthickness=10)
            frame_main.place(x=2, y=2)
            # -------------------------------------------------FRAME--------------------------------------------#
            # -------------------------------------------------LABEL--------------------------------------------#
            lb_titulo = Label(frame_main, bg="#363636", text="ADICIONAR", font="impact 17 bold", foreground="green")
            lb_titulo.place(x=100, y=3)

            lb_nome_funcionario = Label(frame_main, bg="#363636", foreground="white", font=font.lb, text="NOME:")
            lb_nome_funcionario.place(x=5, y=40)
            lb_numero_funcionario = Label(frame_main, bg="#363636", foreground="white", font=font.lb,
                                          text="☎ TELEFONE:")
            lb_numero_funcionario.place(x=5, y=70)
            lb_cpf_funcionario = Label(frame_main, bg="#363636", foreground="white", font=font.lb, text="CPF:")
            lb_cpf_funcionario.place(x=5, y=100)
            lb_erro = Label(frame_main, bg="#363636", foreground="red", font=font.lb, text="Valores inválidos.")
            # -------------------------------------------------LABEL--------------------------------------------#
            # -------------------------------------------------ENTRY--------------------------------------------#
            ed_nome_funcionario = Entry(frame_main, width=20)
            ed_nome_funcionario.place(x=160, y=40)
            ed_numero_funcionario = Entry(frame_main, width=20)
            ed_numero_funcionario.bind("<Key>", entry_telefone)
            ed_numero_funcionario.place(x=160, y=70)
            ed_cpf_funcionario = Entry(frame_main, width=20)
            ed_cpf_funcionario.place(x=160, y=100)
            # -------------------------------------------------ENTRY--------------------------------------------#
            # -------------------------------------------------BOTOES--------------------------------------------#
            bt_salvar = Button(frame_main, text="ADICIONAR", bg=cor.lb_botao_confirmar_off, font=font.botoes,
                               command=add, activebackground=cor.botao_confirmar_active)
            bt_salvar.place(x=100, y=130)
            bt_sair = Button(frame_main, text="x", bg=cor.botao_limpar_off, font=font.botoes, command=close,
                             activebackground=cor.botao_confirmar_active)
            bt_sair.place(x=2, y=2)
            # -------------------------------------------------BOTOES--------------------------------------------#
            # -------------------------------------------------CHECKBOX--------------------------------------------#
            # -------------------------------------------------CHECKBOX--------------------------------------------#
        except:
            None
    def adicionar_nova_atividade(self):
        def close():
            sons('botao')
            janela_adicionar_nova_atividade.destroy()

        def add():
            try:
                nome = str(ed_nome_atividade.get())
                operador.__insert__("atividade", "nome", f"'{nome.upper()}'")
                inserir_atividades_combo()
                janela_adicionar_nova_atividade.destroy()
            except:
                lb_erro.place(x=80, y=150)

        global len_id, tabela, medida, hora_atual
        try:
            janela_adicionar_nova_atividade = Toplevel()
            janela_adicionar_nova_atividade.geometry("325x195+570+200")
            janela_adicionar_nova_atividade["bg"] = "black"
            janela_adicionar_nova_atividade.title("ADICIONAR ATIVIDADE>")
            janela_adicionar_nova_atividade.resizable(width=False, height=False)
            janela_adicionar_nova_atividade.transient()
            janela_adicionar_nova_atividade.focus_force()
            janela_adicionar_nova_atividade.grab_set()
            # -------------------------------------------------FRAME--------------------------------------------#
            frame_main = Frame(janela_adicionar_nova_atividade, width=320, height=190, bg="#363636",
                               highlightbackground="grey", highlightthickness=10)
            frame_main.place(x=2, y=2)
            # -------------------------------------------------FRAME--------------------------------------------#
            # -------------------------------------------------LABEL--------------------------------------------#
            lb_titulo = Label(frame_main, bg="#363636", text="ADICIONAR", font="impact 17 bold", foreground="green")
            lb_titulo.place(x=100, y=3)
            lb_nome_atividade = Label(frame_main, bg="#363636", foreground="white", font=font.lb, text="NOME:")
            lb_nome_atividade.place(x=5, y=40)
            lb_erro = Label(frame_main, bg="#363636", foreground="red", font=font.lb, text="Valores inválidos.")
            # -------------------------------------------------LABEL--------------------------------------------#
            # -------------------------------------------------ENTRY--------------------------------------------#
            ed_nome_atividade = Entry(frame_main, width=20)
            ed_nome_atividade.place(x=160, y=40)
            # -------------------------------------------------ENTRY--------------------------------------------#
            # -------------------------------------------------BOTOES--------------------------------------------#
            bt_salvar = Button(frame_main, text="ADICIONAR", bg=cor.lb_botao_confirmar_off, font=font.botoes,
                               command=add, activebackground=cor.botao_confirmar_active)
            bt_salvar.place(x=100, y=130)
            bt_sair = Button(frame_main, text="x", bg=cor.botao_limpar_off, font=font.botoes, command=close,
                             activebackground=cor.botao_confirmar_active)
            bt_sair.place(x=2, y=2)
            # -------------------------------------------------BOTOES--------------------------------------------#
        except:
            pass
class Historico:
    def historico_produção(self,tipo):
        pass
#------------------------------------------------CLASS---------------------------------------------------------------#
operador=DataBase()
cor=color()
font=font()
cleaner=Cleaner()
new=New()
def check_historico():
	global estoque_auto
	if estoque_auto==False:
		estoque_auto=True
	else:
		estoque_auto=False
def dia_semana():
    global dia
    dia=strftime("%A")
    if dia=="Monday":
        dia="Segunda-Feira"
    if dia=="Tuesday":
        dia="Terça-Feira"
    if dia=="Wednesday":
        dia="Quarta-Feira"
    if dia =="Thursday":
        dia="Quinta-Feira"
    if dia=="Friday":
        dia="Sexta-Feira"
    if dia=="Saturday":
        dia="Sábado"
    if dia=="Sunday":
        dia="Domingo"
def checar_repetido(table):
    global nova_data,dia
    # --------------------REPETE---------------#
    dia_semana()
    datas = []
    operador.__find__(f"{table}","data", datas)
    igual = False
    diferencia = 0
    nova_data = str(data_em_texto)+"-"+str(dia)
    data_a = str(data_em_texto)
    y = 0
    while y < len(datas):
        if str(nova_data) == str(datas[y]):
            diferencia += 1
            nova_data = data_a + "/" + str(diferencia)+"--"+str(dia)
            y = -1
        y += 1
    print(nova_data, data_em_texto,"chequei os repetidos")
    return data_em_texto
def salvar_produção():
    global estoque_auto
    global carne,limpeza,toucinho,alho,sal,total,sabores,ingredientes_quantidade,ingredientes_nome,tipo_porco_frango,nova_data,bacon,peito,tipo_porco_frango,apaga,check_porco,calcula,texto,estoque_auto
    sabores=[]
    ingredientes_quantidade=[]
    ingredientes_nome=[]
    comentario=str(texto.get(1.0,END))
    if comentario == "COMENTÁRIOS\n" :
        comentario="-"
    produzido_por=str(combo_produzido_por.get())
    checar_repetido("historico_calcular")
    operador.__insert__(f"historico_calcular",f"data,carne,peito,limpeza,bacon,toucinho,alho,sal,total,tipo",f"'{nova_data}','{carne:.2f}','{peito:.2f}','{limpeza:.2f}','{bacon:.2f}',{toucinho},'{alho:.2f}','{sal:.2f}','{total:.2f}','{tipo_porco_frango}'")
    operador.__insert__(f"historico_comentarios",f"data,comentario",f"'{nova_data}','{comentario}'")
    operador.__insert__(f"historico_produzido_por",f"data,nome",f"'{nova_data}','{produzido_por}'")
    #---------------------------SALVANDO CALCULAR-----------------------#
    #-------------------------------------SALVANDO INGREDIENTES--------------#
    tabela_sabor="sabor_"+str(tipo_porco_frango)
    operador.__find__(f"{tabela_sabor}","nome",sabores)
    len_id=len(sabores)
    print(sabores,tabela_sabor)
    y=0
    while y<len_id:
        ingredientes_quantidade=[]
        ingredientes_nome=[]
        #--------------MASSA DO ITEN Y----#
        massa=(tabela_ingredientes.item(y,'values')[0])
        if massa=="-":
            print("nao salvei -",tabela_ingredientes.item(y, 'text'))
            y+=1
        else:
            len_string = len(massa)
            len_string = len_string - 2
            massa=float(massa[0:len_string])
            #--------------nomeDO ITEN Y----#
            nome_iten = (tabela_ingredientes.item(y, 'text'))
            #--------------nomeDO ITEN Y----#
            #---------BUSCANDO INGREDIENTES E QUANTIDADE DO SABOR Y -----#
            nome_tabela_iten_y = "sabores_" + tipo_porco_frango + "_" + nome_iten.lower()
            nome_tabela_iten_y_salvar = "historico_ingredientes_" + tipo_porco_frango + "_" + nome_iten.lower()
            operador.__find__(f"{nome_tabela_iten_y}", "nome", ingredientes_nome)
            operador.__find__(f"{nome_tabela_iten_y}", "quantidade", ingredientes_quantidade)
            #---------BUSCANDO INGREDIENTES E QUANTIDADE DO SABOR Y -----#
            itens_salvar_nome ="'data'"
            itens_salvar_value=f"'{nova_data}'"
            x=0
            while x < len(ingredientes_nome):
                quantidade = massa * (float(ingredientes_quantidade[x]))
                itens_salvar_nome+=","+"'"+ingredientes_nome[x].lower()+"'"
                itens_salvar_value+=","+"'"+str(f"{quantidade:.2f}")+"'"
                print(estoque_auto)
                if estoque_auto:
	                if ingredientes_nome[x]!='massa':
	                	cursor.execute(f"SELECT quantidade FROM ingredientes WHERE nome='{ingredientes_nome[x]}'")
	                	quantidade_estoque=float(cursor.fetchone()[0])
	                	quantidade_atualizada=quantidade_estoque-quantidade
	                	cursor.execute(f"UPDATE 'ingredientes' SET 'quantidade' = '{quantidade_atualizada:.2f}' WHERE nome ='{ingredientes_nome[x]}'")
                x += 1
            operador.__insert__(f"{nome_tabela_iten_y_salvar}",f"{itens_salvar_nome}",f"{itens_salvar_value}")
            print("salvei -",nome_tabela_iten_y)
            y+=1
def historico_produção():
    global frame_main_historico,tipo_porco_frango,frame_comentario
    janela_opaca()
    def mostrar_comentario(self):
        a=tabela_historico_produção.selection()[0]
        if (a[0:10]) == "comentario":
            len_a=len(a)
            iten="coment"+(a[10:len_a])
            coment=str(tabela_historico_produção.item(iten, 'text'))
            frame_comentario.place(x=240,y=180)
            texto_coment.delete(0.0,END)
            texto_coment.insert(END,coment)
    def close():
        sons('botao')
        janela_transparente.destroy()
        janela_historico_produção.destroy()
    total_valores=[]
    janela_historico_produção = Toplevel()
    janela_historico_produção.geometry("980x600+200+80")
    janela_historico_produção["bg"] = "black"
    janela_historico_produção.title("ZERAR>")
    janela_historico_produção.resizable(width=False, height=False)
    janela_historico_produção.transient()
    janela_historico_produção.focus_force()
    janela_historico_produção.grab_set()
    frame_main_historico=Frame(janela_historico_produção,bg="#363636",highlightbackground="grey",highlightthickness=10)
    frame_main_historico.pack()
    frame_comentario=Frame(janela_historico_produção,bg="#363636",highlightbackground="grey",highlightthickness=10)
    scroll2 = Scrollbar(frame_main_historico)
    scroll2.pack(side=LEFT, fill=BOTH)
    lb_titulo = Label(frame_main_historico, bg="#363636", text="HISTORICO DE OPERAÇOES", font="impact 17 bold", foreground="green",height=1)
    lb_titulo.pack(side=TOP)
    bt_sair = Button(frame_main_historico, text="x", bg="red", font="Cambria 11 bold", command=close)
    bt_sair.place(x=18, y=1)
    create_table("historico_produção")
    tabela_historico_produção.bind('<<TreeviewOpen>>',mostrar_comentario)
    texto_coment = scrolledtext.ScrolledText(frame_comentario, width=40, height=10)
    texto_coment.pack()
    bt_sair_comentario = Button( frame_comentario, text="x", bg="red", font="Cambria 11 bold", command=cleaner.close_coment)
    bt_sair_comentario.place(x=301, y=1)
    # ------------------------------------------------PESQUISAR VALORES TABELA-------------------------------------------------------------------#
                            #----DATAS-----#
    datas_produção=[]
    tipo=[]
    operador.__find__("historico_calcular","data",datas_produção)
    operador.__find__("historico_calcular","tipo",tipo)
                                # ----DATAS-----#
    #_--------------------------INSERT PARENT-DATAS SEPARADAS POR MES-------------------#
    y=0
    d=1
    mes_save= (datas_produção[0])
    comentario=[]
    produzido_por=[]
    while y<len(datas_produção):
        data = (datas_produção[y])
        mes=(data[3:5])
        comentario=[]
        produzido_por=[]
        if mes!=mes_save:
            tabela_historico_produção.insert("", "end", iid=f"{mes}", text=f'PRODUÇÃO DO MES:{strftime("%Y")}/{mes}')
            mes_save=mes
            #----------------------------HISTORICO CALCULAR-----------------#
            cursor.execute(f"SELECT carne FROM historico_calcular WHERE id={d}")
            h_carne =cursor.fetchone()[0]
            cursor.execute(f"SELECT peito FROM historico_calcular WHERE id={d}")
            h_peito = cursor.fetchone()[0]
            cursor.execute(f"SELECT limpeza FROM historico_calcular WHERE id={d}")
            h_limpeza = cursor.fetchone()[0]
            cursor.execute(f"SELECT bacon FROM historico_calcular WHERE id={d}")
            h_bacon = cursor.fetchone()[0]
            cursor.execute(f"SELECT toucinho FROM historico_calcular WHERE id={d}")
            h_toucinho = cursor.fetchone()[0]
            cursor.execute(f"SELECT alho FROM historico_calcular WHERE id={d}")
            h_alho = cursor.fetchone()[0]
            cursor.execute(f"SELECT sal FROM historico_calcular WHERE id={d}")
            h_sal = cursor.fetchone()[0]
            cursor.execute(f"SELECT total FROM historico_calcular WHERE id={d}")
            h_total = cursor.fetchone()[0]
            tabela_historico_produção.insert(f"{mes}","end",iid=data,text=f'{datas_produção[y]}--{tipo[y].upper()}')
            tabela_historico_produção.insert(data,"end",iid=f"calcular-{data}",text=f'CALCULAR')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'CARNE: {h_carne}KG')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'PEITO: {h_peito}KG')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'LIMPEZA: {h_limpeza}KG')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'BACON: {h_bacon}KG')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'TOUCINHO: {h_toucinho}KG')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'ALHO: {h_alho}g')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'SAL: {h_sal}g')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'TOTAL: {h_total}KG')
            #----------------------------HISTORICO INGREDIENTES-----------------#
            #------BUSCAR-------#
            
            sabores=[]
            ingredientes_nome=[]
            buscar_tipo='sabor_'+str(tipo[y])
            operador.__find__(f"{buscar_tipo}","nome",sabores)
            print(sabores)
            ingredientes_insert_nome=[]
            ingredientes=[]
            x=0
            tabela_historico_produção.insert(f"{data}", "end",iid=f"ingredientes-{data}", text=f'INGREDIENTES')
            p=0
            while x<len(sabores):
                ingredientes = []
                medida=[]
                comentario=[]
                produzido_por=[]
                nome_tabela_sabor_historico="historico_ingredientes_"+str(tipo[y])+"_"+str(sabores[x])
                nome_tabela_sabor = "sabores_"+str(tipo[y])+"_"+str(sabores[x] )
                operador.__find__(f"{nome_tabela_sabor}","nome",ingredientes)
                operador.__find__(f"{nome_tabela_sabor}","medida",medida)
                a=0
                ingredientes_insert_nome=[]
                print("ingredientes--",ingredientes)
                tabela_historico_produção.insert(f"ingredientes-{data}", "end", iid=f"{sabores[x]}-{data}",text=f'{sabores[x].upper()}')
                while a<len(ingredientes):
                    try:
                        cursor.execute(f"SELECT [{ingredientes[a].lower()}] FROM '{nome_tabela_sabor_historico}' WHERE data='{data}'")
                        ingredientes_insert_nome.append(cursor.fetchone()[0])
                        tabela_historico_produção.insert(f"{sabores[x]}-{data}", "end", text=f"{ingredientes[a].upper()}--{ingredientes_insert_nome[a]}{medida[a]}")
                        if medida[a]=="g" and (ingredientes[a])!="massa":
                            total_valores.append(float(ingredientes_insert_nome[a])/1000)
                            total_nomes.append(ingredientes[a].upper())
                            total_medida.append(str(medida[a]))
                        if medida[a]=="KG" and (ingredientes[a])!="massa":
                            total_valores.append(float(ingredientes_insert_nome[a]))
                            total_nomes.append(ingredientes[a].upper())
                            total_medida.append(str(medida[a]))
                    except:
                        print("nao achei registro para a data:",data,ingredientes[a])
                    a+=1
                x+=1
            #------BUSCAR-------#
            _total_ = float(h_total)
            #----------INSERIR--------------#
            while p < len(total_valores):
                _total_ += total_valores[p]
                p += 1
            #----------INSERIR--------------#
            #---------------------------------------------TOTAL--------------#
            p = 0
            tabela_historico_produção.insert(f"{data}", "end", iid=f"total{y}",text=f'TOTAL(CALCULAR+INGREDIENTES):{_total_:.2f}KG')
            tabela_historico_produção.insert(f"total{y}", "end", text=f'MASSA: {(float(h_total)):.3f}')
            while p < len(total_valores):
                tabela_historico_produção.insert(f"total{y}", "end", text=f'{total_nomes[p]}: {total_valores[p]}{total_medida[p]}')
                p += 1            
            #---------------------------------------------INFO-----------------#
            cursor.execute(f"SELECT comentario FROM 'historico_comentarios' WHERE data ='{data}'")
            comentario=str(cursor.fetchone()[0])
            cursor.execute(f"SELECT nome FROM 'historico_produzido_por' WHERE data ='{data}'")
            produzido_por=str(cursor.fetchone()[0])
            tabela_historico_produção.insert(data,"end",iid=f"info-{data}",text=f'INFO')
            tabela_historico_produção.insert(f"info-{data}","end",iid=f"comentario-{data}",text=f'COMENTÁRIOS')
            tabela_historico_produção.insert(f"info-{data}","end",iid=f"produzido_por-{data}",text=f'PRODUZIDO POR')
            tabela_historico_produção.insert(f"comentario-{data}","end",iid=f"coment-{data}",text=f'{comentario.upper()}')
            tabela_historico_produção.insert(f"produzido_por-{data}","end",iid=f"fab-{data}",text=f'{produzido_por.upper()}')
        else:
            total_valores=[]
            total_nomes=[]
            total_medida=[]
            #----------------------------HISTORICO CALCULAR-----------------#
            cursor.execute(f"SELECT carne FROM historico_calcular WHERE id={d}")
            h_carne =cursor.fetchone()[0]
            cursor.execute(f"SELECT peito FROM historico_calcular WHERE id={d}")
            h_peito = cursor.fetchone()[0]
            cursor.execute(f"SELECT limpeza FROM historico_calcular WHERE id={d}")
            h_limpeza = cursor.fetchone()[0]
            cursor.execute(f"SELECT bacon FROM historico_calcular WHERE id={d}")
            h_bacon = cursor.fetchone()[0]
            cursor.execute(f"SELECT toucinho FROM historico_calcular WHERE id={d}")
            h_toucinho = cursor.fetchone()[0]
            cursor.execute(f"SELECT alho FROM historico_calcular WHERE id={d}")
            h_alho = cursor.fetchone()[0]
            cursor.execute(f"SELECT sal FROM historico_calcular WHERE id={d}")
            h_sal = cursor.fetchone()[0]
            cursor.execute(f"SELECT total FROM historico_calcular WHERE id={d}")
            h_total = cursor.fetchone()[0]
            tabela_historico_produção.insert(f"{mes}","end",iid=data,text=f'{datas_produção[y]}--{tipo[y].upper()}')
            tabela_historico_produção.insert(data,"end",iid=f"calcular-{data}",text=f'CALCULAR')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'CARNE: {h_carne}KG')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'PEITO: {h_peito}KG')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'LIMPEZA: {h_limpeza}KG')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'BACON: {h_bacon}KG')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'TOUCINHO: {h_toucinho}KG')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'ALHO: {h_alho}g')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'SAL: {h_sal}g')
            tabela_historico_produção.insert(f"calcular-{data}", "end", text=f'TOTAL: {h_total}KG')
            #----------------------------HISTORICO INGREDIENTES-----------------#
            #------BUSCAR-------#
            
            sabores=[]
            ingredientes_nome=[]
            buscar_tipo='sabor_'+str(tipo[y])
            operador.__find__(f"{buscar_tipo}","nome",sabores)
            print(sabores)
            ingredientes_insert_nome=[]
            ingredientes=[]
            x=0
            tabela_historico_produção.insert(f"{data}", "end",iid=f"ingredientes-{data}", text=f'INGREDIENTES')
            p=0
            while x<len(sabores):
                ingredientes = []
                medida=[]
                comentario=[]
                produzido_por=[]
                nome_tabela_sabor_historico="historico_ingredientes_"+str(tipo[y])+"_"+str(sabores[x])
                nome_tabela_sabor = "sabores_"+str(tipo[y])+"_"+str(sabores[x] )
                operador.__find__(f"{nome_tabela_sabor}","nome",ingredientes)
                operador.__find__(f"{nome_tabela_sabor}","medida",medida)
                a=0
                ingredientes_insert_nome=[]
                print("ingredientes--",ingredientes)
                tabela_historico_produção.insert(f"ingredientes-{data}", "end", iid=f"{sabores[x]}-{data}",text=f'{sabores[x].upper()}')
                while a<len(ingredientes):
                    try:
                        cursor.execute(f"SELECT [{ingredientes[a].lower()}] FROM '{nome_tabela_sabor_historico}' WHERE data='{data}'")
                        ingredientes_insert_nome.append(cursor.fetchone()[0])
                        tabela_historico_produção.insert(f"{sabores[x]}-{data}", "end", text=f"{ingredientes[a].upper()}--{ingredientes_insert_nome[a]}{medida[a]}")
                        if medida[a]=="g" and (ingredientes[a])!="massa":
                            total_valores.append(float(ingredientes_insert_nome[a])/1000)
                            total_nomes.append(ingredientes[a].upper())
                            total_medida.append(str(medida[a]))
                        if medida[a]=="KG" and (ingredientes[a])!="massa":
                            total_valores.append(float(ingredientes_insert_nome[a]))
                            total_nomes.append(ingredientes[a].upper())
                            total_medida.append(str(medida[a]))
                    except:
                        print("nao achei registro para a data:",data,ingredientes[a])
                    a+=1
                x+=1
            #------BUSCAR-------#
            _total_ = float(h_total)
            #----------INSERIR--------------#
            while p < len(total_valores):
                _total_ += total_valores[p]
                p += 1
            #----------INSERIR--------------#
            #---------------------------------------------TOTAL--------------#
            p = 0
            tabela_historico_produção.insert(f"{data}", "end", iid=f"total{y}",text=f'TOTAL(CALCULAR+INGREDIENTES):{_total_:.2f}KG')
            tabela_historico_produção.insert(f"total{y}", "end", text=f'MASSA: {(float(h_total)):.3f}')
            while p < len(total_valores):
                tabela_historico_produção.insert(f"total{y}", "end", text=f'{total_nomes[p]}: {total_valores[p]}{total_medida[p]}')
                p += 1            
            #---------------------------------------------INFO-----------------#
            cursor.execute(f"SELECT comentario FROM 'historico_comentarios' WHERE data ='{data}'")
            comentario=str(cursor.fetchone()[0])
            cursor.execute(f"SELECT nome FROM 'historico_produzido_por' WHERE data ='{data}'")
            produzido_por=str(cursor.fetchone()[0])
            tabela_historico_produção.insert(data,"end",iid=f"info-{data}",text=f'INFO')
            tabela_historico_produção.insert(f"info-{data}","end",iid=f"comentario-{data}",text=f'COMENTÁRIOS')
            tabela_historico_produção.insert(f"info-{data}","end",iid=f"produzido_por-{data}",text=f'PRODUZIDO POR')
            tabela_historico_produção.insert(f"comentario-{data}","end",iid=f"coment-{data}",text=f'{comentario.upper()}')
            tabela_historico_produção.insert(f"produzido_por-{data}","end",iid=f"fab-{data}",text=f'{produzido_por.upper()}')
        y+=1
        d+=1
def janela_salvar_historico():
    global carne, limpeza, toucinho, alho, sal, total,tipo_porco_frango,janela_salvar_historico,combo_produzido_por,texto
    janela_salvar_historico = Toplevel()
    janela_salvar_historico.geometry("560x390+380+140")
    janela_salvar_historico["bg"] = "black"
    janela_salvar_historico.title("ZERAR>")
    janela_salvar_historico.resizable(width=False, height=False)
    janela_salvar_historico.transient()
    janela_salvar_historico.focus_force()
    janela_salvar_historico.grab_set()
    janela_salvar_historico.overrideredirect(True)
    frame_main_historico=Frame(janela_salvar_historico,bg="#363636",highlightbackground="grey",highlightthickness=9,width=560,height=390)
    frame_main_historico.place(x=0,y=0)
    frame_agrupador = Frame(janela_salvar_historico, bg="#363636", highlightbackground="grey",highlightthickness=2)
    frame_agrupador.place(x=65, y=60)
    frame_tabela_historico=Frame(frame_agrupador,bg="#363636",highlightbackground="grey",highlightthickness=2,width=200,height=200)
    frame_tabela_historico.pack(side=TOP)
    frame_historico_texto = Frame(frame_agrupador, bg="#363636", highlightbackground="grey",highlightthickness=2, width=200, height=20)
    frame_historico_texto.pack(side=TOP)
    frame_tabela_historico_botoes=Frame(frame_agrupador,bg="#363636",highlightbackground="grey",highlightthickness=2,width=200,height=20)
    frame_tabela_historico_botoes.pack(side=TOP)
    #---------------------------
    lb_titulo = Label(frame_main_historico, bg="#363636", text="SALVAR", font=font.titulo, foreground="green")
    lb_titulo.place(x=50, y=8)
    # massa = (tabela_ingredientes.item(y, 'values')[0])
    # --------------------------------------
    texto = scrolledtext.ScrolledText(frame_historico_texto, width=50, height=2)
    texto.pack(side=TOP)
    texto.insert(END,"COMENTÁRIOS")
    combo_produzido_por = ttk.Combobox(frame_historico_texto)
    combo_produzido_por.pack(side=BOTTOM, fill=BOTH)
    combo_produzido_por.insert(END,"PRODUZIDO POR>")
    #_--------------------combo values---------#
    funcionarios=[]
    operador.__find__("funcionarios","nome",funcionarios)
    combo_produzido_por['values']=funcionarios
    #-------------------SELECT---------------#
    select_check_calcular=Listbox(frame_tabela_historico, bg="#1C1C1C", foreground="#B22222", height=10,width=20,font='gothic 13 bold')
    select_check_calcular.pack(side=LEFT)
    select_check_calcular.insert(END,f"CALCULAR")
    select_check_calcular.insert(END,f" CARNE:{carne:.2f}KG")
    select_check_calcular.insert(END,f" PEITO:{peito:.2f}KG")
    select_check_calcular.insert(END,f" LIMPEZA:{limpeza:.2f}KG")
    select_check_calcular.insert(END,f" TOUCINHO:{toucinho:.2f}KG")
    select_check_calcular.insert(END,f" BACON: {bacon:.2f}KG")
    select_check_calcular.insert(END,f" ALHO: {alho:.2f}g")
    select_check_calcular.insert(END,f" SAL: {sal:.2f}g")
    select_check_calcular.insert(END,f" TOTAL: {total:.2f}KG")
    #-------------------------------------------------------------#
    select_check_ingredientes=Listbox(frame_tabela_historico, bg="#1C1C1C", foreground="#B22222", height=10,width=21,font='gothic 13 bold')
    select_check_ingredientes.pack(side=LEFT)
    #_--------------#
    nome_sabor="sabor_"+str(tipo_porco_frango)
    sabores=[]
    operador.__find__(f"{nome_sabor}","nome",sabores)
    select_check_ingredientes.insert(END, f"INGREDIENTES")
    y=0
    while y<len(sabores):
        massa = (tabela_ingredientes.item(y, 'values')[0])
        nome=(tabela_ingredientes.item(y, 'text'))
        if massa=="-":
            massa=0
        select_check_ingredientes.insert(END, f"{nome}: {massa}")
        y+=1
    # -------------------SELECT---------------#
    
    check_estoque_auto = Checkbutton(frame_tabela_historico_botoes, text=" ESTOQUE AUTO", font="Cambria 10",command=check_historico)
    check_estoque_auto.pack(side=LEFT)
    #-----------------------------------------------------------------#
    bt_historico_salvar = Button(frame_tabela_historico_botoes, text="SALVAR", bg=cor.botao_confirmar_off, font=font.botoes,activebackground=cor.botao_confirmar_active,width=32,command=salvar_produção)
    bt_historico_salvar.pack(side=LEFT)
    bt_close = Button(frame_main_historico, text="✖", bg=cor.botao_limpar_off, command=cleaner.close_janela_historico,foreground=cor.lb_botao_limpar_off, font=font.botoes,activebackground=cor.botao_confirmar_active)
    bt_close.place(x=510, y=2)
def atividade():
    sons('botao')
    global select,iniciado
    combo_select=(combo_hora.get())
    if select=="FUNCIONARIOS":
        pass
    elif select=="":
        pass
    elif combo_select=="":
        pass
    else:
        hora=strftime("%H:%M:%S")
        tabela_hora_info.insert("", "end",text=f'{select}', values=(f"{combo_select}",f"{hora}"))
    if combo_select=="*INICIAR*":
        iniciado=True
        inserir_atividades_combo()
def divivir_ok():
    sons('botao')
    global divide
    try:
        divide=float(ed_dividir.get())
        if divide==0:
            divide=1
        frame_tabela_calcular_dividir.place(x=1000,y=1000)
    except:
        divide=1
        frame_tabela_calcular_dividir.place(x=1000,y=1000)
def dividir_mostra():
    sons('botao')
    frame_tabela_calcular_dividir.place(x=235,y=190)
    pass
def selecionado():
    global lb_selecionado_produçao
    try:
        id = tabela_ingredientes.selection()
        id = int(id[0])
        lb_selecionado_produçao["text"] = sabores[id].upper()
        #print('rodo select')
    except:
        pass 
def cabeçalho(parent):
    global logo,logo_estoque,logo_wp,logo_fb,logo_instagram,lb_titulo,lb_logo_estoque
    # -------------------------------------------------CABEÇALHO---------------------------------------------------------------#
    frame_cabeçalho = Frame(parent, width=1355, height=110, highlightbackground="#363636", highlightthickness=7,bg="#1d1b1b")
    frame_cabeçalho.place(x=5, y=1)
    frame_credito = Frame(frame_cabeçalho, width=1355, height=110, highlightbackground="#363636", highlightthickness=2,bg="#1d1b1b")
    frame_credito.place(x=1120, y=60)
    # ---------------------------------------------------PHOTO-----------------------------------------------------------------
    logo = PhotoImage(file="img/logo_2.png")
    logo = logo.subsample(3, 4)
    logo_estoque = PhotoImage(file="img/icone_produção.png")
    logo_estoque = logo_estoque.subsample(7, 8)
    logo_wp = PhotoImage(file="img/logo_whats.png")
    logo_wp = logo_wp.subsample(5, 5)
    logo_fb = PhotoImage(file="img/logo_fb.png")
    logo_fb = logo_fb.subsample(14, 14)
    logo_instagram = PhotoImage(file="img/logo_instagran.png")
    logo_instagram = logo_instagram.subsample(5, 5)
    # ---------------------------------------------------LABEL_PHOTO-----------------------------------------------------------------
    lb_logo = Label(frame_cabeçalho, image=logo, bg="#1d1b1b")
    lb_logo.place(x=520, y=2)
    lb_logo_estoque = Label(frame_cabeçalho, image=logo_estoque, bg="#1d1b1b")
    lb_logo_estoque.place(x=12, y=17)
    lb_logo_wp = Label(frame_cabeçalho, image=logo_wp, bg="#1d1b1b")
    lb_logo_wp.place(x=1120, y=1)
    lb_logo_fb = Label(frame_cabeçalho, image=logo_fb, bg="#1d1b1b")
    lb_logo_fb.place(x=930, y=60)
    lb_logo_instagram = Label(frame_cabeçalho, image=logo_instagram, bg="#1d1b1b")
    lb_logo_instagram.place(x=930, y=1)
    # --------------------------------------------------------------------------------------------------------------------#
    lb_titulo = Label(frame_cabeçalho, bg="#1d1b1b", text="➮PRODUÇÃO", font="impact 35 underline", foreground="grey")
    lb_titulo.place(x=100, y=30)
    lb_endereço = Label(frame_cabeçalho, bg="#1d1b1b", foreground="#DCDCDC", font='gothic 13 bold',text="RUA PRAÇA CASTORINO DE SOUZA 84")
    lb_telefone = Label(frame_cabeçalho, bg="#1d1b1b", foreground="#DCDCDC", font='gothic 13 bold',text="(35) 9 91158971")
    lb_telefone.place(x=1160, y=20)
    lb_instagran = Label(frame_cabeçalho, bg="#1d1b1b", foreground="#DCDCDC", font='gothic 10 bold',text="@diegolaraTIKTIM")
    lb_instagran.place(x=970, y=20)
    lb_fb = Label(frame_cabeçalho, bg="#1d1b1b", foreground="#DCDCDC", font='gothic 10 bold', text="/diegolaraTiktim")
    lb_fb.place(x=970, y=70)
    lb_credito = Label(frame_credito, bg="#1d1b1b", foreground="#DCDCDC", font='italic 9 bold underline',text="CREATED BY PEDRO NESTOR")
    lb_credito.pack(anchor=S)
def menu(parent):
    main_menu = Menu(parent)
    barra = Menu(main_menu)
    menu_opçoes = Menu(main_menu)
    menu_configuraçoes = Menu(main_menu)
    menu_historico = Menu(main_menu)

    menu_opçoes.add_command(label="SALVAR",command=janela_salvar_historico)
    menu_opçoes.add_command(label="Adicionar Funcioário",command=new.adicionar_novo_funcionário)
    menu_opçoes.add_command(label="Adicionar Atividade",command=new.adicionar_nova_atividade)
    menu_opçoes.add_command(label="Adicionar Novo sabor",command=new.adicionar_sabor)
    menu_opçoes.add_command(label="Zerar Funcionários",command=cleaner.zerar_tabela_funcionarios)
    menu_opçoes.add_command(label="Zerar Historico Produção",command=cleaner.zerar_tabela_historico_calcular)
    menu_opçoes.add_command(label="Zerar Historico Estoque",command=cleaner.zerar_historico_estoque)
    #menu_opçoes.add_command(label="Zerar Atividades",command=cleaner.zerar_tabela_atividades)
    menu_opçoes.add_command(label="Zerar Sabores Frango",command=cleaner.zerar_tabela_ingredientes_frango)
    menu_opçoes.add_command(label="Zerar Sabores Porco",command=cleaner.zerar_tabela_ingredientes_porco)
    menu_opçoes.add_command(label="SAIR",command=cleaner.sair)
    menu_configuraçoes.add_command(label="Som on/off")
    menu_historico.add_command(label="Produção",command=historico_produção)
    menu_historico.add_command(label="Estoque",command=bt_historico)
    barra.add_cascade(label="Opções", menu=menu_opçoes)
    barra.add_cascade(label="Histórico", menu=menu_historico)
    barra.add_cascade(label="Configurações", menu=menu_configuraçoes)
    janela.config(menu=barra)
def create_table(parent):
    global tabela_calcular,tabela_ingredientes,sabores,frame_main_historico,tabela_historico_produção
    if parent=="calcular":
        tabela_calcular.destroy()
        tabela_calcular = ttk.Treeview(frame_tabela_calcular, columns=( "QUANTIDADE"),height=10, selectmode="browse")
        tabela_calcular.pack()
        tabela_calcular.column('#0', minwidth=159,width=159)
        tabela_calcular.column("QUANTIDADE", width=160, minwidth=160)
        tabela_calcular.heading("#0", text="INGREDIENTES")
        tabela_calcular.heading("QUANTIDADE", text="QUANTIDADE")
    if parent=="ingredientes":
        sabores = []
        tabela_ingredientes.destroy()
        tabela_ingredientes = ttk.Treeview(frame_tabela_ingredientes, columns=("QUANTIDADE"), height=12,selectmode="browse")
        tabela_ingredientes.pack()
        tabela_ingredientes.column('#0', width=350, minwidth=350)
        tabela_ingredientes.column("QUANTIDADE", width=220, minwidth=220)
        style = ttk.Style(janela)
        tabela_ingredientes.heading("#0", text="SABORES")
        tabela_ingredientes.heading("QUANTIDADE", text="QUANTIDADE KG")
        tabela_ingredientes.bind('<<TreeviewSelect>>',selecionado)
    if parent=="historico_produção":
        tabela_historico_produção = ttk.Treeview(frame_main_historico, height=15,selectmode="browse")
        tabela_historico_produção.pack(side=BOTTOM)
        # ----------------------------------------------------------------------------------------------------------------------#
        tabela_historico_produção.column('#0', width=950, minwidth=950)
        tabela_historico_produção.heading("#0", text="DATAS")
    if parent=="historico_calcular":
        tabela_historico_calcular = ttk.Treeview(frame_tabela_historico_calcular, columns=( "QUANTIDADE"),height=10, selectmode="browse")
        tabela_historico_calcular.pack()
        tabela_historico_calcular.column('#0', width=149, minwidth=149)
        tabela_historico_calcular.column("QUANTIDADE", width=160, minwidth=160)
        style = ttk.Style(janela_salvar_historico)
        style.configure("Treeview", font='gothic 17 bold', rowheight=34, background="black", fieldbackground="black",foreground="white")
        tabela_historico_calcular.heading("#0", text="INGREDIENTES")
        tabela_historico_calcular.heading("QUANTIDADE", text="QUANTIDADE")
    if parent=="historico_ingredientes":
        tabela_historico_ingredientes = ttk.Treeview(frame_tabela_historico_ingredientes, columns=("QUANTIDADE"), height=10,selectmode="browse")
        tabela_historico_ingredientes.pack()
        tabela_historico_ingredientes.column('#0', width=350, minwidth=350)
        tabela_historico_ingredientes.column("QUANTIDADE", width=220, minwidth=220)
        style = ttk.Style(janela_salvar_historico)
        style.configure("Treeview", font='gothic 17 bold', rowheight=34, background="black", fieldbackground="black",foreground="white")
        tabela_historico_ingredientes.heading("#0", text="SABORES")
        tabela_historico_ingredientes.heading("QUANTIDADE", text="QUANTIDADE KG")
def entry_telefone(self):
    entrada=""
    entrada=ed_numero_funcionario.get()
    if len(entrada)==1 and entrada[0] !=" (":
        ed_numero_funcionario.insert(0,"(")
    if len(entrada)==3 and entrada[2] !=")":
        ed_numero_funcionario.insert(3,")")
def event_select(self):
    global select
    select=select_funcionarios.selection_get()
    if select=="FUNCIONARIOS":
        lb_select["text"] = ""
    else:
        lb_select["text"]=select
def atualiza():
    atualiza_slide()
    selecionado()
    lb_selecionado_produçao.after(200,atualiza)
def atualiza_slide():
    global restante,save
    lb_relogio["text"] = strftime("%H:%M:%S")
    if save != int(slide1.get()):
        restante_r=restante-int(slide1.get())
        if restante_r<0:
            restante_r=0
        lb_restante_r["text"] = f"{restante_r:.0f}KG"
        save = int(slide1.get())
def inserir_sabores_tabela(tipo):
    global sabores,tabela_calcular,tabela_ingredientes
    sabores=[]
    if tipo=="porco":
        y=0
        operador.__find__("sabor_porco","nome",sabores)
        while y < len(sabores):
            tabela_ingredientes.insert("", "end", iid=f"{y}", text=f'{sabores[y].upper()}', values=("-"))
            y += 1
    if tipo=="frango":
        y=0
        operador.__find__("sabor_frango","nome",sabores)
        while y < len(sabores):
            tabela_ingredientes.insert("", "end", iid=f"{y}", text=f'{sabores[y].upper()}', values=("-"))
            y += 1
def inserir_funcionarios_select():
    funcionarios=[]
    select_funcionarios.delete(0,END)
    select_funcionarios.insert(END,"FUNCIONARIOS")
    y=0
    operador.__find__("funcionarios","nome",funcionarios)
    while y < len(funcionarios):
        select_funcionarios.insert(END,f"  {funcionarios[y].upper()}")
        y += 1
def inserir_atividades_combo():
    atividades=[]
    operador.__find__("atividade","nome",atividades)
    combo_hora['values']=atividades
def adicionar_sabor():
    operador.__find__("ingredientes","nome",ingredientes)
    tipo=""
    ingredientes_adicionar = []
    ingredientes_adicionar_quantidade = []
    ingredientes_adicionar_medida = []
    def limpar():
        global ingredientes_adicionar,ingredientes_quantidade,ingredientes_adicionar_medida,medida,tipo
        select_ver.delete(0,END)
        tipo=""
        medida=""
        ingredientes_adicionar,ingredientes_quantidade,ingredientes_adicionar_medida=[],[],[]
        check_kg.deselect()
        check_g.deselect()
        check_porco.deselect()
        check_frango.deselect()
        ed_nome.delete(0,END)
        combo.set("")
        ed_preço.delete(0,END)
    def checar():
        check=0
        try:
            nome=str(ed_nome.get())
            check+=1
        except:
            pass
        try:
            a=float(ed_preço.get())
            check += 1
        except:
            pass
        try:
            a=(str(medida))
            check += 1
        except:
            pass
        try:
            a=(combo.get())
            if a=="":
                check -=1
            else:
                check += 1
        except:
            pass
        if check==4:
            bt_salvar["command"]=adicionar
            bt_confirmar["command"]=salvar
            bt_salvar["bg"]="blue"
        else:
            bt_salvar["command"]=""
            bt_salvar["bg"]="white"
    def atualizar_atualizar():
        checar()
        janela_adicionar_sabor.after(200,atualizar_atualizar)
    def check_porco_adicionar():
        global tipo
        tipo="porco"
        check_frango.deselect()
    def check_frango_adicionar():
        global tipo
        tipo="frango"
        check_porco.deselect()
    def check_kg():
        global medida
        medida="KG"
        check_g.deselect()
    def check_g():
        global medida
        medida="g"
        check_kg.deselect()
    def close():
        sons('botao')
        janela_adicionar_sabor.destroy()
    def adicionar():
        global medida,tipo,nome_sabor
        """nome = fornecedores_buscar_nome[id]
        nome_ = "fornecedor_" + nome
        nome_item = combo.get()
        preço=float(ed_preço.get())
        cursor.execute(f"UPDATE {nome_} SET preço = {preço} WHERE nome_iten='{nome_item.lower()}'")
        cursor.execute(f"UPDATE {nome_} SET data = '{str(data_em_texto)}--{str(hora_atual)}' WHERE nome_iten='{nome_item.lower()}'")
        connect.commit()"""
        select_ver.delete(0,END)
        nome_sabor=str(ed_nome.get())
        ingredientes_quantidade.append(float(ed_preço.get()))
        ingredientes_adicionar_medida.append(str(medida))
        ingredientes_adicionar.append(str(combo.get()))
        select_ver.insert(END, "NOVO SABOR")
        select_ver.insert(END, f" NOME:{nome_sabor.upper()}")
        select_ver.insert(END,f" TIPO:{tipo.upper()}")
        select_ver.insert(END, f"INGREDIENTES:")
        y=0
        while y<len(ingredientes_adicionar):
            select_ver.insert(END, f"    {ingredientes_adicionar[y].upper()}-{ingredientes_quantidade[y]}{ingredientes_adicionar_medida[y]}/KG")
            y+=1
    def salvar():
        global medida, tipo,nome_sabor
        # -------------------------#
        tabela="sabor_"+tipo
        buscar=[]
        operador.__find__(tabela,"nome",buscar)
        igual=False
        y=0
        while y<len(buscar):
            if nome_sabor==buscar[y]:
                igual=True
                break
            y+=1
        # -------------------------#
        if igual==False:
            operador.__insert__(f'{tabela}',"nome",f"'{nome_sabor}'")
            #-------------------------#
            tabela = "sabores_"+tipo+"_"+ f"{nome_sabor}"
            operador.__create__(f'{tabela}',"id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade REAL, medida TEXT")
            y=0
            operador.__insert__(f'{tabela}', "nome,quantidade,medida",f"'massa','1','KG'")
            while y<len(ingredientes_adicionar):
                operador.__insert__(f'{tabela}',"nome,quantidade,medida",f"'{ingredientes_adicionar[y]}','{ingredientes_quantidade[y]}','{ingredientes_adicionar_medida[y]}'")
                y+=1
        else:
            print("igual!")
    #-----------------------------------------------------------------------------------------------------------------------------------------#
    janela_adicionar_sabor=Toplevel()
    janela_adicionar_sabor.geometry("600x256+530+200")
    janela_adicionar_sabor["bg"]="black"
    janela_adicionar_sabor.title("ATUALIZAR PREÇO>")
    janela_adicionar_sabor.resizable(width=False, height=False)
    janela_adicionar_sabor.transient()
    janela_adicionar_sabor.focus_force()
    janela_adicionar_sabor.grab_set()
    #------------------------------------------------FRAME--------------------------------------------#
    frame_main_main=Frame(janela_adicionar_sabor,width=605,height=250,highlightbackground="grey",highlightthickness=10,bg="#363636")
    frame_main_main.place(x=2,y=2)
    frame_funçoes=Frame(frame_main_main,highlightbackground="grey",highlightthickness=5,height=150,width=280,bg="#363636")
    frame_funçoes.place(x=15,y=45)
    frame_main=Frame(frame_funçoes,highlightbackground="grey",highlightthickness=3,height=100,width=200,bg="#363636")
    frame_main.place(x=10,y=70)
    #-------------------------------------------------FRAME--------------------------------------------#
    combo = ttk.Combobox(frame_main)
    combo.pack(side=BOTTOM, fill=BOTH)
    combo['values']=ingredientes
    #-------------------------------------------------LABEL--------------------------------------------#
    lb_titulo = Label(frame_main_main, bg="#363636", text="ADICIONAR NOVO SABOR", font="impact 17 bold", foreground="green")
    lb_titulo.place(x=80,y=5)
    lb_nome_iten = Label(frame_funçoes, bg="#363636", foreground="white", font='gothic 10 bold', text="NOME:")
    lb_nome_iten.place(x=10,y=10)
    lb_preço_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="QUANTIDADE:")
    lb_preço_iten.pack(side=LEFT)
    lb_erro = Label(frame_main, bg="#363636", foreground="red", font='gothic 10 bold', text="Valores inválidos.")
    #-------------------------------------------------LABEL--------------------------------------------#
    #-------------------------------------------------ENTRY--------------------------------------------#
    ed_preço = Entry(frame_main, width=8)
    ed_preço.pack(side=LEFT)
    ed_nome = Entry(frame_funçoes, width=20)
    ed_nome.place(x=70,y=12)
    #-------------------------------------------------ENTRY--------------------------------------------#
    check_kg = Checkbutton(frame_funçoes, text="KG", font="Cambria 10", command=check_kg)
    check_kg.place(x=110, y=45)
    check_g = Checkbutton(frame_funçoes, text="G", font="Cambria 10", command=check_g)
    check_g.place(x=165, y=45)
    check_porco = Checkbutton(frame_funçoes, text="PORCO", font="Cambria 10", command=check_porco_adicionar,var=chkValue)
    check_porco.place(x=10, y=45)
    check_frango = Checkbutton(frame_funçoes, text="FRANGO", font="Cambria 10", command=check_frango_adicionar)
    check_frango.place(x=50, y=45)
    select_ver=Listbox(frame_main_main, bg="#1C1C1C", foreground="#B22222", height=10,width=25,font='gothic 13 bold')
    select_ver.place(x=300,y=40)
    select_ver.insert(END,"NOVO SABOR:")
    select_ver.insert(END,"NOME:")
    select_ver.insert(END,"TIPO:")
    select_ver.insert(END,"INGREDIENTES:")

    #-------------------------------------------------BOTOES--------------------------------------------#
    bt_salvar = Button(frame_main, text="ADICIONAR", bg=cor.botao_confirmar_off, font=font.botoes,activebackground=cor.botao_confirmar_active)
    bt_salvar.pack(side=BOTTOM)
    bt_confirmar = Button(frame_main_main, text="SALVAR", bg=cor.botao_confirmar_off, font=font.botoes,width=28,activebackground=cor.botao_confirmar_active,foreground=color.lb_botao_confirmar_off)
    bt_confirmar.place(x=16,y=198)
    bt_sair = Button(frame_main_main, text="x", bg=cor.botao_limpar_off, font=font.botoes, command=close,foreground=color.lb_botao_limpar_off,activebackground=cor.botao_confirmar_active)
    bt_sair.place(x=2, y=2)
    bt_limpar = Button(frame_main_main, text="x", bg=cor.botao_limpar_off, font=font.botoes, command=limpar,activebackground=cor.botao_confirmar_active,foreground=color.lb_botao_limpar_off)
    bt_limpar.place(x=400, y=10)
    atualizar_atualizar()
def calculate_frango():
    sons('botao')
    global tempero_quantity,sabores,restante,total,tipo_porco_frango,tabela,carne,peito,limpeza,bacon,alho,sal,toucinho,apaga,calcula
    atualiza()
    sabores=[]
    tempero_quantity=[]
    try:
        # -----------------------------VERIFICA SE OS VALOES SAO POSITIVOS E NUMEICOS--------------------------------------------------#
        try:
            teste = float(ed_carne.get())
            if (float(ed_carne.get())) >= 0:
                lb_erro_calcular_carne.place(x=1000, y=1000)
                carne = float(ed_carne.get())
            else:
                lb_erro_calcular_carne.place(x=180, y=2)
                create_table("calcular")
                create_table("ingredientes")
        except:
            lb_erro_calcular_carne.place(x=180, y=2)
            create_table("calcular")
            create_table("ingredientes")

        try:
            teste = float(ed_limpeza.get())
            if (float(ed_limpeza.get())) >= 0:
                limpeza = float(ed_limpeza.get())
                lb_erro_calcular_limpeza.place(x=1000, y=1000)
            else:
                lb_erro_calcular_limpeza.place(x=180, y=30)
                create_table("calcular")
                create_table("ingredientes")
        except:
            lb_erro_calcular_limpeza.place(x=180, y=30)
            create_table("calcular")
            create_table("ingredientes")
        # --------------------------------------------------------------------------------------#
        try:
            create_table("ingredientes")
            operador.__find__("tempero_frango", "quantidade", tempero_quantity)
            inserir_sabores_tabela("frango")
            value_peito = tempero_quantity[0]
            value_bacon = tempero_quantity[1]
            value_alho = tempero_quantity[2]
            value_sal = tempero_quantity[3]
            peito = (carne * value_peito)
            bacon = (carne + peito) * value_bacon
            alho = (carne + limpeza + peito) * value_alho
            sal = (carne + limpeza + peito) * value_sal
            total = (carne + limpeza + bacon + peito)
            toucinho=0
            restante = total
            lb_restante_r["text"] = f"{restante:.0f}KG"
            slide1['to'] = restante
            create_table("calcular")
            apaga=False
            calcula=True
            if divide==1:
                tabela_calcular.insert("", "end", text="CARNE",values=(f'{carne:.2f}KG'))
                tabela_calcular.insert("", "end", text="LIMPEZA",values=(f'{limpeza:.2f}KG'))
                tabela_calcular.insert("", "end", text="PEITO",values=(f'{peito:.2f}KG'))
                tabela_calcular.insert("", "end", text="BACON",values=(f'{bacon:.2f}KG'))
                tabela_calcular.insert("", "end", text="ALHO",values=(f'{alho:.2f}g'))
                tabela_calcular.insert("", "end", text="SAL",values=(f'{sal:.2f}g'))
                tabela_calcular.insert("", "end", text="TOTAL",values=(f'{total:.2f}KG'))
            else:
                tabela_calcular.insert("", "end", text="DIVIDIR",values=(f'{divide:.2f}'))
                tabela_calcular.insert("", "end", text="CARNE",values=(f'{carne/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text="LIMPEZA",values=(f'{limpeza/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text="PEITO",values=(f'{peito/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text="BACON",values=(f'{bacon/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text="ALHO",values=(f'{alho/divide:.2f}g'))
                tabela_calcular.insert("", "end", text="SAL",values=(f'{sal/divide:.2f}g'))
                tabela_calcular.insert("", "end", text="TOTAL",values=(f'{total/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text="TOTAL*",values=(f'{total:.2f}KG'))
            tipo_porco_frango="frango"
        except:
            create_table("calcular")
            create_table("ingredientes")
    except:
        create_table("calcular")
        create_table("ingredientes")
def calculate_porco():
    sons('botao')
    global tempero_quantity,sabores,restante,total,tipo_porco_frango,tabela_ingredientes,tabela_calcular,ingredientes_salvar,carne,limpeza,toucinho,alho,sal,peito,bacon,apaga,calcula
    atualiza()
    sabores=[]
    tempero_quantity=[]
    try:
        #-----------------------------VERIFICA SE OS VALOES SAO POSITIVOS E NUMEICOS--------------------------------------------------#
        try:
            teste = float(ed_carne.get())
            if(float(ed_carne.get())) >= 0:
                lb_erro_calcular_carne.place(x=1000, y=1000)
                carne=float(ed_carne.get())
            else:
                lb_erro_calcular_carne.place(x=180, y=2)
                create_table("calcular")
                create_table("ingredientes")
        except:
            lb_erro_calcular_carne.place(x=180, y=2)
            create_table("calcular")
            create_table("ingredientes")

        try:
            teste=float(ed_limpeza.get())
            if(float(ed_limpeza.get())) >= 0:
                limpeza = float(ed_limpeza.get())
                lb_erro_calcular_limpeza.place(x=1000, y=1000)
            else:
                lb_erro_calcular_limpeza.place(x=180, y=30)
                create_table("calcular")
                create_table("ingredientes")
        except:
            lb_erro_calcular_limpeza.place(x=180, y=30)
            create_table("calcular")
            create_table("ingredientes")
        #--------------------------------------------------------------------------------------#
        try:
            create_table("ingredientes")
            inserir_sabores_tabela("porco")
            operador.__find__("tempero_porco", "quantidade", tempero_quantity)
            value_toucinho = tempero_quantity[0]
            value_sal = tempero_quantity[2]
            value_alho = tempero_quantity[1]
            toucinho=carne*value_toucinho
            total = (carne + limpeza + toucinho)
            alho=(total*(value_alho))
            sal=(total*(value_sal))
            total=total+(alho/1000)+(sal/1000)
            restante=total
            lb_restante_r["text"]=f"{restante:.0f}KG"
            slide1['to']=restante
            create_table("calcular")
            peito=0
            bacon=0
            apaga=False
            calcula=True
            if divide==1:
                tabela_calcular.insert("", "end", text="CARNE",values=(f'{carne/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text="LIMPEZA",values=(f'{limpeza/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text="TOUCINHO",values=(f'{toucinho/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text="ALHO",values=(f'{alho/divide:.2f}g'))
                tabela_calcular.insert("", "end", text="SAL",values=(f'{sal/divide:.2f}g'))
                tabela_calcular.insert("", "end", text="TOTAL",values=(f'{total/divide:.2f}KG'))
            else:
                tabela_calcular.insert("", "end", text=f"DIVIDIR",values=(f'{divide:.2f}'))
                tabela_calcular.insert("", "end", text=f"CARNE",values=(f'{carne/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text=f"LIMPEZA",values=(f'{limpeza/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text=f"TOUCINHO",values=(f'{toucinho/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text=f"ALHO",values=(f'{alho/divide:.2f}g'))
                tabela_calcular.insert("", "end", text=f"SAL",values=(f'{sal/divide:.2f}g'))
                tabela_calcular.insert("", "end", text=f"TOTAL",values=(f'{total/divide:.2f}KG'))
                tabela_calcular.insert("", "end", text=f"TOTAL*",values=(f'{total:.2f}KG'))
            tipo_porco_frango="porco"
        except:
            create_table("calcular")
            create_table("ingredientes")
            print("erro na parte bd do calculate porco")
    except:
        create_table("calcular")
        create_table("ingredientes")
def bt_calcular_sabores():
    sons('botao')
    global resultado,nome_resultado,massa,tabela_ingredientes,tabela_calcular
    resultado=[]
    try:
        id = tabela_ingredientes.selection()
        id = int(id[0])
        calcular_sabores(sabores[id])
    except:
        pass
    y=0
    try:
        tabela_ingredientes.delete(id)
        tabela_ingredientes.insert("", "end", iid=f"{id}", text=f'{sabores[id].upper()}', values=(f"{massa:.2f}KG"))
    except:
        print('erro calc sabores')
    while y<len(resultado):
        tabela_ingredientes.insert(f"{id}", "end", text=f"{resultado[y]}")
        y+=1
    slide1.set(0)
def calcular_sabores(sabor):
    global sabores,ingredientes_quantidade,ingredientes_nome,resultado,nome_resultado,massa,ingredientes_medida,restante,tipo_porco_frango
    ingredientes_quantidade=[]
    ingredientes_nome=[]
    ingredientes_medida=[]
    massa=float(slide1.get())
    restante = restante - massa
    #--------------------------------#
    try:
        id = tabela_ingredientes.selection()
        id = int(id[0])
        lb_selecionado["text"]=sabores[id].upper()
    #----------------------------------------------------------------------------------------------------
    except:
        print("erro id")
    try:
        massa_anterior = tabela_ingredientes.item(id, 'value')
    except:
        print("primeiro erro")
    try:
        massa_anterior = str(massa_anterior[0])
        len_string = len(massa_anterior)
        len_string = len_string - 2
        massa_anterior=(massa_anterior[0:len_string])
    except:
        print("segundo erro")
    #--------------------------------#
    try:
        massa_anterior=float(massa_anterior)
        massa=massa+massa_anterior
    except:
        print("erro massa anterior")
    if restante<0:
        restante=0
    slide1["to"]=restante
    nome_tabela_sabor="sabores_"+tipo_porco_frango+"_"+ sabor
    operador.__find__(f"{nome_tabela_sabor}","nome",ingredientes_nome)
    operador.__find__(f"{nome_tabela_sabor}","quantidade",ingredientes_quantidade)
    operador.__find__(f"{nome_tabela_sabor}","medida",ingredientes_medida)
    id_quant=len(ingredientes_nome)
    y=0
    while y<id_quant:
        nome_resultado=(f"{ingredientes_nome[y].upper()}----")
        quantidade=ingredientes_quantidade[y]*massa
        quantidade=str(f"{quantidade:.2f}{ingredientes_medida[y]}")
        nome_resultado=nome_resultado+quantidade
        resultado.append(nome_resultado)
        y+=1
def check_porco():
    sons('botao_selecionado')
    bt_calcular["command"]=calculate_porco
    check_frango.deselect()
def check_frango():
    sons('botao_selecionado')
    check_porco.deselect()
    bt_calcular["command"]=calculate_frango
#================================DEF ESTOQUE======================================================#
def sons(nome):
    if nome=="botao":
        winsound.PlaySound('sons/botao.wav', winsound.SND_FILENAME+winsound.SND_ASYNC)
    if nome=="botao_selecionado":
        winsound.PlaySound('sons/click_botao.wav', winsound.SND_FILENAME+winsound.SND_ASYNC)
    if nome=="alerta":
        winsound.PlaySound('sons/alerta.wav', winsound.SND_FILENAME+winsound.SND_ASYNC)
def janela_opaca():
    try:
        global janela_transparente
        janela_transparente=Toplevel()
        janela_transparente.attributes('-alpha', 0.7,)
        janela_transparente.attributes('-fullscreen', True)
        lado, cima = (janela_main.winfo_screenwidth()), (janela_main.winfo_screenheight())
        janela_transparente.geometry(f"{lado}x{cima}")
        janela_transparente.geometry(f"{lado}x{cima}")
        janela_transparente["bg"]="black"
    except:
        print('erro janela opaca')
def bt_linguiça():
    global tabela,nome_tabela,nome_buscar,quantidade_buscar,ultimo_update_buscar,len_id,medida_buscar,preço_buscar,alerta_buscar,alerta_list
    sons("botao")
    cursor.execute("SELECT id FROM linguiça")
    len_id = len(cursor.fetchall())
    bt_linguiça_["bg"]="#CD5C5C"
    bt_utilidade_["bg"]="#87CEFA"
    bt_produtos_["bg"]="#87CEFA"
    bt_ingredientes_["bg"]="#87CEFA"
    bt_fornecedores_["bg"]="#87CEFA"
    nome_buscar=[]
    quantidade_buscar=[]
    ultimo_update_buscar=[]
    medida_buscar=[]
    preço_buscar=[]
    alerta_buscar=[]
    alerta_list=[]
    tabela="linguiça"
    nome_tabela="LINGUIÇAS"
    _buscar_()
def bt_produtos():
    global tabela,nome_tabela,nome_buscar,quantidade_buscar,ultimo_update_buscar,len_id,medida_buscar,preço_buscar,alerta_buscar,alerta_list
    sons("botao")
    cursor.execute("SELECT id FROM produtos")
    len_id = len(cursor.fetchall())
    bt_linguiça_["bg"]="#87CEFA"
    bt_utilidade_["bg"]="#87CEFA"
    bt_produtos_["bg"]="#CD5C5C"
    bt_ingredientes_["bg"]="#87CEFA"
    bt_fornecedores_["bg"] = "#87CEFA"
    nome_buscar=[]
    quantidade_buscar=[]
    ultimo_update_buscar=[]
    medida_buscar = []
    preço_buscar = []
    alerta_buscar=[]
    alerta_list=[]
    tabela="produtos"
    nome_tabela="PRODUTOS"
    _buscar_()
def bt_utilidade():
    global tabela,nome_tabela,nome_buscar,quantidade_buscar,ultimo_update_buscar,len_id,medida_buscar,preço_buscar,alerta_buscar,alerta_list
    sons("botao")
    cursor.execute("SELECT id FROM utilidade")
    len_id = len(cursor.fetchall())
    bt_linguiça_["bg"]="#87CEFA"
    bt_utilidade_["bg"]="#CD5C5C"
    bt_produtos_["bg"]="#87CEFA"
    bt_ingredientes_["bg"]="#87CEFA"
    bt_fornecedores_["bg"] = "#87CEFA"
    nome_buscar=[]
    quantidade_buscar=[]
    ultimo_update_buscar=[]
    medida_buscar = []
    preço_buscar = []
    alerta_buscar=[]
    alerta_list=[]
    tabela="utilidade"
    nome_tabela="PRODUTOS DE UTILIDADE"
    _buscar_()
def bt_ingredientes():
    sons("botao")
    global tabela,nome_tabela,nome_buscar,quantidade_buscar,ultimo_update_buscar,len_id,medida_buscar,preço_buscar,alerta_buscar,alerta_list
    cursor.execute("SELECT id FROM ingredientes")
    len_id = len(cursor.fetchall())
    bt_linguiça_["bg"]="#87CEFA"
    bt_utilidade_["bg"]="#87CEFA"
    bt_produtos_["bg"]="#87CEFA"
    bt_ingredientes_["bg"]="#CD5C5C"
    bt_fornecedores_["bg"] = "#87CEFA"
    nome_buscar=[]
    quantidade_buscar=[]
    ultimo_update_buscar=[]
    medida_buscar = []
    preço_buscar = []
    alerta_buscar=[]
    alerta_list=[]
    tabela="ingredientes"
    nome_tabela="INGREDIENTES"
    _buscar_()
def bt_fornecedores():
    global tabela,nome_tabela,nome_buscar,quantidade_buscar,ultimo_update_buscar,len_id,medida_buscar,preço_buscar,alerta_buscar,alerta_list,fornecedores_buscar,fornecedores_buscar_telefone,fornecedores_buscar_nome
    sons("botao")
    cursor.execute("SELECT id FROM fornecedores")
    len_id = len(cursor.fetchall())
    bt_linguiça_["bg"]="#87CEFA"
    bt_utilidade_["bg"]="#87CEFA"
    bt_produtos_["bg"]="#87CEFA"
    bt_ingredientes_["bg"]="#87CEFA"
    bt_fornecedores_["bg"]="#CD5C5C"
    nome_buscar=[]
    quantidade_buscar=[]
    ultimo_update_buscar=[]
    medida_buscar = []
    preço_buscar = []
    alerta_buscar=[]
    alerta_list=[]
    fornecedores_buscar=[]
    fornecedores_buscar_nome=[]
    fornecedores_buscar_telefone=[]
    tabela="fornecedores"
    select_aviso.delete(0, END)
    _buscar_()
def bt_historico():
    global janela_transparente, janela_estoque
    janela_opaca()
    def close():
        sons('botao')
        global janela_transparente,tabela_estoque_historico
        janela_transparente.destroy()
        tabela_estoque_historico.destroy()
        janela_historico.destroy()
    global tabela,nome_tabela,len_id,nome_buscar_historico,quantidade_buscar_historico,preço_buscar_historico,operaçao_buscar_historico,data_buscar_historico,frame_main_historico,scroll2
    tabela="historico_entrada"
    cursor.execute("SELECT id FROM historico_entrada")
    len_id = len(cursor.fetchall())
    nome_buscar_historico=[]
    quantidade_buscar_historico=[]
    data_buscar_historico_=[]
    preço_buscar_historico= []
    operaçao_buscar_historico=[]
    #=------------------------------------------------------------------------------------------#
    janela_historico = Toplevel()
    janela_historico.geometry("980x600+200+80")
    janela_historico["bg"] = "black"
    janela_historico.title("ZERAR>")
    janela_historico.resizable(width=False, height=False)
    janela_historico.transient()
    janela_historico.focus_force()
    janela_historico.grab_set()
    janela_historico.overrideredirect(True)
    frame_main_historico=Frame(janela_historico,bg="#363636",highlightbackground="grey",highlightthickness=10)
    frame_main_historico.pack()
    scroll2 = Scrollbar(frame_main_historico)
    scroll2.pack(side=LEFT, fill=BOTH)
    _buscar_()
    lb_titulo = Label(frame_main_historico, bg="#363636", text="HISTORICO DE OPERAÇOES", font="impact 17 bold", foreground="green",height=9)
    lb_titulo.pack(side=TOP)
    bt_sair = Button(frame_main_historico, text="x", bg="red", font="Cambria 11 bold", command=close)
    bt_sair.place(x=18, y=1)
    # -------------------------------------------------------------------------------------------------------------------#
def clean_list():
    global tabela_estoque,tabela,tabela_estoque_historico
    if tabela=="historico_entrada":
        global janela_historico,frame_main_historico,scroll2
        # ----------------------------------------------------------------------------------------------------------------------#
        tabela_estoque_historico= ttk.Treeview(frame_main_historico, columns=("QUANTIDADE", "PREÇO", "OPERAÇÃO","DATA"),height=15,selectmode="browse")
        tabela_estoque_historico.pack(side=BOTTOM)
        # ----------------------------------------------------------------------------------------------------------------------#
        tabela_estoque_historico.column('#0', width=200, minwidth=200)
        tabela_estoque_historico.column("QUANTIDADE", width=150, minwidth=150)
        tabela_estoque_historico.column("PREÇO", width=150, minwidth=150)
        tabela_estoque_historico.column("OPERAÇÃO", width=150, minwidth=150)
        tabela_estoque_historico.column("DATA", width=300, minwidth=300)
        tabela_estoque_historico.heading("#0", text="NOME DO ITEN")
        tabela_estoque_historico.heading("QUANTIDADE", text="QUANTIDADE")
        tabela_estoque_historico.heading("PREÇO", text="R$ PREÇO PAGO")
        tabela_estoque_historico.heading("OPERAÇÃO", text="OPERAÇÃO")
        tabela_estoque_historico.heading("DATA", text="DATA")
        style = ttk.Style(janela)
        style.configure("Treeview",font='gothic 17 bold',rowheight=34,background="black",fieldbackground="black", foreground="white")
        # ----------------------------------------------------------------------------------------------------------------------#

        scroll2["command"] = tabela_estoque_historico.yview
        tabela_estoque_historico["yscrollcommand"] = scroll2.set
        tabela_estoque_historico["yscrollcommand"] = scroll2.set
    elif tabela=="fornecedores":
        tabela_estoque.destroy()
        tabela_estoque = ttk.Treeview(frame_tabela, columns=("1"),height=10,selectmode="browse")
        tabela_estoque.pack(side=LEFT)
        # ----------------------------------------------------------------------------------------------------------------------#
        tabela_estoque.column('#0', width=800, minwidth=800)
        tabela_estoque.column("1", width=527, minwidth=527)

        tabela_estoque.heading("#0", text="FORNECEDORES")
        tabela_estoque.heading("1", text="N. TELEFONE")
        style = ttk.Style(frame_tabela)
        style.configure("Treeview",font='gothic 17 bold',rowheight=34,fieldbackground="black")
    else:
        tabela_estoque.destroy()
        tabela_estoque = ttk.Treeview(frame_tabela, columns=("QUANTIDADE", "PREÇO", "DATA"),height=10,selectmode="browse")
        tabela_estoque.pack(side=LEFT)
        # ----------------------------------------------------------------------------------------------------------------------#
        tabela_estoque.column('#0', width=527, minwidth=527)
        tabela_estoque.column("QUANTIDADE", width=200, minwidth=200)
        tabela_estoque.column("PREÇO", width=200, minwidth=200)
        tabela_estoque.column("DATA", width=400, minwidth=400)

        tabela_estoque.heading("#0", text="NOME DO ITEN")
        tabela_estoque.heading("QUANTIDADE", text="QUANTIDADE")
        tabela_estoque.heading("PREÇO", text="R$ PREÇO")
        tabela_estoque.heading("DATA", text="ULTIMO UPDATE")
        style =ttk.Style(janela)
        style.configure("Treeview",font='gothic 17 bold',rowheight=34,background="black",fieldbackground="black", foreground="white")
        select_aviso.delete(0,END)

    # -------------------------------------------------TABELA---------------------------------------------------------------#
def check_alerta():
    global alerta_list,quantidade_buscar
    y=0
    while y<len(alerta_buscar):
        if (alerta_buscar[y]) >= (quantidade_buscar[y]):
            alerta_list.append(nome_buscar[y])
        y+=1
def atualiza_estoque():
    selecionado_estoque()
    lb_selecionado_produçao.after(100,atualiza_estoque)
def selecionado_estoque():
    global nome
    global tabela_estoque,nome_buscar,tabela,id_check
    hora_atual = strftime("%H:%M:%S")
    lb_hora_atual_r["text"]=hora_atual
    try:
        id=tabela_estoque.selection()
        id=int(id[0])-1
        if id_check != id:
            sons("botao_selecionado")
        id_check=id
        bt_adicionar["command"] = janela_adicionar
        bt_remover["command"] = janela_remover
        bt_addnovo["command"] = janela_adicionar_novo
        bt_alterar_nome["command"] = janela_alterar_nome
        bt_zerar["command"] = janela_zerar
        bt_alterar_preço["command"] = janela_alterar_preço

        janela.bind("<KeyPress>", atalhos)
        bt_adicionar['bg']="#4F4F4F"
        bt_remover["bg"]="#4F4F4F"
        bt_addnovo["bg"]="#4F4F4F"
        bt_alterar_nome["bg"]="#4F4F4F"
        bt_zerar["bg"]="#4F4F4F"
        bt_alterar_preço["bg"]="#4F4F4F"

        bt_adicionar["foreground"] = "#FFFFF0"
        bt_remover["foreground"] = "#FFFFF0"
        bt_zerar["foreground"] = "#FFFFF0"
        bt_addnovo["foreground"] = "#FFFFF0"
        bt_alterar_nome["foreground"] = "#FFFFF0"
        bt_alterar_preço["foreground"] = "#FFFFF0"

        lb_atalho_A["bg"]='#4682B4'
        lb_atalho_R["bg"]="#B22222"
        lb_atalho_N["bg"]="orange"
        lb_atalho_D["bg"]="#B8860B"
        lb_atalho_Z["bg"]="#BC8F8F"
        lb_atalho_P["bg"]="#F0E68C"

        if tabela=="historico_entrada":
            bt_zerar["command"]=zerar_tabela_historico
            bt_zerar["foreground"] = "#FFFFF0"
            bt_zerar["bg"] = "#4F4F4F"
            nome = str(nome_buscar_historico[id])

        elif tabela=="fornecedores":
            bt_adicionar["text"] = "ADICIONAR ITEN"
            bt_remover["text"] = "REMOVER ITEN"
            bt_zerar["text"] = "ZERAR ITENS"
            bt_alterar_preço["text"] = "ALTERAR TEL"
            bt_alterar_nome["text"] = "ALTERAR PREÇO"
            nome=str(fornecedores_buscar_nome[id].upper())
            bt_addnovo["command"]=adicionar_novo_fornecedor
            bt_adicionar["command"]=adicionar_iten_fornecedor
            bt_remover["command"]=""
            bt_alterar_nome["command"]=atualizar_preço_fornecedor
            bt_alterar_preço["command"]=janela_alterar_telefone_fornecedor
            bt_zerar["command"]=zerar_iten_fornecedor
            bt_remover["bg"]="#A9A9A9"
            bt_remover["foreground"]="grey"
        else:
            bt_adicionar["text"] = "ADICIONAR"
            bt_remover["text"] = "REMOVER"
            bt_zerar["text"] = "ZERAR"
            bt_alterar_preço["text"] = "ALTERAR PREÇO"
            bt_alterar_nome["text"]="ALTERAR NOME"
            nome = str(nome_buscar[id])
        lb_selecionado["text"] = f"{nome}"
    except:
        janela.bind("<KeyPress>", "")
        lb_selecionado["text"]=""
        bt_adicionar['bg']="#A9A9A9"
        bt_remover["bg"]="#A9A9A9"
        bt_addnovo["bg"]="#A9A9A9"
        bt_alterar_nome["bg"]="#A9A9A9"
        bt_zerar["bg"]="#A9A9A9"
        bt_alterar_preço["bg"]="#A9A9A9"

        bt_adicionar["foreground"] = "grey"
        bt_remover["foreground"] = "grey"
        bt_zerar["foreground"] = "grey"
        bt_addnovo["foreground"] = "grey"
        bt_alterar_nome["foreground"] = "grey"
        bt_alterar_preço["foreground"] = "grey"


        lb_atalho_A["bg"]="grey"
        lb_atalho_R["bg"]="grey"
        lb_atalho_N["bg"]="grey"
        lb_atalho_D["bg"]="grey"
        lb_atalho_Z["bg"]="grey"
        lb_atalho_P["bg"]="grey"

        bt_adicionar["command"] = ""
        bt_remover["command"] = ""
        bt_addnovo["command"] = ""
        bt_alterar_nome["command"] = ""
        bt_zerar["command"] = ""
        bt_alterar_preço["command"] = ""
def animaçao_credito():
    global text,text_animação,c
    try:
        text_animação=text_animação+text[c]
        lb_credito["text"] = text_animação
        c+=1
        if c==3:
            lb_credito["font"]='italic 6 bold underline'
        if c==6:
            lb_credito["font"]='italic 7 bold underline'
        if c==9:
            lb_credito["font"]='italic 8 bold underline'
        if c==10:
            lb_credito["font"]='italic 9 bold underline'
        if c == 12:
            lb_credito["font"] = 'italic 10 bold underline'
    except:
        text_animação=""
        c=0
        lb_credito["text"] = text_animação
def atualiza2():
    animaçao_credito()
    lb_credito.after(30,atualiza2)
#-------------------------------------------------------------------------------------------------------------------#
def buscar_fornecedores_telefone():
    global fornecedores_buscar_telefone, len_id,tabela
    cursor.execute("SELECT id FROM fornecedores")
    len_id = len(cursor.fetchall())
    tabela="fornecedores"
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT telefone FROM {tabela} WHERE id={y}")
        fornecedores_buscar_telefone.append(cursor.fetchone()[0])
        y += 1
def buscar_fornecedores_nome():
    global fornecedores_buscar_nome, len_id,tabela
    cursor.execute("SELECT id FROM fornecedores")
    len_id = len(cursor.fetchall())
    tabela="fornecedores"
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT nome FROM {tabela} WHERE id={y}")
        fornecedores_buscar_nome.append(cursor.fetchone()[0])
        y += 1
def buscar_aviso():
    global alerta_buscar, len_id,tabela
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT alerta FROM {tabela} WHERE id={y}")
        alerta_buscar.append(cursor.fetchone()[0])
        y += 1
def buscar_preço():
    global preço_buscar, len_id,tabela
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT preço FROM {tabela} WHERE id={y}")
        try:
            preço=(cursor.fetchone()[0])
            preço=float(preço)
            preço_buscar.append(preço)
        except:
            preço_buscar.append(0)
        y += 1
def buscar_medida():
    global medida_buscar, len_id,tabela
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT medida FROM {tabela} WHERE id={y}")
        medida_buscar.append(cursor.fetchone()[0])
        y += 1
def buscar_ultimo_update():
    global tabela,ultimo_update_buscar
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT data FROM {tabela} WHERE id={y}")
        ultimo_update_buscar.append(cursor.fetchone()[0])
        y += 1
def buscar_quantidade():
    global tabela,quantidade_buscar
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT quantidade FROM {tabela} WHERE id={y} ")
        add=cursor.fetchone()[0]
        if add < 0:
            quantidade_buscar.append(0)
        else:
            quantidade_buscar.append(add)
        y += 1
def buscar_nome():
    global tabela
    global nome_buscar,len_id
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT nome FROM {tabela} WHERE id={y}")
        nome_buscar.append(cursor.fetchone()[0])
        y += 1
def buscar_nome_check():
    global tabela2
    global nome_buscar_check,len_id
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT nome FROM {tabela2} WHERE id={y}")
        nome_buscar_check.append(cursor.fetchone()[0])
        y += 1
def buscar_nome_historico():
    global tabela
    global nome_buscar_historico,len_id
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT nome FROM {tabela} WHERE id={y}")
        nome_buscar_historico.append(cursor.fetchone()[0])
        y += 1
def buscar_quantidade_historico():
    global tabela
    global quantidade_buscar_historico,len_id
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT quantidade FROM {tabela} WHERE id={y}")
        quantidade_buscar_historico.append(cursor.fetchone()[0])
        y +=1
def buscar_preço_historico():
    global tabela
    global preço_buscar_historico,len_id
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT preço FROM {tabela} WHERE id={y}")
        preço_buscar_historico.append(cursor.fetchone()[0])
        y +=1
def buscar_operação_historico():
    global tabela
    global operaçao_buscar_historico,len_id
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT operaçao FROM {tabela} WHERE id={y}")
        operaçao_buscar_historico.append(cursor.fetchone()[0])
        y +=1
def buscar_data_historico():
    global tabela
    global data_buscar_historico,len_id
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT data FROM {tabela} WHERE id={y}")
        data_buscar_historico.append(cursor.fetchone()[0])
        y +=1
def buscar_medida_historico():
    global tabela
    global medida_buscar_historico,len_id
    y = 1
    while y <= len_id:
        cursor.execute(f"SELECT medida FROM {tabela} WHERE id={y}")
        medida_buscar_historico.append(cursor.fetchone()[0])
        y +=1
def _buscar_():
    global x,tabela,nome_tabela,tabela_estoque,tabela_estoque_historico
    x=0
    y=1
    clean_list()
    if tabela=="historico_entrada":
        buscar_nome_historico()
        buscar_quantidade_historico()
        buscar_preço_historico()
        buscar_operação_historico()
        buscar_data_historico()
        x=0
        while x < len_id:
            tabela_estoque_historico.insert("", "end",text=f'{nome_buscar_historico[x]}', values=(f"{quantidade_buscar_historico[x]}", f'R${preço_buscar_historico[x]:.2f}', f'{operaçao_buscar_historico[x]}',f'{data_buscar_historico[x]}'))
            x=x+1
    elif tabela == "fornecedores":
        buscar_fornecedores_nome()
        buscar_fornecedores_telefone()
        x=0
        while x < len_id:
            tabela_estoque.insert("", "end",iid=y, text=f'{fornecedores_buscar_nome[x].upper()}',values=(f"{fornecedores_buscar_telefone[x]}"))
            fornecedor = "fornecedor_" + fornecedores_buscar_nome[x]
            fornecedor = str(fornecedor)
            cursor.execute(f"SELECT id FROM {fornecedor}")
            id = len(cursor.fetchall())
            a=1
            b=0
            while b<id:
                try:
                    cursor.execute(f"SELECT nome_iten FROM {fornecedor} WHERE id={a}")
                    nome=(cursor.fetchone()[0])
                    nome=nome.upper()
                except:
                    nome="sn"
                try:
                    cursor.execute(f"SELECT preço FROM {fornecedor} WHERE id={a}")
                    preço=float(cursor.fetchone()[0])
                except:
                    preço=00.00
                try:
                    cursor.execute(f"SELECT data FROM {fornecedor} WHERE id={a}")
                    data=(cursor.fetchone()[0])
                except:
                    data="sd"
                tabela_estoque.insert(f"{y}", "end", text=f"{nome}----R${preço:.2f}----{data}")
                a+=1
                b+=1

            y+=1
            x+=1
    else:
        buscar_nome()
        buscar_quantidade()
        buscar_ultimo_update()
        buscar_medida()
        buscar_preço()
        buscar_aviso()
        check_alerta()
        clean_list()
        while x < len_id:
            tabela_estoque.insert("", "end",iid=y, text=f'{nome_buscar[x]}', values=(f"{quantidade_buscar[x]:.2f}-{medida_buscar[x]}", f'R${preço_buscar[x]:.2f}', f"{ultimo_update_buscar[x]}"))
            a=0
            while a<len(fornecedores_buscar_nome):
                fornecedor = "fornecedor_" + fornecedores_buscar_nome[a]
                fornecedor = str(fornecedor)
                try:
                    cursor.execute(f"SELECT nome_iten FROM {fornecedor} WHERE nome_iten='{nome_buscar[x].lower()}'")
                    nome=cursor.fetchone()[0]
                    cursor.execute(f"SELECT preço FROM {fornecedor} WHERE nome_iten='{nome_buscar[x].lower()}'")
                    preço = cursor.fetchone()[0]
                    cursor.execute(f"SELECT data FROM {fornecedor} WHERE nome_iten='{nome_buscar[x].lower()}'")
                    data = cursor.fetchone()[0]
                    tabela_estoque.insert(f"{y}", "end", text=f"{fornecedores_buscar_nome[a].upper()}----R${preço:.2f}/{medida_buscar[x]}----{data}")
                except:
                    None
                a+=1
            y+=1
            x+=1
        # ----------------------------------------------------------------------------------------#
        x=0
        select_aviso.insert(END, "ITENS COM BAIXO VOLUME")
        while x<len(alerta_list):
            select_aviso.insert(END,f"   {alerta_list[x]}")
            x+=1
    scroll["command"] = tabela_estoque.yview
    tabela_estoque["yscrollcommand"] = scroll.set
    tabela_estoque["yscrollcommand"] = scroll.set

    scroll_aviso["command"] = select_aviso.yview
    select_aviso["yscrollcommand"] = scroll_aviso.set
    select_aviso["yscrollcommand"] = scroll_aviso.set
    atualiza_estoque()
def buscar_historico_tabela():
    global x,tabela,nome_tabela
    buscar_nome_historico()
    buscar_quantidade_historico()
    buscar_preço_historico()
    buscar_operação_historico()
    buscar_data_historico()
    x = 0
    while x < len_id:
        tabela_estoque.insert("", "end", text=f'{nome_buscar_historico[x]}', values=(
        f"{quantidade_buscar_historico[x]}", f'R${preço_buscar_historico[x]:.2f}', f'{operaçao_buscar_historico[x]}',
        f'{data_buscar_historico[x]}'))
        x = x + 1
#-------------------------------------------------------------------------------------------------------------------#
def janela_remover():
    global id
    sons("botao")
    id = tabela_estoque.selection()
    id = int(id[0])
    janela_opaca()
    def close():
        sons('botao')
        global janela_transparente
        janela_remover.destroy()
        janela_transparente.destroy()
    def remover_quantidade():
        hora_atual = strftime("%H:%M:%S")
        data_atual = date.today()
        data_em_texto = data_atual.strftime("%d/%m/%Y")
        global tabela,len_id,medida_buscar
        # ----------------------------------------------------------------------------------------#
        try:
            cursor.execute(f"SELECT quantidade FROM {tabela} WHERE id={id} ")
            quantidade_atual = float(cursor.fetchone()[0])
            quantidade_adicionar = float(ed_quantidades_iten.get())
            quantidade_atualizada = quantidade_atual - quantidade_adicionar
            preço=0
            if quantidade_atualizada < 0:
                quantidade_atualizada = 0
            # ----------------------------------------------------------------------------------------#
            cursor.execute(f"UPDATE {tabela} SET quantidade = {quantidade_atualizada} WHERE id ={id}")
            cursor.execute(f"UPDATE {tabela} SET data = '{str(data_em_texto)}--{str(hora_atual)}' WHERE id ={id}")
            connect.commit()
            # ----------------------------------------------------------------------------------------#
            quantidade_adicionar_salvar=f"{quantidade_adicionar:.2f}"
            quantidade_adicionar_salvar=str(quantidade_adicionar_salvar)
            cursor.execute(
                f"INSERT INTO historico_entrada (nome,quantidade,preço,data,operaçao) VALUES ('{nome_buscar[(id - 1)]}','{quantidade_adicionar_salvar}-{medida_buscar[(id - 1)]}',{preço},'{str(data_em_texto)}--{str(hora_atual)}','REMOVER')")
            connect.commit()
            # ----------------------------------------------------------------------------------------#
            janela_remover.destroy()
        except:
            lb_erro.place(x=50, y=126)

        # ----------------------------------------------------------------------------------------#
        if tabela=="linguiça":
            bt_linguiça()
        if tabela=="produtos":
            bt_produtos()
        if tabela=="utilidade":
            bt_utilidade()
        if tabela=="ingredientes":
            bt_ingredientes()
    try:
        janela_remover=Toplevel()
        janela_remover.geometry("255x175+560+200")
        janela_remover["bg"]="black"
        janela_remover.title("REMOVER>")
        janela_remover.resizable(width=False, height=False)
        janela_remover.transient()
        janela_remover.focus_force()
        janela_remover.grab_set()
        janela_remover.overrideredirect(True)

        #---------------------------------------------------------------FRAME - ------------------------------------------------
        frame_main=Frame(janela_remover,width=250,height=170, bg="#363636",highlightbackground="grey",highlightthickness=10)
        frame_main.place(x=3,y=2)
        #---------------------------------------------------------------LABEL-------------------------------------------------#
        lb_titulo = Label(frame_main, bg="#363636", text="REMOVER", font="impact 17 bold", foreground="green")
        lb_titulo.place(x=75, y=6)
        lb_iten = Label(frame_main, bg="#363636", text=f"{nome}",font="Cambria 12 bold", foreground="white")
        lb_iten.place(x=8, y=40)
        lb_quantidade_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="QUANTIDADE:")
        lb_quantidade_iten.place(x=8, y=70)
        lb_quantidade_iten_kg = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="KG/UNID")
        lb_quantidade_iten_kg.place(x=163, y=70)
        lb_erro = Label(frame_main, bg="#363636", foreground="red", font='gothic 10 bold', text="Valores inválidos.")
        #---------------------------------------------------------------LABEL-------------------------------------------------#
        #------------------------------------------------------------ENTRY----------------------------------------------------#
        ed_quantidades_iten = Entry(frame_main, width=8)
        ed_quantidades_iten.place(x=110, y=70)
        #------------------------------------------------------------ENTRY----------------------------------------------------#
        #-------------------------------------------------BOTOES--------------------------------------------#
        bt_salvar = Button(frame_main,text="REMOVER",bg="blue",font="Cambria 12 bold", command=remover_quantidade)
        bt_salvar.place(x=70, y=95)
        bt_sair = Button(frame_main, text="x", bg="red", font="Cambria 12 bold", command=close)
        bt_sair.place(x=2, y=2)
        #-------------------------------------------------BOTOES--------------------------------------------#
    except:
        None
def janela_adicionar():
    global nome,janela_transparente
    sons("botao")
    janela_opaca()
    def close():
        sons('botao')
        janela_adicionar.destroy()
        janela_transparente.destroy()
    def adicionar_quantidade():
        global tabela,len_id,nome_item
        hora_atual = strftime("%H:%M:%S")
        data_atual = date.today()
        data_em_texto = data_atual.strftime("%d/%m/%Y")
        # ----------------------------------------------------------------------------------------#
        id=tabela_estoque.selection()
        id=int(id[0])
        try:
            quantidade_adicionar = float(ed_quantidade_iten.get())
            preço = float(ed_preço_pago_iten.get())
        except:
            lb_erro.place(x=55, y=152)
        cursor.execute(f"SELECT quantidade FROM {tabela} WHERE id={id} ")
        quantidade_atual = float(cursor.fetchone()[0])
        quantidade_atualizada = quantidade_atual + quantidade_adicionar
        if quantidade_atualizada<0:
            quantidade_atualizada=0
        # ----------------------------------------------------------------------------------------#
        cursor.execute(f"UPDATE {tabela} SET quantidade = {quantidade_atualizada} WHERE id ={id}")
        cursor.execute(f"UPDATE {tabela} SET data = '{str(data_em_texto)}--{str(hora_atual)}' WHERE id ={id}")
        connect.commit()
        # ----------------------------------------------------------------------------------------#
        quantidade_adicionar_salvar = f"{quantidade_adicionar:.2f}"
        quantidade_adicionar_salvar = str(quantidade_adicionar_salvar)
        cursor.execute(
                f"INSERT INTO historico_entrada (nome,quantidade,preço,data,operaçao) VALUES ('{nome_buscar[(id - 1)]}','{quantidade_adicionar_salvar}-{medida_buscar[(id - 1)]}',{preço},'{str(data_em_texto)}--{str(hora_atual)}','ADICIONAR')")
        connect.commit()

        # ----------------------------------------------------------------------------------------#
        if tabela=="linguiça":
            bt_linguiça()
        if tabela=="produtos":
            bt_produtos()
        if tabela=="utilidade":
            bt_utilidade()
        if tabela=="ingredientes":
            bt_ingredientes()
        janela_adicionar.destroy()
        # ----------------------------------------------------------------------------------------#
    try:
        janela_adicionar=Toplevel()
        janela_adicionar.geometry("270x200+560+200")
        janela_adicionar["bg"]="black"
        janela_adicionar.title("ADICIONAR>")
        janela_adicionar.resizable(width=False, height=False)
        janela_adicionar.transient()
        janela_adicionar.focus_force()
        janela_adicionar.grab_set()
        janela_adicionar.overrideredirect(True)
        #---------------------------------------------------------------FRAME - ------------------------------------------------
        frame_main=Frame(janela_adicionar,height=192,width=264, bg="#363636",highlightbackground="grey",highlightthickness=10)
        frame_main.place(x=3,y=3)
        #---------------------------------------------------------------LABEL-------------------------------------------------#
        lb_titulo = Label(frame_main, bg="#363636", text="ADICIONAR", font="impact 17 bold", foreground="green")
        lb_titulo.place(x=70, y=3)
        lb_iten = Label(frame_main, bg="#363636", text=f"{nome}",font="Cambria 12 bold", foreground="white")
        lb_iten.place(x=8, y=40)
        lb_quantidade_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="*QUANTIDADE:")
        lb_quantidade_iten.place(x=8, y=70)
        lb_quantidade_iten_kg = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="KG / UNID")
        lb_quantidade_iten_kg.place(x=165, y=70)
        lb_preço_pago = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold',text="*PREÇO PAGO")
        lb_preço_pago.place(x=8, y=94)
        lb_preço_pago_rs = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold',text="R$")
        lb_preço_pago_rs.place(x=165, y=94)
        lb_erro = Label(frame_main, bg="#363636", foreground="red", font='gothic 10 bold', text="Valores inválidos.")
        #---------------------------------------------------------------LABEL-------------------------------------------------#
        #------------------------------------------------------------ENTRY----------------------------------------------------#
        ed_quantidade_iten = Entry(frame_main, width=8)
        ed_quantidade_iten.place(x=110, y=70)
        ed_preço_pago_iten = Entry(frame_main, width=8)
        ed_preço_pago_iten.place(x=110, y=94)
        #------------------------------------------------------------ENTRY----------------------------------------------------#
        #-------------------------------------------------BOTOES--------------------------------------------#
        bt_salvar = Button(frame_main, text="CONFIRMAR",bg="blue",font="Cambria 12 bold",command=adicionar_quantidade)
        bt_salvar.place(x=75, y=122)
        bt_sair = Button(frame_main, text="x", bg="red", font="Cambria 12 bold", command=close)
        bt_sair.place(x=2, y=2)
        #-------------------------------------------------BOTOES--------------------------------------------#
    except:
        None
def janela_adicionar_novo():
    sons("botao")
    janela_opaca()
    def close():
        sons('botao')
        janela_adicionar_novo.destroy()
        janela_transparente.destroy()
    def check_unid():
        global medida
        medida="UNID"
        check1.deselect()
    def check_kg():
        global medida
        medida="KG"
        check2.deselect()
    def chave():
        global medida
        def verificar():

            try:
                chave=str(ed_chave.get())
            except:
                None
            if chave=="35332460":
                adicionar_ingredientes()
                janela_chave.destroy()
                janela_adicionar_novo.destroy()

            else:
                janela_transparente.destroy()
                janela_chave.destroy()
                janela_adicionar_novo.destroy()
                janela_transparente.destroy()
        try:
            nome = str(ed_nome_iten.get())
            #-----------------------------------------------------------#
            if float(ed_quantidade_iten.get()) < 0:
                quantidade=0
            else:
                quantidade=float(ed_quantidade_iten.get())
                #-----------------------------------------------------------#
            if float(ed_alerta_iten.get()) < 0:
                alerta=0
            else:
                alerta=float(ed_alerta_iten.get())
                #-----------------------------------------------------------#
            if float(ed_preço_iten.get()) < 0:
                preço=0
            else:
                preço=float(ed_preço_iten.get())
                #-----------------------------------------------------------#
            janela_chave =Toplevel()
            janela_chave.geometry("212x122+580+260")
            janela_chave["bg"] = "black"
            janela_chave.title("ADICIONAR NOVO>")
            janela_chave.resizable(width=False, height=False)
            janela_chave.transient()
            janela_chave.focus_force()
            janela_chave.grab_set()
            janela_chave.overrideredirect(True)
            # -----------------------------------------------------------#
            frame_login_main = Frame(janela_chave, width=200, height=300, bg="#363636",highlightbackground="grey",highlightthickness=10)
            frame_login_main.pack(side=TOP)
            frame_login=Frame(frame_login_main,width=200,height=300,bg="#363636",highlightbackground="grey",highlightthickness=2)
            frame_login.pack(side=BOTTOM)
            # -----------------------------------------------------------#
            lb_titulo = Label(frame_login_main, bg="black", text="ACESSO RESTRITO", font="impact 17 bold", foreground="red")
            lb_titulo.pack(side=TOP)
            lb_chave = Label(frame_login, bg="black", foreground="blue", font='gothic 12 bold', text="CHAVE DE ACESSO:")
            lb_chave.pack(side=TOP)
            # -----------------------------------------------------------#
            ed_chave = Entry(frame_login, width=10,bg="red",foreground="blue",show="*")
            ed_chave.pack(side=TOP)
            # -----------------------------------------------------------#
            bt_salvar = Button(frame_login, text="CONFIRMAR", bg="blue", font="Cambria 12 bold",command=verificar)
            bt_salvar.pack(side=BOTTOM)
            # -----------------------------------------------------------#
        except:
            lb_erro.place(x=110, y=190)
    def adicionar_ingredientes():
        global len_id,tabela,medida,hora_atual
        try:
            nome = str(ed_nome_iten.get())
            #-----------------------------------------------------------#
            if float(ed_quantidade_iten.get()) < 0:
                quantidade=0
            else:
                quantidade=float(ed_quantidade_iten.get())
            #-----------------------------------------------------------#
            if float(ed_alerta_iten.get()) < 0:
                alerta=0
            else:
                alerta=float(ed_alerta_iten.get())
            #-----------------------------------------------------------#
            if float(ed_preço_iten.get()) < 0:
                preço=0

            else:
                preço=float(ed_preço_iten.get())
            medida = medida
        except:
            lb_erro.place(x=110, y=190)
        hora_atual=strftime("%H:%M:%S")
        cursor.execute(
            f"INSERT INTO {tabela} (nome,quantidade,data,alerta,medida,preço) VALUES ('{nome.upper()}','{quantidade}','{str(data_em_texto)}--{str(hora_atual)}','{alerta}','{medida.upper()}',{preço})")
        connect.commit()
        if tabela=="linguiça":
            bt_linguiça()
        if tabela=="produtos":
            bt_produtos()
        if tabela=="utilidade":
            bt_utilidade()
        if tabela=="ingredientes":
            bt_ingredientes()
        janela_adicionar_novo.destroy()
    janela_adicionar_novo=Toplevel()
    janela_adicionar_novo.geometry("380x252+500+200")
    janela_adicionar_novo["bg"]="black"
    janela_adicionar_novo.title("ADICIONAR NOVO>")
    janela_adicionar_novo.resizable(width=False, height=False)
    janela_adicionar_novo.transient()
    janela_adicionar_novo.focus_force()
    janela_adicionar_novo.grab_set()
    janela_adicionar_novo.overrideredirect(True)
        #-------------------------------------------------FRAME--------------------------------------------#
    frame_main=Frame(janela_adicionar_novo,highlightbackground="GREY",highlightthickness=12,height=240,width=370,bg="#363636")
    frame_main.place(x=5,y=4)
        #-------------------------------------------------FRAME--------------------------------------------#
        #-------------------------------------------------LABEL--------------------------------------------#
    lb_titulo = Label(frame_main, bg="#363636", text="ADICIONAR NOVO", font="impact 17 bold", foreground="green")
    lb_titulo.place(x=90, y=3)
    lb_nome_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="NOME DO ITEN:")
    lb_nome_iten.place(x=10, y=50)
    ed_nome_iten = Entry(frame_main, width=29)
    ed_nome_iten.place(x=150, y=50)
    lb_quantidade_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="QUANTIDADE:")
    lb_quantidade_iten.place(x=10, y=75)
    ed_quantidade_iten = Entry(frame_main, width=9)
    ed_quantidade_iten.place(x=150, y=75)
    lb_preço_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="PREÇO:")
    lb_preço_iten.place(x=10, y=100)
    ed_preço_iten = Entry(frame_main, width=9)
    ed_preço_iten.place(x=150, y=100)
    lb_rs = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="R$")
    lb_rs.place(x=210, y=102)
    lb_alerta = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="QNT. ALERTAR:")
    lb_alerta.place(x=10, y=125)
    ed_alerta_iten = Entry(frame_main, width=9)
    ed_alerta_iten.place(x=150, y=125)
    lb_ce = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="❗")
    lb_ce.place(x=210, y=125)
    lb_erro = Label(frame_main, bg="#363636", foreground="red", font='gothic 10 bold', text="Valores inválidos.")
        #-------------------------------------------------LABEL--------------------------------------------#
    bt_salvar = Button(frame_main, bg="blue",command=chave,text="SALVAR",font="Cambria 12 bold")
    bt_salvar.place(x=140, y=160)
    bt_sair = Button(frame_main, text="x", bg="red", font="Cambria 12 bold", command=close)
    bt_sair.place(x=2, y=2)
    #-------------------------------------------------BOTOES--------------------------------------------#
    #-------------------------------------------------CHECKBOX--------------------------------------------#
    check1=Checkbutton(frame_main,text="KG",bg="#363636",foreground="blue",font="bold 12",onvalue=1, offvalue=0,command=check_kg)
    check1.place(x=210,y=72)
    check2 = Checkbutton(frame_main, text="UNID", bg="#363636", foreground="blue", font="bold 12", onvalue=1,offvalue=0,command=check_unid)
    check2.place(x=265, y=72)
     #-------------------------------------------------CHECKBOX--------------------------------------------#
def janela_zerar():
    sons("alerta")
    janela_opaca()
    def bt_confirmar():
        global tabela,janela_transparente
        hora_atual = strftime("%H:%M:%S")
        data_atual = date.today()
        data_em_texto = data_atual.strftime("%d/%m/%Y")
        id=tabela_estoque.selection()
        id=int(id[0])
        quantidade_adicionar=0
        preço=0
        #---------------------------------------------------------------------------------------------------------#
        cursor.execute(f"UPDATE {tabela} SET quantidade = 0 WHERE id ={id}")
        cursor.execute(f"UPDATE {tabela} SET data = '{str(data_em_texto)}--{str(hora_atual)}' WHERE id ={id}")
        #---------------------------------------------------------------------------------------------------------#

        cursor.execute(
            f"INSERT INTO historico_entrada (nome,quantidade,preço,data,operaçao) VALUES ('{nome_buscar[(id - 1)]}',{quantidade_adicionar},{preço},'{str(data_em_texto)}--{str(hora_atual)}','ZERAR')")
        #---------------------------------------------------------------------------------------------------------#
        connect.commit()
        if tabela=="linguiça":
            bt_linguiça()
        if tabela=="produtos":
            bt_produtos()
        if tabela=="utilidade":
            bt_utilidade()
        if tabela=="ingredientes":
            bt_ingredientes()
        janela_zerar.destroy()
        janela_transparente.destroy()
    def bt_cancelar():
        global  janela_transparente
        janela_zerar.destroy()
        janela_transparente.destroy()
    try:
        janela_zerar=Toplevel()
        janela_zerar.geometry("184x110+590+240")
        janela_zerar["bg"]="black"
        janela_zerar.title("ZERAR>")
        janela_zerar.resizable(width=False, height=False)
        janela_zerar.transient()
        janela_zerar.focus_force()
        janela_zerar.grab_set()
        janela_zerar.overrideredirect(True)
        #----------------------------------------------FRAME - -------------------------------------------
        frame_main=Frame(janela_zerar, bg="#363636",highlightbackground="grey",highlightthickness=10)
        frame_main.place(x=2,y=2)
        #----------------------------------------------FRAME - -------------------------------------------
        #---------------------------------------------LABEL--------------------------------------------#
        lb_titulo = Label(frame_main, bg="#363636", text="ZERAR ITEN", font="impact 17 bold", foreground="green")
        lb_titulo.pack(side=TOP)
        lb_iten = Label(frame_main, bg="#363636", text=f"{nome}",font="Cambria 12 bold", foreground="white")
        lb_iten.pack(side=TOP)
        #---------------------------------------------LABEL--------------------------------------------#
        #----------------------------------------------BOTOES--------------------------------------------#
        bt_sim = Button(frame_main, text="CONFIRMAR", bg="blue", font="Cambria 10 bold", command=bt_confirmar)
        bt_sim.pack(side=LEFT)
        bt_nao = Button(frame_main, text="CANCELAR", bg="blue", font="Cambria 10 bold", command=bt_cancelar)
        bt_nao.pack(side=RIGHT)
        #----------------------------------------------BOTOES--------------------------------------------#
    except:
        None
def janela_alterar_nome():
    sons("botao")
    janela_opaca()
    def close():
        sons('botao')
        global janela_transparente
        janela_alterar_nome.destroy()
        janela_transparente.destroy()
    def alterar_nome():
        hora_atual = strftime("%H:%M:%S")
        data_atual = date.today()
        data_em_texto = data_atual.strftime("%d/%m/%Y")
        global tabela,len_id
        #--------------------------------------------------------------------------------------------------------#
        id=tabela_estoque.selection()
        id=id[0]
        novo_nome=str(ed_quantidades_iten.get())
        #--------------------------------------------------------------------------------------------------------#
        if novo_nome == "":
            janela_alterar_nome.destroy()
        else:
            cursor.execute(f"UPDATE {tabela} SET nome = '{novo_nome.upper()}' WHERE id ={id}")
            cursor.execute(f"UPDATE {tabela} SET data = '{str(data_em_texto)}--{str(hora_atual)}' WHERE id ={id}")
            connect.commit()

        #--------------------------------------------------------------------------------------------------------#
        if tabela=="linguiça":
            bt_linguiça()
        if tabela=="produtos":
            bt_produtos()
        if tabela=="utilidade":
            bt_utilidade()
        if tabela=="ingredientes":
            bt_ingredientes()
        janela_alterar_nome.destroy()
    try:
        janela_alterar_nome=Toplevel()
        janela_alterar_nome.geometry("240x150+560+210")
        janela_alterar_nome["bg"]="black"
        janela_alterar_nome.title("REMOVER>")
        janela_alterar_nome.resizable(width=False, height=False)
        janela_alterar_nome.transient()
        janela_alterar_nome.focus_force()
        janela_alterar_nome.grab_set()
        janela_alterar_nome.overrideredirect(True)
        #---------------------------------------------------------------FRAME-------------------------------------------------#
        frame_main=Frame(janela_alterar_nome,width=236,height=145,highlightbackground="GREY",highlightthickness=10,bg="#363636")
        frame_main.place(x=2,y=2)
        #---------------------------------------------------------------FRAME-------------------------------------------------#
        #---------------------------------------------------------------LABEL-------------------------------------------------#
        lb_titulo = Label(frame_main, bg="#363636", text="ALTERAR NOME", font="impact 17 bold", foreground="green")
        lb_titulo.place(x=50, y=3)
        lb_iten = Label(frame_main, bg="#363636", text=f"{nome}",font="Cambria 12 bold", foreground="white")
        lb_iten.place(x=8,y=38)
        lb_quantidade_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="NOVO NOME:")
        lb_quantidade_iten.place(x=8, y=65)
        #---------------------------------------------------------------LABEL-------------------------------------------------#
        #------------------------------------------------------------ENTRY----------------------------------------------------#
        ed_quantidades_iten = Entry(frame_main, width=14)
        ed_quantidades_iten.place(x=105, y=65)
        #------------------------------------------------------------ENTRY----------------------------------------------------#
        #-------------------------------------------------BOTOES--------------------------------------------#
        bt_salvar = Button(frame_main, text="CONFIRMAR", bg="blue", font="Cambria 12 bold", command=alterar_nome)
        bt_salvar.place(x=60, y=90)
        bt_sair = Button(frame_main, text="x", bg="red", font="Cambria 12 bold", command=close)
        bt_sair.place(x=2, y=2)
        #-------------------------------------------------BOTOES--------------------------------------------#
    except:
        None
def janela_alterar_preço():
    sons("botao")
    janela_opaca()
    def close():
        sons('botao')
        global janela_transparente
        janela_alterar_preço.destroy()
        janela_transparente.destroy()
    def alterar_preço():
        hora_atual = strftime("%H:%M:%S")
        data_atual = date.today()
        data_em_texto = data_atual.strftime("%d/%m/%Y")
        global tabela, len_id,janela_transparente
        # --------------------------------------------------------------------------------------------------------#
        id = tabela_estoque.selection()
        id = id[0]
        try:
            novo_preço = float(ed_quantidades_iten.get())
            # --------------------------------------------------------------------------------------------------------#
            cursor.execute(f"UPDATE {tabela} SET preço = '{novo_preço}' WHERE id ={id}")
            cursor.execute(f"UPDATE {tabela} SET data = '{str(data_em_texto)}--{str(hora_atual)}' WHERE id ={id}")
            connect.commit()
            janela_alterar_preço.destroy()
            janela_transparente.destroy()
        except:
            janela_alterar_preço.destroy()
            janela_transparente.destroy()
        # --------------------------------------------------------------------------------------------------------#
        if tabela == "linguiça":
            bt_linguiça()
        if tabela == "produtos":
            bt_produtos()
        if tabela == "utilidade":
            bt_utilidade()
        if tabela == "ingredientes":
            bt_ingredientes()
    try:
        janela_alterar_preço=Toplevel()
        janela_alterar_preço.geometry("240x150+580+210")
        janela_alterar_preço["bg"]="black"
        janela_alterar_preço.title("ALTERAR PREÇO>")
        janela_alterar_preço.resizable(width=False, height=False)
        janela_alterar_preço.transient()
        janela_alterar_preço.focus_force()
        janela_alterar_preço.grab_set()
        janela_alterar_preço.overrideredirect(True)

        #---------------------------------------------------------------FRAME-------------------------------------------------#
        frame_main=Frame(janela_alterar_preço,width=236,height=145,highlightbackground="GREY",highlightthickness=10,bg="#363636")
        frame_main.place(x=2,y=2)
        #---------------------------------------------------------------FRAME-------------------------------------------------#
        #---------------------------------------------------------------LABEL-------------------------------------------------#
        lb_titulo = Label(frame_main, bg="#363636", text="ALTERAR PREÇO", font="impact 17 bold", foreground="green")
        lb_titulo.place(x=50, y=3)
        lb_iten = Label(frame_main, bg="#363636", text=f"{nome}",font="Cambria 12 bold", foreground="white")
        lb_iten.place(x=8,y=34)
        lb_quantidade_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="NOVO PREÇO:")
        lb_quantidade_iten.place(x=8, y=58)
        lb_rs = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="R$")
        lb_rs.place(x=173, y=58)
        #---------------------------------------------------------------LABEL-------------------------------------------------#
        #------------------------------------------------------------ENTRY----------------------------------------------------#
        ed_quantidades_iten = Entry(frame_main, width=10)
        ed_quantidades_iten.place(x=105, y=58)
        #------------------------------------------------------------ENTRY----------------------------------------------------#
        #-------------------------------------------------BOTOES--------------------------------------------#
        bt_salvar = Button(frame_main, text="CONFIRMAR", bg="blue", font="Cambria 12 bold",command=alterar_preço)
        bt_salvar.place(x=60, y=87)
        bt_sair = Button(frame_main, text="x", bg="red", font="Cambria 12 bold", command=close)
        bt_sair.place(x=2, y=2)
        #-------------------------------------------------BOTOES--------------------------------------------#
    except:
        None
def atalhos(event):
    if tabela=="fornecedores":
        if tabela == "fornecedores":
            if (event.char) == "a" or event.char == "A":
                adicionar_iten_fornecedor()
            if (event.char) == "z" or event.char == "Z":
                zerar_iten_fornecedor()
            if (event.char) == "n" or event.char == "N":
                adicionar_novo_fornecedor()
            if (event.char) == "p" or event.char == "P":
                atualizar_preço_fornecedor()
            if (event.char) == "t" or event.char == "T":
                janela_alterar_telefone_fornecedor()
    else:
        if (event.char)=="a" or event.char=="A":
            janela_adicionar()
        if (event.char)=="r" or event.char=="R":
            janela_remover()
        if (event.char)=="z" or event.char=="Z":
            janela_zerar()
        if (event.char)=="n" or event.char=="N":
            janela_adicionar_novo()
        if (event.char)=="d" or event.char=="D":
            janela_alterar_nome()
        if (event.char)=="p" or event.char=="P":
            janela_alterar_preço()
def adicionar_novo_fornecedor():
    sons("botao")
    janela_opaca()
    def close():
        sons('botao')
        global janela_transparente
        janela_adicionar_novo_fornecedor.destroy()
        janela_transparente.destroy()
    def add():
        try:
            global janela_transparente
            nome=str(ed_nome_fornecedor.get())
            nome_nova_tabela="fornecedor_"+nome
            telefone=str(ed_numero_fornecedor.get())
            cursor.execute(f"INSERT INTO fornecedores(nome,telefone) VALUES('{nome}',{telefone})")
            cursor.execute(f"CREATE TABLE  IF NOT EXISTS  {nome_nova_tabela} (id INTEGER PRIMARY KEY AUTOINCREMENT,nome_iten TEXT,preço REAL,data TEXT)")
            connect.commit()
            janela_adicionar_novo_fornecedor.destroy()
            janela_transparente.destroy()
            bt_fornecedores()
        except:
            lb_erro.place(x=80, y=150)
    global len_id,tabela,medida,hora_atual
    try:
        janela_adicionar_novo_fornecedor=Toplevel()
        janela_adicionar_novo_fornecedor.geometry("325x195+570+200")
        janela_adicionar_novo_fornecedor["bg"]="black"
        janela_adicionar_novo_fornecedor.title("ADICIONAR NOVO>")
        janela_adicionar_novo_fornecedor.resizable(width=False, height=False)
        janela_adicionar_novo_fornecedor.transient()
        janela_adicionar_novo_fornecedor.focus_force()
        janela_adicionar_novo_fornecedor.grab_set()
        janela_adicionar_novo_fornecedor.overrideredirect(True)
        #-------------------------------------------------FRAME--------------------------------------------#
        frame_main=Frame(janela_adicionar_novo_fornecedor,width=320,height=190,bg="#363636",highlightbackground="grey",highlightthickness=10)
        frame_main.place(x=2,y=2)
        #-------------------------------------------------FRAME--------------------------------------------#
        #-------------------------------------------------LABEL--------------------------------------------#
        lb_titulo = Label(frame_main, bg="#363636", text="ADICIONAR", font="impact 17 bold", foreground="green")
        lb_titulo.place(x=100, y=3)

        lb_nome_fornecedor = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="NOME DO FORNECEDOR:")
        lb_nome_fornecedor.place(x=5, y=40)
        lb_numero_fornecedor = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="☎ TELEFONE:")
        lb_numero_fornecedor.place(x=5, y=70)
        lb_erro = Label(frame_main, bg="#363636", foreground="red", font='gothic 10 bold', text="Valores inválidos.")
        #-------------------------------------------------LABEL--------------------------------------------#
        #-------------------------------------------------ENTRY--------------------------------------------#
        ed_nome_fornecedor= Entry(frame_main, width=20)
        ed_nome_fornecedor.place(x=160, y=40)
        ed_numero_fornecedor = Entry(frame_main, width=20)
        ed_numero_fornecedor.place(x=160, y=70)
        #-------------------------------------------------ENTRY--------------------------------------------#
        #-------------------------------------------------BOTOES--------------------------------------------#
        bt_salvar = Button(frame_main, text="ADICIONAR", bg="blue", font="Cambria 12 bold",command=add)
        bt_salvar.place(x=108, y=115)
        bt_sair = Button(frame_main, text="x", bg="red", font="Cambria 12 bold", command=close)
        bt_sair.place(x=2, y=2)
        #-------------------------------------------------BOTOES--------------------------------------------#
        #-------------------------------------------------CHECKBOX--------------------------------------------#
        #-------------------------------------------------CHECKBOX--------------------------------------------#
    except:
        None
def adicionar_iten_fornecedor():
    sons("botao")
    janela_opaca()
    global len_id,tabela2,medida,hora_atual,nome_buscar_check
    def close():
        sons('botao')
        global janela_transparente
        janela_transparente.destroy()
        janela_adicionar_iten.destroy()
    def ingredientes():
        global len_id, tabela2, medida, hora_atual, nome_buscar_check
        cursor.execute("SELECT id FROM ingredientes")
        len_id = len(cursor.fetchall())
        nome_buscar_check=[]
        tabela2="ingredientes"
        buscar_nome_check()
        combo['values']=nome_buscar_check
        check_produtos.deselect()
        check_utilidade.deselect()
        check_linguiças.deselect()
    def produtos():
        global len_id, tabela2, medida, hora_atual, nome_buscar_check

        cursor.execute("SELECT id FROM produtos")
        len_id = len(cursor.fetchall())
        nome_buscar_check=[]
        tabela2="produtos"
        buscar_nome_check()
        combo['values']=nome_buscar_check
        check_ingredientes.deselect()
        check_utilidade.deselect()
        check_linguiças.deselect()
    def linguiças():
        global len_id, tabela2, medida, hora_atual, nome_buscar_check
        cursor.execute("SELECT id FROM linguiça")
        len_id = len(cursor.fetchall())
        nome_buscar_check=[]
        tabela2="linguiça"
        buscar_nome_check()
        combo['values']=nome_buscar_check
        check_produtos.deselect()
        check_utilidade.deselect()
        check_ingredientes.deselect()
    def utilidade():
        global len_id, tabela2, medida, hora_atual, nome_buscar_check
        cursor.execute("SELECT id FROM utilidade")
        len_id = len(cursor.fetchall())
        nome_buscar_check=[]
        tabela2="utilidade"
        buscar_nome_check()
        combo['values']=nome_buscar_check
        check_produtos.deselect()
        check_ingredientes.deselect()
        check_linguiças.deselect()
    def add():
        try:
            nome_item=combo.get()
            nome_item=str(nome_item.lower())
            if nome_item=="":
                lb_erro.place(x=110, y=150)
                check_produtos.deselect()
                check_ingredientes.deselect()
                check_linguiças.deselect()
                check_utilidade.deselect()
            else:
                id = tabela_estoque.selection()
                id = int(id[0])-1
                nome=fornecedores_buscar_nome[id]
                nome_="fornecedor_"+nome
                cursor.execute(f"INSERT INTO {nome_}(nome_iten) VALUES('{nome_item}')")
                connect.commit()
                bt_fornecedores()
                check_produtos.deselect()
                check_ingredientes.deselect()
                check_linguiças.deselect()
                check_utilidade.deselect()
                janela_adicionar_iten.destroy()
        except:
            lb_erro.place(x=110, y=150)
            check_produtos.deselect()
            check_ingredientes.deselect()
            check_linguiças.deselect()
            check_utilidade.deselect()
    try:
        janela_adicionar_iten=Toplevel()
        janela_adicionar_iten.geometry("385x200+500+200")
        janela_adicionar_iten["bg"]="black"
        janela_adicionar_iten.title("ADICIONAR NOVO>")
        janela_adicionar_iten.resizable(width=False, height=False)
        janela_adicionar_iten.transient()
        janela_adicionar_iten.focus_force()
        janela_adicionar_iten.grab_set()
        janela_adicionar_iten.overrideredirect(True)
        #-------------------------------------------------FRAME--------------------------------------------#
        frame_main=Frame(janela_adicionar_iten,width=380,height=190,highlightbackground="GREY",highlightthickness=10,bg="#363636")
        frame_main.place(x=2,y=4)
        frame_check=Frame(frame_main,bg="#363636")
        frame_check.place(x=8,y=60)
        #-------------------------------------------------FRAME--------------------------------------------#
        #-------------------------------------------------LABEL--------------------------------------------#
        lb_titulo = Label(frame_main, bg="#363636", text="ADICIONAR ITEN", font="impact 17 bold", foreground="green")
        lb_titulo.place(x=80,y=3)
        lb_iten = Label(frame_main, bg="#363636", text=f"{nome}",font="Cambria 12 bold", foreground="white")
        lb_iten.place(x=8,y=35)
        lb_erro = Label(frame_main, bg="#363636", foreground="red", font='gothic 10 bold', text="Valores inválidos.")
        #-------------------------------------------------LABEL--------------------------------------------#
        #-------------------------------------------------BOTOES--------------------------------------------#
        bt_salvar = Button(frame_main, text="ADICIONAR", bg="blue", font="Cambria 12 bold",command=add)
        bt_salvar.place(x=130, y=117)
        bt_sair = Button(frame_main, text="x", bg="red", font="Cambria 12 bold", command=close)
        bt_sair.place(x=2, y=2)
        #-------------------------------------------------BOTOES--------------------------------------------#
        #-------------------------------------------------CHECKBOX--------------------------------------------#
        combo=ttk.Combobox(frame_check)
        combo.pack(side=BOTTOM,fill=BOTH)
        check_ingredientes = Checkbutton(frame_check, text="INGREDIENTES", bg="#363636", foreground="blue", font="bold 8",command=ingredientes)
        check_ingredientes.pack(side=LEFT)
        check_produtos = Checkbutton(frame_check, text="PRODUTOS", bg="#363636", foreground="blue", font="bold 8",command=produtos)
        check_produtos.pack(side=LEFT)
        check_linguiças = Checkbutton(frame_check, text="LINGUIÇAS", bg="#363636", foreground="blue", font="bold 8",command=linguiças)
        check_linguiças.pack(side=LEFT)
        check_utilidade = Checkbutton(frame_check, text="UTILIDADE", bg="#363636", foreground="blue", font="bold 8",command=utilidade)
        check_utilidade.pack(side=LEFT)

        #-------------------------------------------------CHECKBOX--------------------------------------------#
    except:
        None
def atualizar_preço_fornecedor():
    sons("botao")
    janela_opaca()
    def close():
        sons('botao')
        global janela_transparente
        janela_transparente.destroy()
        janela_atualizar_preço.destroy()
    def atualizar_preço():
        id = tabela_estoque.selection()
        id = int(id[0]) - 1
        nome = fornecedores_buscar_nome[id]
        nome_ = "fornecedor_" + nome
        nome_item = combo.get()
        preço=float(ed_preço.get())
        cursor.execute(f"UPDATE {nome_} SET preço = {preço} WHERE nome_iten='{nome_item.lower()}'")
        cursor.execute(f"UPDATE {nome_} SET data = '{str(data_em_texto)}--{str(hora_atual)}' WHERE nome_iten='{nome_item.lower()}'")
        connect.commit()
        janela_atualizar_preço.destroy()
        bt_fornecedores()
    id = tabela_estoque.selection()
    id = int(id[0]) - 1
    nome = fornecedores_buscar_nome[id]
    nome_ = "fornecedor_" + nome
    cursor.execute(f"SELECT id FROM {nome_}")
    s_id = len(cursor.fetchall())
    b = 0
    a = 1
    nome_item = []
    while b < s_id:
        cursor.execute(f"SELECT nome_iten FROM {nome_} WHERE id={a}")
        nome_item.append(cursor.fetchone()[0].upper())
        b += 1
        a += 1
    janela_atualizar_preço=Toplevel()
    janela_atualizar_preço.geometry("320x186+530+200")
    janela_atualizar_preço["bg"]="black"
    janela_atualizar_preço.title("ATUALIZAR PREÇO>")
    janela_atualizar_preço.resizable(width=False, height=False)
    janela_atualizar_preço.transient()
    janela_atualizar_preço.focus_force()
    janela_atualizar_preço.grab_set()
    janela_atualizar_preço.overrideredirect(True)
    #------------------------------------------------FRAME--------------------------------------------#
    frame_main_main=Frame(janela_atualizar_preço,width=315,height=180,highlightbackground="grey",highlightthickness=10,bg="#363636")
    frame_main_main.place(x=2,y=2)
    frame_main=Frame(frame_main_main,highlightbackground="grey",highlightthickness=5,height=100,width=200,bg="#363636")
    frame_main.place(x=3,y=72)
    #-------------------------------------------------FRAME--------------------------------------------#
    combo = tktree.Combobox(frame_main)
    combo.pack(side=BOTTOM, fill=BOTH)
    combo['values']=nome_item
    #-------------------------------------------------LABEL--------------------------------------------#
    lb_titulo = Label(frame_main_main, bg="#363636", text="ATUALIZAR PREÇO", font="impact 17 bold", foreground="green")
    lb_titulo.place(x=60,y=5)
    lb_iten = Label(frame_main_main, bg="#363636", text=f"{nome.upper()}", font="Cambria 12 bold", foreground="white")
    lb_iten.place(x=5, y=45)
    lb_preço_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="PREÇO:")
    lb_preço_iten.pack(side=LEFT)
    lb_erro = Label(frame_main, bg="#363636", foreground="red", font='gothic 10 bold', text="Valores inválidos.")
    #-------------------------------------------------LABEL--------------------------------------------#
    #-------------------------------------------------ENTRY--------------------------------------------#
    ed_preço = Entry(frame_main, width=20)
    ed_preço.pack(side=LEFT)
    #-------------------------------------------------ENTRY--------------------------------------------#
    #-------------------------------------------------BOTOES--------------------------------------------#
    bt_salvar = Button(frame_main, text="ADICIONAR", bg="blue", font="Cambria 12 bold",command=atualizar_preço)
    bt_salvar.pack(side=BOTTOM)
    bt_sair = Button(frame_main_main, text="x", bg="red", font="Cambria 12 bold", command=close)
    bt_sair.place(x=2, y=2)
def zerar_iten_fornecedor():
    sons("alerta")
    janela_opaca()
    def close():
        sons('botao')
        global janela_transparente
        janela_zerar.destroy()
        janela_transparente.destroy()
    def bt_confirmar():
        global tabela,janela_transparente
        hora_atual = strftime("%H:%M:%S")
        data_atual = date.today()
        data_em_texto = data_atual.strftime("%d/%m/%Y")
        id = tabela_estoque.selection()
        id = int(id[0]) - 1
        nome = fornecedores_buscar_nome[id]
        nome_ = "fornecedor_" + nome
        cursor.execute(f"SELECT id FROM {nome_}")
        #---------------------------------------------------------------------------------------------------------#
        cursor.execute(f"DROP TABLE {nome_}")
        cursor.execute(f"CREATE TABLE  IF NOT EXISTS  {nome_} (id INTEGER PRIMARY KEY AUTOINCREMENT,nome_iten TEXT,preço REAL,data TEXT)")
        #---------------------------------------------------------------------------------------------------------#
        #---------------------------------------------------------------------------------------------------------#
        connect.commit()
        bt_fornecedores()
        janela_zerar.destroy()
        janela_transparente.destroy()
    def bt_cancelar():
        global janela_transparente
        janela_zerar.destroy()
        janela_transparente.destroy()
    try:
        janela_zerar=Toplevel()
        janela_zerar.geometry("184x110+590+240")
        janela_zerar["bg"]="black"
        janela_zerar.title("ZERAR>")
        janela_zerar.resizable(width=False, height=False)
        janela_zerar.transient()
        janela_zerar.focus_force()
        janela_zerar.grab_set()
        janela_zerar.overrideredirect(True)
        #----------------------------------------------FRAME - -------------------------------------------
        frame_main=Frame(janela_zerar, bg="#363636",highlightbackground="grey",highlightthickness=10)
        frame_main.place(x=2,y=2)
        #----------------------------------------------FRAME - -------------------------------------------
        #---------------------------------------------LABEL--------------------------------------------#
        lb_titulo = Label(frame_main, bg="#363636", text="ZERAR ITENS", font="impact 17 bold", foreground="green")
        lb_titulo.pack(side=TOP)
        lb_iten = Label(frame_main, bg="#363636", text=f"{nome}",font="Cambria 12 bold", foreground="white")
        lb_iten.pack(side=TOP)
        #---------------------------------------------LABEL--------------------------------------------#
        #----------------------------------------------BOTOES--------------------------------------------#
        bt_sim = Button(frame_main, text="CONFIRMAR", bg="blue", font="Cambria 10 bold", command=bt_confirmar)
        bt_sim.pack(side=LEFT)
        bt_nao = Button(frame_main, text="CANCELAR", bg="blue", font="Cambria 10 bold", command=bt_cancelar)
        bt_nao.pack(side=RIGHT)
        #----------------------------------------------BOTOES--------------------------------------------#
    except:
        None
def janela_alterar_telefone_fornecedor():
    sons("botao")
    janela_opaca()
    def close():
        sons('botao')
        global janela_transparente
        janela_alterar_telefone.destroy()
        janela_transparente.destroy()
    def alterar_telefone():
        global janela_transparente
        id = tabela_estoque.selection()
        id = int(id[0]) - 1
        nome = fornecedores_buscar_nome[id]
        nome_ = "fornecedor_" + nome
        cursor.execute(f"SELECT id FROM {nome_}")
        try:
            novo_telefone=int(ed_quantidades_iten.get())
            novo_telefone=str(ed_quantidades_iten.get())
            cursor.execute(f"UPDATE fornecedores SET telefone = '{novo_telefone}' WHERE id ={id+1}")
            connect.commit()
            janela_alterar_telefone.destroy()
            janela_transparente.destroy()
            bt_fornecedores()
        except:
            lb_erro.place(x=50, y=130)
        #--------------------------------------------------------------------------------------------------------#
    try:
        janela_alterar_telefone=Toplevel()
        janela_alterar_telefone.geometry("255x175+560+200")
        janela_alterar_telefone["bg"]="black"
        janela_alterar_telefone.title("ALTERAR TELEFONE>")
        janela_alterar_telefone.resizable(width=False, height=False)
        janela_alterar_telefone.transient()
        janela_alterar_telefone.focus_force()
        janela_alterar_telefone.grab_set()
        janela_alterar_telefone.overrideredirect(True)
        #---------------------------------------------------------------FRAME - ------------------------------------------------
        frame_main=Frame(janela_alterar_telefone,width=250,height=170, bg="#363636",highlightbackground="grey",highlightthickness=10)
        frame_main.place(x=3,y=2)
        #---------------------------------------------------------------LABEL-------------------------------------------------#
        lb_titulo = Label(frame_main, bg="#363636", text="ATUALIZAR N.TEL", font="impact 17 bold", foreground="green")
        lb_titulo.place(x=40, y=6)
        lb_iten = Label(frame_main, bg="#363636", text=f"{nome}",font="Cambria 12 bold", foreground="white")
        lb_iten.place(x=8, y=40)
        lb_quantidade_iten = Label(frame_main, bg="#363636", foreground="white", font='gothic 10 bold', text="NOVO NÚMERO:")
        lb_quantidade_iten.place(x=8, y=70)
        lb_erro = Label(frame_main, bg="#363636", foreground="red", font='gothic 10 bold', text="Valores inválidos.")
        #---------------------------------------------------------------LABEL-------------------------------------------------#
        #------------------------------------------------------------ENTRY----------------------------------------------------#
        ed_quantidades_iten = Entry(frame_main, width=15)
        ed_quantidades_iten.place(x=120, y=70)
        #------------------------------------------------------------ENTRY----------------------------------------------------#
        #-------------------------------------------------BOTOES--------------------------------------------#
        bt_salvar = Button(frame_main,text="CONFIRMAR",bg="blue",font="Cambria 12 bold", command=alterar_telefone)
        bt_salvar.place(x=70, y=95)
        bt_sair = Button(frame_main, text="x", bg="red", font="Cambria 12 bold", command=close)
        bt_sair.place(x=2, y=2)
        #-------------------------------------------------BOTOES--------------------------------------------#
    except:
        None
def chamar_PRODUÇAO():
    sons('botao')
    global logo_estoque,lb_titulo
    frame_root_PRODUÇAO.place(x=6,y=113)
    frame_root_ESTOQUE.place(x=0,y=1000)
    logo_estoque = PhotoImage(file="img/icone_produção.png")
    logo_estoque = logo_estoque.subsample(7, 8)
    lb_titulo['text']='➮PRODUÇÃO'
    lb_logo_estoque.place(x=12, y=15)
    lb_logo_estoque['image']=logo_estoque
def chamar_ESTOQUE():
    sons('botao')
    global logo_estoque
    frame_root_PRODUÇAO.place(x=0,y=1000)
    frame_root_ESTOQUE.place(x=6,y=112)
    lb_titulo['text']='➮ESTOQUE'
    logo_estoque=PhotoImage(file="img/icone_estoque.png")
    logo_estoque=logo_estoque.subsample(3,3)
    lb_logo_estoque['image']=logo_estoque
    lb_logo_estoque.place(x=12, y=17)
def chamar_LOGIN():
    sons('botao')
    global logo_estoque
    frame_root_PRODUÇAO.place(x=0,y=10000)
    frame_root_ESTOQUE.place(x=0,y=10000)
    frame_barra.place(x=0,y=10000)
    lb_titulo['text']='➮LOGIN'
    logo_estoque=PhotoImage(file="img/icone_cadiado.png")
    logo_estoque=logo_estoque.subsample(6,6)
    lb_logo_estoque['image']=logo_estoque
    lb_logo_estoque.place(x=20, y=20)
def login():
    login=ed_login.get()
    senha=ed_senha.get()
    if login=="tiktim" and senha == '35332460':
        chamar_ESTOQUE()
        frame_barra.place(x=2,y=682)
    else:
        frame_senha['highlightbackground']='red'
        frame_senha['highlightcolor']='red'
janela_main=Tk()
janela_main.title("TIKTIM")
#lado, cima = (janela_main.winfo_screenwidth()), (janela_main.winfo_screenheight())
#janela_main.geometry(f"{lado}x{cima}")
janela_main["bg"]="black"
#janela_main.attributes('-zoomed', True)
janela_main.resizable(width=False, height=False)
janela_main.state('zoomed')
janela=janela_main
cabeçalho(janela)
menu(janela)
style = ttk.Style(janela_main)
style.configure("Treeview", font='gothic 17 bold',rowheight=30)
#-------------------------------------------------LOGIN---------------------------------------------------------------#
fundo=['img/foto1.png','img/foto2.png']
foto=PhotoImage(file='img/foto2.png')
foto=foto.subsample(1,2)
logo_estoque = PhotoImage(file="img/icone_cadiado.png")
logo_estoque = logo_estoque.subsample(7, 8)
lb_titulo['text']='➮LOGIN'
lb_logo_estoque.place(x=12, y=15)
lb_logo_estoque['image']=logo_estoque
frame_root_LOGIN=Frame(janela,bg="#363636",highlightbackground="grey",highlightthickness=3,width=1354,height=569)
frame_root_LOGIN.place(x=6,y=110)
frame_fundo=Frame(frame_root_LOGIN,bg="grey",highlightbackground="grey",highlightthickness=3,width=1354,height=600)
frame_fundo.place(x=0,y=0)
frame_senha=Frame(frame_fundo,bg="white",highlightbackground="black",highlightthickness=5,width=200,height=140)
frame_senha.place(x=540,y=180)
lb_login=Label(frame_senha,bg='GREY',text='LOGIN:',font="Cambria 13 bold underline")
lb_login.place(x=10,y=10)
lb_senha=Label(frame_senha,bg='GREY',text='SENHA:',font="Cambria 13 bold underline")
lb_senha.place(x=10,y=50)
frame_ed1=Frame(frame_senha,highlightbackground="grey",highlightthickness=2)
frame_ed1.place(x=80,y=12)
frame_ed2=Frame(frame_senha,highlightbackground="grey",highlightthickness=2)
frame_ed2.place(x=80,y=52)
ed_login=Entry(frame_ed1,width=14)
ed_login.pack()
ed_senha=Entry(frame_ed2,width=14,show='*')
ed_senha.pack()
bt_entrar=Button(frame_senha,width=19,text='ENTRAR',bg='blue',font=font.botoes,command=login)
bt_entrar.place(x=5,y=90)
#-------------------------------------------------LOGIN---------------------------------------------------------------#
#-------------------------------------------------FRAME---------------------------------------------------------------#
frame_root_PRODUÇAO=Frame(janela,bg="#363636",highlightbackground="grey",highlightthickness=3)
#frame_root_PRODUÇAO.place(x=6,y=110)
frame_calcular=Frame(frame_root_PRODUÇAO,width=340,height=560,bg="#363636",highlightbackground="grey",highlightthickness=3)
frame_calcular.pack(side=LEFT)
frame_ingredientes=Frame(frame_root_PRODUÇAO,width=600,height=560,bg="#363636",highlightbackground="grey",highlightthickness=3)
frame_ingredientes.pack(side=LEFT)
frame_hora=Frame(frame_root_PRODUÇAO,width=408,height=548,bg="#363636",highlightbackground="grey",highlightthickness=3)
frame_hora.pack(side=TOP)
#--------------------------------------------------------------------------------------------------------------------#
frame_calculo=Frame(frame_calcular,width=229,height=140,bg="#363636",highlightbackground="grey",highlightthickness=8)
frame_calculo.place(x=50,y=45)
frame_ed_carne=Frame(frame_calculo,highlightbackground="grey",highlightthickness=2)
frame_ed_carne.place(x=110,y=5)
frame_ed_limpeza=Frame(frame_calculo,highlightbackground="grey",highlightthickness=2)
frame_ed_limpeza.place(x=110,y=34)
frame_tabela_calcular=Frame(frame_calcular,width=229,height=50,bg="#363636",highlightbackground="grey",highlightthickness=3)
frame_tabela_calcular.place(x=0,y=190)
frame_tabela_calcular_dividir=Frame(frame_calcular,bg="#363636",highlightbackground="grey",highlightthickness=5)
scroll=Scrollbar(frame_tabela_calcular)
scroll.pack(side=LEFT,fill=BOTH)
#-------------------------------------------------FRAME---------------------------------------------------------------#
#-------------------------------------------------CALCULAR---------------------------------------------------------------#
icone_calcular=PhotoImage(file="img/icone_calcular.png")
icone_calcular=icone_calcular.subsample(8,8)
lb_titulo_calcular = Label(frame_calcular, bg="#363636", text="CALCULAR", font=font.titulo, foreground="white")
lb_titulo_calcular.place(x=40, y=5)
lb_icone_calcular = Label(frame_calcular,bg="#363636",image=icone_calcular)
lb_icone_calcular.place(x=2,y=2)
lb_carne=Label(frame_calculo,text="CARNE :",font="Cambria 13 bold underline",bg="#363636",foreground='white')
lb_carne.place(x=7,y=2)
lb_limpeza=Label(frame_calculo,text="LIMPEZA :",font="Cambria 13 bold underline",bg="#363636",foreground="white")
lb_limpeza.place(x=7,y=31)
lb_erro_calcular_carne=Label(frame_calculo,text="*",font="Cambria 17",bg="#363636",foreground="red")
lb_erro_calcular_limpeza=Label(frame_calculo,text="*",font="Cambria 17",bg="#363636",foreground="red")
check_porco_var= BooleanVar()
check_frango_var= BooleanVar()
check_porco=Checkbutton(frame_calculo,text="PORCO",font="Cambria 10",command=check_porco,variable=check_porco_var)
check_porco.place(x=30,y=64)
check_frango=Checkbutton(frame_calculo,text="FRANGO",font="Cambria 10",command=check_frango,variable=check_frango_var)
check_frango.place(x=115,y=64)
ed_carne=Entry(frame_ed_carne,width=9)
ed_carne.pack()
ed_limpeza=Entry(frame_ed_limpeza,width=9)
ed_limpeza.pack()
ed_dividir=Entry(frame_tabela_calcular_dividir,width=9)
ed_dividir.pack(side=LEFT)
bt_calcular=Button(frame_calculo,text="CALCULAR",font=font.botoes,bg=cor.botao_confirmar_off,width=22,activebackground=cor.botao_confirmar_active,foreground=cor.lb_botao_confirmar_off)
bt_calcular.place(x=3,y=94)
bt_dividir=Button(frame_calcular,text="%",font=font.botoes,bg=cor.botao_confirmar_off,activebackground=cor.botao_confirmar_active,foreground=cor.lb_botao_confirmar_off,command=dividir_mostra)
bt_dividir.place(x=303,y=159)
bt_confirmar_dividir=Button(frame_tabela_calcular_dividir,text="OK",font=font.botoes,bg=cor.botao_confirmar_off,activebackground=cor.botao_confirmar_active,foreground=cor.lb_botao_confirmar_off,command=divivir_ok)
bt_confirmar_dividir.pack(side=LEFT)
bt_clean_calcular=Button(frame_calcular,text="✖",bg=cor.botao_limpar_off,command=cleaner.clean_calcular,foreground=cor.lb_botao_limpar_off,font=font.botoes,activebackground=cor.botao_confirmar_active)
bt_clean_calcular.place(x=300,y=3)
ingredientes_porco=["CARNE","LIMPEZA","TOUCINHO","ALHO","SAL","TOTAL"]
ingredientes_frango=["CARNE","LIMPEZA","BACON","PEITO","ALHO","SAL","TOTAL"]
tabela_calcular=ttk.Treeview()
create_table("calcular")
#-------------------------------------------------INGREDIENTES---------------------------------------------------------------#
frame_restante=Frame(frame_ingredientes,highlightbackground="grey",highlightthickness=2,bg="#363636",width=170,height=40)
frame_restante.place(x=422,y=35)
frame_restante_r=Frame(frame_restante,bg="#363636",width=90,height=30)
frame_restante_r.place(x=80,y=3)
frame_tabela_ingredientes=Frame(frame_ingredientes,highlightbackground="grey",highlightthickness=2,bg="#363636")
frame_tabela_ingredientes.place(x=3,y=75)
frame_ingredientes_calcular=Frame(frame_tabela_ingredientes,highlightbackground="grey",highlightthickness=2,bg="#363636",width=590,height=52)
frame_ingredientes_calcular.pack()
frame_selecionado=Frame(frame_ingredientes_calcular,highlightbackground="green",highlightthickness=3,bg="#363636")
frame_selecionado.place(x=2,y=4)
icone_ingredientes=PhotoImage(file="img/icone_ingredientes.png")
icone_ingredientes=icone_ingredientes.subsample(5,5)
lb_titulo_ingredientes = Label(frame_ingredientes, bg="#363636", text="INGREDIENTES", font="impact 17 bold underline", foreground="white")
lb_titulo_ingredientes.place(x=60, y=7)
lb_icone_ingredientes= Label(frame_ingredientes,bg="#363636",image=icone_ingredientes)
lb_icone_ingredientes.place(x=2,y=0)
lb_restante=Label(frame_restante,bg="#363636",foreground="white" ,text="RESTANTE:",font='gothic 10 bold')
lb_restante.place(x=2,y=10)
lb_select=Label(frame_hora,bg="#363636",foreground="white" ,text="RESTANTE:",font=font.lb)
lb_select.place(x=2000,y=10)
lb_restante_r=Label(frame_restante_r,bg="#363636",foreground="blue" ,text="0KG",font='Cambria 16 bold underline',width=6)
lb_restante_r.pack()
lb_selecionado_produçao = Label(frame_selecionado, bg="#363636", text="", font="impact 15 bold", foreground="green",width=23)
lb_selecionado_produçao.pack()
bt_clean_ingredientes=Button(frame_ingredientes,text="✖",bg=cor.botao_limpar_off,command=cleaner.clean_ingredientes,foreground=cor.lb_botao_limpar_off,activebackground=cor.botao_confirmar_active,font=font.botoes)
bt_clean_ingredientes.place(x=560,y=0)
bt_calcular_ingredientes=Button(frame_ingredientes_calcular,text="CONFIRMAR",font=font.botoes,bg=color.botao_confirmar_off,command=bt_calcular_sabores,width=20,activebackground=cor.botao_confirmar_active,foreground=color.lb_botao_confirmar_off)
bt_calcular_ingredientes.place(x=390,y=10)
scroll_ingredientes=Scrollbar(frame_tabela_ingredientes)
scroll_ingredientes.pack(side=LEFT,fill=BOTH)
slide1=Scale(frame_ingredientes_calcular,from_=0,orient=HORIZONTAL,bg='black',foreground="blue",activebackground="blue",font='gothic 10 bold',width=15)
slide1.place(x=275,y=4)
#-------------------------------------------------------------------------------------------------------------#
tabela_ingredientes=ttk.Treeview()
create_table("ingredientes")
#-------------------------------------------------INGREDIENTES---------------------------------------------------------------#
#-------------------------------------------------HORA---------------------------------------------------------------#
frame_hora_funçoes_=Frame(frame_hora,highlightbackground="grey",highlightthickness=4,bg="#363636",width=395,height=550)
frame_hora_funçoes_.place(x=4,y=100)
frame_hora_funçoes=Frame(frame_hora_funçoes_,highlightbackground="grey",highlightthickness=1,bg="#363636")
frame_hora_funçoes.place(x=0,y=0)
frame_relogio=Frame(frame_hora,highlightbackground="grey",highlightthickness=1,bg="#363636")
frame_relogio.place(x=140,y=50)
icone_hora=PhotoImage(file="img/icone_relogio.png")
icone_hora=icone_hora.subsample(6,6)
lb_titulo_hora = Label(frame_hora, bg="#363636", text="HORÁRIO", font="impact 17 bold underline", foreground="white")
lb_titulo_hora.place(x=50, y=7)
lb_icone_hora= Label(frame_hora,bg="#363636",image=icone_hora)
lb_icone_hora.place(x=5,y=2)
lb_relogio=Label(frame_relogio,bg="#363636",text="00:00:00",font="Cambria 25 bold",foreground="green")
lb_relogio.pack()
select_funcionarios=Listbox(frame_hora_funçoes,bg="#1C1C1C",foreground="#B22222",height=5,width=38,font='gothic 13 bold',selectmode=EXTENDED)
select_funcionarios.bind("<Double-Button-1>",event_select)
select_funcionarios.pack(side=TOP)
select_funcionarios.insert(END,"FUNCIONARIOS")
inserir_funcionarios_select()
combo_hora = ttk.Combobox(frame_hora_funçoes)
combo_hora.pack(side=BOTTOM, fill=BOTH)
bt_confirmar_hora=Button(frame_hora_funçoes,text="CONFIRMAR",font=font.botoes,bg=color.botao_confirmar_off,command=atividade,width=20,activebackground=cor.botao_confirmar_active,foreground=color.lb_botao_confirmar_off)
bt_confirmar_hora.pack(side=BOTTOM, fill=BOTH)
#------------------------------------------------------------------------------------------------------------#
tabela_hora_info = ttk.Treeview(frame_hora_funçoes_, columns=("ATIVIDADE","HORA"),height=11, selectmode="browse")
tabela_hora_info.place(x=0,y=150)
tabela_hora_info.column('#0', width=130, minwidth=130)
tabela_hora_info.column("ATIVIDADE", width=130, minwidth=130)
tabela_hora_info.column("HORA", width=125, minwidth=125)
tabela_hora_info.heading("#0", text="NOME")
tabela_hora_info.heading("ATIVIDADE", text="ATIVIDADE")
tabela_hora_info.heading("HORA", text="HORÁRIO")
combo_hora['values']="*INICIAR*"

#============================================================================================================================#
#=======================================================ESTOQUE==============================================================#
#============================================================================================================================#
#============================================================================================================================#
frame_root_ESTOQUE=Frame(janela,highlightbackground="grey",highlightthickness=3)
#frame_root_ESTOQUE.place(x=6,y=110)
frame_tabela=Frame(frame_root_ESTOQUE,highlightbackground="blue",highlightthickness=1)
frame_tabela.pack(side=TOP)
frame_botoes_tabela=Frame(frame_tabela)
frame_botoes_tabela.pack(side=TOP,ipady=2,ipadx=3)
frame_botoes_operaçoes=Frame(frame_tabela)
frame_botoes_operaçoes.pack(side=BOTTOM,ipady=2,ipadx=3)
frame_cabeçalho=Frame(janela,width=1355,height=110,highlightbackground="#363636",highlightthickness=7,bg="#1d1b1b")
frame_cabeçalho.place(x=5,y=1)
frame_credito=Frame(frame_cabeçalho,width=1355,height=110,highlightbackground="#363636",highlightthickness=2,bg="#1d1b1b")
frame_credito.place(x=1120,y=60)
frame_informaçoes=Frame(frame_root_ESTOQUE,highlightbackground="grey",highlightthickness=3,height=128,width=13,bg="#363636")
frame_informaçoes.pack(side=BOTTOM,fill=BOTH)
frame_atalhos=Frame(frame_informaçoes,highlightbackground="green",highlightthickness=3,height=105,width=480,bg="#363636")
frame_atalhos.place(x=420,y=7)
frame_selecionado=Frame(frame_informaçoes,highlightbackground="green",highlightthickness=3,height=40,width=10)
frame_selecionado.place(x=58,y=70)
frame_aviso=Frame(frame_informaçoes,highlightbackground="green",highlightthickness=3)
frame_aviso.place(x=1018,y=10)
#---------------------------------------------------PHOTO-----------------------------------------------------------------
logo=PhotoImage(file="img/logo_2.png")
logo=logo.subsample(3,4)
logo_estoque=PhotoImage(file="img/icone_estoque.png")
logo_estoque=logo_estoque.subsample(3,3)
logo_wp=PhotoImage(file="img/logo_whats.png")
logo_wp=logo_wp.subsample(5,5)
logo_fb=PhotoImage(file="img/logo_fb.png")
logo_fb=logo_fb.subsample(14,14)
logo_instagram=PhotoImage(file="img/logo_instagran.png")
logo_instagram=logo_instagram.subsample(5,5)
#---------------------------------------------------LABEL_PHOTO-----------------------------------------------------------------
lb_logo=Label(frame_cabeçalho,image=logo,bg="#1d1b1b")
lb_logo.place(x=520,y=2)
lb_logo_estoque=Label(frame_cabeçalho,image=logo_estoque,bg="#1d1b1b")
lb_logo_estoque.place(x=10,y=19)
lb_logo_wp=Label(frame_cabeçalho,image=logo_wp,bg="#1d1b1b")
lb_logo_wp.place(x=1120,y=1)
lb_logo_fb=Label(frame_cabeçalho,image=logo_fb,bg="#1d1b1b")
lb_logo_fb.place(x=930,y=60)
lb_logo_instagram=Label(frame_cabeçalho,image=logo_instagram,bg="#1d1b1b")
lb_logo_instagram.place(x=930,y=1)
#--------------------------------------------------------------------------------------------------------------------#
lb_titulo = Label(frame_cabeçalho, bg="#1d1b1b", text="➮ESTOQUE", font="impact 35", foreground="grey")
lb_titulo.place(x=100,y=30)
lb_endereço=Label(frame_cabeçalho,bg="#1d1b1b",foreground="#DCDCDC" ,font='gothic 13 bold',text="RUA PRAÇA CASTORINO DE SOUZA 84")
lb_telefone=Label(frame_cabeçalho,bg="#1d1b1b",foreground="#DCDCDC" ,font='gothic 13 bold',text="(35) 9 91158971")
lb_telefone.place(x=1160,y=20)
lb_instagran=Label(frame_cabeçalho,bg="#1d1b1b",foreground="#DCDCDC" ,font='gothic 10 bold',text="@diegolaraTIKTIM")
lb_instagran.place(x=970,y=20)
lb_fb=Label(frame_cabeçalho,bg="#1d1b1b",foreground="#DCDCDC" ,font='gothic 10 bold',text="/diegolaraTiktim")
lb_fb.place(x=970,y=70)
lb_credito=Label(frame_credito,bg="#1d1b1b",foreground="#DCDCDC" ,font='italic 5 bold underline',text="RUA PRAÇA CASTORINO DE SOUZA 84")
lb_credito.pack(anchor=S)
#--------------------------------------------------------------------------------------------------------------------
lb_atalho_1=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="--ADICIONAR-NOVO")
lb_atalho_1.place(x=20,y=5)
lb_atalho_2=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="--REMOVER")
lb_atalho_2.place(x=20,y=40)
lb_atalho_3=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="--ADICIONAR")
lb_atalho_3.place(x=20,y=75)
lb_atalho_4=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="--ZERAR")
lb_atalho_4.place(x=280,y=5)
lb_atalho_5=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="--ALTERAR NOME")
lb_atalho_5.place(x=280,y=40)
lb_atalho_6=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="--ALTERAR PREÇO")
lb_atalho_6.place(x=280,y=75)
#--------------------------------------------------------------------------------------------------------------------
lb_atalho_N=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="N")
lb_atalho_N.place(x=10,y=5)
lb_atalho_A=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="A")
lb_atalho_A.place(x=10,y=75)
lb_atalho_D=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="D")
lb_atalho_D.place(x=270,y=40)
lb_atalho_R=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="R")
lb_atalho_R.place(x=10,y=40)
lb_atalho_Z=Label(frame_atalhos,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="Z")
lb_atalho_Z.place(x=270,y=5)
lb_atalho_P=Label(frame_atalhos,foreground="#DCDCDC" ,font='gothic 13 bold',text="P",bg="#363636")
lb_atalho_P.place(x=270,y=75)
#--------------------------------------------------------------------------------------------------------------------
lb_selecionado = Label(frame_selecionado, bg="#363636", text="frango pura", font="impact 17 bold", foreground="green",width=25)
lb_selecionado.pack()
lb_data_atual=Label(frame_informaçoes,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="DATA:")
lb_data_atual.place(x=10,y=5)
lb_hora_atual=Label(frame_informaçoes,bg="#363636",foreground="#DCDCDC" ,font='gothic 13 bold',text="HORA:")
lb_hora_atual.place(x=10,y=35)
lb_data_atual_r=Label(frame_informaçoes,bg="#363636",foreground="#4682B4" ,font='gothic 18 bold',text=f"{data_em_texto}")
lb_data_atual_r.place(x=65,y=3)
lb_hora_atual_r=Label(frame_informaçoes,bg="#363636",foreground="#4682B4" ,font='gothic 18 bold',text="00:00:00" )
lb_hora_atual_r.place(x=65,y=30)
lb_info_bd=Label(frame_informaçoes,bg="#363636",foreground="white" ,font='gothic 13 bold',text="BANCO DE DADOS:")
lb_info_bd.place(x=205,y=5)
lb_info_bd_r=Label(frame_informaçoes,bg="#363636",foreground="lime" ,font='gothic 13 bold',text="ON")
lb_info_bd_r.place(x=355,y=5)
lb_atalhos_vertical=Label(frame_informaçoes,bg="#363636",foreground="#4682B4" ,font='gothic 10 bold',text="ATALHOS",wraplength=1  )
lb_atalhos_vertical.place(x=400,y=10)
lb_atalhos_vertical2=Label(frame_informaçoes,bg="#363636",foreground="#4682B4" ,font='gothic 10 bold',text="ATALHOS",wraplength=1  )
lb_atalhos_vertical2.place(x=910,y=10)
lb_comprar_vertical1=Label(frame_informaçoes,bg="#363636",foreground="#4682B4" ,font='gothic 10 bold',text="COMPRAR",wraplength=1  )
lb_comprar_vertical1.place(x=1000,y=10)
lb_comprar_vertical2=Label(frame_informaçoes,bg="#363636",foreground="#4682B4" ,font='gothic 10 bold',text="COMPRAR",wraplength=1  )
lb_comprar_vertical2.place(x=1290,y=10)
#-------------------------------------------------FRAME---------------------------------------------------------------#
#-------------------------------------------------SCROLL--------------------------------------------------------------#
scroll=Scrollbar(frame_tabela)
scroll.pack(side=LEFT,fill=BOTH)
scroll_aviso=Scrollbar(frame_aviso)
scroll_aviso.pack(side=LEFT,fill=BOTH)
#----------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------TABELA---------------------------------------------------------------#
tabela_estoque=ttk.Treeview(frame_tabela)
tabela_estoque_historico=ttk.Treeview(frame_tabela)
#-------------------------------------------------SELECT---------------------------------------------------------------#
select_aviso=Listbox(frame_aviso,bg="#1C1C1C",foreground="#B22222",height=5,width=24,font='gothic 13 bold')
select_aviso.pack(side=LEFT)
#----------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------RISCO---------------------------------------------------------------#
lb_risco2=Label(janela_main,width=1,height=150)
lb_risco2.place(x=304,y=900)
lb_risco11 =Label(janela,width=0,height=2000)
lb_risco11.place(x=0,y=0)
lb_risco12 =Label(janela,width=0,height=200)
lb_risco12.place(x=1361,y=0)
lb_risco14 =Label(janela,width=10000,height=10)
#lb_risco14.place(x=0,y=696)
lb_risco9=Label(janela,width=200,height=5,bg="#363636")
lb_risco9.place(x=0,y=680)
lb_risco14.place(x=0,y=720)
#-------------------------------------------------BOTOES---------------------------------------------------------------#
bt_ingredientes_=Button(frame_botoes_tabela,text="INGREDIENTES",bg="#87CEFA",font=fonte_botoes,command=bt_ingredientes,width=15)
bt_ingredientes_.pack(side=LEFT)
bt_linguiça_=Button(frame_botoes_tabela,text="LINGUIÇAS",bg="#87CEFA",font=fonte_botoes,command=bt_linguiça,width=15)
bt_linguiça_.pack(side=LEFT)
bt_produtos_=Button(frame_botoes_tabela,text="PRODUTOS",bg="#87CEFA",font=fonte_botoes,command=bt_produtos,width=15)
bt_produtos_.pack(side=LEFT)
bt_utilidade_=Button(frame_botoes_tabela,text="UTILIDADE",bg="#87CEFA",font=fonte_botoes,command=bt_utilidade,width=15)
bt_utilidade_.pack(side=LEFT)
bt_fornecedores_=Button(frame_botoes_tabela,text="FORNECEDORES",bg="#87CEFA",font=fonte_botoes,command=bt_fornecedores,width=15)
bt_fornecedores_.pack(side=LEFT)
#-------------------------------------------------------------------------------------------------------------------#
bt_addnovo=Button(frame_botoes_operaçoes,text="ADICONAR NOVO",bg="grey",font=fonte_botoes,width=15)
bt_addnovo.pack(side=LEFT)
bt_adicionar=Button(frame_botoes_operaçoes,text="ADICIONAR",bg="grey",font=fonte_botoes,width=15)
bt_adicionar.pack(side=LEFT)
bt_remover=Button(frame_botoes_operaçoes,text="REMOVER",bg="grey",font=fonte_botoes,width=15)
bt_remover.pack(side=LEFT)
bt_zerar=Button(frame_botoes_operaçoes,text="ZERAR",bg="grey",font=fonte_botoes,width=15)
bt_zerar.pack(side=LEFT)
bt_alterar_nome=Button(frame_botoes_operaçoes,text="ALTERAR NOME",bg="grey",font=fonte_botoes,width=15)
bt_alterar_nome.pack(side=LEFT)
bt_alterar_preço=Button(frame_botoes_operaçoes,text="ALTERAR PREÇO",bg="grey",font=fonte_botoes,width=15)
bt_alterar_preço.pack(side=LEFT)
if erro==True:
    lb_info_bd_r["text"]="OFF"
    lb_info_bd_r["foreground"]="red"
#-----------------------------------------#
atualiza()
frame_barra=Frame(janela,bg='blue')
frame_barra.place(x=2,y=682)
bt_abrir_produçao=Button(frame_barra,width=28,height=1,text='➮PRODUÇÃO',command=chamar_PRODUÇAO,bg='grey',font="impact 14")
bt_abrir_produçao.pack(side=LEFT)
bt_abrir_estoque=Button(frame_barra,width=28,height=1,command=chamar_ESTOQUE,bg='grey',text='➮ESTOQUE',font="impact 14")
bt_abrir_estoque.pack(side=LEFT)
chamar_PRODUÇAO()
bt_ingredientes()
atualiza2()
janela_main.mainloop()
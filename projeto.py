# Importa a biblioteca Tkinter para criar a interface gráfica
import tkinter as tk

# Importa as caixas de mensagem prontas do Tkinter
from tkinter import messagebox

# Importa bibliotecas da PIL para trabalhar com imagens
from PIL import Image, ImageTk

# Importa o cliente do MongoDB
from pymongo import MongoClient

# Importa biblioteca para manipulação de caminhos de arquivos
import os

# ======================
# CONFIG
# ======================

# Cor de fundo principal do sistema
BG = "#0D2344"

# Cor padrão dos textos
FG = "white"

# ======================
# MONGODB
# ======================

# Cria conexão com o banco MongoDB Atlas
client = MongoClient("mongodb+srv://vertonandrade2005_db_user:phanthon@phanthon.pgzyhpu.mongodb.net/?appName=phanthon")

# Seleciona o banco de dados chamado "phantom_matriculas"
db = client["phantom_matriculas"]

# Seleciona a coleção de alunos
colecao_alunos = db["alunos"]

# Seleciona a coleção de solicitações
colecao_solicitacoes = db["solicitacoes"]

# Evita RGMs duplicados criando índice único
colecao_alunos.create_index("rgm", unique=True)

# ======================
# UI BASE
# ======================

# Função responsável por criar o cabeçalho do sistema
def header():

    # Cria um frame superior
    frame = tk.Frame(root, bg="#081C34", height=50)

    # Faz o frame ocupar toda largura
    frame.pack(fill="x")

    # Cria o título do sistema
    tk.Label(
        frame,
        text="Phantom Matrículas",
        bg="#081C34",
        fg="white",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

# Função para limpar toda a tela atual
def limpar_tela():

    # Percorre todos os componentes da janela
    for widget in root.winfo_children():

        # Remove os componentes da tela
        widget.destroy()

    # Recria o cabeçalho
    header()

# Função que cria um container centralizado
def criar_container():

    # Cria frame principal
    frame = tk.Frame(root, bg=BG)

    # Centraliza o frame na janela
    frame.place(relx=0.5, rely=0.55, anchor="center")

    # Retorna o frame criado
    return frame

# Função para criar labels padronizadas
def criar_label(parent, texto, size=10, bold=False):

    # Retorna um Label configurado
    return tk.Label(
        parent,
        text=texto,
        bg=BG,
        fg=FG,
        font=("Arial", size, "bold" if bold else "normal")
    )

# Função para criar botões padronizados
def criar_botao(parent, texto, comando):

    # Cria o botão
    btn = tk.Button(
        parent,
        text=texto,
        command=comando,
        bg="#2563EB",
        fg="white",
        width=22,
        height=2,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    )

    # Evento quando o mouse entra no botão
    def on_enter(e):

        # Muda a cor do botão
        btn.config(bg="#1D4ED8")

    # Evento quando o mouse sai do botão
    def on_leave(e):

        # Retorna a cor original
        btn.config(bg="#2563EB")

    # Associa evento de entrada do mouse
    btn.bind("<Enter>", on_enter)

    # Associa evento de saída do mouse
    btn.bind("<Leave>", on_leave)

    # Retorna o botão criado
    return btn

# Função para criar Entry com placeholder
def criar_entry_placeholder(parent, texto):

    # Cria campo de texto
    entry = tk.Entry(
        parent,
        fg="grey",
        width=28,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )

    # Insere texto placeholder
    entry.insert(0, texto)

    # Evento quando o usuário clica no campo
    def on_focus_in(event):

        # Se o texto atual for o placeholder
        if entry.get() == texto:

            # Limpa o campo
            entry.delete(0, tk.END)

            # Altera a cor do texto
            entry.config(fg="black")

    # Evento quando o usuário sai do campo
    def on_focus_out(event):

        # Se o campo estiver vazio
        if entry.get() == "":

            # Recoloca o placeholder
            entry.insert(0, texto)

            # Define cor cinza novamente
            entry.config(fg="grey")

    # Associa evento de foco
    entry.bind("<FocusIn>", on_focus_in)

    # Associa evento de perda de foco
    entry.bind("<FocusOut>", on_focus_out)

    # Retorna o campo criado
    return entry

# Função para pegar valor real do campo
def valor_real(entry, placeholder):

    # Se o valor for o placeholder retorna vazio
    return "" if entry.get() == placeholder else entry.get()

# Função para carregar imagens
def carregar_imagem(nome, w=200, h=200):

    try:

        # Monta caminho da imagem
        caminho = os.path.join(os.path.dirname(__file__), nome)

        # Abre imagem
        img = Image.open(caminho)

        # Redimensiona imagem
        img = img.resize((w, h), Image.LANCZOS)

        # Converte imagem para Tkinter
        return ImageTk.PhotoImage(img)

    except:

        # Caso dê erro retorna None
        return None

# ======================
# REGRAS
# ======================

# Busca aluno pelo RGM
def buscar_aluno(rgm):

    # Retorna aluno encontrado
    return colecao_alunos.find_one({"rgm": rgm})

# Função para cadastrar aluno
def cadastrar_aluno(nome, rgm, curso, horario):

    # Verifica campos obrigatórios
    if not nome or not curso:

        messagebox.showerror(
            "Erro",
            "Preencha todos os campos"
        )

        return

    # Verifica se RGM possui 8 dígitos
    if len(rgm) != 8 or not rgm.isdigit():

        messagebox.showerror(
            "Erro",
            "RGM precisa ter 8 dígitos"
        )

        return

    # Verifica se já existe aluno com mesmo RGM
    if buscar_aluno(rgm):

        messagebox.showerror(
            "Erro",
            "RGM já cadastrado"
        )

        return

    try:

        # Insere aluno no banco
        colecao_alunos.insert_one({
            "nome": nome,
            "rgm": rgm,
            "curso": curso,
            "horario": horario,
            "bolsista": False,
            "turma": None,
            "trocas_nome": 0
        })

        # Exibe mensagem de sucesso
        messagebox.showinfo(
            "Sucesso",
            "Aluno cadastrado"
        )

    except:

        # Exibe erro caso falhe
        messagebox.showerror(
            "Erro",
            "Erro ao cadastrar aluno"
        )

# Função para atribuir turma
def atribuir_turma(rgm, turma):

    # Busca aluno
    aluno = buscar_aluno(rgm)

    # Verifica se existe
    if not aluno:

        messagebox.showerror(
            "Erro",
            "Aluno não encontrado"
        )

        return

    # Atualiza turma no banco
    colecao_alunos.update_one(
        {"rgm": rgm},
        {"$set": {"turma": turma}}
    )

    # Exibe mensagem de sucesso
    messagebox.showinfo(
        "Sucesso",
        f"{aluno['nome']} agora está na turma {turma}"
    )

# Função para remover aluno da turma
def remover_da_turma(rgm):

    # Busca aluno
    aluno = buscar_aluno(rgm)

    # Verifica existência
    if not aluno:

        messagebox.showerror(
            "Erro",
            "Aluno não encontrado"
        )

        return

    # Remove turma do aluno
    colecao_alunos.update_one(
        {"rgm": rgm},
        {"$set": {"turma": None}}
    )

    # Mensagem de sucesso
    messagebox.showinfo(
        "Sucesso",
        "Aluno removido da turma"
    )

# Função para criar solicitações
def criar_solicitacao(aluno, tipo, valor=None):

    # Insere solicitação no banco
    colecao_solicitacoes.insert_one({
        "rgm": aluno["rgm"],
        "tipo": tipo,
        "valor": valor
    })

    # Mensagem de sucesso
    messagebox.showinfo(
        "Sucesso",
        "Solicitação enviada"
    )

# Função para solicitar troca de nome
def solicitar_troca_nome(aluno, novo_nome):

    # Verifica limite de trocas
    if aluno["trocas_nome"] >= 1:

        messagebox.showerror(
            "Erro",
            "Limite atingido"
        )

        return

    # Verifica nome válido
    if not novo_nome:

        messagebox.showerror(
            "Erro",
            "Nome inválido"
        )

        return

    # Cria solicitação de troca de nome
    criar_solicitacao(
        aluno,
        "troca_nome",
        novo_nome
    )

# Função para aprovar solicitações
def aprovar(s):

    # Pergunta confirmação
    if not messagebox.askyesno(
        "Confirmação",
        "Deseja aprovar esta solicitação?"
    ):
        return

    # Busca aluno
    aluno = buscar_aluno(s["rgm"])

    # Verifica existência
    if not aluno:
        return

    # Aprovação troca de turma
    if s["tipo"] == "troca_turma":

        colecao_alunos.update_one(
            {"rgm": aluno["rgm"]},
            {"$set": {"turma": s["valor"]}}
        )

    # Aprovação remoção de turma
    elif s["tipo"] == "remover_turma":

        colecao_alunos.update_one(
            {"rgm": aluno["rgm"]},
            {"$set": {"turma": None}}
        )

    # Aprovação bolsa
    elif s["tipo"] == "bolsa":

        colecao_alunos.update_one(
            {"rgm": aluno["rgm"]},
            {"$set": {"bolsista": True}}
        )

    # Aprovação troca de nome
    elif s["tipo"] == "troca_nome":

        colecao_alunos.update_one(
            {"rgm": aluno["rgm"]},
            {
                "$set": {"nome": s["valor"]},
                "$inc": {"trocas_nome": 1}
            }
        )

    # Remove solicitação aprovada
    colecao_solicitacoes.delete_one(
        {"_id": s["_id"]}
    )

    # Mensagem de sucesso
    messagebox.showinfo(
        "Aprovado",
        "Solicitação aprovada"
    )

    # Atualiza tela
    ver_solicitacoes()

# Função para recusar solicitações
def recusar(s):

    # Pergunta confirmação
    if not messagebox.askyesno(
        "Confirmação",
        "Deseja recusar esta solicitação?"
    ):
        return

    # Remove solicitação
    colecao_solicitacoes.delete_one(
        {"_id": s["_id"]}
    )

    # Mensagem de recusa
    messagebox.showinfo(
        "Recusado",
        "Solicitação recusada"
    )

    # Atualiza tela
    ver_solicitacoes()

# ======================
# TELAS
# ======================

# Tela inicial do sistema
def tela_inicial():

    # Limpa a tela
    limpar_tela()

    # Cria container principal
    frame = criar_container()

    # Carrega imagem
    img = carregar_imagem("phantom.png")

    # Verifica se imagem foi carregada
    if img:

        # Cria label com imagem
        lbl = tk.Label(frame, image=img, bg=BG)

        # Mantém referência da imagem
        lbl.image = img

        # Posiciona imagem
        lbl.grid(row=0, column=0, pady=10)

    # Botão área do aluno
    criar_botao(
        frame,
        "Área do Aluno",
        tela_login_aluno
    ).grid(row=1, column=0, pady=10)

    # Botão área coordenador
    criar_botao(
        frame,
        "Área do Coordenador",
        tela_coordenador
    ).grid(row=2, column=0, pady=10)

# Tela de login do aluno
def tela_login_aluno():

    limpar_tela()

    frame = criar_container()

    criar_label(
        frame,
        "Login do Aluno",
        14,
        True
    ).grid(row=0, column=0, pady=10)

    # Campo RGM
    rgm = criar_entry_placeholder(
        frame,
        "Digite seu RGM"
    )

    rgm.grid(row=1, column=0, pady=5)

    # Botão entrar
    criar_botao(
        frame,
        "Entrar",
        lambda: login_aluno(
            valor_real(rgm, "Digite seu RGM")
        )
    ).grid(row=2, column=0, pady=10)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_inicial
    ).grid(row=3, column=0)

# Função login aluno
def login_aluno(rgm):

    # Busca aluno
    aluno = buscar_aluno(rgm)

    # Se encontrar abre tela aluno
    if aluno:
        tela_aluno(aluno)

    else:

        # Caso contrário mostra erro
        messagebox.showerror(
            "Erro",
            "Aluno não encontrado"
        )

# Tela do aluno
def tela_aluno(aluno):

    limpar_tela()

    frame = criar_container()

    # Exibe nome e turma
    criar_label(
        frame,
        f"{aluno['nome']} | Turma: {aluno['turma']}",
        12,
        True
    ).grid(row=0, column=0, pady=10)

    # Variável da turma
    turma = tk.StringVar(value="A")

    # Menu de opções de turma
    tk.OptionMenu(
        frame,
        turma,
        "A",
        "B",
        "C"
    ).grid(row=1, column=0)

    # Solicitação troca de turma
    criar_botao(
        frame,
        "Trocar turma",
        lambda: criar_solicitacao(
            aluno,
            "troca_turma",
            turma.get()
        )
    ).grid(row=2, column=0, pady=5)

    # Solicitação remover turma
    criar_botao(
        frame,
        "Remover turma",
        lambda: criar_solicitacao(
            aluno,
            "remover_turma"
        )
    ).grid(row=3, column=0, pady=5)

    # Solicitação bolsa
    criar_botao(
        frame,
        "Solicitar bolsa",
        lambda: criar_solicitacao(
            aluno,
            "bolsa"
        )
    ).grid(row=4, column=0, pady=5)

    # Campo novo nome
    nome = criar_entry_placeholder(
        frame,
        "Novo nome"
    )

    nome.grid(row=5, column=0)

    # Botão troca nome
    criar_botao(
        frame,
        "Trocar nome",
        lambda: solicitar_troca_nome(
            aluno,
            valor_real(nome, "Novo nome")
        )
    ).grid(row=6, column=0, pady=5)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_inicial
    ).grid(row=7, column=0, pady=10)

# Tela coordenador
def tela_coordenador():

    limpar_tela()

    frame = criar_container()

    criar_label(
        frame,
        "Painel do Coordenador",
        16,
        True
    ).grid(row=0, column=0, pady=10)

    # Botão cadastrar
    criar_botao(
        frame,
        "Cadastrar",
        tela_cadastro
    ).grid(row=1, column=0, pady=5)

    # Botão listar alunos
    criar_botao(
        frame,
        "Listar",
        listar_alunos
    ).grid(row=2, column=0, pady=5)

    # Botão atribuir turma
    criar_botao(
        frame,
        "Atribuir turma",
        tela_atribuir
    ).grid(row=3, column=0, pady=5)

    # Botão remover turma
    criar_botao(
        frame,
        "Remover turma",
        tela_remover
    ).grid(row=4, column=0, pady=5)

    # Botão solicitações
    criar_botao(
        frame,
        "Solicitações",
        ver_solicitacoes
    ).grid(row=5, column=0, pady=5)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_inicial
    ).grid(row=6, column=0, pady=10)

# Tela cadastro de aluno
def tela_cadastro():

    limpar_tela()

    frame = criar_container()

    # Campo nome
    nome = criar_entry_placeholder(
        frame,
        "Nome"
    )

    nome.grid(row=0, column=0)

    # Campo RGM
    rgm = criar_entry_placeholder(
        frame,
        "RGM (8 Digitos)"
    )

    rgm.grid(row=1, column=0)

    # Campo curso
    curso = criar_entry_placeholder(
        frame,
        "Curso"
    )

    curso.grid(row=2, column=0)

    # Variável horário
    horario = tk.StringVar(value="Manhã")

    # Menu horário
    tk.OptionMenu(
        frame,
        horario,
        "Manhã",
        "Tarde",
        "Noite"
    ).grid(row=3, column=0)

    # Botão cadastrar
    criar_botao(
        frame,
        "Cadastrar",
        lambda: cadastrar_aluno(
            valor_real(nome, "Nome"),
            valor_real(rgm, "RGM"),
            valor_real(curso, "Curso"),
            horario.get()
        )
    ).grid(row=4, column=0)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_coordenador
    ).grid(row=5, column=0)

# Tela atribuir turma
def tela_atribuir():

    limpar_tela()

    frame = criar_container()

    # Campo RGM
    rgm = criar_entry_placeholder(
        frame,
        "RGM do aluno"
    )

    rgm.grid(row=0, column=0)

    # Variável turma
    turma = tk.StringVar(value="A")

    # Menu turmas
    tk.OptionMenu(
        frame,
        turma,
        "A",
        "B",
        "C"
    ).grid(row=1, column=0)

    # Botão atribuir
    criar_botao(
        frame,
        "Atribuir",
        lambda: atribuir_turma(
            valor_real(rgm, "RGM do aluno"),
            turma.get()
        )
    ).grid(row=2, column=0)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_coordenador
    ).grid(row=3, column=0)

# Tela remover turma
def tela_remover():

    limpar_tela()

    frame = criar_container()

    # Campo RGM
    rgm = criar_entry_placeholder(
        frame,
        "RGM do aluno"
    )

    rgm.grid(row=0, column=0)

    # Botão remover
    criar_botao(
        frame,
        "Remover",
        lambda: remover_da_turma(
            valor_real(rgm, "RGM do aluno")
        )
    ).grid(row=1, column=0)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_coordenador
    ).grid(row=2, column=0)

# Tela listar alunos
def listar_alunos():

    limpar_tela()

    frame = criar_container()

    # Cria tabela
    tabela = tk.Frame(frame, bg="#112D4E")

    tabela.grid(row=0, column=0)

    # Cabeçalhos da tabela
    headers = [
        "Nome",
        "RGM",
        "Curso",
        "Turma",
        "Status"
    ]

    # Cria cabeçalhos
    for col, h in enumerate(headers):

        tk.Label(
            tabela,
            text=h,
            bg="#1E3A5F",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            relief="solid",
            bd=1
        ).grid(row=0, column=col)

    # Busca todos alunos
    alunos = colecao_alunos.find()

    # Percorre alunos
    for i, aluno in enumerate(alunos, start=1):

        # Dados de cada aluno
        dados = [
            aluno["nome"],
            aluno["rgm"],
            aluno["curso"],
            aluno["turma"] if aluno["turma"] else "-",
            "Bolsista" if aluno["bolsista"] else "Normal"
        ]

        # Cria células da tabela
        for j, valor in enumerate(dados):

            tk.Label(
                tabela,
                text=valor,
                bg="#112D4E",
                fg="white",
                font=("Arial", 9),
                width=12,
                relief="solid",
                bd=1
            ).grid(row=i, column=j)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_coordenador
    ).grid(row=1, column=0, pady=10)

# Tela de solicitações
def ver_solicitacoes():

    limpar_tela()

    frame = criar_container()

    # Busca solicitações
    solicitacoes = colecao_solicitacoes.find()

    # Percorre solicitações
    for i, s in enumerate(solicitacoes):

        # Busca aluno relacionado
        aluno = buscar_aluno(s["rgm"])

        if not aluno:
            continue

        # Cria card da solicitação
        card = tk.Frame(
            frame,
            bg="#112D4E",
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )

        card.grid(
            row=i,
            column=0,
            pady=6,
            sticky="ew"
        )

        # Texto da solicitação
        texto = f"{aluno['nome']} → {s['tipo']}"

        # Adiciona valor se existir
        if s["valor"]:
            texto += f" ({s['valor']})"

        # Exibe texto
        tk.Label(
            card,
            text=texto,
            bg="#112D4E",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(
            side="left",
            expand=True,
            fill="x"
        )

        # Frame para botões
        botoes = tk.Frame(
            card,
            bg="#112D4E"
        )

        botoes.pack(side="right")

        # Botão aprovar
        tk.Button(
            botoes,
            text="✔",
            command=lambda sol=s: aprovar(sol),
            bg="#16A34A",
            fg="white",
            width=3
        ).pack(side="left", padx=2)

        # Botão recusar
        tk.Button(
            botoes,
            text="✖",
            command=lambda sol=s: recusar(sol),
            bg="#DC2626",
            fg="white",
            width=3
        ).pack(side="left", padx=2)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_coordenador
    ).grid(row=100, column=0, pady=10)

# ======================
# APP
# ======================

# Cria janela principal
root = tk.Tk()

# Define título da janela
root.title("Phantom Matrículas - Sistema Acadêmico")

# Define tamanho da janela
root.geometry("400x500")

# Define cor de fundo
root.configure(bg=BG)

# Abre tela inicial
tela_inicial()

# Mantém aplicação em execução
root.mainloop()
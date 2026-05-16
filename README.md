Phantom Matrículas

Sistema acadêmico desktop desenvolvido em Python utilizando Tkinter para interface gráfica e MongoDB Atlas como banco de dados.
O sistema permite gerenciamento de alunos, turmas e solicitações acadêmicas de forma simples e intuitiva.

Funcionalidades
Área do Aluno:
Login utilizando RGM
Solicitação de troca de turma
Solicitação de remoção de turma
Solicitação de bolsa
Solicitação de troca de nome
Visualização da turma atual

Área do Coordenador:
Cadastro de alunos
Listagem completa de alunos
Atribuição de turmas
Remoção de alunos das turmas
Aprovação e recusa de solicitações
Controle de bolsistas

Interface

O sistema possui:

Interface gráfica moderna com Tkinter
Componentes reutilizáveis
Placeholders nos campos
Botões estilizados
Sistema de navegação entre telas
Responsividade básica para desktop

Tecnologias Utilizadas:
Python 3
Tkinter
Pillow (PIL)
MongoDB Atlas
PyMongo

Instalação
1️. Clone o repositório
git clone https://github.com/seu-usuario/phantom-matriculas.git
2️. Acesse a pasta do projeto
cd phantom-matriculas
3️. Instale as dependências
pip install pymongo pillow

Configuração do MongoDB:

No código existe a conexão com o MongoDB Atlas:

client = MongoClient("SUA_STRING_DE_CONEXAO")

Substitua pela sua própria string de conexão do MongoDB Atlas.

Executando o Sistema:

python main.py
Estrutura do Projeto
phantom-matriculas/
│
├── main.py
├── phantom.png
├── README.md
Estrutura do Banco de Dados
Coleção: alunos

Exemplo de documento:

{
  "nome": "João Silva",
  "rgm": "12345678",
  "curso": "ADS",
  "horario": "Noite",
  "bolsista": false,
  "turma": "A",
  "trocas_nome": 0
}
Coleção: solicitacoes

Exemplo de documento:

{
  "rgm": "12345678",
  "tipo": "troca_turma",
  "valor": "B"
}

Regras de Negócio:
O RGM deve possuir exatamente 8 dígitos
Não é permitido cadastrar RGMs duplicados
O aluno pode trocar de nome apenas 1 vez
Solicitações precisam ser aprovadas pelo coordenador

Personalização:

As cores principais podem ser alteradas nas variáveis:

BG = "#0D2344"
FG = "white"

Github dos Participantes:
https://github.com/Gablokis

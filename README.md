# 🎭 Palco em Cena

**Sistema de gerenciamento de apresentações e avaliação do desenvolvimento artístico de alunos de teatro.**

O Palco em Cena é uma aplicação web desenvolvida para auxiliar escolas e grupos de teatro na organização de turmas, apresentações e avaliações artísticas.

A plataforma permite que professores acompanhem a evolução dos alunos por meio de avaliações individuais e coletivas, enquanto os estudantes podem consultar seus próprios resultados e acompanhar seu desenvolvimento.

---

## 📌 Funcionalidades

- **Autenticação:** acesso ao sistema por meio de e-mail e senha.
- **Gerenciamento de usuários:** administração de contas e perfis.
- **Gerenciamento de turmas:** organização dos alunos em grupos.
- **Apresentações:** cadastro de apresentações, descrição, data e participantes.
- **Avaliações individuais:** acompanhamento do desempenho de cada aluno.
- **Avaliações coletivas:** avaliação do desempenho geral de uma apresentação.
- **Rascunhos e publicação:** avaliações podem ser salvas como rascunho e publicadas após revisão.
- **Visualização de resultados:** consulta às avaliações conforme o perfil de acesso.
- **Interface responsiva:** adaptação para computadores, tablets e celulares.

## 👥 Perfis de acesso

O sistema possui três perfis:

| Perfil | Permissões |
|---|---|
| Administrador | Gerenciamento de usuários e acesso administrativo. |
| Professor | Gerenciamento de apresentações e avaliações. |
| Aluno | Consulta às próprias avaliações e às avaliações coletivas das apresentações em que participa. |

## 🎯 Critérios de avaliação

As avaliações artísticas utilizam notas de 1 a 10, considerando cinco critérios:

1. Interpretação
2. Expressão corporal
3. Dicção
4. Criatividade
5. Presença de palco

Os professores também podem adicionar observações para registrar pontos positivos e aspectos que podem ser desenvolvidos.

**O objetivo não é criar rankings, mas incentivar o aprendizado e a evolução artística.**

## 🛠️ Tecnologias utilizadas

- **Python** — linguagem de programação.
- **Flask** — framework para desenvolvimento web.
- **SQLite** — banco de dados.
- **HTML5** — estrutura das páginas.
- **CSS3** — estilização e responsividade.
- **Jinja2** — renderização de páginas dinâmicas.

## 📁 Estrutura do projeto

```text
palco-em-cena/
│
├── models/
│   ├── __init__.py
│   ├── avaliacao.py
│   ├── turma.py
│   └── usuario.py
│
├── routes/
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── avaliacoes.py
│   ├── dashboard.py
│   └── turmas.py
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── admin/
│   ├── avaliacoes/
│   ├── turmas/
│   ├── base.html
│   ├── dashboard.html
│   └── login.html
│
├── instance/
├── .env.example
├── .gitignore
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
└── README.md
```

## 🚀 Como executar o projeto

### 1. Pré-requisitos

- Python instalado.
- Git instalado.
- Editor de código, como Visual Studio Code.

### 2. Clonar o repositório

```bash
git clone https://github.com/Patricker487/palco-em-cena.git
```

Entre na pasta:

```bash
cd palco-em-cena
```

### 3. Criar um ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar as variáveis de ambiente

Crie uma cópia do arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Configure as variáveis necessárias no arquivo `.env`, conforme as instruções do projeto.

**Importante:** não compartilhe seu arquivo `.env`, pois ele pode conter informações sensíveis.

### 6. Inicializar o banco de dados

Siga as instruções de inicialização do banco de dados descritas no arquivo `INSTRUCOES.txt` do projeto.

### 7. Executar a aplicação

```bash
python app.py
```

Acesse no navegador o endereço local indicado pelo Flask no terminal.

---

## 📱 Interface responsiva

O Palco em Cena foi desenvolvido com uma interface adaptável a diferentes tamanhos de tela, buscando manter a navegação e a legibilidade em dispositivos móveis e computadores.

## 🎯 Objetivo do projeto

Este projeto foi desenvolvido como uma aplicação prática para organização de atividades teatrais, buscando aplicar conhecimentos de desenvolvimento web, banco de dados, autenticação, controle de acesso e construção de interfaces responsivas.

Também representa uma oportunidade de aprofundar conhecimentos em desenvolvimento de software e construir um projeto funcional para portfólio.

## 👨‍💻 Desenvolvedor

**Patrick**

- GitHub: [@Patricker487](https://github.com/Patricker487)
- Repositório: [Palco em Cena](https://github.com/Patricker487/palco-em-cena)

---

*Palco em Cena — Desenvolvimento artístico em foco.*

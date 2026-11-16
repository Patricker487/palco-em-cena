# Palco em Cena — primeira versão

## Requisitos
- Windows 10
- Python 3.13
- VS Code (opcional, mas recomendado)

## 1. Criar e ativar o ambiente virtual

No terminal, dentro desta pasta:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, use o terminal CMD:

```bat
.venv\Scripts\activate.bat
```

## 2. Instalar dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configurar a chave da aplicação

Copie `.env.example` para `.env` e substitua o valor de `SECRET_KEY` por uma chave longa e aleatória. Não compartilhe esse arquivo nem o envie ao GitHub.

## 4. Criar o banco de dados

```powershell
flask --app app init-db
```

## 5. Criar o primeiro administrador

```powershell
flask --app app create-admin
```

O terminal solicitará nome, e-mail e senha. A senha será armazenada com hash.

## 6. Executar

```powershell
flask --app app run --debug
```

Abra http://127.0.0.1:5000 no navegador.

## Observações
- Esta é uma base local de desenvolvimento, ainda não pronta para publicação na internet.
- Não há cadastro público: a criação de usuários será feita por uma área administrativa nas próximas etapas.
- Antes de usar com alunos reais, precisamos implementar gestão de usuários, autorização por perfil, trilha de auditoria e regras de privacidade adequadas.

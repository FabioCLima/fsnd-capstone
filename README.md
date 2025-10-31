# Casting Agency API - FSND Capstone Project

API para gerenciar atores e filmes de uma agência de casting, desenvolvida como projeto final do Full Stack Nanodegree da Udacity.

## Tecnologias

- **Python 3.10+**
- **Flask** - Framework web
- **SQLAlchemy 2.0** - ORM com tipagem moderna
- **Pydantic** - Validação de dados e schemas
- **PostgreSQL** - Banco de dados
- **UV** - Gerenciador de dependências moderno
- **Heroku** - Deploy em produção

## Estrutura do Projeto

```
starter/
├── app.py              # Aplicação Flask principal
├── models.py           # Modelos SQLAlchemy e Schemas Pydantic
├── test_app.py         # Testes unitários
├── pyproject.toml      # Configuração do UV e dependências
├── requirements.txt    # Dependências para Heroku
├── Procfile           # Configuração Heroku
├── runtime.txt        # Versão do Python para Heroku
├── setup.sh           # Variáveis de ambiente (local)
└── .env.example       # Exemplo de variáveis de ambiente
```

## Modelos de Dados

### Actor
- `id` (Integer, Primary Key)
- `name` (String, required)
- `age` (Integer, required)
- `gender` (String, required)
- `created_at` (DateTime)

### Movie
- `id` (Integer, Primary Key)
- `title` (String, required)
- `release_date` (DateTime, required)
- `created_at` (DateTime)

### MovieActor (Association Table)
- Relacionamento muitos-para-muitos entre Movies e Actors

## Instalação e Configuração

### Pré-requisitos

1. **PostgreSQL** instalado e rodando
2. **Python 3.10+**
3. **UV** (gerenciador de dependências)

### Instalação do UV

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Ou via pip
pip install uv
```

### Configuração do Projeto

1. **Clone o repositório**
```bash
cd projects/capstone/starter
```

2. **Crie o banco de dados**
```bash
# Conecte ao PostgreSQL
sudo -u postgres psql

# Crie o banco de dados
CREATE DATABASE capstone;

# Saia do psql
\q
```

3. **Configure as variáveis de ambiente**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env com suas configurações
nano .env
```

4. **Instale as dependências com UV**
```bash
# Cria ambiente virtual e instala dependências
uv sync

# Ou usando requirements.txt tradicional
uv pip install -r requirements.txt
```

5. **Configure o ambiente (método alternativo com setup.sh)**
```bash
chmod +x setup.sh
source setup.sh
```

6. **Execute as migrações**
```bash
# Ative o ambiente virtual do UV
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows

# Inicialize as migrações
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Executando a Aplicação

### Modo Desenvolvimento (com UV)

```bash
# Com UV (recomendado)
uv run python app.py

# Ou ativando o ambiente virtual
source .venv/bin/activate
python app.py
```

A API estará disponível em: `http://localhost:8080`

### Modo Produção (com Gunicorn)

```bash
uv run gunicorn app:APP
```

## Endpoints da API

### Health Check
```http
GET /
```

### Movies

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/movies` | Lista todos os filmes |
| GET | `/api/movies/<id>` | Busca filme por ID |
| POST | `/api/movies` | Cria novo filme |
| PATCH | `/api/movies/<id>` | Atualiza filme |
| DELETE | `/api/movies/<id>` | Remove filme |

### Actors

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/actors` | Lista todos os atores |
| GET | `/api/actors/<id>` | Busca ator por ID |
| POST | `/api/actors` | Cria novo ator |
| PATCH | `/api/actors/<id>` | Atualiza ator |
| DELETE | `/api/actors/<id>` | Remove ator |

## Exemplos de Uso

### Criar um Ator

```bash
curl -X POST http://localhost:8080/api/actors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tom Hanks",
    "age": 67,
    "gender": "Male"
  }'
```

### Criar um Filme

```bash
curl -X POST http://localhost:8080/api/movies \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Forrest Gump",
    "release_date": "1994-07-06T00:00:00"
  }'
```

### Listar Atores

```bash
curl http://localhost:8080/api/actors
```

### Atualizar um Ator

```bash
curl -X PATCH http://localhost:8080/api/actors/1 \
  -H "Content-Type: application/json" \
  -d '{
    "age": 68
  }'
```

## Validação com Pydantic

O projeto utiliza Pydantic para validação automática de dados:

- **Campos obrigatórios** são validados automaticamente
- **Tipos de dados** são verificados (int, str, datetime)
- **Constraints** aplicados (idade entre 1-150, strings não vazias)
- **Respostas padronizadas** com serialização automática

Exemplo de erro de validação:
```json
{
  "success": false,
  "error": "Validation error",
  "details": [
    {
      "type": "int_parsing",
      "loc": ["age"],
      "msg": "Input should be a valid integer"
    }
  ]
}
```

## Deploy no Heroku

### 1. Instale o Heroku CLI

```bash
# Linux
curl https://cli-assets.heroku.com/install.sh | sh

# macOS
brew tap heroku/brew && brew install heroku
```

### 2. Faça login no Heroku

```bash
heroku login
```

### 3. Crie a aplicação

```bash
# Crie o app
heroku create nome-do-seu-app

# Adicione o addon do PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Configure as variáveis de ambiente
heroku config:set FLASK_APP=app.py
heroku config:set FLASK_ENV=production
```

### 4. Deploy

```bash
# Faça commit das alterações
git add .
git commit -m "Prepare for Heroku deployment"

# Faça deploy
git push heroku master

# Execute as migrações
heroku run flask db upgrade

# Abra a aplicação
heroku open
```

### 5. Comandos úteis Heroku

```bash
# Ver logs
heroku logs --tail

# Executar comandos
heroku run python

# Ver configurações
heroku config

# Resetar banco de dados
heroku pg:reset DATABASE_URL
heroku run flask db upgrade
```

## Testes

```bash
# Execute os testes
uv run pytest

# Com coverage
uv run pytest --cov=. --cov-report=html
```

## Comandos UV Úteis

```bash
# Adicionar nova dependência
uv add nome-do-pacote

# Adicionar dependência de desenvolvimento
uv add --dev nome-do-pacote

# Sincronizar dependências
uv sync

# Executar script
uv run python script.py

# Atualizar dependências
uv lock --upgrade
```

## Estrutura de Resposta

### Sucesso
```json
{
  "success": true,
  "actors": [...],
  "total_actors": 10
}
```

### Erro
```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```

## Próximos Passos

- [ ] Implementar autenticação Auth0
- [ ] Adicionar roles-based access control (RBAC)
- [ ] Implementar paginação nos endpoints
- [ ] Adicionar filtros e busca
- [ ] Implementar relacionamento Movie-Actor endpoints
- [ ] Adicionar testes de integração
- [ ] Configurar CI/CD

## Licença

Este projeto faz parte do Full Stack Nanodegree da Udacity.

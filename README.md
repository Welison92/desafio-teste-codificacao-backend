# Lu Estilo 👕

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Perfil-blue?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/welisonsantos92)

## 🏗️ Estrutura do README

- [Descrição](#-descrição)
- [Problema e Solução](#-problema-e-solução)
- [Tecnologias e Ferramentas Utilizadas](#-tecnologias-e-ferramentas-utilizadas)
- [Ferramentas de Qualidade de Código](#-ferramentas-de-qualidade-de-código)
- [Requisitos](#-requisitos)
- [Executando o Projeto](#-executando-o-projeto)
- [Autenticação](#-autenticação)
- [Estrutura de Dados](#-estrutura-de-dados)
- [Endpoints](#-endpoints)

## 📝 Descrição

<p align="justify">
Este projeto é uma API RESTful desenvolvida para a <strong>Lu Estilo</strong>, uma empresa de confecção que busca facilitar a comunicação entre o time comercial, os clientes e a empresa, criando novos canais de vendas. A API foi construída com <strong>Python</strong> e <strong>FastAPI</strong> no backend, destinada a ser consumida por uma interface frontend desenvolvida por outro time. A aplicação gerencia usuários, clientes, pedidos e produtos, utilizando autenticação JWT para segurança e um banco de dados relacional para persistência.
</p>

## ⚠️️ Problema e Solução

<p align="justify">
<strong>Problema</strong>: A Lu Estilo não possui ferramentas que facilitem a criação de novos canais de vendas, dificultando a interação do time comercial com os clientes.
</p>

<p align="justify">
<strong>Solução</strong>: Desenvolvimento de uma API RESTful utilizando <strong>FastAPI</strong> para fornecer dados e funcionalidades que otimizem a comunicação entre o time comercial, os clientes e a empresa, permitindo a integração com uma interface frontend.
</p>

## 🛠️ Tecnologias e Ferramentas Utilizadas

- **Python**: Linguagem de programação utilizada para o desenvolvimento do backend;
- **FastAPI**: Framework web para construção de APIs rápidas e eficientes;
- **Uvicorn**: Servidor ASGI para rodar a aplicação FastAPI;
- **SQLAlchemy**: ORM para interação com bancos de dados relacionais;
- **PostgreSQL**: Banco de dados relacional (usando o adaptador `psycopg2`);
- **Alembic**: Ferramenta para gerenciamento de migrações de banco de dados;
- **Pydantic**: Validação de dados e gerenciamento de configurações com tipagem;
- **python-dotenv**: Carregamento de variáveis de ambiente a partir de arquivos `.env`;
- **Git**: Sistema de controle de versão para gerenciar o código-fonte;
- **FastAPI Security**: Suporte para autenticação com OAuth2 e JWT;
- **Passlib**: Biblioteca para hash de senhas;
- **Jose**: Biblioteca para manipulação de tokens JWT;
- **Starlette**: Middleware para suporte a CORS e respostas JSON.

## 🧰️ Ferramentas de Qualidade de Código

- **Flake8**: Ferramenta de linting para verificar o estilo do código Python.

  - Para verificar a conformidade com o PEP 8, execute:

    ```bash
    flake8 .
    ```

  - Para verificar um arquivo específico:

    ```bash
    flake8 nome_do_arquivo.py
    ```

- **Isort**: Ferramenta para organizar automaticamente as importações no código Python.

  - Para organizar as importações em todos os arquivos:

    ```bash
    isort .
    ```

  - Para organizar as importações em um arquivo específico:

    ```bash
    isort nome_do_arquivo.py
    ```

## 📋 Requisitos

Certifique-se de ter os seguintes requisitos instalados:

<div style="display: flex; align-items: center; gap: 10px;">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="40" height="40"/>
  <div style="display: flex; flex-direction: column;">
    <a href="https://www.python.org/" style="text-decoration: none;">Python</a>
  </div>
</div>

<div style="display: flex; align-items: center; gap: 10px;">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" alt="PostgreSQL" width="40" height="40"/>
  <div style="display: flex; flex-direction: column;">
    <a href="https://www.postgresql.org/" style="text-decoration: none;">PostgreSQL</a>
    <a href="https://www.pgadmin.org/download/" style="text-decoration: none;">PgAdmin</a>
  </div>
</div>

<div style="display: flex; align-items: center; gap: 10px;">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" alt="Git" width="40" height="40"/>
  <div style="display: flex; flex-direction: column;">
    <a href="https://git-scm.com/" style="text-decoration: none;">Git</a>
  </div>
</div>

<div style="display: flex; align-items: center; gap: 10px;">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg" alt="Docker" width="40" height="40"/>
  <div style="display: flex; flex-direction: column;">
    <a href="https://www.docker.com/get-started" style="text-decoration: none;">Docker</a>
    <a href="https://docs.docker.com/compose/" style="text-decoration: none;">Docker Compose</a>
  </div>
</div>

## 🚀 Executando o Projeto

1. **Verifique a instalação do Docker e Docker Compose**:

   ```bash
   docker --version
   ```
   
   ```bash
   docker-compose --version
   ```

2. **Clone o repositório**:

   ```bash
   git clone https://github.com/Welison92/desafio-teste-codificacao-backend.git.
   ```

3. **Configure as variáveis de ambiente**:

   1️⃣ Crie a pasta `env`:

     ```bash
     mkdir env
     ```
   2️⃣ Navegue até a pasta `env`:

     ```bash
     cd env
     ```
   3️⃣ Crie o arquivo `.env`:

     ```bash
     touch .env
     ```

   - Adicione as variáveis de ambiente necessárias no arquivo `.env`.

4. **Inicie os serviços**:

   Na pasta raiz do projeto (onde está o arquivo `docker-compose.yml`), execute:

   ```bash
   docker-compose up --build
   ```

   ou, para rodar em modo detached:

   ```bash
   docker compose up -d --build
   ```

   Aguarde até que a configuração do contêiner seja concluída. Se tudo estiver correto, o servidor estará disponível na porta `8080`. Acesse a documentação da API em:

   - http://localhost:8080/docs
   - http://localhost:8080/redoc

5. **Aplicar migrações do banco de dados**:

   ```bash
   alembic revision --autogenerate -m "Criação das tabelas"
   ```

    Esse comando cria um novo arquivo de migração com base nas alterações feitas no modelo de dados.   

   ```bash
   alembic upgrade head
   ```

    Esse comando aplica as migrações pendentes ao banco de dados.

6. **Parar a aplicação**:

   ```bash
   docker-compose stop
   ```

   ou

   ```bash
   docker compose stop
   ```

7. **Reiniciar a aplicação**:

   ```bash
   docker-compose start
   ```

   ou

   ```bash
   docker compose start
   ```

8. **Remover contêineres, redes e volumes**:

   ```bash
   docker-compose down
   ```

   ou

   ```bash
   docker compose down
   ```

9. **Iniciar novamente os serviços**:

   ```bash
   docker-compose up -d
   ```

   ou

   ```bash
   docker compose up -d
   ```

## 🛡️ Autenticação

<p align="justify">
A API utiliza autenticação baseada em <strong>JWT (JSON Web Tokens)</strong> com o esquema <strong>OAuth2PasswordBearer</strong>. As senhas são hasheadas utilizando a biblioteca <strong>Passlib</strong> com o algoritmo <code>bcrypt</code>. Os endpoints protegidos exigem um token de acesso válido, que pode ser obtido via login no endpoint de autenticação.
</p>

## 🗂️ Estrutura de Dados

A aplicação gerencia as seguintes entidades no banco de dados:

- **UserModel**: Gerenciamento de usuários autenticados;
- **ClientModel**: Cadastro de clientes da Lu Estilo;
- **ProductModel**: Catálogo de produtos da confecção;
- **OrderModel** e **OrderItemModel**: Gerenciamento de pedidos e itens associados.

<p align="justify">
Os modelos são definidos com <strong>SQLAlchemy</strong> e validados com <strong>Pydantic</strong>. As migrações são gerenciadas pelo <strong>Alembic</strong>.
</p>

## 🌐 Endpoints

A API é dividida em módulos (routers) para organização:

- **auth**: Endpoints para autenticação e gerenciamento de usuários;
- **clients**: Endpoints para gerenciamento de clientes;
- **orders**: Endpoints para criação e consulta de pedidos;
- **products**: Endpoints para gerenciamento de produtos.

<p align="justify">
Consulte a documentação interativa em <code>http://localhost:8080/docs</code> para detalhes dos endpoints.
</p>
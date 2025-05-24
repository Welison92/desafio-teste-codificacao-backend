## Gerenciamento de Migrações com Alembic

O Alembic é uma ferramenta de migração de banco de dados que facilita a sincronização entre as alterações nos modelos da sua aplicação (definidos, por exemplo, em `models.py` quando usando SQLAlchemy) e o esquema do banco de dados. Abaixo, é explicado os passos principais para criar e aplicar migrações automaticamente após alterações nos modelos.

### 1. Gerando uma Migração Automaticamente

Quando você modifica um modelo (por exemplo, adiciona uma nova coluna, altera um tipo de dado ou remove uma tabela em `models.py`), é necessário criar um script de migração para refletir essas mudanças no banco de dados. Para isso, use o comando abaixo:

```bash
alembic revision --autogenerate -m "Descrição da alteração"
```

**Detalhes do comando:**
- **`--autogenerate`**: Instrui o Alembic a inspecionar automaticamente os modelos definidos (em `models.py`) e comparar com o estado atual do banco de dados, gerando um script de migração com as alterações detectadas.
- **`-m "Descrição da alteração"`**: Adiciona uma mensagem descritiva para identificar o propósito da migração (ex.: `"Adiciona coluna email em Usuario"`). Essa descrição é opcional, mas altamente recomendada para manter um histórico claro das alterações.

**Exemplo:**
```bash
alembic revision --autogenerate -m "Adiciona campo idade na tabela usuarios"
```

O comando criará um novo arquivo de migração no diretório `alembic/versions/`, contendo instruções para aplicar (`upgrade`) e reverter (`downgrade`) as alterações.

**Nota:** Após gerar a migração, **revise o arquivo gerado** para garantir que as alterações detectadas pelo Alembic correspondem às suas intenções. Em alguns casos, o `--autogenerate` pode não capturar todas as mudanças (como renomeações ou alterações complexas) corretamente.

### 2. Aplicando a Migração ao Banco de Dados

Para atualizar o banco de dados com as mudanças definidas no script de migração, execute o seguinte comando:

```bash
alembic upgrade head
```

**Detalhes do comando:**
- **`upgrade`**: Aplica as alterações definidas no script de migração ao banco de dados.
- **`head`**: Indica que o banco deve ser atualizado para a versão mais recente (ou seja, a última migração criada).

**Exemplo:**
```bash
alembic upgrade head
```

Após executar este comando, o esquema do banco de dados será atualizado para refletir as mudanças feitas nos modelos, como a adição de novas colunas, tabelas ou índices.

### 3. Resultado Esperado

Se tudo estiver configurado corretamente:
- O Alembic detectará as diferenças entre os modelos (`models.py`) e o estado atual do banco de dados.
- O script de migração gerado conterá as instruções SQL necessárias para alinhar o banco com os modelos.
- Após aplicar a migração com `alembic upgrade head`, o banco de dados estará sincronizado com as alterações feitas nos modelos.

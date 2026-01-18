# 📚 Blog de Negócios - Flask + Bootstrap + MySQL

Sistema de blog simples e funcional desenvolvido com Flask, Bootstrap e MySQL.

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.7+
- MySQL 5.7+
- pip (gerenciador de pacotes Python)

### Passo 1: Clonar o repositório
```bash
git clone https://github.com/fabricioofc/PROJETOAUTORIAWEBAF.git
cd blog-flask
```

### Passo 2: Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### Passo 3: Instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar banco de dados

1. Abra o MySQL:
```bash
mysql -u root -p
```

2. Execute o script SQL:
```bash
source schema.sql;
```

Ou copie e cole o conteúdo de `schema.sql` no MySQL.

### Passo 5: Rodar a aplicação
```bash
python app.py
```

A aplicação estará disponível em: **http://localhost:5000**

---

## 📖 Como Usar

### Página Inicial
- Acesse: http://localhost:5000/
- Veja todos os posts publicados

### Visualizar Post
- Clique em "Ler Mais" em qualquer post
- O contador de visualizações será incrementado

### Dashboard Admin
- Acesse: http://localhost:5000/admin
- Gerencie posts, categorias e autores

### Gerenciar Posts
1. Vá para Admin → Posts
2. Clique em "+ Novo Post"
3. Preencha os campos:
   - **Título**: Nome do artigo
   - **Slug**: URL amigável (ex: meu-primeiro-post)
   - **Categoria**: Escolha uma categoria
   - **Autor**: Escolha um autor
   - **Conteúdo**: Texto do post
   - **Status**: Rascunho/Publicado/Arquivado
4. Clique em "Criar Post"

### Gerenciar Categorias
1. Vá para Admin → Categorias
2. Clique em "+ Nova Categoria"
3. Preencha nome e descrição
4. Clique em "Criar Categoria"

### Gerenciar Autores
1. Vá para Admin → Autores
2. Clique em "+ Novo Autor"
3. Preencha nome, email e bio
4. Clique em "Criar Autor"

---

## 📁 Estrutura do Projeto

```
blog-flask/
├── app.py                  # Aplicação principal
├── schema.sql              # Script do banco de dados
├── requirements.txt        # Dependências Python
├── README.md               # Este arquivo
├── templates/              # Templates HTML
│   ├── base.html          # Template base
│   ├── index.html         # Página inicial
│   ├── post.html          # Visualizar post
│   └── admin/             # Templates admin
│       ├── dashboard.html
│       ├── posts.html
│       ├── criar_post.html
│       ├── editar_post.html
│       ├── categorias.html
│       ├── criar_categoria.html
│       ├── editar_categoria.html
│       ├── autores.html
│       ├── criar_autor.html
│       └── editar_autor.html
└── static/                # Arquivos estáticos
    └── css/
        └── style.css      # Estilos customizados
```

---

## 🗄️ Banco de Dados

### Tabelas

**Categorias**
- ID_Categoria (INT, PK, AUTO_INCREMENT)
- Nome (VARCHAR 50, UNIQUE)
- Descricao (TEXT)

**Autores**
- ID_Autor (INT, PK, AUTO_INCREMENT)
- Nome (VARCHAR 100)
- Email (VARCHAR 150, UNIQUE)
- Bio (TEXT)

**Posts**
- ID_Post (INT, PK, AUTO_INCREMENT)
- Titulo (VARCHAR 200)
- Slug (VARCHAR 200, UNIQUE)
- Conteudo (TEXT)
- ID_Categoria (INT, FK)
- ID_Autor (INT, FK)
- Data_Publicacao (DATETIME)
- Visualizacoes (INT)
- Status (VARCHAR 20) - Rascunho/Publicado/Arquivado
- Índices: FULLTEXT, categoria_data, status

---

## 🔍 Consultas SQL Otimizadas

```sql
-- Buscar posts publicados por categoria e data
SELECT * FROM Posts 
WHERE ID_Categoria = 3 AND Data_Publicacao > '2025-01-01';

-- Busca full-text em título e conteúdo
SELECT * FROM Posts 
WHERE MATCH(Titulo, Conteudo) AGAINST('MySQL banco de dados');
```

---

## 🐛 Troubleshooting

### Erro: "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

### Erro: "Access denied for user 'root'@'localhost'"
Verifique as credenciais no `app.py` (linhas 10-13)

### Erro: "Unknown database 'blog_db'"
Execute o script `schema.sql` no MySQL

---

## 📝 Notas

- O blog roda **apenas localmente** (localhost:5000)
- Não há autenticação no admin (use em ambiente seguro)
- Dados de exemplo já estão carregados no banco

---

**Desenvolvido com Flask + Bootstrap + MySQL** 🚀

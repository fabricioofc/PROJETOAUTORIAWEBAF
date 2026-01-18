-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS blog_db;
USE blog_db;

-- Tabela de Categorias
CREATE TABLE IF NOT EXISTS Categorias (
    ID_Categoria INT NOT NULL AUTO_INCREMENT,
    Nome VARCHAR(50) NOT NULL UNIQUE,
    Descricao TEXT,
    PRIMARY KEY (ID_Categoria)
);

-- Tabela de Autores
CREATE TABLE IF NOT EXISTS Autores (
    ID_Autor INT NOT NULL AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL,
    Email VARCHAR(150) NOT NULL,
    Bio TEXT,
    PRIMARY KEY (ID_Autor),
    UNIQUE KEY uk_autor_email (Email)
);

-- Tabela de Posts com múltiplas constraints e índices
CREATE TABLE IF NOT EXISTS Posts (
    ID_Post INT NOT NULL AUTO_INCREMENT,
    Titulo VARCHAR(200) NOT NULL,
    Slug VARCHAR(200) NOT NULL UNIQUE,
    Conteudo TEXT NOT NULL,
    ID_Categoria INT,
    ID_Autor INT,
    Data_Publicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    Visualizacoes INT DEFAULT 0,
    Status VARCHAR(20) DEFAULT 'Rascunho',
    PRIMARY KEY (ID_Post),
    FOREIGN KEY (ID_Categoria) REFERENCES Categorias(ID_Categoria) ON DELETE SET NULL,
    FOREIGN KEY (ID_Autor) REFERENCES Autores(ID_Autor) ON DELETE RESTRICT,
    CHECK (Status IN ('Rascunho', 'Publicado', 'Arquivado')),
    FULLTEXT INDEX ft_titulo_conteudo (Titulo, Conteudo),
    KEY idx_post_autor (ID_Autor),
    INDEX idx_data (Data_Publicacao),
    INDEX idx_categoria_data (ID_Categoria, Data_Publicacao),
    INDEX idx_status (Status)
);

-- Inserir categorias de exemplo
INSERT INTO Categorias (Nome, Descricao) VALUES
('Tecnologia', 'Artigos sobre tecnologia e inovação'),
('Programação', 'Tutoriais e dicas de programação'),
('Banco de Dados', 'Conteúdo sobre bancos de dados');

-- Inserir autores de exemplo
INSERT INTO Autores (Nome, Email, Bio) VALUES
('João Silva', 'joao@example.com', 'Desenvolvedor web com 5 anos de experiência'),
('Maria Santos', 'maria@example.com', 'Especialista em banco de dados'),
('Pedro Costa', 'pedro@example.com', 'Entusiasta de tecnologia e inovação');

-- Inserir posts de exemplo
INSERT INTO Posts (Titulo, Slug, Conteudo, ID_Categoria, ID_Autor, Status) VALUES
('Aprendendo MySQL', 'aprendendo-mysql', 'Neste artigo vamos aprender os fundamentos do MySQL, desde instalação até consultas avançadas.', 3, 2, 'Publicado'),
('Python para Iniciantes', 'python-iniciantes', 'Python é uma linguagem de programação versátil e fácil de aprender. Ideal para iniciantes.', 2, 1, 'Publicado'),
('Inteligência Artificial', 'inteligencia-artificial', 'A IA está transformando o mundo. Conheça as principais aplicações e tendências.', 1, 3, 'Rascunho'),
('Web Design Responsivo', 'web-design-responsivo', 'Aprenda a criar sites que funcionam em qualquer dispositivo.', 1, 1, 'Publicado'),
('Segurança em Aplicações Web', 'seguranca-web', 'Dicas e boas práticas para manter suas aplicações seguras.', 2, 2, 'Publicado');

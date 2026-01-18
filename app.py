from flask import Flask, render_template, request, redirect, url_for, flash
import MySQLdb
from MySQLdb import cursors
import re

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Configuração do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blog_db'

mysql = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    passwd=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

def get_db():
    """Retorna conexão com o banco de dados"""
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

# ============================================
# ROTAS - PÁGINA INICIAL
# ============================================

@app.route('/')
def index():
    """Página inicial com listagem de posts publicados"""
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    
    # Buscar posts publicados
    cursor.execute("""
        SELECT p.ID_Post, p.Titulo, p.Slug, p.Conteudo, p.Data_Publicacao, 
               p.Visualizacoes, c.Nome as Categoria, a.Nome as Autor
        FROM Posts p
        LEFT JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
        LEFT JOIN Autores a ON p.ID_Autor = a.ID_Autor
        WHERE p.Status = 'Publicado'
        ORDER BY p.Data_Publicacao DESC
    """)
    posts = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', posts=posts)

@app.route('/post/<slug>')
def view_post(slug):
    """Visualizar post individual"""
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    
    # Buscar post
    cursor.execute("""
        SELECT p.ID_Post, p.Titulo, p.Slug, p.Conteudo, p.Data_Publicacao, 
               p.Visualizacoes, c.Nome as Categoria, a.Nome as Autor
        FROM Posts p
        LEFT JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
        LEFT JOIN Autores a ON p.ID_Autor = a.ID_Autor
        WHERE p.Slug = %s AND p.Status = 'Publicado'
    """, (slug,))
    post = cursor.fetchone()
    
    if post:
        # Incrementar visualizações
        cursor.execute("UPDATE Posts SET Visualizacoes = Visualizacoes + 1 WHERE ID_Post = %s", (post['ID_Post'],))
        conn.commit()
    
    conn.close()
    
    if not post:
        return "Post não encontrado", 404
    
    return render_template('post.html', post=post)

# ============================================
# ROTAS - ADMIN (DASHBOARD)
# ============================================

@app.route('/admin')
def admin_dashboard():
    """Dashboard administrativo"""
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    
    # Contar posts, categorias e autores
    cursor.execute("SELECT COUNT(*) as count FROM Posts WHERE Status = 'Publicado'")
    posts_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM Categorias")
    categorias_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM Autores")
    autores_count = cursor.fetchone()['count']
    
    conn.close()
    
    return render_template('admin/dashboard.html', 
                         posts_count=posts_count,
                         categorias_count=categorias_count,
                         autores_count=autores_count)

# ============================================
# ROTAS - CATEGORIAS
# ============================================

@app.route('/admin/categorias')
def admin_categorias():
    """Listar categorias"""
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute("SELECT * FROM Categorias ORDER BY Nome")
    categorias = cursor.fetchall()
    conn.close()
    
    return render_template('admin/categorias.html', categorias=categorias)

@app.route('/admin/categorias/criar', methods=['GET', 'POST'])
def criar_categoria():
    """Criar nova categoria"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        
        if not nome:
            flash('Nome da categoria é obrigatório', 'error')
            return redirect(url_for('criar_categoria'))
        
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Categorias (Nome, Descricao) VALUES (%s, %s)", 
                         (nome, descricao))
            conn.commit()
            flash('Categoria criada com sucesso!', 'success')
            return redirect(url_for('admin_categorias'))
        except Exception as e:
            flash(f'Erro ao criar categoria: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('admin/criar_categoria.html')

@app.route('/admin/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    """Editar categoria"""
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        
        if not nome:
            flash('Nome da categoria é obrigatório', 'error')
            return redirect(url_for('editar_categoria', id=id))
        
        try:
            cursor.execute("UPDATE Categorias SET Nome = %s, Descricao = %s WHERE ID_Categoria = %s",
                         (nome, descricao, id))
            conn.commit()
            flash('Categoria atualizada com sucesso!', 'success')
            return redirect(url_for('admin_categorias'))
        except Exception as e:
            flash(f'Erro ao atualizar categoria: {str(e)}', 'error')
    
    cursor.execute("SELECT * FROM Categorias WHERE ID_Categoria = %s", (id,))
    categoria = cursor.fetchone()
    conn.close()
    
    if not categoria:
        return "Categoria não encontrada", 404
    
    return render_template('admin/editar_categoria.html', categoria=categoria)

@app.route('/admin/categorias/deletar/<int:id>')
def deletar_categoria(id):
    """Deletar categoria"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM Categorias WHERE ID_Categoria = %s", (id,))
        conn.commit()
        flash('Categoria deletada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao deletar categoria: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin_categorias'))

# ============================================
# ROTAS - AUTORES
# ============================================

@app.route('/admin/autores')
def admin_autores():
    """Listar autores"""
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute("SELECT * FROM Autores ORDER BY Nome")
    autores = cursor.fetchall()
    conn.close()
    
    return render_template('admin/autores.html', autores=autores)

@app.route('/admin/autores/criar', methods=['GET', 'POST'])
def criar_autor():
    """Criar novo autor"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        bio = request.form.get('bio')
        
        if not nome or not email:
            flash('Nome e email são obrigatórios', 'error')
            return redirect(url_for('criar_autor'))
        
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Autores (Nome, Email, Bio) VALUES (%s, %s, %s)",
                         (nome, email, bio))
            conn.commit()
            flash('Autor criado com sucesso!', 'success')
            return redirect(url_for('admin_autores'))
        except Exception as e:
            flash(f'Erro ao criar autor: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('admin/criar_autor.html')

@app.route('/admin/autores/editar/<int:id>', methods=['GET', 'POST'])
def editar_autor(id):
    """Editar autor"""
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        bio = request.form.get('bio')
        
        if not nome or not email:
            flash('Nome e email são obrigatórios', 'error')
            return redirect(url_for('editar_autor', id=id))
        
        try:
            cursor.execute("UPDATE Autores SET Nome = %s, Email = %s, Bio = %s WHERE ID_Autor = %s",
                         (nome, email, bio, id))
            conn.commit()
            flash('Autor atualizado com sucesso!', 'success')
            return redirect(url_for('admin_autores'))
        except Exception as e:
            flash(f'Erro ao atualizar autor: {str(e)}', 'error')
    
    cursor.execute("SELECT * FROM Autores WHERE ID_Autor = %s", (id,))
    autor = cursor.fetchone()
    conn.close()
    
    if not autor:
        return "Autor não encontrado", 404
    
    return render_template('admin/editar_autor.html', autor=autor)

@app.route('/admin/autores/deletar/<int:id>')
def deletar_autor(id):
    """Deletar autor"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM Autores WHERE ID_Autor = %s", (id,))
        conn.commit()
        flash('Autor deletado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao deletar autor: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin_autores'))

# ============================================
# ROTAS - POSTS
# ============================================

@app.route('/admin/posts')
def admin_posts():
    """Listar posts"""
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute("""
        SELECT p.ID_Post, p.Titulo, p.Slug, p.Data_Publicacao, p.Status, 
               p.Visualizacoes, c.Nome as Categoria, a.Nome as Autor
        FROM Posts p
        LEFT JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
        LEFT JOIN Autores a ON p.ID_Autor = a.ID_Autor
        ORDER BY p.Data_Publicacao DESC
    """)
    posts = cursor.fetchall()
    conn.close()
    
    return render_template('admin/posts.html', posts=posts)

@app.route('/admin/posts/criar', methods=['GET', 'POST'])
def criar_post():
    """Criar novo post"""
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        slug = request.form.get('slug')
        conteudo = request.form.get('conteudo')
        categoria_id = request.form.get('categoria_id')
        autor_id = request.form.get('autor_id')
        status = request.form.get('status')
        
        if not titulo or not slug or not conteudo:
            flash('Título, slug e conteúdo são obrigatórios', 'error')
            return redirect(url_for('criar_post'))
        
        try:
            cursor.execute("""
                INSERT INTO Posts (Titulo, Slug, Conteudo, ID_Categoria, ID_Autor, Status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (titulo, slug, conteudo, categoria_id if categoria_id else None, 
                  autor_id if autor_id else None, status))
            conn.commit()
            flash('Post criado com sucesso!', 'success')
            return redirect(url_for('admin_posts'))
        except Exception as e:
            flash(f'Erro ao criar post: {str(e)}', 'error')
    
    cursor.execute("SELECT * FROM Categorias ORDER BY Nome")
    categorias = cursor.fetchall()
    cursor.execute("SELECT * FROM Autores ORDER BY Nome")
    autores = cursor.fetchall()
    conn.close()
    
    return render_template('admin/criar_post.html', categorias=categorias, autores=autores)

@app.route('/admin/posts/editar/<int:id>', methods=['GET', 'POST'])
def editar_post(id):
    """Editar post"""
    conn = get_db()
    cursor = conn.cursor(cursors.DictCursor)
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        slug = request.form.get('slug')
        conteudo = request.form.get('conteudo')
        categoria_id = request.form.get('categoria_id')
        autor_id = request.form.get('autor_id')
        status = request.form.get('status')
        
        if not titulo or not slug or not conteudo:
            flash('Título, slug e conteúdo são obrigatórios', 'error')
            return redirect(url_for('editar_post', id=id))
        
        try:
            cursor.execute("""
                UPDATE Posts 
                SET Titulo = %s, Slug = %s, Conteudo = %s, ID_Categoria = %s, 
                    ID_Autor = %s, Status = %s
                WHERE ID_Post = %s
            """, (titulo, slug, conteudo, categoria_id if categoria_id else None,
                  autor_id if autor_id else None, status, id))
            conn.commit()
            flash('Post atualizado com sucesso!', 'success')
            return redirect(url_for('admin_posts'))
        except Exception as e:
            flash(f'Erro ao atualizar post: {str(e)}', 'error')
    
    cursor.execute("SELECT * FROM Posts WHERE ID_Post = %s", (id,))
    post = cursor.fetchone()
    cursor.execute("SELECT * FROM Categorias ORDER BY Nome")
    categorias = cursor.fetchall()
    cursor.execute("SELECT * FROM Autores ORDER BY Nome")
    autores = cursor.fetchall()
    conn.close()
    
    if not post:
        return "Post não encontrado", 404
    
    return render_template('admin/editar_post.html', post=post, categorias=categorias, autores=autores)

@app.route('/admin/posts/deletar/<int:id>')
def deletar_post(id):
    """Deletar post"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM Posts WHERE ID_Post = %s", (id,))
        conn.commit()
        flash('Post deletado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao deletar post: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin_posts'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

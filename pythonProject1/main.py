from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/book'
db = SQLAlchemy(app)

class Livro(db.Model):
    id_livro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100))
    autor = db.Column(db.String(254))
    ano_publicacao = db.Column(db.Integer)

@app.route('/')
def index():
    livros = Livro.query.all()
    return render_template('cadastro_livros.html', outro=livros)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='novolivro')

@app.route('/criar', methods=['POST'])
def criar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano_publicacao = request.form['ano_publicacao']

    livro = Livro.query.filter_by(titulo=titulo).first()
    if livro:
        flash("Livro já existente!")
        return redirect(url_for('novo'))

    novo_livro = Livro(titulo=titulo, autor=autor, ano_publicacao=ano_publicacao)
    db.session.add(novo_livro)
    db.session.commit()
    return redirect(url_for('index'))


# aqui ele verifica pelo id o livrio do qual eu vou editar
@app.route("/editar/<int:id>")
def editar(id):
    livro = Livro.query.filter_by(id_livro=id).first()
    return render_template("editar.html", titulo = "Editando livro", livro=livro)


@app.route("/atualizar", methods=["POST"])
def atualizar():
    livro = Livro.query.filter_by(id_livro = request.form["id"]).first()
    livro.titulo = request.form["titulo"]
    livro.autor = request.form["autor"]
    livro.ano_publicacao = request.form["ano_publicacao"]

    db.session.add(livro)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    Livro.query.filter_by(id_livro=id).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
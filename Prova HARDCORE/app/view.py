from app import app, db
from flask import render_template, url_for, request, redirect, Flask
from app.forms import UserForm, LoginForm, TurmaForm, AtividadeForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Turma, Atividade
from sqlalchemy import or_


@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
    return render_template('index.html', form=form)

@app.route('/cadastro', methods=['GET', 'POST'])
def paginaCadastro():
    form = UserForm ()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template ("usuario_cadastro.html", form=form)

@app.route('/sair')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/turmas', methods=['GET', 'POST'])
@login_required
def turmas_lista():
    pesquisa = request.args.get('pesquisa', '')
    dados = Turma.query.order_by(Turma.numero)
    if pesquisa:
        dados = dados.filter(Turma.numero.ilike(f"%{pesquisa}%"))
    context = {'dados': dados.all()}
    return render_template("turmas_lista.html", context=context)

@app.route('/turmas/cadastro', methods=['GET', 'POST'])
def turmas_cadastro():
    form = TurmaForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('turmas_lista'))
    return render_template("turmas_cadastro.html", form=form)

@app.route('/turma/excluir/<int:id>', methods=['POST'])
@login_required
def delete_turma(id):
    turma = Turma.query.get_or_404(id)
    db.session.delete(turma)
    db.session.commit()
    return redirect(url_for('turmas_lista'))

@app.route('/turmas/atividades', methods=['GET', 'POST'])
@login_required
def atividades():
    pesquisa = request.args.get('pesquisa', '')
    dados = Atividade.query.order_by(Atividade.id)
    if pesquisa:
        dados = dados.filter(Atividade.numero.ilike(f"%{pesquisa}%"))
    context = {'dados': dados.all()}
    return render_template("atividades_lista.html", context=context)

@app.route('/turmas/atividades/cadastro', methods=['GET', 'POST'])
def atividades_cadastro():
    form = AtividadeForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('atividades'))
    return render_template("atividades_cadastro.html", form=form)

@app.route('/turma/atividades/excluir/<int:id>', methods=['POST'])
@login_required
def delete_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    db.session.delete(atividade)
    db.session.commit()
    return redirect(url_for('atividades'))
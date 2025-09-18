from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt()

import os
from werkzeug.utils import secure_filename

from app import db
from app.models import User, Turma, Atividade

class UserForm(FlaskForm):
    nome = StringField ('Nome', validators=[DataRequired()])
    sobrenome = StringField ('Sobrenome', validators=[DataRequired()])
    email = StringField ('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirme sua senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail já cadastrado')
        
    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha.decode('utf-8')
        )
        
        db.session.add(user)
        db.session.commit()
        return(user)
    
class LoginForm(FlaskForm):
    email = StringField ('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')
    
    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                return user
            else:
                raise Exception('Senha incorreta!')
        else:
            raise Exception ('Usuário não encontrado!')
        
class TurmaForm(FlaskForm):
    numero = IntegerField('numero', validators=[DataRequired()])
    quantidade = IntegerField('quantidade', validators=[DataRequired()])
    
    def save(self):
        turma = Turma(
            numero = self.numero.data,
            quantidade = self.quantidade.data
        )
        
        db.session.add(turma)
        db.session.commit()
        return turma
    
    def update(self, turma):
        turma.numero = self.numero.data
        turma.quantidade = self.quantidade.data
        db.session.commit()
        return turma
    
class AtividadeForm(FlaskForm):
    nome = StringField('nome', validators=[DataRequired()])
    descricao = StringField('descricao', validators=[DataRequired()])
    data = DateField('data', validators=[DataRequired()])
    
    def save(self):
        atividade = Atividade(
            nome = self.nome.data,
            descricao = self.descricao.data,
            data = self.data.data
        )
        
        db.session.add(atividade)
        db.session.commit()
        return atividade
    
    def update(self, atividade):
        atividade.nome = self.nome.data
        atividade.descricao = self.descricao.data
        atividade.data = self.data.data
        db.session.commit()
        return atividade
        
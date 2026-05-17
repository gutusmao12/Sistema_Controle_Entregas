from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models.usuario import Usuario

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        condominio = request.form['condominio']
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(
            email=email,
            condominio=condominio
        ).first()

        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            return redirect('/encomendas')

        flash('E-mail ou senha inválidos.')
        return redirect('/login')

    return render_template('login.html')


@auth_routes.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
from flask import Flask, redirect, render_template
from dotenv import load_dotenv
from app.database.db import db
from app.models.encomenda import Encomenda
from app.routes.encomenda_routes import init_app
from flask_login import LoginManager, login_required
from app.models.usuario import Usuario
from app.routes.auth_routes import auth_routes
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = 'sua_chave_secreta'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Faça login para acessar o sistema.'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

init_app(app)

app.register_blueprint(auth_routes)

@app.route('/')
@login_required
def home():
    total_pendentes = Encomenda.query.filter_by(retirado=False).count()
    total_retiradas = Encomenda.query.filter_by(retirado=True).count()
    total_encomendas = total_pendentes + total_retiradas

    return render_template(
        'dashboard.html',
        total_pendentes=total_pendentes,
        total_retiradas=total_retiradas,
        total_encomendas=total_encomendas
    )

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    
from app.models.encomenda import Encomenda
from app.routes.encomenda_routes import init_app

with app.app_context():
    db.create_all()
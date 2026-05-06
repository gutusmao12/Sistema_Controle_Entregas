from flask import Flask
from dotenv import load_dotenv
from app.database.db import db
from app.models.encomenda import Encomenda
from app.routes.encomenda_routes import init_app
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_app(app)

@app.route('/')
def home():
    return 'Sistema de Controle de Entregas'

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    
from app.models.encomenda import Encomenda
from app.routes.encomenda_routes import init_app

with app.app_context():
    db.create_all()
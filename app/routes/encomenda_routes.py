from flask import render_template, request, redirect
from app.models.encomenda import Encomenda
from app.database.db import db

def init_app(app):

    @app.route('/encomendas')
    def listar_encomendas():

        encomendas = Encomenda.query.all()

        return render_template(
            'encomendas.html',
            encomendas=encomendas
        )

    @app.route('/encomendas/nova', methods=['GET', 'POST'])
    def nova_encomenda():

        if request.method == 'POST':

            nova = Encomenda(
                destinatario=request.form['destinatario'],
                bloco=request.form['bloco'],
                apartamento=request.form['apartamento'],
                descricao=request.form['descricao']
            )

            db.session.add(nova)
            db.session.commit()

            return redirect('/encomendas')

        return render_template('nova_encomenda.html')
    
    @app.route('/encomendas/retirar/<int:id>')
    def retirar_encomenda(id):

        encomenda = Encomenda.query.get(id)

        encomenda.retirado = True

        db.session.commit()

        return redirect('/encomendas')
    
    
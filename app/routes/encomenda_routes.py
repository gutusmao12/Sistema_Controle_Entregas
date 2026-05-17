from flask import render_template, request, redirect
from app.models.encomenda import Encomenda
from app.database.db import db
from flask_login import login_required
import unicodedata

def remover_acentos(texto):

    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def init_app(app):

    @app.route('/encomendas')
    @login_required
    def listar_encomendas():

        status = request.args.get('status')
        busca = request.args.get('busca')
        ordem = request.args.get('ordem', 'recentes')

        query = Encomenda.query

        if status == 'pendentes':
            query = query.filter_by(retirado=False)

        elif status == 'retiradas':
            query = query.filter_by(retirado=True)

        if busca:

            encomendas = query.all()

            busca_normalizada = remover_acentos(busca)

            encomendas = [
                encomenda for encomenda in encomendas
                if busca_normalizada in remover_acentos(encomenda.destinatario)
            ]

        else:

            encomendas = query.all()

        if ordem == 'antigas':
            query = query.order_by(Encomenda.data_recebimento.asc())
        else:
            query = query.order_by(Encomenda.data_recebimento.desc())

        return render_template(
            'encomendas.html',
            encomendas=encomendas,
            status=status,
            busca=busca,
            ordem=ordem
        )

    @app.route('/encomendas/nova', methods=['GET', 'POST'])
    @login_required
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
    @login_required
    def retirar_encomenda(id):

        encomenda = Encomenda.query.get(id)

        encomenda.retirado = True

        db.session.commit()

        return redirect('/encomendas')
    
    
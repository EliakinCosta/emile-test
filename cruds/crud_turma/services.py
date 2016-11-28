from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_aluno.models import User
from cruds.crud_aula.models import Aula
import datetime
from sqlalchemy import and_, cast, DateTime


turma = Blueprint("turma", __name__)


@turma.route('/turmas', methods=['GET'])
def get_turmas():
    return jsonify(turmas=[dict(id=turma.id, codigo=turma.codigo) for turma in models.Turma.query.all()])


@turma.route('/add_turma', methods=['POST'])
def add_turma():
    """ This method it was implemented considering that all fields are required in client """

    turma = models.Turma()
    turma.set_fields(dict(request.form.items()))

    db.session.add(turma)
    db.session.commit()

    return jsonify(turma=[turma.serialize() for turma in models.Turma.query.filter_by(codigo=turma.codigo)])


@turma.route('/add_aluno_turma/<turma_id>/<user_id>', methods=['POST'])
def add_aluno_turma(turma_id, user_id):
    turma = models.Turma.query.get(turma_id)
    turma.alunos.append(User.query.get(user_id))
    db.session.commit()
    return jsonify(turma=models.Turma.query.get(turma_id).serialize())


@turma.route('/turma_details/<turma_id>', methods=['GET'])
def turma_details(turma_id):
    return jsonify(turma=models.Turma.query.get(turma_id).serialize())


@turma.route('/add_aula_turma/<turma_id>', methods=['POST'])
def add_aula_turma(turma_id):

    turma = models.Turma.query.get(turma_id)

    t1 = datetime.datetime.strptime('28/11/2016-00:00:00', '%d/%m/%Y-%H:%M:%S')
    t2 = datetime.datetime.strptime('28/11/2016-23:00:00', '%d/%m/%Y-%H:%M:%S')

    aula = Aula(data_inicio_aula=t1, data_fim_aula=t2)

    with db.session.no_autoflush:
        turma.aulas.append(aula)

    db.session.commit()

    return jsonify(turma=models.Turma.query.get(turma_id).serialize())


@turma.route('/alunos_turma/<turma_id>', methods=['GET'])
def alunos_turma(turma_id):
    turma = models.Turma.query.get(turma_id)
    return jsonify(alunos_turma=[dict(id=aluno.id, username=aluno.username) for aluno in turma.alunos])

from flask import Blueprint
from app import developers
from flask import request
from database.mysql import Database as MySql
from database.mongo import Database as Mongo
from sqlalchemy import insert

developer_bp = Blueprint('developer', __name__, url_prefix='/developers')

@developer_bp.post('')
def create():
    try:
        db = MySql()
        ins = insert(developers).values(first_name = request.json.get('first_name'), 
                                last_name = request.json.get('last_name'),
                                expert = request.json.get('expert'))
        result = db.connection.execute(ins)
        Mongo().db.logs.insert_one({
            'type': 'activity',
            'url': request.url,
            'function': 'create developer'
        })
        return {'status': True, 'data': result.rowcount}
    except Exception as ex:
        Mongo().db.logs.insert_one({
            'type': 'error',
            'url': request.url,
            'message': ex.__str__()
        })
        return {'status': False, 'error': ex.__str__()}

@developer_bp.get('')
def fetch():
    try:
        db = MySql()
        ins = developers.select()
        result = db.connection.execute(ins)
        developers_list = []
        for row in result:
            developer_dict = {'id': row.id, 'first_name': row.first_name, 'last_name': row.last_name, 'expert': row.expert}
            developers_list.append(developer_dict)
        Mongo().db.logs.insert_one({
            'type': 'activity',
            'url': request.url,
            'function': 'fetch all developers'
        })
        return {'status': True, 'data': developers_list}
    except Exception as ex:
        Mongo().db.logs.insert_one({
            'type': 'error',
            'url': request.url,
            'message': ex.__str__()
        })
        return {'status': False, 'error': ex.__str__()}

@developer_bp.patch('/<int:id>')
def update(id):
    try:
        db = MySql()
        ins = developers.update().where(developers.c.id == id).values(**request.json)
        db.connection.execute(ins)
        updated_row = db.connection.execute(developers.select().where(developers.c.id == id))
        developers_list = []
        for row in updated_row:
            developer_dict = {'id': row.id, 'first_name': row.first_name, 'last_name': row.last_name, 'expert': row.expert}
            developers_list.append(developer_dict)
        Mongo().db.logs.insert_one({
            'type': 'activity',
            'url': request.url,
            'function': 'update a developer'
        })
        return {'status': True, 'data': developers_list[0]}
    except Exception as ex:
        Mongo().db.logs.insert_one({
            'type': 'error',
            'url': request.url,
            'message': ex.__str__()
        })
        return {'status': False, 'error': ex.__str__()}

@developer_bp.delete('/<int:id>')
def delete(id):
    try:
        db = MySql()
        ins = developers.delete().where(developers.c.id == id)
        db.connection.execute(ins)
        Mongo().db.logs.insert_one({
            'type': 'activity',
            'url': request.url,
            'function': 'delete a developer'
        })
        return {'status': True, 'data': {'deleted_id': id}}
    except Exception as ex:
        Mongo().db.logs.insert_one({
            'type': 'error',
            'url': request.url,
            'message': ex.__str__()
        })
        return {'status': False, 'error': ex.__str__()}
from flask import Blueprint
from flask import request
from database.mongo import Database as Mongo
from bson import ObjectId
import json

developer_bp = Blueprint('developer', __name__, url_prefix='/developers')

@developer_bp.post('')
def create():
    try:
        result = Mongo().db.developers.insert_one({
            'first_name': request.json.get('first_name'),
            'last_name': request.json.get('last_name'),
            'expert': request.json.get('expert')
        })
        Mongo().db.logs.insert_one({
            'type': 'activity',
            'url': request.url,
            'function': 'create developer'
        })
        return {'status': True, 'data': json.loads(json.dumps(result.inserted_id, default=str))}
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
        result = Mongo().db.developers.find({})
        Mongo().db.logs.insert_one({
            'type': 'activity',
            'url': request.url,
            'function': 'fetch all developers'
        })
        return {'status': True, 'data': json.loads(json.dumps(list(result), default=str))}
    except Exception as ex:
        Mongo().db.logs.insert_one({
            'type': 'error',
            'url': request.url,
            'message': ex.__str__()
        })
        return {'status': False, 'error': ex.__str__()}

@developer_bp.patch('/<string:id>')
def update(id):
    try:
        result = Mongo().db.developers.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': request.json},
            upsert=True,
            new=True
        )
        Mongo().db.logs.insert_one({
            'type': 'activity',
            'url': request.url,
            'function': 'update a developer'
        })
        return {'status': True, 'data': json.loads(json.dumps(result, default=str))}
    except Exception as ex:
        Mongo().db.logs.insert_one({
            'type': 'error',
            'url': request.url,
            'message': ex.__str__()
        })
        return {'status': False, 'error': ex.__str__()}

@developer_bp.delete('/<string:id>')
def delete(id):
    try:
        Mongo().db.developers.delete_one({'_id': ObjectId(id)})
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
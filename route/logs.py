from flask import Blueprint
from database.mongo import Database as Mongo
from bson import ObjectId
import json

log_bp = Blueprint('log', __name__, url_prefix='/logs')

@log_bp.get('')
def fetchAlllogs():
    try:
        logs = list(Mongo().db.logs.find({}))
        return {'status': True, 'data': json.loads(json.dumps(logs, default=str))}
    except Exception as ex:
        return {'status': False, 'error': ex.__str__()}
    
@log_bp.put('/<string:doc_id>/')
def softDeletLog(doc_id):
    try:
        updated_doc = Mongo().db.logs.find_one_and_update({'_id': ObjectId(doc_id)},
            {
                '$set':  {'deleted': True}
            }, 
            upsert=True, 
            new=True
        )
        return {'status': True, 'data': json.loads(json.dumps(updated_doc, default=str))}
    except Exception as ex:
        return {'status': False, 'error': ex.__str__()}

@log_bp.delete('/<string:doc_id>/')
def deletLog(doc_id):
    try:
        Mongo().db.logs.delete_one({'_id': ObjectId(doc_id)})
        return {'status': True, 'data': {'deleted_id': doc_id}}
    except Exception as ex:
        return {'status': False, 'error': ex.__str__()}
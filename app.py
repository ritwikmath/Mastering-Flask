from flask import Flask, request
from database.mysql import Database as MySql
from database.mongo import Database as Mongo
from sqlalchemy import Table, Column, Integer, String, MetaData, insert
import json

app = Flask(__name__)

meta = MetaData()

developers = Table(
   'developers', meta, 
   Column('id', Integer, primary_key = True), 
   Column('first_name', String(255)), 
   Column('last_name', String(255)), 
   Column('expert', String(255)), 
)

@app.before_request
def logRequest():
    # Store data in Mongo
    pass

@app.post('/')
def create():
    try:
        db = MySql()
        ins = insert(developers).values(first_name = request.json.get('first_name'), 
                                last_name = request.json.get('last_name'),
                                expert = request.json.get('expert'))
        result = db.connection.execute(ins)
        return {'status': True, 'data': result.rowcount}
    except Exception as ex:
        return {'status': False, 'error': ex.__str__()}

@app.get('/')
def fetch():
    try:
        db = MySql()
        ins = developers.select()
        result = db.connection.execute(ins)
        developers_list = []
        for row in result:
            developer_dict = {'id': row.id, 'first_name': row.first_name, 'last_name': row.last_name, 'expert': row.expert}
            developers_list.append(developer_dict)
        return {'status': True, 'data': developers_list}
    except Exception as ex:
        return {'status': False, 'error': ex.__str__()}

@app.patch('/<int:id>')
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
        return {'status': True, 'data': developers_list[0]}
    except Exception as ex:
        return {'status': False, 'error': ex.__str__()}

@app.delete('/<int:id>')
def delete(id):
    try:
        db = MySql()
        ins = developers.delete().where(developers.c.id == id)
        db.connection.execute(ins)
        return {'status': True, 'data': {'deleted_id': id}}
    except Exception as ex:
        return {'status': False, 'error': ex.__str__()}

if __name__ == '__main__':
    db = MySql()
    db.connect()
    meta.create_all(db.engine)
    app.run(debug=True)
from flask import Flask, request, url_for, current_app
from bson import ObjectId
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
    if request.path in ['/', '/logs']:
        return
    Mongo().db.logs.insert_one({
        'type': 'request',
        'client_addr': request.remote_addr,
        'url': request.url,
        'http_method': request.method,
        'body': request.method in ['POST', 'PATCH'] and request.get_json() or None
    })

if __name__ == '__main__':
    db = MySql()
    db.connect()
    meta.create_all(db.engine)
    Mongo().connect()
    from route.logs import log_bp
    from route.developers import developer_bp
    from route.home import home_bp
    app.register_blueprint(log_bp)
    app.register_blueprint(developer_bp)
    app.register_blueprint(home_bp)
    app.run(debug=True)
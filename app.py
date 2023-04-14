from flask import Flask, request
from datetime import datetime
from database.mongo import Database as Mongo

app = Flask(__name__)

@app.before_request
def logRequest():
    if request.path in ['/', '/logs']:
        return
    Mongo().db.logs.insert_one({
        'type': 'request',
        'client_addr': request.remote_addr,
        'url': request.url,
        'http_method': request.method,
        'body': request.method in ['POST', 'PATCH'] and (request.headers["Content-Type"] == 'application/json' and request.get_json() or request.form) or None,
        'created_at': datetime.now()
    })

if __name__ == '__main__':
    Mongo().connect()
    from route.logs import log_bp
    from route.developers import developer_bp
    from route.home import home_bp
    from route.auth import auth_bp
    app.register_blueprint(log_bp)
    app.register_blueprint(developer_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.secret_key = '03df06392079d7b37dce3c1c460de7c7'
    app.run(debug=True)
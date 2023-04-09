from flask import Flask, render_template, url_for, request, abort, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Developers!'

@app.route('/', methods=['POST'])
def postIndex():
    return 'You have made a POST request'

@app.route('/users/<string:name>')
def userName(name):
    return f'Name: {name}'

@app.route('/path/<path:path>')
def path(path):
    return f'Entered subpath: {path}'

@app.route('/my-name')
def myName():
    return 'Ritwik'

@app.get('/user-info')
def form():
    message = request.args.get('message')
    return render_template('form.html', message=message)

@app.post('/user-info')
def formRequest():
    data = request.form
    if not data.get('firstname') or not data.get('lastname') or not data.get('country'):
        abort(401)
    message = f"{data.get('firstname')} {data.get('lastname')} lives in {data.get('country')}"
    return redirect(f"{url_for('form')}?message={message}")

if __name__ == '__main__':
    app.run(debug=True)
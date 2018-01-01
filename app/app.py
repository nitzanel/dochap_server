import flask


app = flask.Flask('Dochap')

@app.route('/')
def index():
    return 'success'

if __name__ == '__main__':
    app.run('0.0.0.0',port=5555,debug=True)


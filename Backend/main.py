from flask import Flask

name = 'Gradebook'
app = Flask(name)


@app.route('/')
def index():
    return 'Welcome to the Gradebook!'


if __name__ == '__main__':
    app.run(debug=True, port='5000', host='0.0.0.0')


from flask import Flask, render_template
app = Flask(__name__)
print(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/products/')
def products():
    return 'this is product pages'


@app.route('/index/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)

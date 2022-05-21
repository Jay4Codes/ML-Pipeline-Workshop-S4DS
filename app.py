from flask import Flask, render_template

app = Flask(__name__)

""" @app.route("/")
def hello_world():
    return "<p>Hello, World!</p>" """
    

from flask import render_template

@app.route('/')
def hello():
    return render_template('hello.html')


if __name__ == '__main__':
    app.run(debug=True)
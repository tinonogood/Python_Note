from flask import Flask, redirect, url_for, request    
from flask import render_template
from flask.ext.script import Manager

app = Flask(__name__) 
manager = Manager(app)

@app.route('/')
def hello():
    return(str("hello"))

@app.route('/<name>')
def hello_name(name, age=0):
    return render_template("hiuser.html", name=name, age=age)

@app.route('/<name> + <age>')
def hello_world(name, age):
    return render_template("hiuser.html", name=name, age=age)

if __name__ == '__main__':
#    manager.run(debug=True,host='0.0.0.0')
    manager.run()

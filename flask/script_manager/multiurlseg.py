from flask import Flask, redirect, url_for, request    
from flask import render_template
from flask.ext.script import Manager

app = Flask(__name__) 
manager = Manager(app)

@app.route('/')
def hello():
    return render_template("base2.html")


if __name__ == '__main__':
#    manager.run(debug=True,host='0.0.0.0')
    manager.run()

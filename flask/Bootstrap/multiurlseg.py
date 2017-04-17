from flask import Flask, redirect, url_for, request    
from flask import render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__) 
Bootstrap(app)
manager = Manager(app)

@app.route('/')
def hello():
    return render_template("user.html")


if __name__ == '__main__':
#    manager.run(debug=True,host='0.0.0.0')
    manager.run()

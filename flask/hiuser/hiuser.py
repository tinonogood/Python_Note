from flask import Flask, redirect, url_for, request    
from flask import render_template

app = Flask(__name__) 

@app.route('/', methods =["GET", "POST"])
def hello_world():
    return render_template("login.html")
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('hiuser',name = user))

@app.route('/hiuser', methods =["GET"])
def hiuser():
    if request.method == 'GET':
        name = request.args.get("name", "Error")
        return render_template("hiuser.html", name = name)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

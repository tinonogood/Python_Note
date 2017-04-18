from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

con = sql.connect('database.db')
con.execute('DROP TABLE IF EXISTS members')
con.execute('CREATE TABLE members (name TEXT, project TEXT)')

@app.route('/', methods= ['POST','GET'])
def home():
	con = sql.connect('database.db')
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM members")
	rows = cur.fetchall()
	return render_template('home.html', rows = rows)

@app.route('/addmember', methods= ['POST', 'GET'])
def addmember():
	if request.method == 'POST':
		try:
			nm = request.form['nm']
			pj = request.form['pj']
		
#		with sql.connect('database.db') as con:
			con = sql.connect('database.db')
			cur = con.cursor()
			cur.execute("INSERT INTO members (name, project) VALUES (?,?)", (nm, pj))
			con.commit()
			msg = "Add Successfully"
		except:
			con.rollback()
			msg = "Error in insert operation"

		finally:
			return render_template("result.html", msg = msg)

@app.route('/delmember', methods= ['POST', 'GET'])
def delmember():	
	if request.method == 'POST':
		try:
			pj = request.form['pj']
			con = sql.connect('database.db')
			cur = con.cursor()
			cur.execute("DELETE FROM members WHERE project = ?", pj)
			con.commit()
			msg_del = "Delete Successfully"
		except:
			con.rollback()
			msg_del = "Error in delete operation"

		finally:
			return render_template("result.html", msg = msg_del)


if __name__=='__main__':
	app.run(debug = True) 


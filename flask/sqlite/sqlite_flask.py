from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

con = sql.connect('database.db')
con.execute('DROP TABLE IF EXISTS members')
con.execute('CREATE TABLE members (name TEXT, number TEXT)')

@app.route('/')
def home():
	con = sql.connect('database.db')
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("select * from members")
	rows = cur.fetchall();
	return render_template('home.html', rows = rows)

@app.route('/addmember', methods= ['POST', 'GET'])
def addmember():
	if request.method == 'POST':
		try:
			nm = request.form['nm']
			nu = request.form['nu']
		
#		with sql.connect('database.db') as con:
			con = sql.connect('database.db')
			cur = con.cursor()
			cur.execute("INSERT INTO members (name, number) VALUES (?,?)", (nm, nu))
			con.commit()
			msg = "Add Successfully"
		except:
			con.rollback()
			msg = "Error in insert operation"

		finally:
			return render_template("result.html", msg = msg)


if __name__=='__main__':
	app.run(debug = True) 

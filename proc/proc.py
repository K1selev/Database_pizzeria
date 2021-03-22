import json
import mysql.connector
from DBcm import UseDatabase, ConnectionError, SQLError
from flask import Flask, render_template, request, redirect, url_for, Blueprint, current_app, session

proc = Blueprint('proc', __name__, template_folder='templates')


@proc.route('/', methods=['GET', 'POST'])
def index():
	if 'user' in session:
		print("robit!")
		if 'send' in request.form and request.form['send']=='Отправить':
			information = request.form.get('year')
			print(information)
			if information:
				try:
					with UseDatabase(current_app.config['dbconfig']) as cursor:
						employees = find_employees(cursor, information)
					return render_template('proc.html', information = information, employees = employees)
				except ConnectionError as err:
					print("Вот ошибка соединения", str(err))
					str_err = "Ошибка соединения"
				#except SQLError as err:
				#	print("Вот ошибка выполнения запроса", str(err))
				#	str_err = "Ошибка выпонения запроса. "
				return str_err
			else:
				return render_template('entry.html')
		else:
				return render_template('entry.html')
	else:
		session['ind1'] = True
		print("------------authorization is needed------------")
		return redirect(url_for('auth_blueprint.auth'))



def find_employees(cursor, information):
	SQL = """Select * from otchet
	where year='{0}'""".format(information)
	cursor.execute(SQL)
	result = cursor.fetchall()
	res = []
	schema = ['id','title','sold','price','cost','month', 'year']
	for blank in result:
		res.append(dict(zip(schema,blank)))
	return res

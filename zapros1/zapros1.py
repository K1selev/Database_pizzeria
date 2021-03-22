import json
import mysql.connector
from DBcm import UseDatabase, ConnectionError, SQLError
from flask import Flask, render_template, request, redirect, url_for, Blueprint, current_app, session



zapros1 = Blueprint('zapros1', __name__, template_folder = 'templates')

@zapros1.route('/', methods=['GET','POST'])
def index():
	if 'user' in session:
		try:
			with UseDatabase(current_app.config['dbconfig']) as cursor:
				employees = find_employees(cursor)
			return render_template('zapros1.html', blanks = employees)
		except ConnectionError as err:
			str_err = "Ошибка соединения"
		except SQLError as err:
			str_err = "Ошибка выпонения запроса. "
		return str_err
	else:
		print("------------authorization is needed------------")
		return redirect(url_for('auth_blueprint.auth'))


def find_employees(cursor):
	SQL = """SELECT id_dish, Title, COUNT(`id_Order`), SUM(Cost)
			FROM Dish JOIN `Order` USING (id_dish)
			WHERE YEAR(Delivery_Time) = 2017 AND MONTH(Delivery_Time) = 3
			GROUP BY `id_Order`;"""
	cursor.execute(SQL)
	result = cursor.fetchall()
	res = []
	schema = ['id_dish', 'title', 'count', 'sum']
	for blank in result:
		res.append(dict(zip(schema, blank)))
	return res


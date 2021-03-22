import json
import mysql.connector
from DBcm import UseDatabase, ConnectionError, SQLError
from flask import Flask, render_template, request, redirect, url_for, Blueprint, current_app, session

redact = Blueprint('redact', __name__, template_folder='templates')


@redact.route('/',methods=['GET','POST'])
def index():
    if 'user' in session:
        try:
            with UseDatabase(current_app.config['dbconfig']) as cursor:
                pizzas = find_pizzas(cursor)

                if 'delete' in request.form and request.form['delete'] == 'Удалить':
                    to_del = request.form.get('toDel')
                    delete_pizzas(cursor,to_del)
                    pizzas = find_pizzas(cursor)
                    return render_template('list.html', pizzas = pizzas)
                if 'add_pizza' in request.form and request.form['add_pizza'] == 'Добавить пиццу':
                    return render_template('add_pizza.html')
                if 'add' in request.form and request.form['add'] == 'Добавить':
                    pizza = request.form.get('pizza')
                    for str in pizzas:
                        if str['name'] == pizza:
                            return "Пицца, которую вы пытаетесь добавить уже существует!"
                    add_pizzas(cursor, pizza)
                    pizzas = find_pizzas(cursor)
                    return render_template('list.html', pizzas = pizzas)
                if 'redact' in request.form and request.form['redact'] == 'Редактировать':
                    to_del = {'name': request.form.get('toDel')}
                    return render_template('redact_pizzas.html',pizzas = to_del)
                if 'change' in request.form and request.form['change'] == 'Изменить':
                    name = request.form.get('pizza')
                    to_upd = request.form.get('toUpd')
                    upd_pizza(cursor, name, to_upd)
                    pizzas = find_pizzas(cursor)
                    return render_template('list.html', pizzas = pizzas)
                else:
                    return render_template('list.html', pizzas = pizzas)
        except ConnectionError as err:
            print("Вот ошибка соединения", err)
            str_err = "Ошибка соединения"
        except SQLError as err:
            print("Вот ошибка выполнения запроса", err)
            str_err = "Ошибка выпонения запроса. "
        return str_err

    else:
        return redirect(url_for('auth_blueprint.auth'))


def find_pizzas(cursor):
    SQL = """SELECT id, name
            FROM dishes"""
    cursor.execute(SQL)
    result = cursor.fetchall()
    res = []
    schema = ['id', 'name']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res


def add_pizzas(cursor, movie):
    SQL = """INSERT INTO dishes VALUES(NULL,'{0}')""".format(movie)
    cursor.execute(SQL)
    return


def delete_pizzas(cursor, name):
    SQL = """DELETE FROM dishes
            WHERE name = '{0}'""".format(name)
    cursor.execute(SQL)
    return


def upd_pizza(cursor, name,to_upd):
    SQL = """UPDATE dishes SET name = %s WHERE name = %s"""
    cursor.execute(SQL, (name,to_upd))
    #SQL = """UPDATE dishes SET name = '{0}' WHERE name = '{1}'""".format(name, to_upd)
    #cursor.execute(SQL)
    return

import json
import mysql.connector
from DBcm import UseDatabase, ConnectionError, SQLError
from flask import Flask, render_template, request, redirect, url_for, Blueprint, current_app, session

manage = Blueprint('manage', __name__, template_folder='templates')


@manage.route('/',methods=['GET','POST'])
def index():
    if 'user' in session:
        try:
            with UseDatabase(current_app.config['dbconfig']) as cursor:
                users = find_users(cursor)

                if 'delete' in request.form and request.form['delete'] == 'Удалить':
                    to_del = request.form.get('toDel')
                    delete_users(cursor,to_del)
                    users = find_users(cursor)
                    return render_template('listq.html', users = users)
                if 'add_user' in request.form and request.form['add_user'] == 'Добавить пользователя':
                    return render_template('add_user.html')
                if 'add' in request.form and request.form['add'] == 'Добавить':
                    login = request.form.get('login')
                    password = request.form.get('password')
                    gr_log = 'manager1'
                    adress = request.form.get('adress')
                    add_users(cursor, login, password, adress)
                    users = find_users(cursor)
                    return render_template('listq.html', users = users)
                if 'redact' in request.form and request.form['redact'] == 'Редактировать':
                    to_del = {'name': request.form.get('toDel')}
                    return render_template('redact_user.html',users = to_del)
                else:
                    return render_template('listq.html', users = users)
        except ConnectionError as err:
            print("Вот ошибка соединения", err)
            str_err = "Ошибка соединения"
        #except SQLError as err:
        #    print("Вот ошибка выполнения запроса", err)
        #    str_err = "Ошибка выпонения запроса. "
        return str_err

    else:
        return redirect(url_for('auth_blueprint.auth'))


def find_users(cursor):
    SQL = """SELECT *
            FROM sys_table
            WHERE gr_pass = 'manager_pas'"""
    cursor.execute(SQL)
    result = cursor.fetchall()
    res = []
    schema = ['id', 'login', 'password', 'gr_log', 'gr_pass','adress']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res


def add_users(cursor, login, password, adress):
    SQL = """INSERT INTO sys_table VALUES(NULL,'{0}','{1}', 'manager1', 'manager_pas', '{2}')""".format(login, password, adress)
    cursor.execute(SQL)
    return


def delete_users(cursor, name):
    SQL = """DELETE FROM sys_table
            WHERE login = '{0}'""".format(name)
    cursor.execute(SQL)
    return

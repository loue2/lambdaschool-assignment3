from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def server():
    return render_template('home.html')

@app.route('/enternew/')
def enternew():
    return render_template('food.html')

@app.route('/addfood', methods = ['POST'])
def addfood():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        name = request.form['name']
        calories = request.form['calories']
        cuisine = request.form['cuisine']
        is_vegetarian = request.form['is_vegetarian']
        is_gluten_free =  request.form['is_gluten_free']
        foodinfo = (name, calories, cuisine, is_vegetarian, is_gluten_free)
        cursor.execute('INSERT INTO foods VALUES (?,?,?,?,?)', foodinfo)
        connection.commit()
        message = 'Food added. Thank you.'
    except:
        connection.rollback()
        message = 'Error. Is the table initialized? Try running python initdb.py from the command line.'
    finally:
        return render_template('result.html', message = message)
        connection.close()

@app.route('/favorite')
def favorite():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM foods WHERE name = "pizza"')
        connection.commit()
        result = cursor.fetchone()
    except:
        connection.rollback()
        result = ('Database error')
    finally:
        return jsonify(result)
        connection.close()

@app.route('/search/')
def search():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        searchname = (request.args.get('name'),)

        cursor.execute('SELECT * FROM foods WHERE name =?', searchname)
        connection.commit()
        result = cursor.fetchall()
    except:
        connection.rollback()
        result = ('Database error')
    finally:
        return jsonify(result)
        connection.close()

@app.route('/drop')
def drop():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        cursor.execute('DROP TABLE foods')
        connection.commit()
        message = 'Dropped. Table "foods" was deleted'
    except:
        connection.rollback()
        message = 'Error in dropping table'
    finally:
        return render_template('result.html', message = message)
        connection.close()

# Hamelmil Financial Record System
# By Absera Temesgen - abseratemesgen@gmail.com
# December 2020

from flask import Flask, render_template, request, redirect, flash, session
import sqlite3
from utility import dateToInt, intToDate
import webbrowser
import os, sys
import jinja2.ext

# base_dir = '.'
# if hasattr(sys, '_MEIPASS'):
#     base_dir = os.path.join(sys._MEIPASS)


# Flask app generate
# app = Flask(__name__, static_folder=os.path.join(base_dir, 'static'),
#         template_folder=os.path.join(base_dir, 'templates'))

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
app.secret_key = 'secretkey'

# Sqlite3 database connection
try:
    database = sqlite3.connect("C:\\users\\Public\\Hamelmil_database.db", uri=True, check_same_thread=False)
except:
    database = sqlite3.connect("Hamelmil_database.db", uri=True, check_same_thread=False)
database_cursor = database.cursor()

create_table_query = """ CREATE TABLE IF NOT EXISTS hdb_table (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        title text,
                                        date integer,
                                        price integer,
                                        description text
                                    ); """
database_cursor.execute(create_table_query)


@app.route("/", methods=["GET", "POST"])
def login():
    password = request.form.get("password")
    session.permanent = False
    if password:
        if password == "1234":
            session["password"] = password
            return redirect("/home")
        else:
            flash("Incorrect password", "Error")
    elif password == "":
        flash("Please enter your password", "Error")
    return render_template("login.html")


@app.route("/home")
def show_home():
    if "password" in session:
        db_result_default = database_cursor.execute("SELECT * FROM hdb_table ORDER BY id DESC").fetchall()
        dates = []
        for i in db_result_default:
            dates.append(intToDate(i[2]))
        return render_template("index.html", db_result=db_result_default, dates=dates)
    else:
        return redirect("/")


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected_option = request.form.getlist('customRadio')
        if selected_option:
            if selected_option[0] == 'dftl':
                db_result_dftl = database_cursor.execute("SELECT * FROM hdb_table ORDER BY date DESC").fetchall()
                dates = []
                for i in db_result_dftl:
                    dates.append(intToDate(i[2]))
                return render_template("index.html", db_result=db_result_dftl, dates=dates)
            elif selected_option[0] == 'dltf':
                db_result_dltf = database_cursor.execute("SELECT * FROM hdb_table ORDER BY date ASC").fetchall()
                dates = []
                for i in db_result_dltf:
                    dates.append(intToDate(i[2]))
                return render_template("index.html", db_result=db_result_dltf, dates=dates)
            elif selected_option[0] == 'phtl':
                db_result_phtl = database_cursor.execute("SELECT * FROM hdb_table ORDER BY price DESC").fetchall()
                dates = []
                for i in db_result_phtl:
                    dates.append(intToDate(i[2]))
                return render_template("index.html", db_result=db_result_phtl, dates=dates)
            elif selected_option[0] == 'plth':
                db_result_plth = database_cursor.execute("SELECT * FROM hdb_table ORDER BY price ASC").fetchall()
                dates = []
                for i in db_result_plth:
                    dates.append(intToDate(i[2]))
                return render_template("index.html", db_result=db_result_plth, dates=dates)
            elif selected_option[0] == 'faf':
                db_result_faf = database_cursor.execute("SELECT * FROM hdb_table ORDER BY id ASC").fetchall()
                dates = []
                for i in db_result_faf:
                    dates.append(intToDate(i[2]))
                return render_template("index.html", db_result=db_result_faf, dates=dates)
            else:
                return redirect("/home")
        else:
            return redirect("/home")


@app.route("/add")
def show_add():
    if "password" in session:
        return render_template("add.html")
    else:
        return redirect("/")


@app.route("/add", methods=["GET", "POST"])
def add():
    title = request.form.get("title")
    date = request.form.get("date")
    price = request.form.get("price")
    description = request.form.get("description")
    if title == "" or date == "" or price == "" or description == "":
        flash("Please enter all info", "Error")
    else:
        try:
            intDate = dateToInt(date)
            database_cursor.execute(''' INSERT INTO hdb_table ( title, date, price, description )
                VALUES ( ?, ?,
                ?, ?); ''', (title, intDate, price, description))
            database.commit()
            flash("Successfully Added", "Info")
        except:
            flash("Some Error Occurred. Please Restart", "Error")
    return render_template("add.html")


@app.route("/search")
def show_search():
    if "password" in session:
        return render_template("search.html")
    else:
        return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_text = request.form.get("search-text")
        query = "SELECT * FROM hdb_table WHERE title LIKE ? or price LIKE ? or description LIKE ?"
        values = ("%" + search_text + "%", "%" + search_text + "%", "%" + search_text + "%")
        database_cursor.execute(query, values)
        search_results = database_cursor.fetchall()

        dates = []
        for i in search_results:
            dates.append(intToDate(i[2]))
        return render_template("search.html", search_results=search_results, dates=dates)


if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run()


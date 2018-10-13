import sqlite3
from flask import Flask
from flask import render_template, request, redirect, url_for, g
from forms import SearchForm
app = Flask(__name__)

DATABASE = "datos.db"

# Gestion de la base de données (copier-coller de la doc de FLASK)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def change_db(query,args=()):
    cur = get_db().execute(query, args)
    get_db().commit()
    cur.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Routage des URL et traitement

@app.route('/', methods = ['GET', 'POST'])
def index(s = ""):
    Search = SearchForm(request.form)
    if request.method =='POST':
        s = Search.search.data
    libreria_list=query_db("SELECT * FROM libreria")
    return render_template("index.html",libreria_list=libreria_list, form = Search, se = s)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template("create.html",libreria=None)
    
    if request.method == "POST":
        libreria=request.form.to_dict()
        values=[libreria["Imagen"],libreria["ISBN"],libreria["Nombre"]]
        change_db("INSERT INTO libreria (Imagen,ISBN,Nombre) VALUES (?,?,?)",values)
        return redirect(url_for("index"))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def udpate(id):
    if request.method == "GET":
        libreria=query_db("SELECT * FROM libreria WHERE id=?",[id],one=True)
        return render_template("update.html",libreria=libreria)
    
    if request.method == "POST":
        print(request.form)
        libreria=request.form.to_dict()
        print(libreria)
        values=[libreria["Imagen"],libreria["ISBN"],libreria["Nombre"],id]
        change_db("UPDATE libreria SET Imagen=?, ISBN=?, Nombre=? WHERE id=?",values)
        return redirect(url_for("index"))

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == "GET":
        libreria=query_db("SELECT * FROM libreria WHERE id=?",[id],one=True)
        return render_template("delete.html",libreria=libreria)

    if request.method == "POST":
        change_db("DELETE FROM libreria WHERE id = ?",[id])
        return redirect(url_for("index"))

if __name__== '__main__':
    app.run(debug = True)

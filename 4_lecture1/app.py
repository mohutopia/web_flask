from flask import Flask, render_template, request
from cs50 import SQL

app = Flask(__name__)
db = SQL("sqlite:///register.db")

@app.route("/")
def index():
 rows = db.execute("SELECT * FROM registrants")
 print("Server running")
 return render_template("index.html", rows = rows)

@app.route("/search")
def search():
 q = request.args.get("q")
 # rows = db.execute(f"SELECT * FROM registrants WHERE nam = '{q}'") : vulnerable to injection attakcs
 rows = db.execute("SELECT * FROM registrants WHERE nam = :name", name = q) 
 return render_template("index.html", rows = rows)
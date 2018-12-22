from flask import Flask, render_template, request

app = Flask(__name__) # has to be in every flask app

@app.route("/")
def index():
 q = request.args.get("q", "world") # a variable that holds any arguments in query ?q= ... if None, outputs "world"
 return render_template("index.html", q = q) # sets the query ?q= to the variable q

@app.route("/register", methods = ["POST"])
def register():
 # error check
 name = request.form.get("name")
 dorm = request.form.get("dorm")

 if not name or not dorm:
  return render_template("failure.html")
 return render_template("success.html")

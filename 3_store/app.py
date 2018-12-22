from flask import Flask, session, render_template, request
from flask_session import Session

app = Flask(__name__) # configure app

# configure  sessions
app.config("SESSION_PERMANENT") = False
app.config("SESSION_TYPE") = "filesystem"
Session(app)

ITEMS = ["foo", "bar", "baz"] # items for sale

@app.route('/')
def index():
 return render_template("index.html")

@app.route('/update', methods = ['POST'])
def update():
 for item in request.form:
  session[item] = int(request.form.get(item))
 return redirect('/cart')

@app.route('/cart')
def cart():
 return render_template('cart.html', cart = session)

from flask import Flask, render_template, request

app = Flask(__name__)

# write all the content of the large file to the WORDS' list
WORDS = []
with open("large", "r") as file:
 for line in file.readlines():
  WORDS.append(line.rstrip())

@app.route("/")
def index():
 return render_template("index.html")

@app.route("/search")
def search():
 q = request.args.get('q')
 words = [word for word in WORDS if q and word.startswith(q)]
 return render_template("search.html", words = words)
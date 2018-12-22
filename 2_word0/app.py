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
 words = [word for word in WORDS if word.startswith(request.args.get('q'))]
 # the line above does exactly the same as the ones below
 # words = []
 # q = request.args.get('q')
 # for word in WORDS:
 #  if word.startswith(q):
 #   words.append(word)
 return render_template("search.html", words = words)

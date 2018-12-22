"""
I have a problem appending new registrants to the csv file
line 16 - 29
"""


from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

@app.route("/")
def index():
 return render_template("index.html")

@app.route("/register", methods = ["POST"])
def register():
 # error check
 name = request.form.get("name")
 dorm = request.form.get("dorm")
 if not name or not dorm:
  return render_template("failure.html")
 # append to a csv file
 file = open("registered.csv", "a")
 writer = csv.writer(file)
 writer.writerow((name, dorm))
 file.close()
 # close the csv file and redirect to success.html
 return render_template("success.html")

@app.route("/registered")
def registered():
 # better approach to deal with files
 file = open("registered.csv", "r")
 reader = csv.reader(file)
 students = list(reader)
 file.close()
 return render_template("registered.html", students = students)

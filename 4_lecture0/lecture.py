from cs50 import SQL

db = SQL("sqlite:///register.db")

rows = db.execute("SELECT * FROM registrants") # store the database's rows in a list
for row in rows:
 print(row['nam'] + " registered")
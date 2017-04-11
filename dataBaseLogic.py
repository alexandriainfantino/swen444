from flask import Flask, g
import sqlite3

DATABASE = 'C:\\Users\\alexa\\PycharmProjects\\swen444\\donatoro.db'

app = Flask(__name__)
app.config.from_object(__name__)

def get_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    # rv = cur.fetchall()
    test = [dict(test1=row[0], test2=row[1], test3 = row[2]) for row in cur.fetchall()]
    cur.close()
    return test
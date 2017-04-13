from flask import Flask, g
import sqlite3

DATABASE = 'C:\\Users\\alexa\\PycharmProjects\\swen444\\donatoro.sqlite'

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
    return cur
    cur.close()
    return test

def getUsers():
    return [dict(id=row[0], password=row[1], email=row[2], isDonor=row[3]) for row in query_db('select * from user').fetchall()]

def getUserById(userId):
    user = query_db('select * from user where id = ?', (userId,)).fetchone()
    user = [dict(id=user[0], password=user[2].encode('ascii', 'ignore'), email=user[1].encode('ascii', 'ignore'), isDonor=user[3])]
    return user

def getUserByEmail(email):
    user = query_db('select * from user where email = ?', (email,)).fetchone()
    user = [dict(id=user[0], password=user[2], email=user[1],
                 isDonor=user[3])]
    return user

def getCreditCardByUserId(userId):
    return [dict(ccn=row[0], ccv=row[1], expMonth=row[2], expYear=row[3], streetAdd1 =row[4], streetAdd2=row[5], city=row[6],
                 state=row[7], zip=row[8], userId=row[9], id=row[10]) for row in
             query_db('select * from cc where userId=?', (userId,)).fetchall()]

def getCharityInfoByCharityId(charityId):
    charity = query_db('select * from charity_info where charID = ?', (charityId,)).fetchone()
    charity = [dict(name=charity[0], identificationNum=charity[1], description=charity[2], streetAdd = charity[3],
                 city=charity[4], state=charity[5], zip=charity[6], userId=charity[7], charId=charity[8])]
    return charity

def getDonorInfoByUserId(userId):
    donor = query_db('select * from donor_info where userID = ?', (userId,)).fetchone()
    donor = [dict(firstName=donor[0], lastName=donor[1], streetAdd1=donor[2], streetAdd2=donor[3],
                    city=donor[4], state=donor[5], zip=donor[6], userId=donor[7])]
    return donor

def getDonorFavorites(userId):
    return [dict(name=row[0], identificationNum=row[1], description=row[2], streetAdd = row[3],
                 city=row[4], state=row[5], zip=row[6], country=row[7], userId=row[8], charId=row[9]) for row in
            query_db('select * from charity_info inner join favorites on charity_info.charID = favorites.charityId '
                     'where favorites.userId = ?', (userId,)).fetchall()]

def getCharityPosts(charityId):
    return [dict(date=row[0], title=row[1], post=row[2], charId=row[3], Id=row[4]) for row in
        query_db('select * from posts where charId=?', (charityId,)).fetchall()]

def getCharityTags(charityId):
    return [dict(charityId=row[0], tag=row[1], Id=row[2]) for row in
            query_db('select * from tags where charityId=?', (charityId,)).fetchall()]

def getCharitiesByTags(tag):
    return [dict(name=row[0], identificationNum=row[1], description=row[2], streetAdd = row[3],
                 city=row[4], state=row[5], zip=row[6], userId=row[7], charId=row[8]) for row in
            query_db('select * from charity_info inner join tags on charity_info.charID = tags.charityId where '
                     'tags.tag = ?', (tag,)).fetchall()]
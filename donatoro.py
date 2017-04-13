from flask import Flask, render_template, g
from dataBaseLogic import *

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/newsFeed')
def news_feed():
    charities = getDonorFavorites(1)
    news = []
    for c in charities:
        news.append(getCharityPosts(c['charId']))
    return render_template('newsFeed.jinja', username="Fake Name", news = news[0])

@app.route('/')
def log_in():
    return render_template('logIn.jinja')

@app.route('/selection')
def selection():
    return render_template('registration/selection.jinja')

@app.route('/charityRegistration1')
def charityRegistrationOne():
    return render_template('registration/charityRegistration/registrationPage1.jinja')

@app.route('/charityRegistration2')
def charityRegistration2():
    return render_template('registration/charityRegistration/registrationPage2.jinja')

@app.route('/charityConfirmation')
def charityConfirmation():
    charityInformation = {"name":"Fake Charity", "501c":"123456789", "tags": "Environment", "email":"fakeCharity@fakeCharity.com", "billing": "1 Main St, Rochester, NY, 14623", "description":"This organization is aimed to plant 50,000 new trees every year, as well as replant trees in areas across the country affected by natural disasters. All trees planted will be native to the area they are planted in to avoid introducing invasive species."}
    return render_template('registration/charityRegistration/confirmation.jinja', charityInfo = charityInformation)

@app.route('/donorRegistration')
def donorRegistration():
    return render_template('registration/donorRegistration/donorRegistration.jinja')

@app.route('/donorBilling')
def donorBilling():
    return render_template('registration/donorRegistration/donorBilling.jinja')

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
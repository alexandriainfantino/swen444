from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/newsFeed')
def news_feed():
    fakeNews = [{"title": "Fake News Title", "date": "01/01/2017", "article" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris dui lorem, porta sit amet tellus non, semper blandit augue. Vivamus vitae ligula quis neque venenatis blandit eget nec sapien. Duis sodales orci in est feugiat lobortis. Integer non purus sem. Vestibulum eu fermentum tellus, eu vulputate leo. Aliquam vitae est nec diam ornare efficitur. Aenean congue fermentum justo, aliquam porta velit consequat nec. Duis ac tortor metus.."}, {"title":"Fake news article 2", "date":"02/03/2017", "article": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris dui lorem, porta sit amet tellus non, semper blandit augue. Vivamus vitae ligula quis neque venenatis blandit eget nec sapien. Duis sodales orci in est feugiat lobortis. Integer non purus sem. Vestibulum eu fermentum tellus, eu vulputate leo. Aliquam vitae est nec diam ornare efficitur. Aenean congue fermentum justo, aliquam porta velit consequat nec. Duis ac tortor metus.."}]
    return render_template('newsFeed.jinja', username="Johnny Bravo", news = fakeNews)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    user = "donor"
    if user == "donor":
        return render_template('DonorProfile/donorProfile.jinja', username="Johnny Bravo", email="Johnny.Bravo@gmail.com", address="123 Rainbow Drive", address2="", city="Rochester", state="New York", zipcode="14623")
    else:
        return render_template('CharityProfile/charityProfile.jinja', username="Johnny Bravo", email="Johnny.Bravo@gmail.com", address="123 Rainbow Drive", address2="", city="Rochester", state="New York", zipcode="14623")

@app.route('/personal')
def donor_edit_personal():
	return render_template('DonorProfile/donorPersonal.jinja', username="Johnny Bravo", first_name="Johnny", last_name="Bravo", email="Johnny.Bravo@gmail.com", address="123 Rainbow Drive", address2="", city="Rochester", state="New York", zipcode="14623")

@app.route('/savePersonal', methods = ['POST'])
def save_personal():    
    return redirect('../profile')

@app.route('/savePassword', methods = ['POST'])
def save_password():
    return redirect('../profile')

@app.route('/savePayment', methods = ['POST'])
def save_payment():
    return redirect('../payment')

@app.route('/password')
def donor_edit_password():
	return render_template('DonorProfile/donorPassword.jinja', username="Johnny Bravo")

@app.route('/payment')
def donor_edit_payment():
	fakeCards = ["5678","6666"]
	return render_template('DonorProfile/donorPayment.jinja', username="Johnny Bravo", cards=fakeCards)

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
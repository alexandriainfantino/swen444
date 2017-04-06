from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def news_feed():
    fakeNews = [{"title": "Fake News Title", "date": "01/01/2017", "article" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris dui lorem, porta sit amet tellus non, semper blandit augue. Vivamus vitae ligula quis neque venenatis blandit eget nec sapien. Duis sodales orci in est feugiat lobortis. Integer non purus sem. Vestibulum eu fermentum tellus, eu vulputate leo. Aliquam vitae est nec diam ornare efficitur. Aenean congue fermentum justo, aliquam porta velit consequat nec. Duis ac tortor metus.."}, {"title":"Fake news article 2", "date":"02/03/2017", "article": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris dui lorem, porta sit amet tellus non, semper blandit augue. Vivamus vitae ligula quis neque venenatis blandit eget nec sapien. Duis sodales orci in est feugiat lobortis. Integer non purus sem. Vestibulum eu fermentum tellus, eu vulputate leo. Aliquam vitae est nec diam ornare efficitur. Aenean congue fermentum justo, aliquam porta velit consequat nec. Duis ac tortor metus.."}]
    return render_template('newsFeed.jinja', username="Fake Name", news = fakeNews)

@app.route('/Profile')
def donor_profile():
	return render_template('DonorProfile/donorProfile.jinja', username="Johnny Bravo", email="Johnny.Bravo@gmail.com", address="123 Rainbow Drive", address2="", city="Rochester", state="New York", zipcode="14623")

@app.route('/Personal')
def donor_edit_personal():
	return render_template('DonorProfile/donorPersonal.jinja', username="Johnny Bravo", first_name="Johnny", last_name="Bravo", email="Johnny.Bravo@gmail.com", address="123 Rainbow Drive", address2="", city="Rochester", state="New York", zipcode="14623")

@app.route('/Password')
def donor_edit_password():
	return render_template('DonorProfile/donorPassword.jinja', username="Johnny Bravo")

@app.route('/Payment')
def donor_edit_payment():
	fakeCards = ["5678","6666"]
	return render_template('DonorProfile/donorPayment.jinja', username="Johnny Bravo", cards=fakeCards)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
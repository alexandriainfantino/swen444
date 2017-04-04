from flask import Flask, render_template

app = Flask(__name__)


@app.route('/newsFeed')
def news_feed():
    fakeNews = [{"title": "Fake News Title", "date": "01/01/2017", "article" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris dui lorem, porta sit amet tellus non, semper blandit augue. Vivamus vitae ligula quis neque venenatis blandit eget nec sapien. Duis sodales orci in est feugiat lobortis. Integer non purus sem. Vestibulum eu fermentum tellus, eu vulputate leo. Aliquam vitae est nec diam ornare efficitur. Aenean congue fermentum justo, aliquam porta velit consequat nec. Duis ac tortor metus.."}, {"title":"Fake news article 2", "date":"02/03/2017", "article": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris dui lorem, porta sit amet tellus non, semper blandit augue. Vivamus vitae ligula quis neque venenatis blandit eget nec sapien. Duis sodales orci in est feugiat lobortis. Integer non purus sem. Vestibulum eu fermentum tellus, eu vulputate leo. Aliquam vitae est nec diam ornare efficitur. Aenean congue fermentum justo, aliquam porta velit consequat nec. Duis ac tortor metus.."}]
    return render_template('newsFeed.jinja', username="Fake Name", news = fakeNews)

@app.route('/')
def log_in():
    return render_template('logIn.jinja')

@app.route('/selection')
def selection():
    return render_template('registration/selection.jinja')

@app.route('/charityRegistration1')
def charityRegistrationOne():
    return render_template('registration/charityRegistration/registrationPage1.jinja')

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
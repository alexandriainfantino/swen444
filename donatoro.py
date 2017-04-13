from flask import Flask, render_template, redirect, request, g
from dataBaseLogic import *

app = Flask(__name__)

states=["Alabama" ,"Alaska" ,"Arizona" ,"Arkansas" ,"California" ,"Colorado","Connecticut","Delaware" ,"Florida","Georgia" ,"Hawaii" ,"Idaho","Illinois", "Indiana" ,"Iowa" ,"Kansas" ,"Kentucky" ,"Louisiana" ,"Maine" ,"Maryland" ,"Massachusetts" ,"Michigan" ,"Minnesota" ,"Mississippi" ,"Missouri" ,"Montana", "Nebraska" ,"Nevada" ,"New Hampshire" ,"New Jersey" ,"New Mexico" ,"New York" ,"North Carolina" ,"North Dakota" ,"Ohio" ,"Oklahoma" ,"Oregon","Pennsylvania", "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin" ,"Wyoming"]
countries=["Afghanistan","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antigua and Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","The Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","People 's Republic of China","Republic of China","Christmas Island","Cocos(Keeling) Islands","Colombia","Comoros","Congo","Cook Islands","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","Gabon","The Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guernsey","Guinea","Guinea - Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","North Korea","South Korea","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Nagorno - Karabakh","Namibia","Nauru","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","Norfolk Island","Turkish Republic of Northern Cyprus","Northern Mariana","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Pitcairn Islands","Poland","Portugal","Puerto Rico","Qatar","Romania","Russia","Rwanda","Saint Barthelemy","Saint Helena","Saint Kitts and Nevis","Saint Lucia","Saint Martin","Saint Pierre and Miquelon","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","Somaliland","South Africa","South Ossetia","Spain","Sri Lanka","Sudan","Suriname","Svalbard","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor - Leste","Togo","Tokelau","Tonga","Transnistria Pridnestrovie","Trinidad and Tobago","Tristan da Cunha","Tunisia","Turkey","Turkmenistan","Turks and Caicos Islands","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","British Virgin Islands","Isle of Man","US Virgin Islands","Wallis and Futuna","Western Sahara","Yemen","Zambia","Zimbabwe"]

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    user = "donor"
    if user == "donor":
        return render_template('DonorProfile/donorProfile.jinja', username="Johnny Bravo", email="Johnny.Bravo@gmail.com", address="123 Rainbow Drive", address2="Apartment 1216B", city="Rochester", state="New York", zipcode="14623")
    else:
        return render_template('CharityProfile/charityProfile.jinja', username="Charity Name", email="charity@gmail.com", address="123 Rainbow Drive", city="Rochester", state="New York", zipcode="14623", country="United States")

@app.route('/personal')
def edit_personal():
    user = "donor"
    if user == "donor":
        return render_template('DonorProfile/donorPersonal.jinja', username="Johnny Bravo", first_name="Johnny", last_name="Bravo", email="Johnny.Bravo@gmail.com", address="123 Rainbow Drive", address2="", city="Rochester", state="New York", zipcode="14623", states=states)
    else:
        return render_template('CharityProfile/charityPersonal.jinja', username="Charity Name", email="charity@gmail.com", address="123 Rainbow Drive", city="Rochester", state="New York", zipcode="14623", country="United States", states=states, countries=countries)
  
@app.route('/savePersonal', methods = ['POST'])
def save_personal():    
    print(request.form["country"])#This is how you get data
    return redirect('../profile')

@app.route('/savePassword', methods = ['POST'])
def save_password():
    return redirect('../profile')

@app.route('/savePayment', methods = ['POST'])
def save_payment():
    return redirect('../payment')

@app.route('/password')
def edit_password():
    user = "Charity Name"
    return render_template('password.jinja', username=user)

@app.route('/payment')
def donor_edit_payment():
	fakeCards = ["5678","6666"]
	return render_template('DonorProfile/donorPayment.jinja', username="Johnny Bravo", cards=fakeCards)

@app.route('/charityHome')
def charity_home():
    info="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris dui lorem, porta sit amet tellus non, semper blandit augue. Vivamus vitae ligula quis neque venenatis blandit eget nec sapien. Duis sodales orci in est feugiat lobortis. Integer non purus sem. Vestibulum eu fermentum tellus, eu vulputate leo. Aliquam vitae est nec diam ornare efficitur. Aenean congue fermentum justo, aliquam porta velit consequat nec. Duis ac tortor metus.."
    pics=['tree1.jpg','tree2.jpg','tree3.jpg','tree4.jpg']
    message="Thank you for your donation!"
    return render_template('charityHome.jinja', username="Johnny Bravo", charityName="I LUV TREES", info=info, pics=pics, message=message)

@app.route('/newsFeed')
def news_feed():
    charities = getDonorFavorites(1)
    news = []
    message=""
    for c in charities:
        news.append(getCharityPosts(c['charId']))
    return render_template('newsFeed.jinja', username="Johnny Bravo", news = news[0], message=message)

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

@app.route('/donationConfirmation')
def donationConfirmation():
    donation={'card':1234,'amount':100,'charity':'Electronic Frontier Foundation'}
    return render_template('donation/confirm.jinja', donation = donation)

@app.route('/donate')
def donate():
    creditCard = {'last4':1234}
    charity = {'name':'Electronic Frontier Foundation'}
    return render_template('donation/donation.jinja', charity=charity, creditCard=creditCard)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()

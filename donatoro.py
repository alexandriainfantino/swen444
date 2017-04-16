from flask import Flask, render_template, redirect, request, g, session
from dataBaseLogic import *

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

states=["Alabama" ,"Alaska" ,"Arizona" ,"Arkansas" ,"California" ,"Colorado","Connecticut","Delaware" ,"Florida","Georgia" ,"Hawaii" ,"Idaho","Illinois", "Indiana" ,"Iowa" ,"Kansas" ,"Kentucky" ,"Louisiana" ,"Maine" ,"Maryland" ,"Massachusetts" ,"Michigan" ,"Minnesota" ,"Mississippi" ,"Missouri" ,"Montana", "Nebraska" ,"Nevada" ,"New Hampshire" ,"New Jersey" ,"New Mexico" ,"New York" ,"North Carolina" ,"North Dakota" ,"Ohio" ,"Oklahoma" ,"Oregon","Pennsylvania", "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin" ,"Wyoming"]
countries=["Afghanistan","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antigua and Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","The Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","People 's Republic of China","Republic of China","Christmas Island","Cocos(Keeling) Islands","Colombia","Comoros","Congo","Cook Islands","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","Gabon","The Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guernsey","Guinea","Guinea - Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","North Korea","South Korea","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Nagorno - Karabakh","Namibia","Nauru","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","Norfolk Island","Turkish Republic of Northern Cyprus","Northern Mariana","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Pitcairn Islands","Poland","Portugal","Puerto Rico","Qatar","Romania","Russia","Rwanda","Saint Barthelemy","Saint Helena","Saint Kitts and Nevis","Saint Lucia","Saint Martin","Saint Pierre and Miquelon","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","Somaliland","South Africa","South Ossetia","Spain","Sri Lanka","Sudan","Suriname","Svalbard","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor - Leste","Togo","Tokelau","Tonga","Transnistria Pridnestrovie","Trinidad and Tobago","Tristan da Cunha","Tunisia","Turkey","Turkmenistan","Turks and Caicos Islands","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","British Virgin Islands","Isle of Man","US Virgin Islands","Wallis and Futuna","Western Sahara","Yemen","Zambia","Zimbabwe"]

@app.errorhandler(404)
def pageNotFound(error):
    return redirect('./')

@app.errorhandler(500)
def pageNotFound(error):
    return redirect('./')

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    user = getUserById(session['userId'])
    if user["isDonor"] == 1:        
        info = getDonorInfoByUserId(session['userId'])
        return render_template('DonorProfile/donorProfile.jinja', username=(info["firstName"]+" "+info["lastName"]), email=user["email"], address=info["streetAdd1"], address2=info["streetAdd2"], city=info["city"], state=info["state"], zipcode=info["zip"])
    else:
        info = getCharityInfoByUserId(session['userId'])
        return render_template('CharityProfile/charityProfile.jinja', username=info["name"], email=user["email"], address=info["streetAdd"], city=info["city"], state=info["state"], zipcode=info["zip"], country=info["country"])

@app.route('/personal')
def edit_personal():
    user = getUserById(session['userId'])
    if user["isDonor"] == 1:        
        info = getDonorInfoByUserId(session['userId'])
        return render_template('DonorProfile/donorPersonal.jinja', username=(info["firstName"]+" "+info["lastName"]), first_name=info["firstName"], last_name=info["lastName"], email=user["email"], address=info["streetAdd1"], address2=info["streetAdd2"], city=info["city"], state=info["state"], zipcode=info["zip"], states=states)
    else:
        info = getCharityInfoByUserId(session['userId'])
        return render_template('CharityProfile/charityPersonal.jinja', username=info["name"], email=user["email"], address=info["streetAdd"], city=info["city"], state=info["state"], zipcode=info["zip"], country=info["country"], states=states, countries=countries)
  
@app.route('/password')
def edit_password():
    user = getUserById(session['userId'])
    if user["isDonor"] == 1:
        info = getDonorInfoByUserId(session['userId'])
        return render_template('password.jinja', username=(info["firstName"]+" "+info["lastName"]), message="")
    else:
        info = getCharityInfoByUserId(session['userId'])
        return render_template('password.jinja', username=info["name"], message="")

@app.route('/payment')
def donor_edit_payment():
    user = getUserById(session['userId'])
    if user["isDonor"] == 1:
        info = getDonorInfoByUserId(session['userId'])  
        cards = []      
        for card in getCreditCardByUserId(session['userId']):
            cards.append(dict(num=str(card["ccn"])[-4:],id=card["id"]))
        return render_template('DonorProfile/donorPayment.jinja', username=(info["firstName"]+" "+info["lastName"]), cards=cards, states=states)


#FORM ACTIONS  
@app.route('/savePersonal', methods = ['POST'])
def save_personal():   
    user = getUserById(session['userId'])
    if user["isDonor"] == 1: 
        editDonorPersonalInfo(user["email"], request.form["emailInput"], request.form["firstName"], request.form["lastName"], request.form["streetAddress1"], request.form["streetAddress2"], request.form["city"], request.form["state"], request.form["zip"]) 
    else:
        editCharityPersonalInfo(user["email"], request.form["emailInput"], request.form["streetAddress1"], request.form["city"], request.form["state"], request.form["zip"], request.form["country"]) 
    return redirect('../profile')

@app.route('/savePassword', methods = ['POST'])
def save_password():
    user = getUserById(session['userId'])
    print(request.form["oldpassword"]+" - "+user["password"])
    if request.form["oldpassword"] == user["password"]:
        editPassword(user["email"],request.form["newpassword"])
        return redirect('../profile')
    else:
        if user["isDonor"] == 1:
            info = getDonorInfoByUserId(session['userId'])
            return render_template('password.jinja', username=(info["firstName"]+" "+info["lastName"]), message="Password Does Not Match Current Password!")
        else:
            info = getCharityInfoByUserId(session['userId'])
            return render_template('password.jinja', username=info["name"], message="Password Does Not Match Current Password!")

@app.route('/savePayment', methods = ['POST'])
def save_payment():
    print("HIT")
    addCreditCard("Johnny.Bravo@gmail.com", request.form["ccNum"], request.form["ccv"], request.form["expMonth"], request.form["expYear"], request.form["streetAddress1"], request.form["streetAddress2"], request.form["city"], request.form["state"], request.form["zip"])
    return redirect('../payment')

@app.route('/removeCards', methods = ['POST'])
def remove_cards():
    for card in request.form:
        deleteCard("Johnny.Bravo@gmail.com", card)
    return redirect('../payment')



@app.route('/charityHome/<charity>')
def charity_home(charity):
    userInfo = getDonorInfoByUserId(session['userId'])
    info = getCharityInfoByName(charity)
    pics=['tree1.jpg','tree2.jpg','tree3.jpg','tree4.jpg']
    return render_template('charityHome.jinja', username=(userInfo["firstName"]+" "+userInfo["lastName"]), charityName=info["name"], info=info["description"], pics=pics, message="")

@app.route('/newsFeed')
def news_feed():
    charities = getDonorFavorites(session['userId'])
    news = []
    message=""
    for c in charities:
        news.append(getCharityPosts(c['charId']))
    return render_template('newsFeed.jinja', username="Johnny Bravo", news = news[0], message=message)

@app.route('/')
def log_in():
    return render_template('logIn.jinja')

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = getUserByEmail(request.form['email'])
    session['userId'] = user["id"]
    if user["isDonor"] == 1:
        return redirect('../newsFeed')
    else:
        #Charity Admin Page
        pass

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('userId', None)
    return redirect('/')

@app.route('/selection')
def selection():
    return render_template('registration/selection.jinja')

@app.route('/charityRegistration1')
def charityRegistrationOne():
    return render_template('registration/charityRegistration/registrationPage1.jinja')

@app.route('/charityRegistration2')
def charityRegistration2():
    return render_template('registration/charityRegistration/registrationPage2.jinja', states=states, countries=countries)

@app.route('/charityConfirmation')
def charityConfirmation():
    charityInformation = {"name":"Fake Charity", "501c":"123456789", "tags": "Environment", "email":"fakeCharity@fakeCharity.com", "billing": "1 Main St, Rochester, NY, 14623", "description":"This organization is aimed to plant 50,000 new trees every year, as well as replant trees in areas across the country affected by natural disasters. All trees planted will be native to the area they are planted in to avoid introducing invasive species."}
    return render_template('registration/charityRegistration/confirmation.jinja', charityInfo = charityInformation)

@app.route('/donorRegistration')
def donorRegistration():
    return render_template('registration/donorRegistration/donorRegistration.jinja', states=states)

@app.route('/donorBilling')
def donorBilling():
    return render_template('registration/donorRegistration/donorBilling.jinja', states=states)

@app.route('/donationConfirmation')
def donationConfirmation():
    donation={'card':1234,'amount':100,'charity':'Electronic Frontier Foundation'}
    return render_template('donation/confirm.jinja', username="Johnny Bravo", donation = donation)

@app.route('/donate/<charity>')
def donate(charity):
    creditCard = {'last4':1234}
    charityName = {'name':charity}
    return render_template('donation/donation.jinja', username="Johnny Bravo", charity=charityName, creditCard=creditCard, states=states)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()

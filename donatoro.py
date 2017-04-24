from flask import Flask, render_template, redirect, request, g, session
from dataBaseLogic import *
import sys
import ast

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
        return redirect('../charity/admin')

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

@app.route('/donationConfirmation/<charity>', methods=["POST"])
def donationConfirmation(charity):
    user = getUserById(session['userId'])
    search_term = request.form['searchQuery']
    donation = {'charity': charity}
    if "radio" in request.form:
        if request.form['radio'] == "new":
            donation['radio'] = request.form['radio']
        else:
            donation['radio'] = "saved"
    # User using a new card.
    print "FORM", request.form
    if request.form['radio'] == "new":
        # Billing Location Info Submitted
        if "streetAddress1" in request.form:
            donation['streetAddress1'] = request.form['streetAddress1']
        if "streetAddress2" in request.form:
            donation['streetAddress2'] = request.form['streetAddress2']
        if "city" in request.form:
            donation['city'] = request.form['city']
        if "state" in request.form:
            donation['state'] = request.form['state']
        if "zip" in request.form:
            donation['zip'] = request.form['zip']
        print "Filled in loc"
        # Credit Card Info Submitted
        if "ccNum" in request.form:
            donation['ccNum'] = request.form['ccNum']
            donation['last4'] = request.form['ccNum'][-4:]
        if "ccv" in request.form:
            donation['ccv'] = request.form['ccv']
        if "expMonth" in request.form:
            donation['expMonth'] = request.form['expMonth']
        if "expYear" in request.form:
            donation['expYear'] = request.form['expYear']
        print "Filled in CC"
    else:
        ccInfo = ast.literal_eval(request.form['radio'])
        print ccInfo
        if "streetAdd1" in ccInfo:
            donation['streetAddress1'] = ccInfo['streetAdd1']
        if "streetAdd2" in ccInfo:
            donation['streetAddress2'] = ccInfo['streetAdd2']
        if "city" in ccInfo:
            donation['city'] = ccInfo['city']
        if "state" in ccInfo:
            donation['state'] = ccInfo['state']
        if "zip" in ccInfo:
            donation['zip'] = ccInfo['zip']
        # Credit Card Info Submitted
        if "ccn" in ccInfo:
            donation['ccNum'] = ccInfo['ccn']
            donation['last4'] = str(ccInfo['ccn'])[-4:]
        if "ccv" in ccInfo:
            donation['ccv'] = ccInfo['ccv']
        if "expMonth" in ccInfo:
            donation['expMonth'] = ccInfo['expMonth']
        if "expYear" in ccInfo:
            donation['expYear'] = ccInfo['expYear']
    if "amount" in request.form:
        donation['amount'] = request.form['amount']
    if user["isDonor"] == 1:
        info = getDonorInfoByUserId(session['userId'])
    print donation['last4']
    return render_template('donation/confirm.jinja', username=(info["firstName"] + " " + info["lastName"]), email=user["email"], donation = donation, query=search_term)

@app.route('/donate/<charity>', methods=['POST'])
def donate(charity):
    user = getUserById(session['userId'])
    search_term = request.form['searchQuery']

    if user["isDonor"] == 1:
        info = getDonorInfoByUserId(session['userId'])
        credit_cards = getCreditCardByUserId(info['userId'])
        for card in credit_cards:
            print card

    donation = {}
    if 'radio' in request.form:
        # Going back from confirmation page to donate page, after filling in new credit card.
        if request.form['radio'] == "new":
            donation['radio'] = "new"
            if "streetAddress1" in request.form:
                donation['streetAddress1'] = request.form['streetAddress1']
            else:
                donation['streetAddress1']=""
            if "streetAddress2" in request.form:
                donation['streetAddress2'] = request.form['streetAddress2']
            else:
                donation['streetAddress2']=""
            if "city" in request.form:
                donation['city'] = request.form['city']
            else:
                donation['city']=""
            if "state" in request.form:
                donation['state'] = request.form['state']
            else:
                donation['state']=""
            if "zip" in request.form:
                donation['zip'] = request.form['zip']
            else:
                donation['zip']=""
            # Credit Card Info Submitted
            if "ccNum" in request.form:
                donation['ccNum'] = request.form['ccNum']
                donation['last4'] = request.form['ccNum'][-4:]
            else:
                donation['ccNum']=""
                donation['last4'] = ""
            if "ccv" in request.form:
                donation['ccv'] = request.form['ccv']
            else:
                donation['ccv']=""
            if "expMonth" in request.form:
                donation['expMonth'] = request.form['expMonth']
            else:
                donation['expMonth']=""
            if "expYear" in request.form:
                donation['expYear'] = request.form['expYear']
            else:
                donation['expYear']=""
        if "ccNum" in request.form:
            donation['ccNum'] = request.form['ccNum']
            donation['last4'] = request.form['ccNum'][-4:]
        else:
            donation['ccNum'] = ""
            donation['last4'] = ""
        if "amount" in request.form:
            donation['amount'] = request.form['amount']
        else:
            donation['amount']=""


    charityName = {'name':charity}
    return render_template('donation/donation.jinja', username=(info["firstName"] + " " + info["lastName"]), email=user["email"], charity=charityName, creditCard=credit_cards, states=states, query=search_term, donation=donation)

@app.route('/enterDonation', methods=['POST'])
def enter_donation():
    addr1 = request.form['streetAddress1']
    addr2 = request.form['streetAddress2']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    ccNum = request.form['ccNum']
    ccv = request.form['ccv']
    expMonth = request.form['expMonth']
    expYear = request.form['expYear']
    amount = request.form['amount']
    charity = request.form['charity']
    return redirect('/newsFeed')

@app.route('/charity/admin')
def charity_admin_welcome():
    info = getCharityInfoByUserId(session['userId'])
    return render_template('charity/charityAdminWelcome.jinja', username=info["name"])

@app.route('/charity/stats')
def charity_admin_stats():
    info = getCharityInfoByUserId(session['userId'])
    return render_template('charity/charityAdminStats.jinja', username=info["name"])

@app.route('/results', methods=['POST'])
def results():
    # results = [
    #     {'Title':'Electronic Frontier Foundation','Description':'EFF'}
    #     ,{'Title':'Canonical','Description':'Creators of Ubuntu'}
    #     #,{'Title':'I Love Trees', 'Description':'We Plant Trees'}
    # ]
    search_term = request.form['searchQuery']
    user = getUserById(session['userId'])
    if user["isDonor"] == 1:
        info = getDonorInfoByUserId(session['userId'])
        all_tags = getTags()
        search_tags = []
        for item in all_tags:
            if search_term in str(item['tag']):
                search_tags.append(item['tag'].encode("ascii"))
        print search_tags

        search_results = []
        counter = 0
        temp = []
        for tag in search_tags:
            for item in getCharitiesByTags(tag):
                temp.append(
                    {'Description':item['description'],
                     'Title':item['name']
                     }
                )
                counter+=1
                if counter%2 ==0:
                    search_results.append(temp)
                    temp = []
            if len(temp) != 0:
                search_results.append(temp)

        print search_term
        return render_template('searchResults.jinja', results=search_results, username=(info["firstName"] + " " + info["lastName"]), email=user["email"], query=search_term)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    if len(sys.argv) > 1:
        app.run(host='0.0.0.0', port=sys.argv[1])
    else:
        app.run()

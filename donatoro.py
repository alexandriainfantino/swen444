from flask import Flask, render_template, redirect, request, g, session, url_for
from dataBaseLogic import *
import sys
import ast
import traceback

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.debug = True

states=["Alabama" ,"Alaska" ,"Arizona" ,"Arkansas" ,"California" ,"Colorado","Connecticut","Delaware" ,"Florida","Georgia" ,"Hawaii" ,"Idaho","Illinois", "Indiana" ,"Iowa" ,"Kansas" ,"Kentucky" ,"Louisiana" ,"Maine" ,"Maryland" ,"Massachusetts" ,"Michigan" ,"Minnesota" ,"Mississippi" ,"Missouri" ,"Montana", "Nebraska" ,"Nevada" ,"New Hampshire" ,"New Jersey" ,"New Mexico" ,"New York" ,"North Carolina" ,"North Dakota" ,"Ohio" ,"Oklahoma" ,"Oregon","Pennsylvania", "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin" ,"Wyoming"]
countries=["Afghanistan","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antigua and Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","The Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","People 's Republic of China","Republic of China","Christmas Island","Cocos(Keeling) Islands","Colombia","Comoros","Congo","Cook Islands","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","Gabon","The Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guernsey","Guinea","Guinea - Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","North Korea","South Korea","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Nagorno - Karabakh","Namibia","Nauru","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","Norfolk Island","Turkish Republic of Northern Cyprus","Northern Mariana","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Pitcairn Islands","Poland","Portugal","Puerto Rico","Qatar","Romania","Russia","Rwanda","Saint Barthelemy","Saint Helena","Saint Kitts and Nevis","Saint Lucia","Saint Martin","Saint Pierre and Miquelon","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","Somaliland","South Africa","South Ossetia","Spain","Sri Lanka","Sudan","Suriname","Svalbard","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor - Leste","Togo","Tokelau","Tonga","Transnistria Pridnestrovie","Trinidad and Tobago","Tristan da Cunha","Tunisia","Turkey","Turkmenistan","Turks and Caicos Islands","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","British Virgin Islands","Isle of Man","US Virgin Islands","Wallis and Futuna","Western Sahara","Yemen","Zambia","Zimbabwe"]

@app.errorhandler(Exception)
def exception_handler(e):
    if app.debug:
        stack = traceback.format_exc()
        return render_template('error-debug.jinja', error=e, stack=stack), 500
    else:
        return render_template()

def render_template_logged_in(template, **context):
    user = getUserById(session['userId'])
    info = getInfoByUserId(session['userId'])
    return render_template(template, user=user, userInfo=info, **context)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    user = getUserById(session['userId'])
    if user["isDonor"]:
        return render_template_logged_in('DonorProfile/donorProfile.jinja')
    else:
        return render_template_logged_in('CharityProfile/charityProfile.jinja')

@app.route('/personal')
def edit_personal():
    user = getUserById(session['userId'])
    if user["isDonor"] == 1:
        return render_template_logged_in('DonorProfile/donorPersonal.jinja', states=states)
    else:
        return render_template_logged_in('CharityProfile/charityPersonal.jinja', states=states, countries=countries)
  
@app.route('/password')
def edit_password():
    user = getUserById(session['userId'])
    if user["isDonor"] == 1:
        return render_template_logged_in('password.jinja', message="")
    else:
        return render_template_logged_in('password.jinja', message="")

@app.route('/payment')
def donor_edit_payment():
    user = getUserById(session['userId'])
    if user["isDonor"] == 1:
        cards = []      
        for card in getCreditCardByUserId(session['userId']):
            cards.append(dict(num=str(card["ccn"])[-4:],id=card["id"]))
        return render_template_logged_in('DonorProfile/donorPayment.jinja', cards=cards, states=states)


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
    if request.form["oldpassword"] == user["password"]:
        editPassword(user["email"],request.form["newpassword"])
        return redirect('../profile')
    else:
        if user["isDonor"] == 1:
            return render_template_logged_in('password.jinja', message="Password Does Not Match Current Password!")
        else:
            return render_template_logged_in('password.jinja', message="Password Does Not Match Current Password!")

@app.route('/savePayment', methods = ['POST'])
def save_payment():
    addCreditCard("Johnny.Bravo@gmail.com", request.form["ccNum"], request.form["ccv"], request.form["expMonth"], request.form["expYear"], request.form["streetAddress1"], request.form["streetAddress2"], request.form["city"], request.form["state"], request.form["zip"])
    return redirect('../payment')

@app.route('/removeCards', methods = ['POST'])
def remove_cards():
    for card in request.form:
        deleteCard("Johnny.Bravo@gmail.com", card)
    return redirect('../payment')



@app.route('/charityHome/<charity>')
def charity_home(charity):
    charityInfo = getCharityInfoByName(charity)
    pics=['tree1.jpg','tree2.jpg','tree3.jpg','tree4.jpg']
    return render_template_logged_in('charityHome.jinja', charityInfo=charityInfo, pics=pics, message="")

@app.route('/newsFeed')
def news_feed():
    charities = getDonorFavorites(session['userId'])
    if len(charities) < 1:
        charities = getAllCharities()
    news = []
    message=""
    if session.get('message'):
        print("HiT")
        if session['message'] == 1:
            message = "Thank you for registering! You have now been logged in!"
        elif session['message'] == 2:
            message = "Thank you for your donation!"
        session.pop('message',None)
    for c in charities:
        news.append(getCharityPosts(c['charId']))
    return render_template_logged_in('newsFeed.jinja', news = news[0], message=message)

@app.route('/')
def log_in():
    return render_template('logIn.jinja', error1="", error2="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = getUserByEmail(request.form['email'])
    if user != None:
        if user["password"] == request.form['password']:
            session['userId'] = user["id"]
            if user["isDonor"] == 1:
                return redirect('../newsFeed')
            else:
                return redirect('../charity/admin')
        else:
            error1 = ""
            error2 = "Password Does Not Match!"
    else:
            error1 = "Email Not Found!"
            error2 = ""
    return render_template('logIn.jinja', error1=error1, error2=error2)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('userId', None)
    return redirect('/')

@app.route('/selection')
def selection():
    session.clear()
    return render_template('registration/selection.jinja')

@app.route('/charityRegistration1')
def charityRegistrationOne():
    return render_template('registration/charityRegistration/registrationPage1.jinja')

@app.route('/charityRegistration2', methods=['POST'])
def charityRegistration2():
    session['charityName'] = request.form['charityName']
    session['501c'] = request.form['501c']
    session['tags'] = request.form['tags']
    session['description'] = request.form['description']
    session['email'] = request.form['email']
    return render_template('registration/charityRegistration/registrationPage2.jinja', states=states, countries=countries)

@app.route('/charityConfirmation', methods=['POST'])
def charityConfirmation():
    addressInfo = []
    addressInfo.append(request.form['streetAddress'])
    addressInfo.append(request.form['city'])
    addressInfo.append(request.form['state'])
    addressInfo.append(request.form['zip'])
    charityInformation = {"name":session['charityName'], "501c":session['501c'], "tags": session['tags'], "email":session['email'], "billing": addressInfo, "description":session['description']}
    return render_template('registration/charityRegistration/confirmation.jinja', charityInfo = charityInformation)

@app.route('/donorRegistration')
def donorRegistration():
    return render_template('registration/donorRegistration/donorRegistration.jinja', states=states)

@app.route('/donorBilling', methods=["POST"])
def donorBilling():
    if request.form:
        formData = request.form
        session['email'] = request.form['email']
        session['firstName'] =request.form['firstName']
        session['lastName'] = request.form['lastName']
        session['streetAddress1'] = request.form['streetAddress1']
        session['streetAddress2'] = request.form['streetAddress2']
        session['city'] = request.form['city']
        session['state'] = request.form['state']
        session['zip'] = request.form['zip']
        return render_template('registration/donorRegistration/donorBilling.jinja', states=states, formData=formData)
    else:
        return redirect('/donorRegistration')

@app.route('/donorRegister', methods=["POST"])
def donorRegister():
    formData = request.form
    userId = addDonor(formData['email'], formData['password'], formData['fname'], formData['lname'], formData['addr1'], formData['addr2'], formData['city'], formData['state'], formData['zip'])
    if formData["ccNum"]:
        addCreditCard(formData['email'], formData['ccNum'], formData['ccv'], formData['expMonth'], formData['expYear'], formData['ccAddr1'], formData['ccAddr2'], formData['ccCity'], formData['ccState'], formData['ccZip'])
    user = getUserById(userId)
    if user != None:
        session['userId'] = userId
        session['message'] = 1
        if user["isDonor"] == 1:
            return redirect('../newsFeed')
        else:
            return redirect('../charity/admin')
    return redirect('/')


@app.route('/donationConfirmation/<charity>', methods=["POST"])
def donationConfirmation(charity):
    user = getUserById(session['userId'])
    search_term = ""
    if 'searchQuery' in request.args:
        search_term = request.args['searchQuery']
    donation = {'charity': charity}
    if "radio" in request.form:
        if request.form['radio'] == "new":
            donation['radio'] = request.form['radio']
        else:
            donation['radio'] = "saved"
    # User using a new card.
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
    else:
        ccInfo = ast.literal_eval(request.form['radio'])
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
        info = getInfoByUserId(session['userId'])
    return render_template_logged_in('donation/confirm.jinja', donation = donation, query=search_term)



@app.route('/donate/<charity>', methods=['GET', 'POST'])
def donate(charity):
    user = getUserById(session['userId'])
    search_term = ""
    if 'searchQuery' in request.args:
        search_term = request.args['searchQuery']

    if user["isDonor"] == 1:
        info = getInfoByUserId(session['userId'])
        credit_cards = getCreditCardByUserId(info['userId'])

    donation = {}
    if request.method == 'POST':
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

    return render_template_logged_in('donation/donation.jinja', charity=charityName, creditCard=credit_cards, states=states, donation=donation, query=search_term)

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
    session['message'] = 2
    return redirect('/newsFeed')

@app.route('/charity/admin')
def charity_admin_welcome():
    return render_template_logged_in('charity/charityAdminWelcome.jinja')

@app.route('/charity/stats')
def charity_admin_stats():
    return render_template_logged_in('charity/charityAdminStats.jinja')

@app.route('/results', methods=['GET'])
def results():
    # results = [
    #     {'Title':'Electronic Frontier Foundation','Description':'EFF'}
    #     ,{'Title':'Canonical','Description':'Creators of Ubuntu'}
    #     #,{'Title':'I Love Trees', 'Description':'We Plant Trees'}
    # ]

    #search_term = request.form['searchQuery']
    search_term = ""
    if 'searchQuery' in request.args:
        search_term = request.args['searchQuery']
    user = getUserById(session['userId'])
    if user["isDonor"] == 1:
        info = getInfoByUserId(session['userId'])
        all_tags = getTags()
        search_tags = []
        for item in all_tags:
            if search_term in str(item['tag']):
                search_tags.append(item['tag'])

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

        return render_template_logged_in('searchResults.jinja', results=search_results, query=search_term)


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    if len(sys.argv) > 1:
        app.run(host='0.0.0.0', port=int(sys.argv[1]))
    else:
        app.run()

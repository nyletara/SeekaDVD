
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import stripe

from flask_cors import CORS, cross_origin 

STRIPE_PUBLISHABLE_KEY = 'pk_test_HPcZRSKmS17XqjEEA48QoYvh'  
STRIPE_SECRET_KEY = 'sk_test_TRBGyYCU1ze6s9uOhBSr52f5'

stripe.api_key = STRIPE_SECRET_KEY
stripe.api_base = "https://api-tls12.stripe.com"

application = Flask(__name__,template_folder='templates')

CORS(application)

application.config['MONGO_DBNAME'] = 'userdb'
application.config['MONGO_URI'] = 'mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb'

mongo = PyMongo(application)

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

@application.route('/')
def index():
    return render_template('login.html')

@application.route('/login', methods=['POST', 'GET'])
#@jwt_required()
def login():
    print('Cool stuff bro')
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['inputEmail']})

    if login_user:
        if request.form['inputPassword'] == login_user['password'] :    
            session['inputEmail'] = request.form['inputEmail']
            email = request.form['inputEmail']
            return render_template('index3.html', email=email)

    return 'Invalid inputEmail/password combination'

@application.route('/register', methods=['POST', 'GET'])
def register():
    print('registering user')
    if request.method == 'POST':
        try: 
            users = mongo.db.users
            existing_user = users.find_one({'name' : request.form['inputEmail']})
        except:
            print "failed to find user"

        if existing_user is None:
            print('creating user')
            hashpass = request.form['inputPassword']
            users.insert({'name' : request.form['inputEmail'], 'password' : hashpass})
            session['inputEmail'] = request.form['inputEmail']
            email = request.form['inputEmail']
            return render_template('index3.html', email=email)
        
        return 'That inputEmail already exists!'
#
    return render_template('login.html')


@application.route('/payment', methods=['POST', 'GET'])
def payment():
    
    print("Making payment")
    token = request.form['stripeToken']
    # Amount in cents
    amount = 25000
    print(token)

    # customer = stripe.Customer.create(
    #    email=request.form['stripeEmail'],
    #    source=request.form['stripeToken']
    # )

    # print("Customer created")
    # print(customer)

    print("Charging Customer")
    charge = stripe.Charge.create(
        amount=amount,
        currency='usd',
        # customer=request.form['stripeEmail'],
        description='A payment for the Hello World project',
        source=token
    )
    print(charge)

    return render_template('index3.html')

if __name__ == '__main__':
    
    application.secret_key = 'newsecret'
    application.run(debug=True, host='0.0.0.0')
from CryptoReturns import application, db
from flask import Flask, render_template, redirect, request, flash, url_for, session, jsonify
from decimal import *
from pycoingecko import CoinGeckoAPI
from sqlalchemy.sql import func
from CryptoReturns.forms import Crypto_Form
from functools import wraps
from werkzeug.exceptions import HTTPException
from six.moves.urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth



# Import data from models.py file
from CryptoReturns.models import Coin

import requests
import json
import os
cg = CoinGeckoAPI()

oauth = OAuth(application)

auth0 = oauth.register(
    'auth0',
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    api_base_url=os.environ.get("AUTH0_DOMAIN"),
    access_token_url=os.environ.get("AUTH0_ACCESS_TOKEN_URL"),
    authorize_url=os.environ.get("AUTH0_AUTHROIZE_URL"),
    client_kwargs={
        'scope': 'openid profile email',
    },
)

@application.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    print(ex)
    return response

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)
    return decorated

# Controllers API
@application.route('/')
def home():
    return render_template('home.html')

# Here we're using the /callback route.

@application.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    
    return redirect('/dashboard')

@application.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=os.environ.get('AUTH0_CALLBACK_URL'))

@application.route('/signup')
def signup():
    return auth0.authorize_redirect(redirect_uri=os.environ.get('AUTH0_CALLBACK_URL'))

@application.route("/dashboard", methods=["GET", "POST"])
@requires_auth
def dashboard():
    form = Crypto_Form()
    coins = None
    #print(form.submit.data)
    print('------ {0}'.format(request.form))
    print(form.errors, "Test")
    
    # The form validates regardless if it's True or False weird.
    if form.validate_on_submit():
        try:
            TWOPLACES = Decimal(10) ** -2
            Decimal('3.214').quantize(TWOPLACES)
            user_input = form.name.data
            coin_name = user_input.lower().replace(" ", "-")
            coin_gecko_name = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            initial_investment = form.intial_investment.data
            coin_image = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            coin_price = float(cg.get_price(ids=[coin_name.lower()], vs_currencies='usd')[coin_name.lower()]['usd'])
            presale_price = form.coin_price.data
            multiplier = Decimal(float(coin_price) / float(presale_price)).quantize(TWOPLACES)
            profit = round((float(initial_investment) / float(presale_price)) * float(coin_price))
            twenty_four_hour_change = Decimal(cg.get_price(ids=[coin_name.lower()], vs_currencies='usd', include_24hr_change='true')[coin_name.lower()]['usd_24h_change']).quantize(TWOPLACES)
            ath = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            ath_change_percentage = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            session['name'] = form.name.data
            #coin_gecko_sparkline = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='true')[0]
            
            coin = Coin(
                        crypto_name=coin_gecko_name['name'],
                        coin_initial_invesment=initial_investment,
                        image=coin_image['image'],
                        current_price=coin_price,
                        presale_price=presale_price,
                        multiple= multiplier,
                        profit=profit,
                        twenty_four_hour=twenty_four_hour_change,
                        all_time_high=ath['ath'],
                        all_time_percentage_change=Decimal(ath['ath_change_percentage']).quantize(TWOPLACES),
                        #sparkline=coin_gecko_sparkline['sparkline_in_7d']['price']
                        )
            #print(coin.crypto_name)
            #duplicate_coin = Coin.query.filter_by(crypto_name=coin_gecko_name['name']).first()
            
            
            # Check if the coin already exist
            #if duplicate_coin == None:
                #q = db.session.query(coin).filter(coin.crypto_name)
                #session.query(q.exists())
            db.session.add(coin)
            db.session.commit()
            
            
            
            #print(coin_profit)
            
            #qry = db.session.query(func.max(coin.profit).label("profit"))
            #print(qry)
            # Delete the coin and overwrite it with the new information
            # Or maybe update the coin instead
            """elif duplicate_coin != None:
                #Coin.query.filter(Coin.id == 123).delete()
                coin.crypto_name = coin_gecko_name['name']
                coin.coin_initial_invesment=initial_investment
                db.session.commit()
                #db.session.delete()
                print(coin.crypto_name + "Already exist!")"""
            #print(user_input)
        except Exception as e:
            db.session.rollback()
            print('Failed to add coin')
            print(e)
            #print(coin_name)
            flash(f"Could not find {coin_name}. Please try again.")
        return redirect(url_for('dashboard'))
    coins = Coin.query.all()
    coin_profit = Coin.query.with_entities(func.sum(Coin.profit).label('total')).first().total
    if coin_profit is None:
        coin_profit = 0
    return render_template("dashboard.html", coins=coins, value=coin_profit, form=form, name=session.get('name'), userinfo=session['profile'])
    """ return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4)) """

@application.route("/profile", methods=["GET", "POST"])
@requires_auth
def profile():
    
    return render_template("profile.html",
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


@application.route("/update", methods=["GET", "POST"])
def update():
    newcrypto_name = request.form.get("newcrypto_name")
    oldcrypto_name = request.form.get("oldcrypto_name")
    #coin_name = newcrypto_name.lower().replace(" ", "-")

    # Need to restrict user to certain coins in the future
    coin_gecko_name = cg.get_coins_markets(vs_currency='usd', ids=[newcrypto_name.lower().replace(" ", "-")], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
    
    
    coin = Coin.query.filter_by(crypto_name=oldcrypto_name).first()
    coin.crypto_name = coin_gecko_name['name']
    #coin.
    db.session.commit()
    
    return redirect("dashboard")

@application.route("/delete", methods=["POST"])
def delete():
    crypto_name = request.form.get("coin")
    coin = Coin.query.filter_by(crypto_name=crypto_name).first()
    db.session.delete(coin)
    db.session.commit()
    
    return redirect("dashboard")

@application.route('/logout')
def logout():

    # clear session stored data

    session.clear()

    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'm2kNjhXz5Y9ZSQed20pH38VSNvB7KeLH'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

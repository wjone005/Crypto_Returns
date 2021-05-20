import requests
import json
import os

from pycoingecko import CoinGeckoAPI

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import flash

from flask_sqlalchemy import SQLAlchemy

from decimal import *

cg = CoinGeckoAPI()

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "Coin_Database.db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'something only you know'

db = SQLAlchemy(app)

class Coin(db.Model):

    crypto_name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    image = db.Column(db.String(80), unique=False, nullable=True)
    current_price = db.Column(db.Float(), unique=False, nullable=True)
    presale_price = db.Column(db.Float(), unique=False, nullable=True)
    multiple = db.Column(db.Float(), unique=False, nullable=True)
    coin_initial_invesment = db.Column(db.Float(), unique=False, nullable=True)
    profit = db.Column(db.Float(), unique=False, nullable=True)
    twenty_four_hour = db.Column(db.Float(), unique=False, nullable=True)
    all_time_high = db.Column(db.Float(), unique=False, nullable=True)
    all_time_percentage_change = db.Column(db.Float(), unique=False, nullable=True)
    sparkline = db.Column(db.String(80), unique=False, nullable=True)
    def __repr__(self):
        return "<Crypto_name: {}>".format(self.crypto_name)

@app.route("/", methods=["GET", "POST"])

def home():
    coins = None

    if request.form:
        try:
            
            TWOPLACES = Decimal(10) ** -2
            Decimal('3.214').quantize(TWOPLACES)
            user_input = request.form.get("coin")
            coin_name = user_input.lower().replace(" ", "-")
            coin_gecko_name = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            initial_investment = request.form.get("initial_investment")
            coin_image = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            coin_price = float(cg.get_price(ids=[coin_name.lower()], vs_currencies='usd')[coin_name.lower()]['usd'])
            presale_price = float(request.form.get("presale_price"))
            multiplier = Decimal(float(coin_price) / float(presale_price)).quantize(TWOPLACES)
            profit = round((float(initial_investment) / float(presale_price)) * float(coin_price))
            twenty_four_hour_change = Decimal(cg.get_price(ids=[coin_name.lower()], vs_currencies='usd', include_24hr_change='true')[coin_name.lower()]['usd_24h_change']).quantize(TWOPLACES)
            ath = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            ath_change_percentage = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            print(ath_change_percentage)
            #coin_gecko_sparkline = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='true')[0]
            print(type(ath_change_percentage))
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
            #q = db.session.query(coin).filter(coin.name == coin_name)
            #session.query(q.exists())
            db.session.add(coin)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Failed to add coin')
            print(e)
            #print(coin_name)
            #flash(f"Could not find {coin_name}. Please enter {coin_name} full name.")
    coins = Coin.query.all()
    
    return render_template("home.html", coins=coins)

@app.route("/update", methods=["POST"])

def update():
    newcrypto_name = request.form.get("newcrypto_name")
    oldcrypto_name = request.form.get("oldcrypto_name")
    coin_name = newcrypto_name.lower().replace(" ", "-")
    coin_gecko_name = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
    
    
    coin = Coin.query.filter_by(crypto_name=oldcrypto_name).first()
    coin.crypto_name = coin_gecko_name['name']
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])

def delete():
    crypto_name = request.form.get("coin")
    coin = Coin.query.filter_by(crypto_name=crypto_name).first()
    db.session.delete(coin)
    db.session.commit()
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
import requests
import json
import os

from pycoingecko import CoinGeckoAPI

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

cg = CoinGeckoAPI()

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "Coin_Database.db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Coin(db.Model):

    crypto_name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    image = db.Column(db.String(80), unique=False, nullable=True)
    current_price = db.Column(db.String(80), unique=False, nullable=True)
    presale_price = db.Column(db.String(80), unique=False, nullable=True)
    multiple = db.Column(db.String(80), unique=False, nullable=True)
    coin_initial_invesment = db.Column(db.String(80), unique=False, nullable=True)
    profit = db.Column(db.String(80), unique=False, nullable=True)
    twenty_four_hour = db.Column(db.String(80), unique=False, nullable=True)
    all_time_high = db.Column(db.String(80), unique=False, nullable=True)
    all_time_percentage_change = db.Column(db.String(80), unique=False, nullable=True)
    sparkline = db.Column(db.String(80), unique=False, nullable=True)
    def __repr__(self):
        return "<Crypto_name: {}>".format(self.crypto_name)

@app.route("/", methods=["GET", "POST"])

def home():
    coins = None

    if request.form:
        try:

            user_input = request.form.get("coin")
            coin_name = user_input.lower().replace(" ", "-")
            coin_gecko_name = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            initial_investment = request.form.get("initial_investment")
            coin_image = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            coin_price = float(cg.get_price(ids=[coin_name.lower()], vs_currencies='usd')[coin_name.lower()]['usd'])
            presale_price = request.form.get("presale_price")
            multiplier = float(coin_price) / float(presale_price)
            profit = round((float(initial_investment) / float(presale_price)) * float(coin_price))
            twenty_four_hour_change = cg.get_price(ids=[coin_name.lower()], vs_currencies='usd', include_24hr_change='true')[coin_name.lower()]['usd_24h_change']
            ath = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            ath_change_percentage = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
            coin_gecko_sparkline = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='true')[0]

            coin = Coin(
                        crypto_name=coin_gecko_name['name'],
                        coin_initial_invesment=initial_investment,
                        image=coin_image['image'],
                        current_price="${:,.2f}".format(coin_price),
                        presale_price=presale_price,
                        multiple= "{:,.2f}".format(multiplier)+"x",
                        profit="${:,.2f}".format(profit),
                        twenty_four_hour="{:,.2f}".format(twenty_four_hour_change),
                        all_time_high="${:,.2f}".format(ath['ath']),
                        all_time_percentage_change="{:,.2f}".format(ath['ath_change_percentage']),
                        #sparkline=coin_gecko_sparkline['sparkline_in_7d']['price']
                        )
            db.session.add(coin)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Failed to add coin')
            print(e)
    coins = Coin.query.all()
    return render_template("home.html", coins=coins)

@app.route("/update", methods=["POST"])

def update():
    newcrypto_name = request.form.get("newcrypto_name")
    oldcrypto_name = request.form.get("oldcrypto_name")
    coin = Coin.query.filter_by(crypto_name=oldcrypto_name).first()
    coin.crypto_name = newcrypto_name
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])

def delete():
    crypto_name = request.form.get("coin")
    coin = Coin.query.filter_by(crypto_name=crypto_name).first()
    db.session.delete(coin)
    db.session.commit()
    return redirect("/")


""" coin_name = input('What coin you want to search for?: ')
initial_invesment = int(input('Enter your initial investment?: '))
presale_price = float(input('Enter presale token price: '))

coin_price = cg.get_price(ids=[coin_name.lower()], vs_currencies='usd')[coin_name.lower()]['usd']
twenty_four_hour_change = cg.get_price(ids=[coin_name.lower()], vs_currencies='usd', include_24hr_change='true')[coin_name.lower()]['usd_24h_change']
ath = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
ath_change_percentage = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
coin_image = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]

profit = round((initial_invesment / presale_price) * int(coin_price))
multiplier = coin_price / presale_price

print('Image: ',coin_image['image'])
print('Coin: ', coin_name)
print('Current Price: ',"${:,.2f}".format(int(coin_price)))
print(f"Presale Price: ${presale_price}")
print(f'Xs: {multiplier}x')
print('Your Initial Investment Price: ',"${:,.2f}".format(initial_invesment))
print('Your profit: ', "${:,.2f}".format(profit))
print('24h: ',twenty_four_hour_change)
print('ATH: ', "${:,.2f}".format(ath['ath']))
print("% From ATH:", int(ath['ath_change_percentage'])) """

if __name__ == "__main__":
    app.run(debug=True)
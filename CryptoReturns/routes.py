from CryptoReturns import application, db
from flask import Flask, render_template, redirect, request, flash
from decimal import *
from pycoingecko import CoinGeckoAPI
from sqlalchemy.sql import func

# Import data from models.py file
from CryptoReturns.models import Coin

import requests
import json
import os

cg = CoinGeckoAPI()

@application.route("/", methods=["GET", "POST"])

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
            duplicate_coin = Coin.query.filter_by(crypto_name=coin_gecko_name['name']).first()
            
            
            # Check if the coin already exist
            #if duplicate_coin == None:
                #q = db.session.query(coin).filter(coin.crypto_name)
                #session.query(q.exists())
            db.session.add(coin)
            db.session.commit()
            
            qry = db.session.query(func.max(coin.profit).label("profit"))
            print(qry)
            # Delete the coin and overwrite it with the new information
            # Or maybe update the coin instead
            """elif duplicate_coin != None:
                #Coin.query.filter(Coin.id == 123).delete()
                coin.crypto_name = coin_gecko_name['name']
                coin.coin_initial_invesment=initial_investment
                db.session.commit()
                #db.session.delete()
                print(coin.crypto_name + "Already exist!")"""
        except Exception as e:
            db.session.rollback()
            print('Failed to add coin')
            print(e)
            #print(coin_name)
            #flash(f"Could not find {coin_name}. Please enter {coin_name} full name.")
    coins = Coin.query.all()
    
    
    return render_template("home.html", coins=coins)

@application.route("/update", methods=["POST"])

def update():
    newcrypto_name = request.form.get("newcrypto_name")
    oldcrypto_name = request.form.get("oldcrypto_name")
    #coin_name = newcrypto_name.lower().replace(" ", "-")
    #coin_gecko_name = cg.get_coins_markets(vs_currency='usd', ids=[coin_name.lower()], order='market_cap_desc', per_page='1', page='1', sparkline='false')[0]
    
    
    coin = Coin.query.filter_by(crypto_name=oldcrypto_name).first()
    coin.crypto_name = newcrypto_name
    db.session.commit()
    return redirect("/")

@application.route("/delete", methods=["POST"])

def delete():
    crypto_name = request.form.get("coin")
    coin = Coin.query.filter_by(crypto_name=crypto_name).first()
    db.session.delete(coin)
    db.session.commit()
    return redirect("/")
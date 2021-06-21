from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, validators

class Crypto_Form(FlaskForm):
    name = StringField("Enter Coin Name", [validators.InputRequired(message="Please enter the Crypto Currency name.")])
    intial_investment = DecimalField("Enter Initial Investment", [validators.InputRequired(message="Please enter a number")])
    coin_price = DecimalField("Enter Coin Price", [validators.InputRequired(message="Please enter a number")])
    submit = SubmitField("Submit")
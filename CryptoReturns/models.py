from CryptoReturns import db

"""class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    picture = db.Column(db.String(80),unique=False, nullable=True)
    coins = db.relationship('Coin', backref='user')

    def __repr__(self):
        return "Name: {}>".format(self.name)
"""

class Coin(db.Model):
    #__tablename__ = 'users'
    # id will allow duplicate coins. In the future allow new coins to replace existing coin in database maybe.
    id = db.Column(db.Integer, primary_key=True)
    crypto_name = db.Column(db.String(80), unique=False, nullable=False)
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
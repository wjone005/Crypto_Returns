from CryptoReturns import db

class Coin(db.Model):
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
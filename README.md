# Crypto Currency Returns ₿

A Flask app that calculates your crypto currency returns based off your initial investment.

![app demo](https://github.com/wjone005/Crypto_Returns/blob/main/CryptoReturns/static/images/website.gif)

## Installation
1. Install Requirements 

    ```$ pip3 install -r requirements.txt (Python 3)```

2. Obtain an API Key for Auth0. Set the keys as an environment variable. Using the following format for macOS and Linux Distributions:

   ```
   export KEY=value
   export client_id=AUTH0_CLIENT_ID
   export client_secret=AUTH0_CLIENT_SECRET
   export api_base_url=AUTH0_DOMAIN
   export access_token_url=AUTH0_ACCESS_TOKEN_URL
   export authorize_url=AUTH0_AUTHROIZE_URL

   ```
   and add them with the following format KEY=environ.get("value")

   If you are ever adding your own code to GitHub and choose to use a .env file, make sure it's listed under a .gitignore file. Therefore, it doesn't accidently get published to GitHub!

## Usage
#### To launch the app:
    $ python3 CryptoReturns.py

Once the Flask app is running, navigate to the `localhost` link provided:

<code> * Running on <b>https://127.0.0.1:5000/</b> (Press CTRL+C to quit)</code>


## Special Thanks

* [CoinGecko API](https://www.coingecko.com/en/api) - Documentation on how to setup CoinGecko's API

* [Manolis Christoforou CoinGecko API wrapper](https://github.com/man-c/pycoingecko) - Python3 wrapper around the CoinGecko API (V3)

* [Auth0 API](https://auth0.com/docs/) - Documentation on how to setup Auth0's API for login purposes.

## Learn More

* [Flask Starter Guide](https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/) - A great starter guide on how to learn Flask
* [Flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) - A more in-depth tutorial on Flask
* [About .gitignore and config files](https://medium.com/black-tech-diva/hide-your-api-keys-7635e181a06c) - A step-by-step guide on how to hide your API keys

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/wjone005/Crypto_Returns/blob/main/LICENSE) file for details.

## Future Features Currently Working On
* Dockerize this project
* Display realtime data 

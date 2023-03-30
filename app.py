import smtplib
import requests
import json
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
api_key = "dfeeae90140eeff39890af7816f2b570"
news_api_key = '606f1e300ba54864a1d6df7fa2d275bf'


def weather():
    location = '04074'
    response = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?zip={location}&units=imperial&type=accurate&mode=json&APPID={api_key}')
    forecast = response.json()
    temp = forecast['main']['temp']
    weather_description = forecast["weather"][0]["description"]
    return forecast, temp, weather_description


def get_news():
    url = f"https://newsapi.org/v2/everything?q=bitcoin&language=en&sortBy=publishedAt&apiKey={news_api_key}"
    response = requests.get(url)
    articles = response.json()['articles']
    return articles


articles = get_news()
news_body = ""
for article in articles[:10]:
    news_body += article['title'] + '\n' + article['url'] + '\n\n'
btc_price = cg.get_price(ids='bitcoin', vs_currencies='usd')
price_in_usd = btc_price['bitcoin']['usd']
send_email = 'brian.baltovski@gmail.com'
email = 'bbaltovski@yahoo.com'
passwd = 'aucjoqtuxqfdcxvr'
subject = 'Daily Update \n'
forecast, temp, weather_description = weather()
message = f'Subject: {subject}\n\nTemperature: {temp}F\n\nWeather Description: {weather_description}\n\n Bitcoin Price: ${price_in_usd}\n\nBitcoin News:\n\n{news_body}'.encode(
    'utf-8')
connection = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
connection.ehlo()
connection.login(user=email, password=passwd)
connection.sendmail(email, send_email, message)

print("Sent successfully")

import pandas as pd
import requests
import time
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_WAPI
import json

from datetime import datetime

def get_date():

    input_date = datetime.now()
    input_date = input_date.strftime("%Y-%m-%d")

    return input_date

def request_wapi(api_key,query):

    url = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try :
        response = requests.get(url).json()
    except Exception as e:
        print(e)

    return response

def get_forecast(response, i):
    
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    temperatura = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    lluvia = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_lluvia = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    
    return fecha, hora, condicion, temperatura, lluvia, prob_lluvia

def create_df_temp_min(data):
    col = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'Prob_lluvia']
    df = pd.DataFrame(data, columns=col)
    temp_min = df['Temperatura'].min()
    df_temperatura = pd.DataFrame({'Temperatura Mínima': [temp_min]})
    df_temperatura.set_index('Temperatura Mínima', inplace=True)
    
    return temp_min

def create_df_temp_max(data):
    col = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'Prob_lluvia']
    df = pd.DataFrame(data, columns=col)
    temp_max = df['Temperatura'].max()
    df_temperatura = pd.DataFrame({'Temperatura Máxima': [temp_max]})
    df_temperatura.set_index('Temperatura Máxima', inplace=True)
    
    return temp_max




def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,query, temp_min, temp_max):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    body=f"""¡Hola!
El pronóstico del tiempo para hoy {input_date} en {query} es:
Temperatura Mínima: {temp_min}°C
Temperatura Máxima: {temp_max}°C
    
¡Que tengas un buen día!
""",
    from_= PHONE_NUMBER,
    to = '+56998111213'
    )

    return message.sid

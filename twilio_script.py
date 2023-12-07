import os
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER,API_KEY_WAPI
import time
from requests import Request
import json
from functions import get_date, request_wapi, get_forecast, create_df_temp_min, create_df_temp_max, send_message

query = 'Los Angeles, Chile'
api_key = API_KEY_WAPI

input_date= get_date()
response = request_wapi(api_key,query)

datos = []

for i in range(24):

    datos.append(get_forecast(response,i))

temp_min = create_df_temp_min(datos)
temp_max = create_df_temp_max(datos)


# Send Message
message_id = send_message(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, input_date, query, temp_min, temp_max)
query

print('Mensaje Enviado con exito ' + message_id)

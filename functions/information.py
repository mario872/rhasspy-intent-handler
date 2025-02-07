from pyowm.owm import OWM
from .secrets import *
import os
from openai import OpenAI
from simplegmail import Gmail
from datetime import datetime as dt
from datetime import timedelta


os.environ["OPENAI_API_KEY"] = openai_api_key
client = OpenAI()

def chatgpt(prompt, text, temperature=0.8, model="gpt-4o-mini"):
    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": text
            }
        ]
    )
    response = completion.choices[0].message.content
    return response


def GetWeather(text):
    owm = OWM(owm_api_key)
    reg = owm.city_id_registry()
    print(reg.ids_for("Sydney", matching="exact")[0])

    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=owm_lat, lon=owm_lon, exclude="minutely")

    one_call_data = {
        "lat": one_call.lat,
        "lon": one_call.lon,
        "timezone": one_call.timezone,
        "current": one_call.current.to_dict(),
        "hourly": [weather.to_dict() for weather in one_call.forecast_hourly[0:11]],
        "daily": [weather.to_dict() for weather in one_call.forecast_daily[0:6]]
    }
    
    response = chatgpt("Here is weather data: " + str(one_call_data), "Please be as conscise as possible and only answer the users question, you are playing the part of Jarvis from Iron Man. User: " + text)
    
    return response

def GetEmails(days):
    gmail = Gmail(client_secret_file="secrets/client_secret.json", creds_file="secrets/gmail_token.json")
    days_ago = (dt.now() - timedelta(days=int(days))).strftime('%Y/%-m/%-d')
    messages = gmail.get_unread_inbox(query=f"after:{days_ago}")
    num_emails = len(messages)
    
    print(messages)
    
    if num_emails == 0:
        return "No unread emails found."
    
    if num_emails > 4:
        info = ""
        
        for message in messages:
            info += f"From: {message.sender.split(' <')[0]} Subject: {message.subject} | "
        
        response = chatgpt(f"Here are emails for the user from the past {days} days: " + info, "Please be as conscise as possible and summarise the user\'s inbox for them. You are playing the part of Jarvis from Iron Man, and as such there is no text interface, only response with pronouncible characters.")
    else:
        response = f"You have received {num_emails} emails. "
        for message in messages:
            response += f"From: {message.sender.split(' <')[0]}. Subject: {message.subject}. "
    
    return response
#importing the libraries
import numpy as np
import pandas as pd
import yfinance as yf
import win32com
import win32com.client 
import datetime 
import random

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps


# Define list for all stocks to track
ticker_list = ['MSFT', 'IBM', 'AVGO', 'INTC', 'AAPL']


# Define functions for the bot to use
# Returns a random sentence for greeting the user
def begruessung():
    greeting = random.choice(["Hallo!", "Ich gruesse dich!", "Hi, wie kann ich helfen?"])
    return greeting


# Return a sentence to introduce 
def name():
    name = random.choice(["Ich heiße Turtle!", "Mein Name ist Turtle, sehr erfreut dich kennenzulernen!", "Ich bin Turtle."])
    return name


# Returns a smalltalk sentence
def smalltalk01():
    smalltalk = random.choice(["Danke, gut soweit!", "Mir geht es gut, ich hoffe dir auch!", "Danke, ja mir geht es gut. :-)"])
    return smalltalk


# Prints out a list of stock prices 
def aktien():
    print('Hier sind die letzten Schlusspreise deiner Aktien...')
    # Uses the yfinance API to get latest closing price of a stock
    for stock in ticker_list:
        stock_data = yf.Ticker(stock)
        hist = stock_data.history(period="max")
        print(f'Der Preis für {stock} ist: ', round(hist['Open'][-1], 2), ' $')
    return 'Das waren alle Aktien!'


# Lists a the current to dos
def show_todo():
    print('Deine aktuellen to dos sind...')
    with open('todo.txt', 'r') as todo_list:
        for line in todo_list.readlines():
            print('-> ' + line)
    return 'Das sind all deine to dos.'


# Appends a to do to the to do list
def add_todo():
    todo = str(input('To do hinzufügen: '))
    with open('todo.txt', 'a+') as todo_list:
        todo_list.write('\n')
        todo_list.write(todo)
    return 'Ich habe den Eintrag hinzugefügt.'


# Removes a to do from the to do list 
def remove_todo():
    # Get the index of the do to that is to be deleted
    index = int(input('To do entfernen (Nummer): ')) - 1

    # Open the file and load into list
    todo_list = open('todo.txt', 'r')
    full_list = todo_list.readlines()
    todo_list.close()

    # Delete to do that user wants removes
    del full_list[index]

    # Write updated list to text file S
    updated_list = open('todo.txt', 'w+')
    for line in full_list:
        updated_list.write(line)
    updated_list.close()

    return 'Ich habe den Eintrag gelöscht.'


# Returns a random 'your welcome' sentence
def bedankung():
    bedankung = random.choice(["Gerne!", "Keine Ursache.", "Immer wieder gerne!"])
    return bedankung


# Returns a random goodbye sentence 
def verabschiedung():
    verabschiedung = random.choice(["Bis dann! Ich hoffe, ich konnte dir weiterhelfen!"])
    return verabschiedung


# Returns a random fact about turtles
def schildkröten():
    fakten = random.choice(["Schildkröten können besser sehen als Menschen, da sie ultraviolettes und infrarotes Licht wahrnehmen können", 
                            "Schildkröten gibt es schon seit über 220 Millionen Jahren!"
                            "Zierschildkröten können bis zu 30 Stunden lang tauchen!",
                            "Schildkröten essen Blätter."])
    return fakten


# Prints out the current weather in Düsseldorf, Germany
def wetter():
    # API Key from OpenWeather goes there
    API = 'b46395bdd02e94d3e6f339dffd9ebd6f'

    # Get weather for Düsseldorf 
    owm = OWM(API)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Düsseldorf')
    weather = observation.weather

    return f'In Düsseldorf ist es {weather.temperature("celsius")["temp"]} C° bei {weather.humidity} % Luftfeuchtigkeit.'


# Prints out all events if my outlook calender for the next two days
def kalender():
    # Use win32com to access the calendar data from outlook
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    calender = outlook.GetDefaultFolder(9)
    items = calender.Items #This item is each "plan"
    select_items = [] 

    # Specify the period for which you want to extract the schedule
    end_date = datetime.date.today() + datetime.timedelta(days=5)
    start_date = datetime.date.today() 

    # Filter the timeframe of appointments to display
    for item in items:
        if start_date <= item.start.date() <= end_date:
            select_items.append(item)

    # Empty list to store the events in
    event_list = []

    # Display the details of the extracted schedule
    for select_item in select_items:
        sub = select_item.subject

        start = select_item.start.strftime('%m/%d/%Y, %H:%M')
        ende =  select_item.end.strftime('%H:%M')
        
        print(f'-> {sub} am {start} bis {ende}')

    return 'Das sind all deine Ereignisse.'

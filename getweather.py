#####################################################
# Name:   getweather.py
# Author: Martin Vacula
# Date:   14.06.2018
# Version:1.0
#####################################################
# Importing modules
import json
import os
import requests
import sys

# Setting variables 
WORKED = 1
FAILED = 0
PASSED = 2
User = "Default"

# Defining functions
def yes_no(question):
    yes = set(['yes','y'])
    no = set(['no','n'])
    while True:
        choice = input(question).lower()
        if choice in yes:
           return 1
        elif choice in no:
           return 0
        else:
           print("Please respond with 'yes' or 'no':\n ")

def check_connection(status_check):
    if status_check == 400:
        print('Wrong credentials! Exitting...')
        quit()
    elif status_check == 401:
        print('Bad request! Exitting...')
        quit()
    elif status_check == 403:
        print('Not enough permissions! Exitting...')
        quit()
    elif status_check == 404:
        print('Resource not found! Exitting...')
        quit()
    elif status_check == 200:
        pass
    else:
        print('Error occured! Exitting...')

def output(data):
    # format the data first
    main_data = data['main']
    temp_convert = int(main_data['temp'])
    temp = str("%4.1f" %(temp_convert - 273.15))
    weather = data['weather'][0]['description']
    city = data['name']
    humidity_int = main_data['humidity']
    humidity = str(humidity_int)
    source = "http://api.openweathermap.org"
    # printing the output
    print('\n')
    print('Location: '+ city)
    print('Weather: ' + weather)
    print('Temperature: '+ temp +'°C')
    print('Humidity: ' + humidity + '%')
    print('\n')
    print('Data source: ' + source)
    print('\n== ENVIRONMENT VARIABLES FOR THIS PROCESS==') 
    print(os.environ['CITY_NAME'])
    print(os.environ['OPENWEATHER_API_KEY'])
    print('===================END===================== \n')
    return

##################### main body #####################
print("\n")
print("============= Getweather v1.0 ============ \n")

# Check if API KEY is set in env
APIKEY = os.environ.get('OPENWEATHER_API_KEY')
if APIKEY is None:
        print('Apikey is not already set!')
        Api_Question = yes_no('Would you like to provide API KEY? yes/no: ')
else:
        Api_Question = PASSED
        pass

# Check if API KEY was found and we can proceed
if Api_Question == FAILED:
        print("No API Key provided! Exiting...")
        quit()
elif Api_Question == PASSED:
        pass
elif Api_Question == WORKED:
        APIKEY = input("Please enter the API KEY: ")
        if APIKEY is "":
            print("No API Key provided! Exiting...")
            quit()
        else:
            pass
else:
       pass

# Temporary set env for this process - not needed
os.environ['OPENWEATHER_API_KEY'] = APIKEY 

# Set city to check
SetCity = input("Enter the City Name to see weather information: ")

# Check if city was entered
if SetCity is "":
        print('City name was not entered!')
        City_Question = yes_no('Would you like to continue and provide City name? yes/no: ')
else:
        City_Question = PASSED
        pass

if City_Question == FAILED:
        print("No City name provided! Exiting...")
        quit()
elif City_Question == PASSED:
        pass
else:
        SetCity = input("Please enter the City name: ")
        if SetCity is "":
           print("No City name provided! Exiting...")
           quit()
        else:
            pass

# Set to env for this process - not needed
os.environ['CITY_NAME']= str(SetCity)

# Check if entered city exists in DB downloaded from "http://bulk.openweathermap.org/sample/"
# Opening json file that is in the same directory as script
database = open('city.list.json')
Cities = json.loads(database.read())
check = None
for data in Cities:
    if data["name"] == SetCity:
        check = "Presented"
    else:
        pass
if check is None:
    print("Entered City doesn't exist in database! Exiting...")
    quit()
else:
    pass

# preparing full URL. User is preddefined as "Default" - the user we obtained together with API key
url = 'http://api.openweathermap.org'
full_url = url + '/data/2.5/weather?q=' + SetCity + '&id=' + User + '&APPID=' + APIKEY

# Create API call
req = requests.get(full_url)
data = req.json()
status_check = req.status_code

# Check the response 
check_connection(status_check)

# Print formated API respond
output(data)

quit()



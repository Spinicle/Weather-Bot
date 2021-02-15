#Print to tell bot is loading.
print("The bot is loading..")
print()

#Import the required modules.
import discord
from discord.ext import commands
import asyncio
from colorama import Fore
import json
import requests
from datetime import datetime

#Making a variable with the current time.
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

#Open the `config.json` file and read the data in it.
with open('config.json') as config_file:
    data = json.load(config_file)

#Assign variables with the data from `config.json` file.
token = data['TOKEN']
prefix = data['PREFIX']
weather_key = data['WEATHER_KEY']

#Declare a bot.
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

#print text when connected to discord.
@bot.event
async def on_ready():
	print(f"{bot.user.name} had connected to discord! | Prefix = {prefix}")

#Help command
@bot.command()
async def help():
	em = discord.Embed(name="Help Command")
	em.add_field(name="Help command", value=f"{prefix}weather [city]")

#Weather command
@bot.command()
async def weather(ctx, *, city):
    print(f"Command initiated at {current_time}")
    req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}')
    r = req.json()
    temperature = round(float(r["main"]["temp"]) - 273.15, 1)
    lowest = round(float(r["main"]["temp_min"]) - 273.15, 1)
    highest = round(float(r["main"]["temp_max"]) - 273.15, 1)
    weather = r["weather"][0]["main"]
    humidity = round(float(r["main"]["humidity"]), 1)
    wind_speed = round(float(r["wind"]["speed"]), 1)
    em = discord.Embed(description=f'''
    Temperature: `{temperature}`
    Lowest: `{lowest}`
    Highest: `{highest}`
    Weather: `{weather}`
    Humidity: `{humidity}`
    Wind Speed: `{wind_speed}`
    ''')
    em.add_field(name='City', value=city.capitalize())
    em.timestamp = datetime.datetime.utcnow()
    em.set_thumbnail(url='https://ak0.picdn.net/shutterstock/videos/1019313310/thumb/1.jpg')
    await ctx.send(embed=em)

#Error handler
@weather.error
async def weather_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter the name of city.')

#Run the bots token.
bot.run(token)
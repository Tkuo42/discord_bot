# Imports
import token
import discord
from dotenv import load_dotenv
import os
import mysql.connector
from discord.ext import commands
from datetime import date
import throwbackImage as tb


# Initializing the discord client

load_dotenv()

token = os.getenv('TOKEN')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


# Global Variables

mydb = mysql.connector.connect(
    host="localhost",
    user='root',
    password=password,
    database=database
)
cursor = mydb.cursor(buffered=True)

# Methods


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return

    if msg.startswith('!hello'):
        await message.channel.send('Hello!')

    if msg.startswith('!quote'):
        try:
            cursor.execute(
                'SELECT * FROM quote ORDER BY RAND() LIMIT 1')
            row = cursor.fetchone()
            await message.channel.send(str(row))
            cursor.reset()
        except:
            await message.channel.send('No quotes found')

    if msg.startswith('!addquote'):
        cursor.execute("INSERT INTO quote (quote, author) VALUES (%s, %s)",
                       (msg.split('!addquote')[1], str(message.author).split('#')[0]))
        mydb.commit()
        await message.channel.send('Quote added!')
        cursor.reset()

    if msg.startswith('!delquote'):
        try:
            cursor.execute("DELETE FROM quote WHERE id = %s",
                           (msg.split('!delquote')[1],))
            mydb.commit()
            await message.channel.send('Quote deleted!')
            cursor.reset()
        except:
            await message.channel.send('ID does not exist')

    if msg.startswith('!showquotes'):
        cursor.execute("SELECT * FROM quote")
        quotes = cursor.fetchall()
        for entry in quotes:
            await message.channel.send(entry)
        cursor.reset()

    if msg.startswith('!addTb'):
        try:
            tb.addThrowback(str(message.author).split(
                '#')[0], message.attachments[0].url, date.today(), msg.split('!addTb')[1])
            await message.channel.send('Throwback added!')
        except:
            await message.channel.send('No image found')

    if msg.startswith('!showTb'):
        throwbacks = tb.showThrowbacks()
        for throwback in throwbacks:
            await message.channel.send(throwback)

    if msg.startswith('!delTb'):
        try:
            tb.deleteThrowback(msg.split('!delTb')[1])
            await message.channel.send('Throwback deleted!')
        except:
            await message.channel.send('ID does not exist')
# Running the client
client.run(token)

# how do I store the attachments in the message?

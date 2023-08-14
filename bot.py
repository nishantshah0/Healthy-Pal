import discord
import responses
import random
import time
from discord.ext import commands
from asyncio import sleep as s

async def send_message(message, user_message):
  try:
    response = responses.get_response(user_message, message)
    await message.channel.send(response)

  except Exception as e:
    print(e)

def run_discord_bot():
  TOKEN = 'MTEzOTk1OTMwMzI4NjA0MjY4Ng.GkwLRn.1FjAHQcuZqQlz2sOm7nIhwpEEdOK4ZHtz1S0nU'
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    await send_message(message, user_message)
    

  client.run(TOKEN) 
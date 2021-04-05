import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
     return

  if message.content.startswith('+Willkommen'):
      await message.channel.send('Willkommen auf dem server. wir hoffen du hast Spaß!')

@client.event
async def on_message(message):
  if message.author == client.user:
     return

  if message.content.startswith('+Info'):
      await message.channel.send('Dieser Bot wurde von ItIzYe mithilfe von Python programmiert. Die Quellcodes sind auf Anfrage bereit!')

@client.event
async def on_message(message):
  if message.author == client.user:
     return

  if message.content.startswith('+Bot'):
      await message.channel.send('Name: Flickbertus#8879''Version: 1.0.0''Author: ItIzYe!')
client.run(os.getenv('TOKEN'))
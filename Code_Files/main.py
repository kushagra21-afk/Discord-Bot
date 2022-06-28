import discord
import os
import requests
import json
import random
from replit import db
from keepprojectalive import lol
client = discord.Client()

hello= ['hello kush', 'hellu kush']

sad_words = ["sad", "depressed", 'unhappy', "angry", "miserable", "depressing"]

strt_encouragements = ["you are a great person", 'it will be alright'," hang in there u ll get over it", "dont give up try harder"]

def get_motivation():
  response=requests.get("https://animechanapi.xyz/api/quotes/random")
  json_data = json.loads(response.text)
  quote = json_data['data'][0]['quote'] + '                                                                     -' + json_data['data'][0]['character'] + '(' + json_data['data'][0]['anime'] + ')'
  return(quote)


def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return(quote)

def update_encouragements(encg_msg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encg_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encg_msg]

def dl8_encouragements(msg_to_be_deleted):
  encouragements = db["encouragements"]
  if len(encouragements) > msg_to_be_deleted:
    del encouragements[msg_to_be_deleted]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print("we have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg=message.content.upper()
  msgs=message.content
  a=message.content.lower()

  if msg.startswith('$INSPIRE'):
    quote= get_quote()
    await message.channel.send(quote)

  if any (word in a for word in hello):
    await message.channel.send('Henlo')

  options = strt_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if any(word in a for word in sad_words):
    await message.channel.send(random.choice(options))
  
  if msg.startswith('$MOTIVATION'):
    quote=get_motivation()
    await message.channel.send(quote)

  if msg.startswith('$NEW'):
    encg_msg = msgs.split("$new ",1)[1]
    update_encouragements(encg_msg)
    await message.channel.send("new encouraging message added.")

  if msg.startswith("$DEL"):
    encouragements = []
    if "encouragements" in db.keys():
      msg_to_be_deleted = int(msgs.split("$del",1)[1])
      dl8_encouragements(msg_to_be_deleted)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
        

lol()
client.run(os.getenv('TOKEN'))
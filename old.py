import discord
import os
import csv
import yaml
from keep_alive import keep_alive
from dotenv import load_dotenv
load_dotenv()

def spoiler(scp):
  with open('SCPspoiler.csv', 'r') as f:
    r = csv.reader(f)
    for row in r:
      if scp in row:
        return(True)
  return(False)

def Proposals(n, i):
  with open('001.yaml', 'r') as f:
    docs = yaml.load(f, Loader=yaml.FullLoader)
    if i == 0:
      return(docs[n][0]['author'])
    else:
      return(docs[n][1]['name'])

def Author(n, i):
  with open('author.yaml', 'r') as f:
    docs = yaml.load(f, Loader=yaml.FullLoader)
    if i == 0:
      return(docs[n][0]['author'])
    else:
      return(docs[n][1]['number'])

def aType(n, i):
  with open('type.yaml', 'r') as f:
    docs = yaml.load(f, Loader=yaml.FullLoader)
    if i == 0:
      return(docs[n][0]['type'])
    else:
      return(docs[n][1]['number'])

def setField(field, a):
  i = 1
  some_string = ""
  if a == 'n':
    while i < 6:
      some_string += f"{field(i, 1)}\n"
      i += 1
    return some_string
  else:
    while i < 6:
      some_string += f"{field(i, 0)}\n"
      i += 1
    return some_string

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
   
    if message.content.startswith('!spoiler'): 
        if message.content == "!spoiler":
          await message.channel.send('Please include an SCP number `!spoiler 173`')
        else:
          scp = message.content.split(" ")[1:][0]
          if spoiler(scp):
            if scp == '001': # If SCP == 001 return embed listing all the 001's read
              i = 1
              embedMsg = discord.Embed(title="001 Proposals", description="The 001 proposals that have been read on the podcast are", color=0x109319)
              while i < 6: 
                embedMsg.add_field(name=Proposals(i,0), value=Proposals(i,1), inline=True)
                if i % 2 == 0:
                   embedMsg.add_field(name = u'\u200b', value = u'\u200b')
                i += 1
              embedMsg.set_footer(text="If you wish to discuss an 001 proposal that hasn't been read on the podcast please use the ||Spoiler tag||.")
              await message.channel.send(embed=embedMsg)
            else:
              await message.channel.send('It has been read. No spoiler tag needed.')
          elif RepresentsInt(scp) == False:
            await message.channel.send('Please enter an SCP number. If looking for a tale, they currently aren\'t supported by the bot')
          else:
            await message.channel.send('It has not been read. Please spoiler tag by using \|\|Spoiler text here\|\|.')
    if message.content.startswith('!stats'):
      if message.content == "!stats":
          embedMsg = discord.Embed(title="Discovering SCP stats", description="These are the stats for DSCP Podcast", color=0x109319)
          embedMsg.add_field(name='Episodes',value='93\n**No. SCPs/Tales***\n254\n**Total Runtime**\n117h29m')
          embedMsg.add_field(name='Most read Author*', value=setField(Author, 'x'), inline = 'True')
          embedMsg.add_field(name = 'Count', value = setField(Author, 'n'))
          embedMsg.add_field(name = 'Longest Ep', value = 'Episode 28 (133:41)\n**Shortest Ep**\nEpisode 27B (51:35)')
          embedMsg.add_field(name='Type of Article*', value=setField(aType, 'x'), inline = 'True')
          embedMsg.add_field(name = u'\u200b', value = setField(aType, 'n'))
          embedMsg.set_footer(text="* Inluding streams\nFeel free to ping @Very Funny if these stats are wrong")
          await message.channel.send(embed=embedMsg)

keep_alive()
client.run(os.getenv('TOKEN'))

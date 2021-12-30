import discord
import os
import csv
import json
from keep_alive import keep_alive
from dotenv import load_dotenv
load_dotenv()

def spoiler(scp):
    with open('SCPspoiler.csv', 'r', encoding='utf-8') as f:
        r = csv.reader(f)
        for row in r:
            if row == [scp]:
                return True
    return False

def stats(s):
    with open('stats.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        cat = data[s]
        rs = []
        if s == 'authors' or s == '001':
            for i in range(len(cat)):
                rs.append([cat[i]['author'], cat[i]['number']])
        else:
            for i in range(len(cat)):
                rs.append([cat[i]['type'], cat[i]['number']])
    return rs

def setField(field, a):
    some_string = ""
    for i in range(5):
        some_string += f"{field[i][a]}\n"
    return some_string

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
            scp = [x.strip(',') for x in message.content.split()][1:]
            if len(scp) > 5:
                await message.channel.send('A maximum of 5 SCPs can be checked at once')
            else:
                a = False
                rd, nrd, nv = '', '', ''
                embedMsg = discord.Embed(title = "SCP Spoiler Checker", color = 0x109319)
                for i in range(len(scp)):
                    if scp[i].isnumeric():
                        if scp[i] == '001':
                            a = True
                            one = stats('001')
                            embedMsg2 = discord.Embed(title = "001 Proposals", description = "The 001 proposals that have been read on the podcast are", color = 0x109319)
                            for i in range(len(one)):
                                embedMsg2.add_field(name = one[i][0], value = one[i][1])
                            embedMsg2.set_footer(text = "If you wish to discuss an 001 proposal that hasn't been read on the podcast please use the ||Spoiler tag||.\nFeel free to ping @Very Funny for any queries")
                        elif spoiler(scp[i]):
                            rd += (f'{scp[i]}, ')
                        else:
                            nrd += (f'{scp[i]}, ')
                    else:
                        nv += (f'{scp[i]}, ')
                if rd:
                    embedMsg.add_field(name = 'No spoiler tag needed', value = rd[:len(rd)-2], inline = False)
                if nrd:
                    embedMsg.add_field(name = 'Spoiler tag needed*', value = nrd[:len(nrd)-2], inline = False)
                if nv:
                    embedMsg.add_field(name = 'Not valid. Please enter an SCP number^', value = nv[:len(nv)-2], inline = False)
                embedMsg.set_footer(text = '^Tales aren\'t currently supported by the bot.\n*To spoiler tag \|\|Spoiler text here\|\|\nFeel free to ping @Very Funny for any queries')
                await message.channel.send(embed=embedMsg)
                if a:
                    await message.channel.send(embed=embedMsg2)

    elif message.content.startswith('!stats'):
        author, category = stats('authors'), stats('category')
        embedMsg = discord.Embed(title = "Discovering SCP stats", description = "These are the stats for DSCP Podcast", color = 0x109319)
        embedMsg.add_field(name = 'Episodes',value = '94\n**No. SCPs/Tales***\n255\n**Total Runtime**\n119h48m')
        embedMsg.add_field(name = 'Most read Author*', value = setField(author, 0))
        embedMsg.add_field(name = 'Count', value = setField(author, 1))
        embedMsg.add_field(name = 'Longest Ep', value = 'Episode 94 (139:50)\n**Shortest Ep**\nEpisode 27B (51:35)')
        embedMsg.add_field(name='Type of Article*', value = setField(category, 0))
        embedMsg.add_field(name = '\u200b', value = setField(category, 1))
        embedMsg.set_footer(text='* Inluding streams\nFeel free to ping @Very Funny for any queries')
        await message.channel.send(embed=embedMsg)

keep_alive()
client.run(os.getenv('TOKEN'))
# client.run(os.environ['TOKEN'])
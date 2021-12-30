import discord
import os
import csv
import json
from keep_alive import keep_alive
from dotenv import load_dotenv # Not needed for repl.it
load_dotenv()

def spoiler(scp):
    with open('SCPspoiler.csv', 'r', encoding='utf-8') as f:
        r = csv.reader(f)
        return next((row for row in r if row == [scp]), False)

def stats(s, n):
    with open('stats.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        cat = data[s]
        rs = []
        [rs.append([cat[i][n], cat[i]['number']]) for i in range(len(cat))]
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
                            one = stats('001', 'author')
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
                msg = lambda a, b: embedMsg.add_field(name = b, value = a[:len(a)-2], inline = False) if a else None
                msg(rd, 'No spoiler tag needed')
                msg(nrd, 'Spoiler tag needed*')
                msg(nv, 'Not valid. Please enter an SCP number^')
                embedMsg.set_footer(text = '^Tales aren\'t currently supported by the bot.\n*To spoiler tag \|\|Spoiler text here\|\|\nFeel free to ping @Very Funny for any queries')
                await message.channel.send(embed=embedMsg)
                if a:
                    await message.channel.send(embed=embedMsg2)
    elif message.content.startswith('!stats'):
        author, category = stats('authors', 'author'), stats('category', 'type')
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
# client.run(os.environ['TOKEN']) For repl.it
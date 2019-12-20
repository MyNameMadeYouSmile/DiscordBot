import discord
from discord.ext.commands import Bot
from discord.ext import *
import os
from googletrans import Translator
import urllib.request
import json
import praw
import requests
from bs4 import BeautifulSoup
import random
import datetime

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)

reddit = praw.Reddit(client_id=os.environ['14_chars'], \
                     client_secret=os.environ['27_chars'], \
                     user_agent='Tester', \
                     username=os.environ['reddit_u'], \
                     password=os.environ['reddit_p'])

client.remove_command('help')

@client.event
async def on_ready():
  activity = discord.Game(name="!help")
  await client.change_presence(status=discord.Status.online, activity=activity)
  print("Bot Name: {}".format(client.user.name))
  print("Bot ID: {}".format(client.user.id))
  
@client.command(pass_context=True)
async def help(ctx):
  await ctx.send("Hello! I am a naughty discord bot created by MyNameMadeYouSmile. I can't do much right now, cause I'm still under development, but it's nice to meet you anyways :) Type !commands for the list of all cool commands you can use.")
  
@client.command(pass_context=True)
async def commands(ctx):
  await ctx.send("""```
          **COMMANDS LIST**
          
!help - Bot help.

!commands - Request for list of all commands.

!translate - Translate a word or sentence from one language to another.

!urban - Request a definition for a term from urban dictionary.

!searchgwa - Search for posts in gonewildaudio (5 posts per request).

!love - Calculate the possibility of two users loving eachother.```""")
  
@client.command(pass_context=True)
async def translate(ctx, From, To, *, sentence):
  translator = Translator()
  try:
    translation = translator.translate(sentence, dest=To, src=From)
    await ctx.send(translation.text)
  except ValueError:
    await ctx.send("""```diff
Language Codes

English - en  | Russian - ru | German - de
Dutch - nl    | Italian - it | Polish - pl  
Japanese - ja | Spanish - es | French - fr
Swedish - sv  | Chech - cz   | Portuguese - pt```""")
    await ctx.send("More codes here: https://ctrlq.org/code/19899-google-translate-languages")
    
@client.command(pass_context=True)
async def urban(ctx, *, term):
  try:
    url = 'http://api.urbandictionary.com/v0/define?term=%s' % (term)
    res = urllib.request.urlopen(url) 
    data = json.loads(res.read().decode('utf-8'))
    definition = data['list'][0]['definition']
    await ctx.send(definition)
  except IndexError:
    print("index error")
    await ctx.send('There\'s no definition for this word.')
  except urllib.error.URLError:
    pass
  
@client.command(pass_context=True)
async def love(ctx, pupil1, pupil2):
  girlie = pupil1
  n = 1
  rnd = random.randint(1,20)
  princie = pupil2
  boi = (len(princie))
  gurl = (len(girlie))
  score = 100-(boi*gurl)-rnd
  await ctx.send("There is a " + str(score) + "% chance that {} and {} love eachother.".format(pupil1, pupil2))
  
@client.command(pass_context=True)
async def clear(ctx):
  mgs = [] #Empty list to put all the messages in the log
  #number = int(number) #Converting the amount of messages to delete to an integer
  async for x in ctx.message.channel.history():
    mgs.append(x)
  await ctx.message.channel.delete_messages(mgs)
  
@client.command(pass_context=True)
async def searchgwa(ctx, *, searchterm):
  resultnum = 1
  for searchgwa in reddit.subreddit('gonewildaudio').search(searchterm, limit=5):
    if len(searchgwa.title) > 256:
      searchgwa.title = searchgwa.title[:253] + '...'
    time = searchgwa.created
    Date = datetime.datetime.fromtimestamp(time)
    embed=discord.Embed(title=searchgwa.title, url=searchgwa.url, description=searchgwa.selftext, color=0x5b5bff)
    embed.set_author(name="Result #" + str(resultnum))
    #embed.set_thumbnail(url="https://www.redditstatic.com/desktop2x/img/avatar_over18.png")
    embed.add_field(name="Post Author", value="/u/" + str(searchgwa.author), inline=True)
    embed.add_field(name="Post Date", value=str(Date), inline=True)
    #embed.add_field(name="Content Warning", value="NSFW", inline=True)
    await ctx.send(embed=embed)
    resultnum += 1
  
@client.command(pass_context=True)
async def newgwa(ctx):
  for submission1 in reddit.subreddit('gonewildaudio').new(limit=1):
    await ctx.send("""```Gone Wild Audio
  
    """ + submission1.title + """```""")
  for submission2 in reddit.subreddit('gonewildaudible').new(limit=1):
    await ctx.send("""```Gone Wild Audible
  
    """ + submission2.title + """```""")
    
  for submission3 in reddit.subreddit('gwascriptguild').new(limit=1):
    await ctx.send("""```GWA Script Guild
  
    """ + submission3.title + """```""")
    
  for submission4 in reddit.subreddit('gwabackstage').new(limit=1):
    await ctx.send("""```GWA Backstage
  
    """ + submission4.title + """```""")
    
@client.command(pass_context=True)
async def search(ctx, *, query):

  google_url = "https://www.google.com/search?q=site:soundgasm.net+" + query + "&num=5"
  response = requests.get(google_url)
  soup = BeautifulSoup(response.text, "html.parser")

  result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

  links = []
  titles = []
  descriptions = []
  for r in result_div:
    link = r.find('a', href = True)
    titleone = r.find('div', attrs={'class':'vvjwJb'}).get_text()
    description = r.find('div', attrs={'class':'s3v9rd'}).get_text()
        
    if link != '' and titleone != '' and description != '': 
      links.append(link['href'])
      titles.append(titleone)
      descriptions.append(description)
        
      embed=discord.Embed(title=titles[0], url=links[0], description=descriptions[0], color=0x5b5bff)
      embed.add_field(name="[" + titles[1] + "](" + links[1] + ")", value=description[1], inline=False)
      embed.add_field(name="[" + titles[2] + "](" + links[2] + ")", value=description[2], inline=False)
      embed.add_field(name="[" + titles[3] + "](" + links[3] + ")", value=description[3], inline=False)
      await ctx.send(embed=embed)
    
@translate.error
async def translate_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !translate [from lang code] [to lang code] [sentence]")
 
@translate.error
async def urban_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !urban [term]")
  
@love.error
async def love_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !love [boy] [girl]")
  
client.run(os.environ['BOT_TOKEN'])

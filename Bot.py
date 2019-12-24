import discord
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound
from discord.utils import get
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
import asyncio
import mycleverbot
from mycleverbot import CleverBot

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)

reddit = praw.Reddit(client_id=os.environ['14_chars'], \
                     client_secret=os.environ['27_chars'], \
                     user_agent='Tester', \
                     username=os.environ['reddit_u'], \
                     password=os.environ['reddit_p'])

cb = CleverBot()

client.remove_command('help')

async def chatbot(ctx, message):
  await cb.init()
  response = await cb.getResponse(message)
  await cb.close()
  await ctx.send(ctx.message.author.mention + " " + response)

@client.event
async def on_ready():
  activity = discord.Game(name="!help")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='!help'))
  print("Bot Name: {}".format(client.user.name))
  print("Bot ID: {}".format(client.user.id))
  
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
    return await ctx.send(str(error))
  
@client.event
async def on_member_join(member):
  new_channel = client.get_channel(657937578539876373)
  rules_channel = client.get_channel(657939389623697448)
  main_channel = client.get_channel(657950668853739520)
  
  print(">> " + member.name + " has just joined The Smiley House.")
  await new_channel.send("Hello " + member.mention+ "! Welcome to **The Smiley House!** Please go to the " + rules_channel.mention + " channel and take a look at some of the rules you need to follow in order to stay.\n\nSay hello in " + main_channel.mention + " and I hope you have fun in Mike's server :)")
 
@client.event
async def on_member_remove(member):
  gone_channel = client.get_channel(658375828496973824)
  
  print(">> " + member.name + " has just left The Smiley House.")
  await gone_channel.send(">> " + member.mention + " just left the server :( We will miss you " + member.name + "!")
  
@client.event
async def on_message(message):
  if message.content.startswith("!"):
    if "!chat" not in message.content:
      print(">> " + message.author.name + ": " + message.content)
      await client.process_commands(message)
    else:
      await client.process_commands(message)
    
@client.command(pass_context=True)
async def chat(ctx, *, message):
  asyncio.get_event_loop().run_until_complete(chatbot(ctx, str(message)))
  
@client.command(pass_context=True, aliases=['randcol', 'rc'])
async def randomcolor(ctx):
  a = hex(random.randrange(0,256))
  b = hex(random.randrange(0,256))
  c = hex(random.randrange(0,256))
  a = a[2:]
  b = b[2:]
  c = c[2:]
  if len(a)<2:
    a = "0" + a
  if len(b)<2:
    b = "0" + b
  if len(c)<2:
    c = "0" + c
  z = a + b + c
  
  hexcolor = z.upper()
  rgbcolor = tuple(int(hexcolor[i:i+2], 16) for i in (0, 2, 4))
  red = rgbcolor[0]
  green = rgbcolor[1]
  blue = rgbcolor[2]
  
  newhex = "0x" + hexcolor
  embed=discord.Embed(title="Generated New Color For " + ctx.message.author.name, color=int(newhex, 16))
  embed.add_field(name="RGB Color", value=str(rgbcolor), inline=True)
  embed.add_field(name="Hex Color", value="#" + hexcolor, inline=True)
  await ctx.send(embed=embed)
  
@client.command(pass_context=True)
async def help(ctx):
  await ctx.send("Hello! I'm a naughty discord bot created by MyNameMadeYouSmile#8651 ! It's nice to meet you :)\n\nType !commands for the list of all my cool commands!")
  
@client.command(pass_context=True)
async def commands(ctx):
  await ctx.send("""```
          **COMMANDS LIST**
          
!help - Bot help.

!commands - Request for list of all commands.

!translate - Translate a word or sentence from one language to another.

!urban - Request a definition for a term from urban dictionary.

!searchgwa - Search for posts in gonewildaudio (5 posts per request).

!love - Calculate the possibility of two users loving eachother.

!chat - Chat with an AI bot.

!randomcolor - Generate random RGB & HEX color. Command aliases: !randcol, !rc```""")
  
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
  if str(ctx.message.channel) != "bot-playground":
    bot_channel = client.get_channel(657209517288718366)
    await ctx.send("Go to the " + bot_channel.mention + " channel to use the !urban command. Let's keep this channel clean.")
  else:
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
  if ctx.message.author.id != 649355698840535061:
    print(str(ctx.message.author) + " tried using the !clear command.")
  else:
    mgs = []
    async for x in ctx.message.channel.history():
      mgs.append(x)
    await ctx.message.channel.delete_messages(mgs)
    print("Successfully deleted all messages in chat.")
  
@client.command(pass_context=True)
async def searchgwa(ctx, *, searchterm):
  if str(ctx.message.channel) != "Direct Message with " + str(ctx.message.author):
    await ctx.send("Please PM me to use the !searchgwa command. Let's keep the server clean.")
  else:
    resultnum = 1
    for searchgwa in reddit.subreddit('gonewildaudio').search(searchterm, limit=5):
      if len(searchgwa.title) > 256:
        searchgwa.title = searchgwa.title[:253] + '...'
      time = searchgwa.created
      Date = datetime.datetime.fromtimestamp(time)
      embed=discord.Embed(title=searchgwa.title, url=searchgwa.url, description=searchgwa.selftext, color=random.randint(0, 0xffffff)) #color=0x5b5bff
      embed.set_author(name="Result #" + str(resultnum))
      embed.set_thumbnail(url=searchgwa.author.icon_img) #"https://www.redditstatic.com/desktop2x/img/avatar_over18.png"
      embed.add_field(name="Post Author", value="/u/" + str(searchgwa.author), inline=True)
      embed.add_field(name="Post Date", value=str(Date), inline=True)
      await ctx.send(embed=embed)
      resultnum += 1
    
@translate.error
async def translate_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !translate [from lang code] [to lang code] [sentence]")
 
@searchgwa.error
async def searchgwa_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !searchgwa [type what you're looking for]")
  
@urban.error
async def urban_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !urban [term]")
  
@love.error
async def love_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !love [boy] [girl]")
  
@chat.error
async def chat_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !chat [message]")
  
client.run(os.environ['BOT_TOKEN'])

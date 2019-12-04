import discord
from discord.ext.commands import Bot
from discord.ext import *
import os
from googletrans import Translator
import urllib.request
import json
import praw

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
  await ctx.send("""```diff
. :: COMMANDS LIST :: .
!help - Bot help.

!commands - Request for list of all commands.

!translate - Translate a word or sentence from one language to another.

!urban - Request a definition for a term from urban dictionary.```""")
  
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
async def newgwa(ctx):
  for submission in reddit.subreddit('gonewildaudio', 'gonewildaudible', 'gwascriptguild', 'gwabackstage').new(limit=1):
    await ctx.send("""```""" + submission.title + """```""")
    
@translate.error
async def translate_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !translate [from lang code] [to lang code] [sentence]")
 
@translate.error
async def urban_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !urban [term]")
  
client.run(os.environ['BOT_TOKEN'])

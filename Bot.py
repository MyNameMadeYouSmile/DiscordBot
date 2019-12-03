import discord
from discord.ext.commands import Bot
from discord.ext import *
import os
from googletrans import Translator

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)

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

!commands - Request for list of all commands.```""")
  
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
    ")
    await ctx.send("More codes here: https://ctrlq.org/code/19899-google-translate-languages")
    
@translate.error
async def translate_error(error, ctx):
    return await error.send(error.message.author.mention + " Usage: !translate [from lang code] [to lang code] [sentence]")
  
client.run(os.environ['BOT_TOKEN'])

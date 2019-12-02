import discord
from discord.ext.commands import Bot
from discord.ext import *
import os

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
  
client.run(os.environ['BOT_TOKEN'])

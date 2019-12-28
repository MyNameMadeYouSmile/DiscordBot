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
from calculator import Calc
from PIL import ImageDraw
import pymysql

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)

reddit = praw.Reddit(client_id=os.environ['14_chars'], \
                     client_secret=os.environ['27_chars'], \
                     user_agent='Tester', \
                     username=os.environ['reddit_u'], \
                     password=os.environ['reddit_p'])

cb = CleverBot()
chatterbotter = False

magicResponses = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
                 'Don’t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.',
                 'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.',
                 'Yes.', 'Yes – definitely.', 'You may rely on it.']

client.remove_command('help')

lotteryMoney = ['1000', '-500', '500', '10', '0', '10000', '-9999', '200', '150000']

async def urbangen(ctx, term):
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
  
async def insertMoney(ctx, prefiX, wonMoney, user):
  dbServer = 'remotemysql.com'
  dbUser = 'MPbzulZgmy'
  dbPass = os.environ['db_password']
  dbName = 'MPbzulZgmy'
  
  conn = pymysql.connect(host=dbServer, user=dbUser, passwd=dbPass, db=dbName)
  cur = conn.cursor()
  sql = "SELECT money FROM users WHERE username ='%s'"
  cur.execute(sql % user)
  row_count = cur.rowcount
  
  if row_count == 0:
    try:
      sql2 = "INSERT INTO users (username, money) VALUES (%s, %s)"
      args = (user, wonMoney)
      cur.execute(sql2, args)
      conn.commit()
    except Exception as e:
      print(e)
      
    await ctx.send(ctx.message.author.mention + " " + prefiX + wonMoney + " dollars. Check your bank status.")
  else:
    for row in cur:
      user_money = row[0]
    newMoney = int(user_money) + int(wonMoney)
    try:
      sql2 = "UPDATE users SET money=%s WHERE username=%s"
      args = (str(newMoney), user)
      cur.execute(sql2, args)
      conn.commit()
    except Exception as e:
      print(e)
      
    await ctx.send(ctx.message.author.mention + " " + prefiX + wonMoney + " dollars. Check your bank status.")
      
  conn.close()

async def chatbot(ctx):
  def pred(m):
    return m.author == ctx.message.author and m.channel == ctx.message.channel
  
  chatterbotter = True
  await cb.init()
  await ctx.send(ctx.message.author.mention + " I opened our chatting session, let's talk now :)")
  
  while chatterbotter == True:
    try:
      msg = await client.wait_for('message', check=pred, timeout=60.0)
    except asyncio.TimeoutError:
      await ctx.send('You took too long... closing our chat session.')
      await cb.close()
      chatterbotter = False
    else:
      if msg.content == "!stop":
        await ctx.send('It was nice talking to you... closing our chat session.')
        await cb.close()
        chatterbotter = False
      elif msg.content.startswith("!") and msg.content != "!stop":
        pass
      else:
        text = msg.content
        if text.lower().find("end") != -1:
          break
        response = await cb.getResponse(text)
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
    if str(error) == 'Command "stop" is not found':
      pass
    else:
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
async def chat(ctx):
  asyncio.get_event_loop().run_until_complete(chatbot(ctx))
  
@client.command(pass_context=True, name="8ball")
async def _8ball(ctx, *, question):
  await ctx.send(random.choice(magicResponses))
  
@client.command(pass_context=True)
async def calc(ctx, *, calculation):
  await ctx.send("Math Result: " + Calc.evaluate(calculation))
  
@client.command(pass_context=True)
async def quote(ctx):
  r=requests.get("https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
  quote_dict = json.loads(r.content)
  theQuote = quote_dict['quoteText']
  theAuthor = quote_dict['quoteAuthor']
  await ctx.send('"' + theQuote + '"\n\n~ ' + theAuthor)
  
@client.command(pass_context=True)
async def dog(ctx):
  r=requests.get("https://dog.ceo/api/breeds/image/random")
  dog_dict = json.loads(r.content)
  theDog = dog_dict['message']
  embed=discord.Embed(title=":dog: Woof!", url=theDog)
  embed.set_image(url=theDog)
  await ctx.send(embed=embed)
  
@client.command(pass_context=True)
async def cat(ctx):
  r = requests.get("https://api.thecatapi.com/api/images/get?format=src&results_per_page=1")
  embed=discord.Embed(title=":cat: Meowww..", url=r.url)
  embed.set_image(url=r.url)
  await ctx.send(embed=embed)
  
@client.command(pass_context=True)
async def bird(ctx):
  r = requests.get("http://random.birb.pw/tweet.json/")
  bird_dict = json.loads(r.content)
  theBird = bird_dict['file']
  embed=discord.Embed(title=":bird: Tweet tweet..", url="https://random.birb.pw/img/" + theBird)
  embed.set_image(url="https://random.birb.pw/img/" + theBird)
  await ctx.send(embed=embed)
  
@client.command(pass_context=True, aliases=['rb'])
async def removebg(ctx, imgUrl):
  urllib.request.urlretrieve(imgUrl, "remove-new-bg.png")
  
  response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('remove-new-bg.png', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': os.environ['apiKey']},
  )
  if response.status_code == requests.codes.ok:
    with open('new-removed-bg.png', 'wb') as out:
      out.write(response.content)
      await ctx.send(file=discord.File('new-removed-bg.png'))
  else:
      print("Error:", response.status_code, response.text)
      
@client.command(pass_context=True)
async def money(ctx):
  #dbServer = 'www.db4free.net'
  #dbUser = 'discordbot'
  #dbPass = os.environ['db_password']
  #dbName = 'discord_bank'
  dbServer = 'remotemysql.com'
  dbUser = 'MPbzulZgmy'
  dbPass = os.environ['db_password']
  dbName = 'MPbzulZgmy'
  
  conn = pymysql.connect(host=dbServer, user=dbUser, passwd=dbPass, db=dbName)
  cur = conn.cursor()
  sql = "SELECT money FROM users WHERE username ='%s'"
  cur.execute(sql % str(ctx.message.author))
  row_count = cur.rowcount
  if row_count == 0:
    try:
      sql2 = "INSERT INTO users (username, money) VALUES (%s, %s)"
      args = (str(ctx.message.author), "0")
      cur.execute(sql2, args)
      conn.commit()
    except Exception as e:
      print(e)
    embed=discord.Embed(title=str(ctx.message.author.display_name) + "'s Bank Status", color=0x866f0f)
    embed.add_field(name="Money Amount", value="$ 0")
    
    await ctx.send(embed=embed)
  else:
    for row in cur:
      embed=discord.Embed(title=str(ctx.message.author.display_name) + "'s Bank Status", color=0x866f0f)
      embed.add_field(name="Money Amount", value="$ " + row[0])
      
      await ctx.send(embed=embed)
      
  conn.close()
  
@client.command(pass_context=True)
async def lottery(ctx):
  msgPrefix = ''
  msgPrefix2 = ''
  
  wonMoney = random.choice(lotteryMoney)
  
  if wonMoney.startswith('-'):
    msgPrefix = 'You just lost '
  else:
    msgPrefix = 'You just won '
    
  if wonMoney == '150000':
    doubleWonMoney = random.choice(lotteryMoney)
    if doubleWonMoney.startswith('-'):
      msgPrefix2 = 'You just lost '
    else:
      msgPrefix2 = 'You just won '
        
    asyncio.get_event_loop().run_until_complete(insertMoney(ctx, msgPrefix2, doubleWonMoney, str(ctx.message.author)))
      
    #await ctx.send(ctx.message.author.mention + " " + msgPrefix2 + doubleWonMoney + " dollars. Check your bank status.")
      
  else:
    asyncio.get_event_loop().run_until_complete(insertMoney(ctx, msgPrefix, wonMoney, str(ctx.message.author)))
      
    #await ctx.send(ctx.message.author.mention + " " + msgPrefix + wonMoney + " dollars. Check your bank status.")
  
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
  embed.add_field(name="RGB Color", value=str(red) + ", " + str(green) + ", " + str(blue), inline=True)
  embed.add_field(name="Hex Color", value="#" + hexcolor, inline=True)
  embed.set_thumbnail(url="https://color.dyno.gg/color/{}/80x80.png".format(hexcolor))
  await ctx.send(embed=embed)
  
@client.command(pass_context=True)
async def help(ctx):
  await ctx.send("Hello! I'm a naughty discord bot created by MyNameMadeYouSmile#8651 ! It's nice to meet you :)\n\nType !commands for the list of all my cool commands!")
  
@client.command(pass_context=True)
async def commands(ctx):
  embed=discord.Embed(title="-----------Naughty Bot Commands---------", description="!help - Bot help.\n\n!commands - Request for list of all commands.\n\n!translate - Translate a word or sentence from one language to another.\n\n!urban - Request a definition for a term from urban dictionary.\n\n!searchgwa - Search for posts in gonewildaudio (5 posts per request).\n\n!love - Calculate the possibility of two users loving eachother.\n\n!chat - Chat with an intelligent robot.\n\n!randomcolor - Generate random RGB & HEX color. Command aliases: !randcol, !rc\n\n!8ball - Ask magic 8ball a question.\n\n!calc - Use a calculator.\n\n!quote - Get a random quote.\n\n!cat - Request a cute cat picture.\n\n!dog - Request a cute dog picture.\n\n!bird - Request a random adorable bird picture.\n\n!removebg - Remove background from an image. Command alias: !rb", color=0x707a08)
  
  await ctx.send(embed=embed)
  
  #await ctx.send("""```
         # **COMMANDS LIST**
          
#!help - Bot help.

#!commands - Request for list of all commands.

#!translate - Translate a word or sentence from one language to another.

#!urban - Request a definition for a term from urban dictionary.

#!searchgwa - Search for posts in gonewildaudio (5 posts per request).

#!love - Calculate the possibility of two users loving eachother.

#!chat - Chat with an intelligent robot.

#!randomcolor - Generate random RGB & HEX color. Command aliases: !randcol, !rc

#!8ball - Ask magic 8ball a question.

#!calc - Use a calculator.

#!quote - Get a random quote.```""")
  
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
    if str(ctx.message.channel) == "testing-bot":
      await urbangen(ctx, term)
      #asyncio.get_event_loop().run_until_complete(urbangen(ctx, term))
    else:
      bot_channel = client.get_channel(657209517288718366)
      await ctx.send("Go to the " + bot_channel.mention + " channel to use the !urban command. Let's keep this channel clean.")
  else:
    await urbangen(ctx, term)
    #asyncio.get_event_loop().run_until_complete(urbangen(ctx, term))
  
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
  
@_8ball.error
async def _8ball_error(error, ctx):
  return await error.send(error.message.author.mention + " Usage: !8ball [Your question]")
  
@love.error
async def love_error(error, ctx):
  return await error.send(error.message.author.mention + " Usage: !love [boy] [girl]")

@removebg.error
async def removebg_error(error, ctx):
  return await error.send(error.message.author.mention + " Usage: !removebg [image url]")
  
client.run(os.environ['BOT_TOKEN'])

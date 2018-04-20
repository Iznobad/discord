import discord
import asyncio
import os
import requests
from discord.ext import commands
from discord.ext.commands import Bot

client = discord.Client()

@client.event
async def on_ready():
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print('Let\'s go!')

@client.event
async def on_message(message):

  if message.content.startswith('!ping'):
    await client.send_message(message.channel, 'Pong!')
  elif message.content.startswith('€zk'):
    response = getEzkValue()
    await client.send_message(message.channel, response)
  elif message.content.startswith('$'):
    coin = message.content[1:].upper().strip(' ,')
    response = getCurrentValues(coin)
    await client.send_message(message.channel, response)
  elif message.content.startswith('!top'):
    """ Hier die coins für !top eintragen """
    coin = 'BTC,ETH,ICN,XLM,XMR,LSK,SAN'
    response = getCurrentValues(coin)
    await client.send_message(message.channel, response)
  elif message.content.startswith('!buffet'):
    response = 'https://imgur.com/02Bxkye'
    await client.send_message(message.channel, response)
  elif message.content.startswith('!rip'):
    response = ':meat_on_bone: :meat_on_bone: :meat_on_bone:'
    await client.send_message(message.channel, response)
  elif message.content.startswith('!moon'):
    response = ':rocket: :full_moon:'
    await client.send_message(message.channel, response)
    
def getCurrentValues(coin):
  """Grab current values for a coin from Cryptocompare."""
  apiRequest = requests.get(
    'https://min-api.cryptocompare.com/data/pricemultifull?fsyms='
    + coin +
    '&tsyms=EUR').json()

  """Create and initiate lists for coins, values and %change"""
  coins = coin.split(',')
  values = []
  change = []
  """Build response"""
  r = '```\n'
  for x in coins:
    try:
      coinStats = apiRequest['RAW'][x]['EUR']
    except KeyError:
      r = 'Heast du elelelendige Scheißkreatur, schau amoi wos du für an Bledsinn gschrieben host. Oida!'
      return r
    
    """Build arrays"""
    values.append(round(coinStats['PRICE'],2))
    change.append(round(coinStats['CHANGEPCT24HOUR'],2))
    
  """Dynamic indent width"""
  valuewidth = len(max(map(str, values), key=len))
  changewidth = len(max(map(str, change), key=len))
  
  r = '```\n'
  for x in coins:  
    r += coins[coins.index(x)] + ': '+ ('%.2f' % (values[coins.index(x)])).rjust(valuewidth) + ' EUR |' + ('%.2f' % (change[coins.index(x)])).rjust(changewidth) + '%\n'
  r += '```'
  return r

def getEzkValue():

  amountBTC = 0.0280071
  amountETH = 0.38042397
  apiRequest = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=EUR').json()
  valueBTC = float(apiRequest['BTC']['EUR'])
  valueETH = float(apiRequest['ETH']['EUR'])
  value = round(amountBTC * valueBTC + amountETH * valueETH,2)
  r = '```'
  r += str(value) + ' EUR (' + '{:+}%'.format(round((value/220-1)*100,2)) + ')'
  r += '```'
  return r

client.run(os.environ['BOT_TOKEN'])

import json, discord, asyncio, time, os, sys, aiohttp, io, requests
from discord.ext import commands
data = {}
if os.path.exists('config.json') == False:
    data['Token'] = ''
    data['Server_IP'] = ''
    with open("config.json", "w") as outfile:
        json.dump(data, outfile)
with open('config.json') as config_file:
    data = json.load(config_file)
if data['Token'] == '':
    Token = input("Podaj Token Bota!: ")
    data['Token'] = Token
    with open("config.json", "w") as outfile:
        json.dump(data, outfile)
if data['Server_IP'] == '':
    Server_IP = input("Podaj IP Serwera!: ")
    data['Server_IP'] = Server_IP
    with open("config.json", "w") as outfile:
        json.dump(data, outfile)

bot = commands.Bot(command_prefix='>')
@bot.event
async def on_ready():
    print('Zalogowano Jako: ', bot.user)
    activity = discord.Activity(name='Wyspa OFF', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
async def change_status():
    await bot.wait_until_ready()
    
    print("> Status Changer Loaded")
    while not bot.is_closed():
        try: 
            response = requests.get(f'http://{data["Server_IP"]}:30120/players.json')
            p2 = str(response.json())
            player_count = p2.count("name")
            current_status = f"Obywatele {player_count}/64"
            print(current_status,"\r", end='')
            activity2 = discord.Activity(name=current_status, type=discord.ActivityType.watching)
            await bot.change_presence(activity=activity2)
        except:
            activity2 = discord.Activity(name='Wyspa OFF', type=discord.ActivityType.watching)
            await bot.change_presence(activity=activity2)
        await asyncio.sleep(30)
bot.loop.create_task(change_status())
bot.run(data['Token'])

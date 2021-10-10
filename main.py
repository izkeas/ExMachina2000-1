import discord, util, os
from discord.ext import commands, tasks

# Http server
import threading
th = threading.Thread(target=util.http_server)
th.start()

# discord bot
intents = discord.Intents.all()
client  = commands.Bot(command_prefix=util.get_prefix, intents=intents)
commands_file = 'commands'

@client.event
async def on_ready():
    guilds_string = ''

    for guild in client.guilds:
        guilds_string += f"{guild.name} "
      
    print(f"{client.user} Is ready!!")
    print(f"Connected in: {guilds_string}")

    loop_function.start()

@tasks.loop(seconds=10)
async def loop_function():
    pass

# Cogs
for file in os.listdir(commands_file):
    if file.endswith('.py'):
        client.load_extension(f"{commands_file}.{file[:-3]}")

# Run
TOKEN = os.environ['TOKEN']
client.run(TOKEN)
th.join()
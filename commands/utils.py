from discord.ext import commands
from discord import Embed
import datetime
import search
import random, asyncio
import re

class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['GiveAway'])
    async def giveaway(self, msg, *args):
        
        try:
            args = [x.strip() for x in args]

            participants_amount = args.__len__()
            random_winner = int(random.uniform(1,participants_amount))

            await msg.channel.send(f"raffling off the winner...")
            await asyncio.sleep(3)

            winner = args[random_winner].replace(',',"")
            await msg.channel.send(f"The Winner Is: {winner}")
        except:
            await msg.channel.send("Use .GiveAway {@person1} {@person2} {etc...}")
    
    @commands.command()
    async def gcp(self, msg, *args):
        x = search.google_completion(" ".join(args))
        xs = "\n".join(x)
        xss = [ xs[i:i+1000] for i in range(0, xs.__len__(), 1000)]
        for xs in xss:
          await msg.channel.send(xs)
    
    @commands.command(aliases=['gsh'])
    async def gsearch(self, msg, *args):
        embed=Embed(title="Results")
        for x in search.google_search(" ".join(list(args))):
            value = f"{x.abstract}"
            if (x.metadata != None): 
                value += f"\n{x.metadata}"
            value += f"\n{x.url}"
            embed.add_field(name=x.title, value=value, inline=False)
      
        await msg.send(embed=embed)
    
    @commands.command(aliases=['sinonimos'])
    async def synos(self, msg, sin):
        embed=Embed(title="Synonyms")
        results = search.synonms(sin)
        results = re.sub(r'(\d{1,2} )', "", results).split("\n\n")

        for result in results:
          title = "None"
          value = ""
          for x in result.splitlines():
            x = x.replace("\n", "")
            if (x.endswith(":")):
              title = x
            else:
              value += x +"\n"

          embed.add_field(name=title, value=value, inline=True)
        await msg.send(embed=embed)
    
    @commands.command(aliases=['dict'])
    async def dicio(self, msg, word):
      results = search.dicio(word)
      await msg.send(results)
    
    @commands.command(aliases=["trls"])
    async def translate(self, msg, src, des, *args):
      results = search.translate(src, des, " ".join(args))
      await msg.channel.send("\n".join(results))
  
    @commands.command(aliases=["quediahoje", 'dia'])
    async def hoje(self, msg):
      today = datetime.datetime.today()
      week_day = today.weekday()

      if (week_day == 0):
        week_day = "Segunda"
      elif (week_day == 1):
        week_day = "Terça"
      elif (week_day == 2):
        week_day = "Quarta"
      elif (week_day) == 3:
        week_day = "Quinta"
      elif (week_day) == 4:
        week_day = "Sexta"
      elif (week_day) == 5:
        week_day = "Sadabdo"
      elif (week_day) == 6:
        week_day = "Domingo"
      
      await msg.send(f"Hoje é {week_day}, {today.day} de {today.month}, {today.year}")

    @commands.command(aliases=[""])
    async def calendarioporra(self, msg):
      pass

def setup(client):
    client.add_cog(Utils(client))
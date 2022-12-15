from nextcord.ext import commands 
import os 
bot = commands.Bot(command_prefix= '>')
from tempo import tempo
import threading

@bot.event
async def on_ready():
    print(f"{bot.user.name} está online!")
    #threading.Thread(target= tempo).start()

def load_cogs(bot):
    for file in os.listdir("commands"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f"commands.{cog}")

load_cogs(bot)

with open("./.env") as f:
    _token = f.read().strip()


if __name__ == "__main__":
    bot.run(_token)
from nextcord.ext import commands
import datetime
import asyncio

class TimeEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def timer_message(self):
        now = datetime.datetime.now()
        then = now.replace(hour= 17, minute= 20)
        wait_time = (then - now).total_seconds()
        await asyncio.sleep(wait_time)
        channel = self.bot.get_channel(882027203402022925)
        await channel.send("Oi")

def setup(bot):
    bot.add_cog(TimeEvent(bot))
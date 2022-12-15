from nextcord.ext import commands

class Daily_Comentado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def daily(self, ctx, tipo = '', numero = ''):
        await ctx.send("To funfa")

def setup(bot):
    bot.add_cog(Daily_Comentado(bot))
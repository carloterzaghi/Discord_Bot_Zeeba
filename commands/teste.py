from nextcord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



class Teste(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name= "teste")
    async def send_teste(self, ctx):
        user = ctx.message.author.id
        #db.collection('teste').add({'oi' : 'teste'})
        await ctx.send("To funfa")

    @commands.command(name= "emoji")
    async def emoji(self, ctx):
        await ctx.send(":grinning:")

def setup(bot):
    bot.add_cog(Teste(bot))
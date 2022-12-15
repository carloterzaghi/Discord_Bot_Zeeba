from nextcord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import nextcord
from typing import Union
from nextcord import Member

class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, ctx, tipo = '', ra : Union[Member, str] = '', nome = '', nome2 = '', nome3 = '', nome4 = '', nome5 = '', nome6 = '', nome7 = ''):
        db = firestore.client()
        user = ctx.message.author.id
        if tipo == '':
            await ctx.send("Comando inválido, use `>comandos` para ver como usa o código!")
        elif tipo == 'edit':
            if ra == '' and nome == '':
                await ctx.send("Coloque o seu **R.A.** e o **Nome**, dúvidas use `>comandos`.")
            elif ra == '':
                await ctx.send("Coloque o seu **R.A.**, dúvidas use `>comandos`.")
            elif nome == '':
                await ctx.send("Coloque o seu **Nome**, dúvidas use `>comandos`.")
            else:
                db.collection("users").document(str(user)).set({
                    "nome" : nome + nome2 + nome3 + nome4 + nome5 + nome6 + nome7,
                     "RA" : ra
                    })
                await ctx.send('O seu user foi criado/editado!')
        elif tipo == 'perfil':
            if ra != '':
                try:
                    user_pega = db.collection("users").document(str(ra.id)).get()
                    embed = nextcord.Embed(
                        title = "__R.A.__",
                        description = user_pega.to_dict()["RA"],
                        color = 0x97CBFF
                    )  
                    embed.set_author(name = ra.display_name, icon_url= ra.avatar) 
                    embed.add_field(name= "__NOME:__", value=
                        user_pega.to_dict()["nome"]
                        , inline=False)
                    await ctx.send(embed = embed)
                except:
                    await ctx.send('User ainda não criado, dúvidas use `>comandos`.')
            elif ra == '': 
                try:
                    user_pega = db.collection("users").document(str(user)).get()
                    embed = nextcord.Embed(
                        title = "__R.A.__",
                        description = user_pega.to_dict()["RA"],
                        color = 0x97CBFF
                    )  
                    embed.set_author(name = ctx.author.display_name, icon_url= ctx.author.avatar)
                    embed.add_field(name= "__NOME:__", value=
                        user_pega.to_dict()["nome"]
                        , inline=False)
                    await ctx.send(embed = embed)
                except:
                    await ctx.send('User ainda não criado, dúvidas use `>comandos`.')
            else:
                await ctx.send("Comando inválido, use `>comandos` para ver como usa o código!")

        else:
            await ctx.send("Comando inválido, use `>comandos` para ver como usa o código!")

def setup(bot):
    bot.add_cog(Users(bot))
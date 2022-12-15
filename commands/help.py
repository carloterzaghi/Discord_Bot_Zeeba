import nextcord
from nextcord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def comandos(self, ctx, tipo = ''):
        embed = nextcord.Embed(
                title = "__Informações do Bot__",
                description = "*Este bot foi feito somente para este server.*",
                color = 0x97CBFF
            )   
        embed.set_author(name = self.bot.user.name, icon_url= self.bot.user.avatar)
        embed.add_field(name= "⠀\n__USER:__", value=
             '➤ **>user <Tipo do comando>**\n' + 
             "Tipos:" + "\n" +
             "› **edit <Número do R.A.> <Seu nome>** : Cria/Edita o User"  + "\n" +
             "› **perfil** : Mostra o seu User" + "\n" +
             "› **perfil <@ do User que deseja ver>** : Mostra o User do @"
             , inline=False)
        embed.add_field(name= "⠀\n__PROJETO:__", value=
             '➤ **>projeto <Tipo do comando>**\n' + 
             "Tipos:" + "\n" +
             "› **criar <Nome do Projeto>** : Criar o Projeto"  + "\n" +
             "› **horario <Nome do Projeto> <Horário da Daily> <Dia da Semana>** : Adiciona um Horário a Daily" + "\n" +
             "› **horario tirar <Nome do Projeto> <Dia da Semana>** : Tirar um Horário a Daily" + "\n" +
             "› **mostrar <Nome do Projeto>** : Mostra sobre o Projeto" + '\n' +
             "› **mostrar** : Mostra o nome de todos os Projetos" + '\n' +
             "› **add <Nome do Projeto> <@ do User>** : Adiciona o @ User ao Projeto" + '\n' +
             "› **tirar <Nome do Projeto> <@ do User>** : Tirar o @ User ao Projeto" + '\n' +
             "› **canal <Nome do Projeto> pegar** : Adiciona o canal de voz que está ao Projeto" + '\n' +
             "› **canal <Nome do Projeto> pegar <ID do Canal de Voz>** : Adiciona o canal de voz do ID ao Projeto" + '\n' +
             "› **canal <Nome do Projeto> tirar** : Tira o canal de voz que está do Projeto" + '\n' +
             "› **canal <Nome do Projeto> tirar <ID do Canal de Voz>** : Tira o canal de voz do ID do Projeto" + '\n'
             , inline=False)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Help(bot))
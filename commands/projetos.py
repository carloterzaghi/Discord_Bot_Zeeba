from nextcord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import nextcord
from nextcord import Member

class Projetos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def projeto(self, ctx, tipo = '', nome = '', horario = '', semana = ''):
        db = firestore.client()
        user = ctx.message.author.id
        if tipo == '':
            await ctx.send("Comando inválido, use `>comandos` para ver como usa o código!")
        elif tipo == 'criar':
            db.collection("projects").document().set({
                    "daily" : ['hora'],
                    "nome" : nome,
                    'user' : [str(user)],
                    'canais' : ['canal1']
                    })
            await ctx.send(f"Projeto **{nome}** criado!")
        elif tipo == 'horario': 
            if nome == '':
                await ctx.send("Escolha o **Projeto** que deseja modificar, dúvidas use `>comandos`.")
            elif nome == 'tirar':
                if horario == '':
                    await ctx.send("Escolha o **Projeto** que deseja modificar, dúvidas use `>comandos`.")
                elif semana == '':
                    await ctx.send("Escolha a **Semana** que deseja modificar, dúvidas use `>comandos`.")
                else:
                    docs = db.collection('projects').get()
                    daily_list = []
                    for doc in docs:
                        if doc.to_dict()['nome']==horario:
                            key = doc.id
                            pegar_user = db.collection('projects').document(key).get()
                            for i in pegar_user.to_dict()["daily"]:
                                for n in i:
                                    if semana != n:
                                        daily_list.append(i)
                            if daily_list == []:
                                    db.collection('projects').document(key).update({
                                    "daily" : ['hora'],
                                })
                            else:
                                db.collection('projects').document(key).update({
                                    "daily" : daily_list,
                                })
                            return await ctx.send(f"Projeto **{horario}** editado!")
                    await ctx.send(f"Projeto **{horario}** não encontrado!")
            elif horario == '':
                await ctx.send("Escreva o **Horário** que adicionar, dúvidas use `>comandos`.")
            elif semana == '':
                await ctx.send("Escreva o dia da **Horário** que adicionar, dúvidas use `>comandos`.")
            else:
                docs = db.collection('projects').get()
                daily_list = []
                for doc in docs:
                    if doc.to_dict()['nome']==nome:
                        key = doc.id
                        pegar_user = db.collection('projects').document(key).get()
                        for i in pegar_user.to_dict()["daily"]:
                            daily_list.append(i)
                        if daily_list == ['hora']:
                            daily_list = []
                        daily_list.append({semana : horario})
                        db.collection('projects').document(key).update({
                            "daily" : daily_list,
                        })
                        return await ctx.send(f"Projeto **{nome}** editado!")
                await ctx.send(f"Projeto **{nome}** não encontrado!")
        elif tipo == 'mostrar':
            if nome == '':
                docs = db.collection('projects').get()
                projects_nomes = ''
                for doc in docs:
                    projects_nomes += f"**{doc.to_dict()['nome']}**" + '\n'
                embed = nextcord.Embed(
                            title = "__TODOS OS PROJETOS__",
                            description = 
                            '*Para mostrar um projeto detalhado use* `>projeto mostrar <Nome do Projeto>` \n\n **__Nomes:__**\n' +
                            projects_nomes,
                            color = 0x97CBFF
                        )  
                embed.set_author(name = ctx.author.display_name, icon_url= ctx.author.avatar)
                await ctx.send(embed = embed) 
            else:
                try:
                    docs = db.collection('projects').get()
                    for doc in docs:
                        if doc.to_dict()['nome']==nome:
                            key = doc.id
                            _pegar = db.collection('projects').document(key).get()
                            users = ''
                            daily = ''
                            canais = ''
                            for i in _pegar.to_dict()["user"]:
                                member = await self.bot.fetch_user(int(i))
                                users += "› "+str(member) + '\n'
                            for i in _pegar.to_dict()["daily"]:
                                for n in i:
                                    daily += "› "+str(n) + f' : {i[n]} \n'
                            for i in _pegar.to_dict()["canais"]:
                                canais += f"› <#{str(i)}> \n"
                    embed = nextcord.Embed(
                            title = "__PROJETO__",
                            description = f'Nome : {nome} \n⠀',
                            color = 0x97CBFF
                        )  
                    embed.set_author(name = ctx.author.display_name, icon_url= ctx.author.avatar)
                    embed.add_field(name= "__DAILY__", value=
                        f'Horário(s):\n {daily} ⠀'
                        , inline=False)
                    embed.add_field(name= "__CANAIS__", value=
                        f'Canais:\n {canais} ⠀'
                        , inline=False)
                    embed.add_field(name= "__USERS__", value=
                        f'{users}'
                        , inline=False)
                    await ctx.send(embed = embed)
                except:
                    await ctx.send(f"Projeto **{nome}** não encontrado!")
        elif tipo == 'add':
            if nome == '':
                await ctx.send("Coloque o **Nome** do Projeto, dúvidas use `>comandos`.")
            elif horario == '':
                await ctx.send("Coloque o **@ do User** que deseja adicionar ao projeto, dúvidas use `>comandos`.")
            else:
                user_list =[]
                docs = db.collection('projects').get()
                for doc in docs:
                    if doc.to_dict()['nome']==nome:
                        key = doc.id
                pegar_user = db.collection('projects').document(key).get()
                for i in pegar_user.to_dict()["user"]:
                    user_list.append(i)
                user_list.append(horario[3:-1])
                db.collection("projects").document(key).update({
                    "user" : user_list
                })
                await ctx.send(f'O User **{horario}** foi adicionado ao Projeto **{nome}**!')
        elif tipo == 'tirar':
            if nome == '':
                await ctx.send("Coloque o **Nome** do Projeto, dúvidas use `>comandos`.")
            elif horario == '':
                await ctx.send("Coloque o **@ do User** que deseja tirar do projeto, dúvidas use `>comandos`.")
            else:
                try:
                    user_list =[]
                    docs = db.collection('projects').get()
                    for doc in docs:
                        if doc.to_dict()['nome']==nome:
                            key = doc.id
                    pegar_user = db.collection('projects').document(key).get()
                    for i in pegar_user.to_dict()["user"]:
                        user_list.append(i)
                    user_list.remove(horario[3:-1])
                    db.collection("projects").document(key).update({
                        "user" : user_list
                    })
                    await ctx.send(f'O User **{horario}** foi tirado do Projeto **{nome}**!')
                except:
                    await ctx.send(f'O User **{horario}** não está no Projeto **{nome}**!')
        elif tipo == 'canal':
            docs = db.collection('projects').get()
            if nome == '':
                await ctx.send("Escolha o **Projeto** que deseja modificar, dúvidas use `>comandos`.")
            else:
                try:
                    if horario == '': 
                        await ctx.send("Erro no comando, dúvidas use `>comandos`.")
                    elif horario == 'pegar':
                        if semana == '':#>projeto canal <Projeto> pegar
                            if (ctx.author.voice):
                                channel = ctx.message.author.voice.channel.id
                                for doc in docs:
                                    if doc.to_dict()['nome']==nome:
                                        key = doc.id
                                    canal_list = []
                                    pegar_canal = db.collection('projects').document(key).get()
                                    for i in pegar_canal.to_dict()["canais"]:
                                        if i != 'canal1':
                                            canal_list.append(i)
                                    canal_list.append(channel)
                                db.collection("projects").document(key).update({
                                    "canais" : canal_list
                                })
                                await ctx.send(f'Canal <#{channel}> foi adicionado ao Projeto **{nome}**!')
                            else:
                                await ctx.send("Você não está em nenhum canal de voz, dúvidas use `>comandos`.")
                        else: #>projeto canal <Projeto> pegar ID
                            for doc in docs:
                                if doc.to_dict()['nome']==nome:
                                    key = doc.id
                                canal_list = []
                                pegar_canal = db.collection('projects').document(key).get()
                                for i in pegar_canal.to_dict()["canais"]:
                                    if i != 'canal1':
                                        canal_list.append(i)
                                canal_list.append(semana)
                            db.collection("projects").document(key).update({
                                "canais" : canal_list
                            })
                            await ctx.send(f'Canal <#{semana}> foi adicionado ao Projeto **{nome}**!')
                    elif horario == 'tirar': 
                        if semana == '':#>>projeto canal <Projeto> tirar
                            if (ctx.author.voice):
                                channel = ctx.message.author.voice.channel.id
                                for doc in docs:
                                    if doc.to_dict()['nome']==nome:
                                        key = doc.id
                                    canal_list = []
                                    pegar_canal = db.collection('projects').document(key).get()
                                    for i in pegar_canal.to_dict()["canais"]:
                                        if i != 'canal1':
                                            canal_list.append(i)
                                    canal_list.remove(channel)
                                db.collection("projects").document(key).update({
                                    "canais" : canal_list
                                })
                                await ctx.send(f'Canal <#{channel}> foi tirado do Projeto **{nome}**!')
                            else:
                                await ctx.send("Você não está em nenhum canal de voz, dúvidas use `>comandos`.")
                        else: #>projeto canal <Projeto> tirar ID
                            for doc in docs:
                                if doc.to_dict()['nome']==nome:
                                    key = doc.id
                                canal_list = []
                                pegar_canal = db.collection('projects').document(key).get()
                                for i in pegar_canal.to_dict()["canais"]:
                                    if i != 'canal1':
                                        canal_list.append(i)
                                canal_list.remove(semana)
                            db.collection("projects").document(key).update({
                                "canais" : canal_list
                            })
                            await ctx.send(f'Canal <#{semana}> foi tirado do Projeto **{nome}**!')
                    else:
                        await ctx.send("Erro no comando, dúvidas use `>comandos`.")
                except:
                    await ctx.send(f"Projeto **{nome}** não encontrado!")
        elif nome == '':
            await ctx.send("Coloque o **Nome** do Projeto, dúvidas use `>comandos`.")

def setup(bot):
    bot.add_cog(Projetos(bot))
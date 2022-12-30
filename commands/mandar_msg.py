from venv import create
from nextcord.ext import commands, tasks
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
from datetime import date
import datetime
import threading
import asyncio
import nextcord

cred = credentials.Certificate({
   
  })
firebase_admin.initialize_app(cred)
db = firestore.client()

DIAS = [
    'segunda',
    'terça',
    'quarta',
    'quinta',
    'sexta',
    'sabado',
    'domingo'
]

day = datetime.datetime.now()
data = date(year=day.year, month=day.month, day=day.day)
indice_da_semana = data.weekday()
dia_da_semana = DIAS[indice_da_semana]

class Mandar_MSG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        threading.Thread(target= self.tempo).start()

    def tempo(self):
        while True:
            list_horarios = []
            list_semana = []
            list_dailys = []
            docs = db.collection('projects').get()
            for doc in docs:
                for i in doc.to_dict():
                    if i == 'daily':   
                        if doc.to_dict()[i][0] == 'hora':
                            pass
                        else:
                            for n in doc.to_dict()[i]:
                                for m in n:
                                    if m.lower() == 'segunda' or 'segunda' in m.lower():
                                        list_semana.append('segunda')
                                    elif m.lower() == 'terça' or 'terça' in m.lower() or m.lower() == 'terca' or 'terca' in m.lower():
                                        list_semana.append('terça')
                                    elif m.lower() == 'quarta' or 'quarta' in m.lower():
                                        list_semana.append('quarta')
                                    elif m.lower() == 'quinta' or 'quinta' in m.lower():
                                        list_semana.append('quinta')
                                    elif m.lower() == 'sexta' or 'sexta' in m.lower():
                                        list_semana.append('sexta')
                                    elif m.lower() == 'sabado' or 'sabado' in m.lower() or m.lower() == 'sábado' or 'sábado' in m.lower():
                                        list_semana.append('sabado')
                                    elif m.lower() == 'domingo' or 'domingo' in m.lower():
                                        list_semana.append('domingo')
                                    list_horarios.append(n[m])
                                    list_dailys.append(doc.to_dict()['nome'])
            list_eventos_dia = []
            list_daily_dia = []
            if dia_da_semana in list_semana:
                encontrar = 0
                for n in list_semana:
                    if n == dia_da_semana:
                        list_eventos_dia.append(list_horarios[encontrar])
                        list_daily_dia.append(list_dailys[encontrar])
                    encontrar += 1
            if list_eventos_dia != []:
                self.daily(list_eventos_dia, list_daily_dia)
            # print(list_daily_dia)
            # print(list_eventos_dia)
            # print(list_semana)
            # print(list_horarios)
            time.sleep(5)

    def daily(self, list_horas, list_daily):
        hora_agora = time.localtime()[3]
        minuto_agora = time.localtime()[4]
        hora_daily = ''
        minuto_daily = ''
        encontrar = 0
        for n in list_horas:
            hora_daily = n[0:2]
            if ':' in hora_daily:
                hora_daily = n[0:1]
            minuto_daily = n[2:5]
            if ':' in minuto_daily:
                minuto_daily = n[3:5]
                if minuto_daily[0] == '0':
                    minuto_daily = minuto_daily[1]
            elif '-' in minuto_daily:
                minuto_daily = n[2:4]
            if hora_daily == str(hora_agora) and str(minuto_agora) in minuto_daily :
                # print(list_daily) 
                # print(dia_da_semana)  
                canais = ''
                #Pegar os Canais da 
                docs = db.collection('projects').get()
                for doc in docs:
                    if doc.to_dict()['nome']==list_daily[encontrar]:
                        key = doc.id
                        _pegar = db.collection('projects').document(key).get()
                        for i in _pegar.to_dict()["canais"]:
                            canais += f"› <#{str(i)}> \n"
                # _pegar = db.collection('projects').document(key).get()
                # for i in _pegar.to_dict()["canais"]:
                #     canais += f"› <#{str(i)}> \n"
                mandar = f'Daily: **__{list_daily[encontrar]}__** \n Horário: {dia_da_semana.title()} das {n} \n Canais: \n{canais}\n Status: **Começando Agora**'                                           
                db.collection('Ronaldinho').document('mandar').update({
                    'msg' : mandar
                })
                time.sleep(50)
            encontrar += 1

def setup(bot):
    bot.add_cog(Mandar_MSG(bot))

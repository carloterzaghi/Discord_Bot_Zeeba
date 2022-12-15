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
    "type": "service_account",
    "project_id": "zeebadata-d91ec",
    "private_key_id": "b65685ae72ded8aaf8b1817f29a812872f53684a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC1lNZJ6SzdVQG9\nPULqpIpeuJd/9r2x/l8uahrVWt4lt/RPPwwKrF4XrU6lYQ7uDczdFs3qjH/F312T\njW3nWjro3/q/YYvbtEGZnq6cHoZtJOyyGB54tpkvTwczC+IJwURIuVwBSKCuO4b8\nTF4KwSd37SSG3n9xF2CdYSaFv8CjYcRJIz+JIIZfKdJgRUjv6CSne6A3YjLMWnbb\nSm7xkRISd7lBFWGdkXOgXpqGoHhQusG5SKeF4zo2VU5+oUH7uqy6UEWzW0q1cbLC\nd5ek0b9+3WrHtOmU0urzRz1XO5twJ20G0PPLR4urgt/S3GjxfdvwLPoEF8MjzVzY\nbZABMQPnAgMBAAECggEAFTawvEzODYOXYuzryu7zLXLCXFROwCM4KnuB7AgkKOLv\nW2zBsuOFUJ3SMNcAgAZDt1apMuw8JzlbvNfKjbtIY5l7OW2jgcTy3wgfXSThzpGA\nR6QytyaaCeFhNXD/dOVL3XUuTwYVo5VXxVUErZv4SPX/DPSkjelNw8UsU3beAhhA\n+rTitbMyTyQvqKSqZf8TxQPMOW4QFCNkOq5ZOBlwm+n1m9oz3d6yAm4sCgJ0Q4gN\n+95XxcRQ27ktj3ZDKSFAd/ycXrP9bGsNfquLUqiM9Cfu0TW1lZS8o4V9Uuhk9tTW\n6oGQi8ZFJDv16eh9HbbHv/72SO2DXDnUkP4zH5L+RQKBgQDjx9Lu9Q997lUyBYJa\nQZ21Q5uDOBtZxozsy7CZ9SNpE6WbRSa33rNTIl8JCRKOvVCGOFzBYMd638KIvlsW\nrBCq60lM9e9D6bP6gBsjx5nuJ/u0UuMyWefAoqrZ2pxSk1fg/B5Ys2LimhBiP1TY\nMxo3Oc6je4ewAYj38xCXapLmawKBgQDME8h38iyd+GmJ6IBCod7HuVn2IykKIgYI\ngxoLVmGzLnKS8sKwGI6FS+ORJmeRvaq++aFEFCdP3MhkzLwb/AtilIdnGbnLKp2T\nBWxiiaZecpY/1q83kCs0NATlmuQQ5oN9SP0qYxzioKHHwfVM5WDvswSSFgTfXhPA\nkM/vhKRfdQKBgQDOeaFkSLIdVkDWEhZiWF5sJHfAj8iDLa8rK0zPkl3h7xRMVnfN\nbsshDeQV3ap7x3JJ6Kd0B5VrdY/ywpLxT1HgjV2prLmR1zP1W9C+Mz3+mzHX+NbI\nGqUwgoPa7QaM99FOOVwMzbdSb5Nwa7YuMMyPyQ/eM6kAy7NsB2I/zzSQNwKBgQCb\nU19cc9WjsoPZdD3S+VMP3rJrFd3RmY3QAsDa6jdYYrzPvbeSwk4PhHBDdOCVW6/O\nxT8KCvDU5y0bE30FK7QapwPb5Ae2a8wdL56L7UrUThCvrB4Wg0Nu6zzi6R43AswH\nmnsePOuqTip0WNr0WQ2Lw0xySBITVI5iHZY2LlXRVQKBgA0v85RSkEuWtfB/eLCI\nKrXeDUWtB7zKe4M+/SO1ZYPjPwonWNT5J26UYEgPA6MoqmsExW5i2zW7aIxnonM6\neAoAlSyW8k7ruywQeoJeyrg5ScXOHoZjKuV7YufV4Zug1VpHSDJ4jnoidmTJ8q3F\nl6C/afC/8MrOuTsZ10Nsenh+\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-y5j9q@zeebadata-d91ec.iam.gserviceaccount.com",
    "client_id": "111104499525836044876",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-y5j9q%40zeebadata-d91ec.iam.gserviceaccount.com"
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
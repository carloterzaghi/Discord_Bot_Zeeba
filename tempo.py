import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
from datetime import date
import datetime
from nextcord.ext import commands 

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

def tempo():
    while True:
        db = firestore.client()
        list_horarios = []
        list_semana = []
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
        list_eventos_dia = []
        if dia_da_semana in list_semana:
            encontrar = 0
            for n in list_semana:
                if n == dia_da_semana:
                    list_eventos_dia.append(list_horarios[encontrar])
                encontrar += 1
        if list_eventos_dia != []:
            daily(list_eventos_dia)
        print(list_eventos_dia)
        print(list_semana)
        print(list_horarios)
        time.sleep(5)

    # db = firestore.client()
    # docs = db.collection('projects').get()
    # daily_list = []
    # for doc in docs:
    #     daily_list.append(doc)
    # return daily_list

def daily(list_horas):
    hora_agora = time.localtime()[3]
    minuto_agora = time.localtime()[4]
    hora_daily = ''
    minuto_daily = ''
    for n in list_horas:
        hora_daily = n[0:2]
        if ':' in hora_daily:
            hora_daily = n[0:1]
        minuto_daily = n[2:5]
        if ':' in minuto_daily:
            minuto_daily = n[3:5]
        elif '-' in minuto_daily:
            minuto_daily = n[2:4]
        if hora_daily == str(hora_agora) and minuto_daily == str(minuto_agora):
            print('penis') #Depois daqui ele tem que mandar no channel selecionado uma msg falando que a daily vai começar aquela hora junto com o canal da daily
            #Depois ele começa a ver quem entra contando as horas
            #Depois quando bater a hora de sair ele manda que a daily acabou no channel selecionado

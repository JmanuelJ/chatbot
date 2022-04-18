import telebot
import pymongo
import dateparser

bot = telebot.TeleBot("inserta la Telegram API TOKEN")
client = pymongo.MongoClient("cadena de MongoDB Atlas")  
db_name = "Telegram_RecuerdoDatos"  
collection_name = "usarios"  
db = client[db_name][collection_name]
dic_user = {}

@bot.message_handler(commands=['start'])  
def _start(message):   
    msg = "Hola "+str(message.chat.username)+\
    "! Yo puedo ayudar a resolver las dudas mas comunes acerca de nuestro servicio."   
    bot.send_message(message.chat.id, msg)
    msg = "Estos comandos te podran ayudar:\n"+\
    "/ubi - Te proporcionare la ubicacion exacta de nuestro establecimiento\n"+\
    "/horario - Te proporcionare los horarios de atencion a clientes\n"+\
    "/costo - Te explicare cuales son nuestras tarifas\n"+\
    "/servicios - Te describire brevemente los servicios que ofrecemos\n"+\
    "/cita - Te dare la opcion de agendar una cita para que puedas conocernos"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['ubi'])  
def _save(message):   
    msg = "¡Nos complace saber que estas interesado en nuestros servicios!\n"+\
    "Actualmente nuestras instalaciones se encuentran en la siguiente locacion:"   
    message = bot.reply_to(message, msg)   
    ##Enviar localizacion
    latitud = 18.974694
    longitud = -98.240166
    bot.send_location(message.chat.id, latitud, longitud)

@bot.message_handler(commands=['horario'])  
def _save(message):
    photo = open('C:/Users/penta/Documents/entornos/chatbot/images/Horario.png', 'rb') 
    bot.send_photo(message.chat.id, photo)   
    msg = "Cabe mencionar que los dias festivos no se labora y por lo tanto no sera posible concretar cita"  
    message = bot.reply_to(message, msg) 

@bot.message_handler(commands=['costo'])  
def _save(message):   
    photo = open('C:/Users/penta/Documents/entornos/chatbot/images/Precios.png', 'rb') 
    bot.send_photo(message.chat.id, photo)
    msg = "En cuanto al servicio de Hojalateria y Restauracion "+\
        "se recomienda hacer "+\
        "una cita para evaluar el automovil o camioneta y asi brindarle un presupuesto más acertado.\n"
    message = bot.reply_to(message, msg)   

@bot.message_handler(commands=['servicios'])  
def _save(message):   
    msg = "Actualmente contamos con los siguientes servicios:\n"+\
        "* Pintura General\n"+\
        "* Pintura por pieza\n"+\
        "* Pulido y encerado\n"+\
        "* Hojalateria y restauracion\n"   
    message = bot.reply_to(message, msg)   
    bot.register_next_step_handler(message, save_event)

@bot.message_handler(commands=['cita'])  
def _save(message):   
    msg = "Para solicitar una cita es importante que considere hacerla con una semana de anticipacion.\n"+\
    "El formato para pedir tu cita es el siguiente 'Nombre del solicitante' : 'mes dia', por ejemplo: \n"+\
    "Juan : Dec 25 \n"   
    message = bot.reply_to(message, msg)   
    bot.register_next_step_handler(message, save_event)


def save_event(message):   
    dic_user["id"] = str(message.chat.id)     
    ## get text   
    txt = message.text   
    name= txt.split(":")[0].strip()    
    date = txt.split(":")[1].strip()     
    ## check date   
    date = dateparser.parse(date).strftime('%b %d')    
     ## save   
    lst_users = db.distinct(key="id")   
    if dic_user["id"] not in lst_users:   
        db.insert_one({"id":dic_user["id"], "events":{name:date}})   
    else:   
        dic_events = db.find_one({"id":dic_user["id"]})["events"]   
        dic_events.update({name:date})   
        db.update_one({"id":dic_user["id"]}, {"$set":   
                      {"events":dic_events}})    
    ## send done   
    msg = "Cita "+name+": "+date+" guardada."   
    bot.send_message(message.chat.id, msg)

@bot.message_handler(func=lambda m: True)
def chat(message):
    txt = message.text
    if any(x in txt.lower() for x in ["thank","grax","cool","gracias"]):
        msg = "Es un gusto servirte!"
    elif any(x in txt.lower() for x in ["perfecto","ok","entendido"]):
        msg = "¡Esperamos verte pronto,"+str(message.chat.username)+"!"
    else:
        msg = "Es un gusto servirte!"
    bot.send_message(message.chat.id, msg)


# run
try:
    bot.polling(True)
    # ConnectionError and ReadTimeout because of possible timout of the requests library

    # TypeError for moviepy errors

    # maybe there are others, therefore Exception
except Exception as e:
    logger.error(e)
        #time.sleep(15)


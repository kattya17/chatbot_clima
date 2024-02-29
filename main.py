import telebot
from telebot import types
import requests

TOKEN = 'TUTOKENAQUI'
# APIKEY DE API DE DATOS DE UN SISTEMA DE CLIMA
API_KEY = "API_KEY"

bot = telebot.TeleBot(TOKEN)
base_url = "https://api.openweathermap.org/data/2.5/weather?"


def get_weather(city_name):
    complete_url = base_url + "q=" + city_name + "&appid=" + API_KEY
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != 404:
        main_data = data["main"]
        weather_data = data["weather"][0]
        temperature = main_data["temp"] - 273.15
        description = weather_data["description"]
        return f"Temperatura: {temperature:.2f}C\n{description.capitalize()}"
    else:
        return "Ciudad no encontrada"


@bot.message_handler(commands=["clima"])
def send_weather(message):
    city_name = message.text.split()[1] if len(message.text.split()) > 1 else None
    if city_name:
        weather_info = get_weather(city_name)
        bot.reply_to(message, weather_info)
    else:
        bot.reply_to(message, "Por favor, proporciona el nombre de la ciudad")


# cREACION DE COMANDOS SIMPLES
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hola, soy un bot creado para proporcionarte el clima de una ciudad que quieras, y hablar un poco sobre el clima si quieres ver comandos  solicita: /help",
    )


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Puedes interactuar usando comandos /help /start /pregunta /clima /meme",
    )
    


# repite el mensaje que se envia
# @bot.message_handler(func=lambda m:True)
# def echo_all(message):
#   bot.reply_to(message,message.text)


@bot.message_handler(commands=["pregunta"])
def send_options(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    # Creando botones
    btn_frio = types.InlineKeyboardButton("Frio", callback_data="pregunta_frio")
    btn_calor = types.InlineKeyboardButton("Calor", callback_data="pregunta_calor")

    # Agrega botones al markup
    markup.add(btn_frio, btn_calor)
    # Enviar mensajes con los botones
    bot.send_message(message.chat.id, "Que prefieres?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pregunta_frio":
        bot.answer_callback_query(call.id, "Cada uno con sus gustos")
    elif call.data == "pregunta_calor":
        bot.answer_callback_query(call.id, "A mi tambien!!!")


@bot.message_handler(commands=["meme"])
def send_image(message):
    img_url = "https://www.lavoz.com.ar/resizer/1_9S8JbPvthokUto0V02nuJMEic=/1023x682/smart/cloudfront-us-east-1.images.arcpublishing.com/grupoclarin/T2DMODBZWVC23KXV4BEO66BD2Y.webp"
    bot.send_photo(chat_id=message.chat.id, photo=img_url, caption="Pov: no llueve")


if __name__ == "__main__":
    bot.polling(none_stop=True)

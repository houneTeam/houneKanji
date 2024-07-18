import telebot
from kanji_lists import JLPT
from jisho_api.kanji import Kanji

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может показать вам уровень JLPT, кунёми и онёми чтения для заданного иероглифа. Просто отправьте мне иероглиф.")

@bot.message_handler(func=lambda message: True)
def send_kanji_info(message):
    kanji = message.text
    kanji_info = Kanji.request(kanji)
    kun_readings = ', '.join(kanji_info.data.main_readings.kun)
    on_readings = ', '.join(kanji_info.data.main_readings.on)

    level = None
    for i, lvl in enumerate([JLPT.N1, JLPT.N2, JLPT.N3, JLPT.N4, JLPT.N5], start=1):
        if kanji in lvl:
            level = 'N' + str(i)
            break

    if level:
        bot.reply_to(message, f"Иероглиф: {kanji}\nУровень JLPT: {level}\nКунёми чтения: {kun_readings}\nОнёми чтения: {on_readings}")
    else:
        bot.reply_to(message, f"Иероглиф: {kanji}\nЭтот иероглиф не входит в JLPT.\nКунёми чтения: {kun_readings}\nОнёми чтения: {on_readings}")

bot.polling()

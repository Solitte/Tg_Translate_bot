import telebot
import json
import requests
'''
Телеграм-бот для перевода текста на различные языки с помощью Яндекс переводчика. 
Находится по адресу: https://t.me/SolitteTranslate_bot.
'''
API_URL='https://translate.api.cloud.yandex.net/translate/v2/translate'
API_TOKEN = '6614493130:AAEvNYY4kgDE-uehLkdNkYB42aWwDutT2Wk'
API_KEY = 'AQVN3Le8ILyZXEQa3isMvcstqOoxJ8vtwNCSxvix'
bot = telebot.TeleBot(API_TOKEN)
lang = 'ru'
text_original = ''
translate_text = ''


@bot.message_handler(commands=['start'])
def start_message(message):
    '''
    Выводит инструкцию, как пользоваться ботом.
    '''
    bot.send_message(message.chat.id,'Введите текст и получите перевод на русский язык!')
    bot.send_message(message.chat.id, 'Для смены языка перевода используйте команду /lang с кодом языка (ru,en,de,fr...)')
    bot.send_message(message.chat.id, 'Список кодов по адресу: https://yandex.ru/dev/translate/doc/ru/concepts/api-overview#languages')
    bot.send_message(message.chat.id, 'Вы можете использовать команду /save для сохранения последнего перевода в файл')


@bot.message_handler(commands=['lang'])
def language(message):
    '''
    Смена целевого языка для перевода.
    '''
    global lang
    if '/' not in message.text[message.text.find(' ')+1:]:
        lang = message.text[message.text.find(' ')+1:]
        bot.send_message(message.chat.id, f'Язык перевода сменен на {lang}')
    else:
        bot.send_message(message.chat.id, f'Язык перевода прежний {lang}')


@bot.message_handler(commands=['save'])
def save_translate(message):
    '''
    Сохранение последнего введеного текста и его перевода в текстовый файл.
    '''
    with open('tg_translate.txt', 'a', encoding='utf-8') as f:
        print(f'{text_original} - {translate_text}({lang})', file=f)
    bot.send_message(message.chat.id, 'Перевод сохранен в файл tg_translate.txt')


@bot.message_handler(content_types=['text'])
def translate(message):
    '''
    Перевод текста на целевой язык с помощью Яндекс переводчика.
    '''
    target_language = lang
    global text_original
    text_original = message.text
    body = {
        "targetLanguageCode": target_language,
        "texts": text_original,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key {0}".format(API_KEY)
    }

    response = requests.post(API_URL,
                             json=body,
                             headers=headers
                             )
    responce_dict = json.loads(response.text)
    global translate_text
    translate_text = responce_dict['translations'][0]['text']
    bot.send_message(message.chat.id, translate_text)

bot.polling()
from covid import Covid
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import settings

covid = Covid()


def get_cases(country):
    country_cases = covid.get_status_by_country_name(str(country))
    result = 'Болеет: {} \nВыздоровело: {} \nУмерло: {}'.format(country_cases["active"], country_cases["recovered"],
                                                                country_cases["deaths"])
    return result


def start(bot, update, user_data):
    # location_button = KeyboardButton('Отправить геопозицию', request_location = True)
    my_keyboard = ReplyKeyboardMarkup(
        [["Russia", "US", "China"], ["Spain", "Italy", "Iran"], ["United Kingdom",
                                                                 "Turkey", "Switerland"]])
    update.message.reply_text(
        'Я - бот собирающий информацию по COVID-19. \nДля начала, выберите страну из списка, или введите вручную: ',
        reply_markup=my_keyboard)
    print(update.message["chat"]["id"])
    return "country"


def country_set(bot, update, user_data):
    covid = Covid()

    statistic_markup = ReplyKeyboardMarkup([["Узнать статистику"], ["Изменить страну"]])

    user_country = update.message.text
    countries_list = covid.list_countries()
    countries = []
    for country in countries_list:
        countries.append(country["name"])

    if user_country in countries:
        settings.users_countries[update.message["chat"]["id"]] = user_country
        print(settings.users_countries)
        update.message.reply_text(
            "Страна задана! Теперь можете пользоваться кнопками для быстрого получения актуальной статистики и настроек.",
            reply_markup=statistic_markup)
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "Введенной Вами страны не существует, либо вы ошиблись. Напоминаю, что название страны должно вводиться на латинице.")
        return "country"


def get_statistic(bot, update, user_data):
    update.message.reply_text(get_cases(settings.users_countries[update.message["chat"]["id"]]))


def change_country(bot, update, user_data):
    my_keyboard = ReplyKeyboardMarkup(
        [["Russia", "US", "China"], ["Spain", "Italy", "Iran"], ["United Kingdom",
                                                                 "Turkey", "Switerland"]])
    update.message.reply_text(
        "Вы решили изменить страну отслеживания. Выберите из списка или введите сами новую страну:",
        reply_markup=my_keyboard)
    return "change"


def change_complete(bot, update, user_data):
    covid = Covid()

    statistic_markup = ReplyKeyboardMarkup([["Узнать статистику"], ["Изменить страну"]])

    user_country = update.message.text
    countries_list = covid.list_countries()
    countries = []
    for country in countries_list:
        countries.append(country["name"])

    if user_country in countries:
        settings.users_countries[update.message["chat"]["id"]] = user_country
        print(settings.users_countries)
        update.message.reply_text(
            "Страна изменена!", reply_markup=statistic_markup)
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "Введенной Вами страны не существует, либо вы ошиблись. Напоминаю, что название страны должно вводиться на латинице.")
        return "change"




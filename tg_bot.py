from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import logging
import settings
import functions
import os
import pickle

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    # Logging
    logging.info('Бот запускается')

    if os.path.exists('settings.pkl'):
        with open('settings.pkl', 'rb') as f:
            settings.users_countries = pickle.load(f)
    else:
        settings.users_countries = {}

    dp = mybot.dispatcher

    # Handlers declaration
    start = ConversationHandler(
        entry_points=[CommandHandler("start", functions.start, pass_user_data=True)],
        states={
            "country": [MessageHandler(Filters.text, functions.country_set, pass_user_data=True)]
        },
        fallbacks=[]
    )
    change_country = ConversationHandler(
        entry_points=[RegexHandler("^(Изменить страну)$", functions.change_country, pass_user_data=True)],
        states={
            "change": [MessageHandler(Filters.text, functions.change_complete, pass_user_data=True)]
        },
        fallbacks=[]
    )
    dp.add_handler(start)
    dp.add_handler(change_country)
    dp.add_handler(RegexHandler("^(Узнать статистику)$", functions.get_statistic, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, functions.print_user, pass_user_data=True))

    # Starting bot
    mybot.start_polling()
    mybot.idle()

    # Bot stops working
    with open('settings.pkl', 'wb') as f:
        pickle.dump(settings.users_countries, f)
    logging.info('Бот остановлен!')


main()

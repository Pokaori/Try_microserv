from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot,ParseMode

import os
import sys

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','books.settings')
import django
django.setup()
from django.conf import settings

from admin_books.serializers import SubscriberSerializer,Subscriber
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f'Nice to meet you,{user["username"]}! Welcome to the Sharing Book bot!\n'
                              'You can subscribe to get information about new book reviews!\n'
                              'write /help to learn commands')


def help(update, context):
    update.message.reply_text('/subscribe - subscribe to new book reviews \n'
                              '/unsubscribe - unsubscribe from new book reviews')


def error(update, context):
    update.message.reply_text('Something broke!')

def send_review(subscribers,book):
    bot = Bot(token=settings.TOKEN)
    ms=f"New book {book['title']} review is already on our webpage\n" \
       f"Go to the {book['url']}  and read new review!\n"
    for subscriber in subscribers: bot.send_message(chat_id=subscriber["id"], text=ms,parse_mode=ParseMode.HTML)

def subscribe(update, context):
    try:
        serializer = SubscriberSerializer(data={"id":update.message.from_user['id']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception:
        update.message.reply_text("Can`t subscribe. Probably, you have subscribed already.")
    else:
        update.message.reply_text(f"You subscribed, {update.message.from_user['username']}")

def unsubscribe(update, context):
    try:
        subscriber= Subscriber.objects.get(id=update.message.from_user['id'])
    except ObjectDoesNotExist:
        update.message.reply_text("Can`t unsubscribe. Probably, you haven`t subscribed.")
    else:
        subscriber.delete()
        update.message.reply_text(f"You unsubscribed, {update.message.from_user['username']}")


# function to handle normal text

def main():

    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialoge
    updater = Updater(settings.TOKEN, use_context=True)
    dispatcher = updater.dispatcher


    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    dispatcher.add_handler(CommandHandler("unsubscribe", unsubscribe))


    # add an handler for normal text (not commands)

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
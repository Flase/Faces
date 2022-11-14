import telebot
import os
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from draw_ph1 import my_func

images_dir = 'images'
repost_channel = os.getenv('REPOST_CHANNEL')

TOKEN = '5767456606:AAGsg9GAg_hoXwHPLe8T-ZNmqnMAmTy7iGs'
bot = telebot.TeleBot(TOKEN, parse_mode=None)


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


args = Namespace(src=None, dst=None, out=None, warp_2d=True, correct_color=True, no_debug_window=True)


@bot.message_handler(commands=['start'])
def welcome(message):
    '''welcome msg'''
    bot.send_message(message.chat.id, "Здарова, бродяга! Ты мне фотку, я тебе мем.")


k = 0


@bot.message_handler(content_types=['photo'])
def image(message) -> None:
    '''processing incoming image'''
    global k
    global args
    k += 1
    if k == 1:
        bot.reply_to(message, "И куда мы это засунем?")
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        file_downloaded = bot.download_file(file_info.file_path)
        file_name = "{}_{}.jpg".format(datetime.now().strftime("%Y-%m-%d_%H:%M_srcimg"), message.from_user.id)
        file_path = "{}/{}".format(images_dir, file_name)
        with open(file_path, 'wb') as file_new:
            file_new.write(file_downloaded)
        args.src = file_path
    else:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        file_downloaded = bot.download_file(file_info.file_path)
        file_name = "{}_{}.jpg".format(datetime.now().strftime("%Y-%m-%d_%H:%M_destimg"), message.from_user.id)
        file_path = "{}/{}".format(images_dir, file_name)
        with open(file_path, 'wb') as file_new:
            file_new.write(file_downloaded)
        args.dst = file_path
        args.out = file_path
        my_func(args)

        with open(file_path, 'rb') as f:
            bot.send_photo(message.chat.id, f)
            k = 0
            args = Namespace(src=None, dst=None, out=None, warp_2d=True, correct_color=True, no_debug_window=True)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call) -> None:
    '''grab callback from inline keyboard'''
    if call.data == "share_this":
        bot.answer_callback_query(call.id, "Окей!")
        bot.forward_message(repost_channel, call.from_user.id, call.message.message_id)


# start bot
bot.infinity_polling()


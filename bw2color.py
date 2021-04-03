import telebot
from os import system
from time import sleep

bot = telebot.TeleBot("xxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxx")  # Telebot-api-key

@bot.message_handler(content_types = ['photo'])
def send_document(message):
	fileid = message.photo[0].file_id
	bot.send_message(message.chat.id, "Your photo received  Please wait this may take some time...")
	file = bot.get_file(fileid)
	filepath = file.file_path
	download = bot.download_file(filepath)
	with open("bw.jpg", 'wb') as new_file:
          new_file.write(download)
	system("python bw2color_image.py -i bw.jpg --prototxt model/colorization_deploy_v2.prototxt --model model/colorization_release_v2.caffemodel --points model/pts_in_hull.npy")
	color_img = open("color.jpg","rb")
	bot.send_photo(message.chat.id, color_img)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	bot.send_message(message.chat.id, "Black and white to color image bot ! Just send B/w and see the magic")

@bot.message_handler(func = lambda x : True)
def send_file(message):
	bot.send_message(message.chat.id, "send black and white images ! Not text !")
bot.polling(none_stop=False, interval=5, timeout=20)

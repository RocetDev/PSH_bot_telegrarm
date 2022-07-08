import requests
from bs4 import BeautifulSoup as bs
import telebot
from time import sleep

TOKEN = <YOUR_TOKEN>

bot = telebot.TeleBot(TOKEN)
url = r'http://psh.magtu.ru/'
flag = True


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
	bot.send_message(message.chat.id, "Привет!\
		Я бот который смотрит новости на сайте проектной школы\
		и отсылает их вам.\n \
		/post - начать отслеживать новые новости\n \
		/stop - прекратить отслеживать новости\n \
		/listnews - присылает список последних новостей")


@bot.message_handler(commands=['stop'])
def stop_post(message):
	global flag
	flag = False
	bot.send_message(message.chat.id, "Оправка новостей прекращена")


def parser(url_site):
	response = requests.get(url_site)
	soup = bs(response.text, "html.parser")
	title = soup.find_all("h3", class_="elementor-post__title")
	text = soup.find_all("div", class_="elementor-post__excerpt")
	info = []

	for tit, tex in zip(title, text):
		user_text = tit.text.replace("	", '') + " | " + tex.text + "\n" + url
		info.append(user_text)

	return info


@bot.message_handler(commands=['post'])
def post_news(message):
	global flag, url
	if not flag:
		flag = True
	bot.send_message(message.chat.id, 'Отправка новостей начата')
	old_news = parser(url)[0]
	while flag:
		if old_news != parser(url)[0]:
			old_news = parser(url)[0]
			bot.send_message(message.chat.id, old_news)


@bot.message_handler(commands=['listnews'])
def list_post_news(message):
	global url
	bot.send_message(message.chat.id, "Последние 4 новости:")
	for news in parser(url):
		bot.send_message(message.chat.id, news)


print("bot start to work")
if __name__ == "__main__":
	bot.infinity_polling()

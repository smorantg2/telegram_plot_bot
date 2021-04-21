

import telebot
from telebot import types
import numpy as np
import matplotlib.pyplot as plt

kind = None
X = None
Y = None
x_name = None
y_name = None
title = ""

bot = telebot.TeleBot("insert_your_token", parse_mode=None)

###############################################
#############   START MESSAGE    ##############
###############################################

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	chat_id = message.chat.id

	bot.send_message(chat_id,"Hey there! I'm Dome Agraph. \nI'm guessing you are craving for some plots... 😏")

	markup = types.ReplyKeyboardMarkup(row_width=2)
	itembtn1 = types.KeyboardButton('Bar Plot')
	itembtn2 = types.KeyboardButton('Line Plot')
	itembtn3 = types.KeyboardButton('Pie Chart')
	markup.add(itembtn1, itembtn2, itembtn3)

	bot.send_message(chat_id,"Tell me, what kind of plot do you want me to do?", reply_markup=markup)

###############################################
#############   BAR PLOT    ##############
###############################################

@bot.message_handler(regexp=(r'bar|line|pie'))
def kind_plot(message):
	chat_id = message.chat.id
	global kind
	if kind == None:
		wasempty = True
	else:
		wasempty = False

	kind = message.text.lower().split(" ")[0]


	bot.send_message(chat_id," Nice! Let's do it! 💥")
	if wasempty:
		bot.send_message(chat_id, "I need values and names for X an Y axis. "
							  "Please, use \"X_values:\" format before the data and separate each value with a comma. "
							  "\nThe first value will be used as axis name."
							  "\nIf you want a title type /title.")
	bot.send_message(chat_id, "Type /plot when you've finished entering data.")


@bot.message_handler(regexp=(r'x_values:'))
def x_axis_values(message):
	chat_id = message.chat.id
	global X
	global x_name
	try:
		values = np.array(message.text.split(":")[1].split(","))
		X = values[1:]
		x_name = values[0]
		bot.send_message(chat_id, "Got it! ✅")
	except:
		bot.send_message(chat_id, "I'm sorry, something went wrong... 🥺. Please check the format.")

@bot.message_handler(regexp=(r'y_values:'))
def y_axis_values(message):
	chat_id = message.chat.id
	global Y
	global y_name
	try:
		values = np.array(message.text.split(":")[1].split(","))
		Y = np.array(values[1:], dtype = np.float64)
		y_name = values[0]
		bot.send_message(chat_id, "Got it! ✅")
	except:
		bot.send_message(chat_id, "I'm sorry, something went wrong... 🥺. Please check the format.")

@bot.message_handler(commands=['title'])
def ask_title(message):
	chat_id = message.chat.id
	answer = bot.send_message(chat_id, "Please, tell me the title")
	bot.register_next_step_handler(answer, add_title)

def add_title(message):
	global title
	chat_id = message.chat.id
	title = str(message.text)
	bot.send_message(chat_id, "Gotcha!")


@bot.message_handler(commands=['plot'])
def domeaplot(message):
	chat_id = message.chat.id
	global X,Y,y_name,x_name, kind,title

	print(x_name);print(X)
	print(y_name);print(Y)
	print(kind)

	try:
		if kind == "bar":
			plt.figure(figsize = (8,4.5))
			y_pos = np.arange(len(X))
			plt.bar(y_pos, Y, align="center", alpha = 0.55, edgecolor = "black", color = (0.1,0.2,0.7))#, c = "#bf280a")
			plt.xticks(y_pos, X)
			plt.ylabel(y_name)
			plt.xlabel(x_name)
			plt.title(title)
			plt.savefig("last_plot.png")
		if kind == "line":
			plt.figure(figsize=(8,4.5))
			plt.plot(X, Y, alpha = 0.7, c = "#bf280a")
			plt.scatter(X, Y, alpha=0.7, c="#bf280a")
			plt.ylabel(y_name)
			plt.xlabel(x_name)
			plt.title(title)
			plt.savefig("last_plot.png")
		if kind == "pie":
			fig1, ax1 = plt.subplots(figsize=(8,4.5))
			ax1.pie(Y,labels=X, autopct='%1.1f%%',
					shadow=False, startangle=90)
			ax1.axis('equal')
			plt.title(title,bbox={'facecolor':'1', 'pad':6})
			plt.savefig("last_plot.png")

		# plt.ylim(0,np.max(Y))


		bot.send_photo(chat_id, photo=open('last_plot.png', 'rb'))
		bot.send_message(chat_id, "There you go! Hope you like it!")
	except:
		bot.send_message(chat_id, "I'm sorry, something went wrong... 🥺. Please check the format.")

###############################################
#############   CONTACT MESSAGE    ##############
###############################################

@bot.message_handler(regexp=(r'contact|reach out|get in touch|thanks'))
def send_contact(message):
	chat_id = message.chat.id

	contact_message = "My pleasure! Sergio Morant is the creator of this project, you can find him here:" \
					  "\nhttps://www.linkedin.com/in/sergio-morant-galvez/ 🌐"

	bot.send_message(chat_id,contact_message)

###############################################
#############   DATA TYPE MESSAGE    ##############
###############################################

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
	bot.reply_to(message, "I'm sorry, but I haven't learned to deal with that kind of information yet.")

###############################################
#############   ANY OTHER MESSAGE    ##############
###############################################

@bot.message_handler(func=lambda m: True)
def echo_all(message):

	chat_id = message.chat.id
	bot.send_message(chat_id,"I'm sorry, I cannot help you with that yet. I'm still learning 📖🎓.")




bot.polling()

import sqli
import telebot

bot = telebot.TeleBot("1249683899:AAHhysctjhbFB61j4pngsyPusRsRDbwkw48")
db = sqli.Sql('databeys.db')

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if bot.get_chat_member(message.chat.id, message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id, message.from_user.id).status == "creator":
            if not db.create(message.chat.id):
                bot.send_message(message.chat.id, "Guruh bazada mavjud!")
            else:
                bot.send_message(message.chat.id, "Guruh bazaga qo'shildi!")
    else:
        bot.send_message(message.chat.id, "Assalom aleykum!\nSiz ushbu bot yordamida kim nechta odam qo'shganini bilib borishingiz mumkin bo'ladi!\nBu uchun botni guruhga quwing va /start buyrug'ini bering.\n\nXatoliklar bo'lsa - support @murodov_azizmurod")



@bot.message_handler(content_types=['new_chat_members'])
def message_new_member(message):
    try:
        db.create(message.chat.id)
        if not db.create(message.chat.id):
            if not db.check_user(message.chat.id, message.from_user.id):
                db.add(message.chat.id, message.from_user.id, message.from_user.first_name, message.from_user.last_name)
                db.give_message(message.chat.id, message.from_user.id, len(message.new_chat_members))
                bot.delete_message(message.chat.id, message.message_id)
    except:
        bot.send_message(message.chat.id, "Xatolik yuz berdi!\nKod: 2. Botga administratorlik huquqi berilgan bo'lishi lozim!")

@bot.message_handler(commands=['result'])
def result(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if bot.get_chat_member(message.chat.id, message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id, message.from_user.id).status == "creator":
            try:
		db.create(message.chat.id)
                if len(db.results(message.chat.id)) > 0:
                    bot.send_message(message.chat.id, text=db.results(message.chat.id))
                else:
                    bot.send_message(message.chat.id, text="Ma'lumoat mavjud emas!")
            except:
                bot.send_message(message.chat.id, "Xatolik yuz berdi!\nKod: 3")
@bot.message_handler(content_types=['left_chat_member'])
def message_left_member(message):
	try:
		bot.delete_message(message.chat.id, message.message_id)
	except:
		bot.send_message(message.chat.id, text="Botga administratorlik huquqi berilgan bo'lishi lozim!")
	

if __name__ == "__main__":
    bot.polling(none_stop = True)


from telegram import Message, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from env_config import Config
import random

# todo
lbg_people = []

gossip_text_starts = [
	"Я тут таке почув 😮",
	"Тут ходять чутки, що...",
	"Інсайдік під'їхав 🕵️",
	"Ти не повіриш, але",
	"Кажуть, що...",
	"Слухай, що я дізнався 🤯",
]

gossip_photo_starts = [
	"Подивись на це 😲",
	"Тут таке фото надіслали...",
	"Ти бачив це? 😳",
	"Це просто неймовірно!",
	"Що скажеш на це? 📸",
	"Ось що я знайшов 🤯",
]

config = Config()

# Command handler for '/start'
async def start_async(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if access_granted(update):
		await update.message.reply_text("Вітаю! Надішліть повідомлення, і я перешлю його в чат.")
	else:
		await update.message.reply_text("На жаль, у вас немає доступу до цього бота.")

# Command handler for '/help'
async def help_async(update: Update, context: ContextTypes.DEFAULT_TYPE):
	text = \
	"""
		Надішліть повідомлення мені, і я перешлю його у обраний чат.\n
		Якщо у вас немає доступу, зверніться до @eltagun.

		V 2.0
	"""
	await update.message.reply_text(text)

# Command handler for '/enable'
async def enable_async(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if not update.effective_chat.type == 'group' and not update.effective_chat.type == 'supergroup':
		await update.message.reply_text("Ця команда доступна тільки в групових чатах.")
		return

	if not access_granted(update):
		await update.message.reply_text("На жаль, у вас немає доступу до цієї команди.")
		return

	config.set_forvarding(config.is_forwarding_enable() is False)
	await update.message.reply_text(f"Бота {'ввімкнено' if config.is_forwarding_enable() else 'вимкнено'}!")

# Message handler for forwarding messages
async def forward_message_async(update: Update, context: ContextTypes.DEFAULT_TYPE):

	if not access_granted(update):
		await update.message.reply_text("На жаль, ви не маєте доступу до написання госіпів 🥲")
		return
	
	if update.effective_chat.type == 'group' or update.effective_chat.type == 'supergroup':
		return

	if config.is_forwarding_enable() is False:
		await update.message.reply_text("Бота в групі було вимкнено!")
		return

	# todo catch exceptions
	if update.message.text:
		await forward_text_async(update.message.text, context)
	elif update.message.media_group_id:
		await forward_media_group_async(update, context)
		return
	elif update.message.photo:
		await forward_photo_async(update.message, context)
	else:
		await update.message.reply_text("Невідомий тип повідомлення")
		return

	await update.message.reply_text("Повідомлення надіслано!")

async def forward_text_async(text: str, context: ContextTypes.DEFAULT_TYPE):
	start_msg = random.choice(gossip_text_starts)
	text = f"🗣️ <b>{start_msg}</b>\n<blockquote>{text}</blockquote>"

	await context.bot.send_message(
		chat_id=config.get_chat_id(),
		text=text,
		parse_mode='HTML')

async def forward_photo_async(message: Message, context: ContextTypes.DEFAULT_TYPE):
	text = None
	if message.caption is not None:
		start_msg = random.choice(gossip_photo_starts)
		text = f"🗣️ <b>{start_msg}</b>\n<blockquote>{message.caption}</blockquote>"

	fileID = message.photo[-1]['file_id']
	await context.bot.send_photo(
		chat_id=config.get_chat_id(),
		photo = fileID,
		caption = text,
		parse_mode='HTML')

async def forward_media_group_async(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text("Я не вмію в групові фото😢. Надішліть їх по одному з підписом(або без)")
	return

def access_granted(update: Update) -> bool:
	if not config.is_access_check_enable():
		return True

	user_tag = update.effective_user.username
	if user_tag in config.get_coreteam_people():
		return True

	if user_tag in lbg_people:
		return True
	return False

def main():
	application = ApplicationBuilder().token(config.get_access_token()).build()

	application.add_handler(CommandHandler("start", start_async))
	application.add_handler(CommandHandler("help", help_async))
	application.add_handler(CommandHandler("enable", enable_async))

	# tbd /set_public_password

	application.add_handler(MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, forward_message_async))

	application.run_polling()
	print("Bot is running...")

if __name__ == "__main__":
	main()

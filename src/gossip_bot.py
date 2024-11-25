from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import Config
import random

# todo load from storage
lbg_people = []

coreteam_people = [
    'eltagun',
    'vskruta',
    'vtrachenaa',
    'komarivna',
    'shikouno',
    'OlhaVernik',
    'golomovzaa',
    'Vurchun',
    'dia_me_tr',
    'NAST_0111',
    'kseniyayaya',
    'valeriya_akmn',
    'SiNn_maks',
]

gossip_starts = [
    "Я тут таке почув",
    "Тут ходять чутки, що",
    "Ти не повіриш, але",
    "Слухай, що я дізнався",
]

config = Config()

# Command handler for '/start'
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if access_granted(update):
        await update.message.reply_text("Вітаю! Надішліть повідомлення, і я перешлю його в чат.")
    else:
        await update.message.reply_text("На жаль, у вас немає доступу до цього бота.")

# Command handler for '/help'
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = \
    """
        Надішліть повідомлення мені, і я перешлю його у обраний чат.\n
        Якщо у вас немає доступу, зверніться до @eltagun.
    """
    await update.message.reply_text(text)

# Command handler for '/enable'
async def enable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat.type == 'group' and not update.effective_chat.type == 'supergroup':
        await update.message.reply_text("Ця команда доступна тільки в групових чатах.")
        return

    if not access_granted(update):
        await update.message.reply_text("На жаль, у вас немає доступу до цієї команди.")
        return

    config.set_forvarding(True)
    await update.message.reply_text("Бота ввімкнено!")

# Command handler for '/disable'
async def disable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat.type == 'group' and not update.effective_chat.type == 'supergroup':
        await update.message.reply_text("Ця команда доступна тільки в групових чатах.")
        return

    if not access_granted(update):
        await update.message.reply_text("На жаль, у вас немає доступу до цієї команди.")
        return

    config.set_forvarding(False)
    await update.message.reply_text("Бота вимкнено!")

# # Command handler for '/chat_id'
# async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     title = update.effective_chat.title

#     # todo catch exceptions
#     # todo timeout
#     await update.message.reply_text(
#         f"Chat ID: `{chat_id}`. Type: `{title}`",
#         parse_mode='Markdown')

def access_granted(update: Update) -> bool:
    if not config.is_access_check_enable():
        return True

    user_tag = update.effective_user.username
    if user_tag in coreteam_people:
        return True

    if user_tag in lbg_people:
        return True
    return False

# Message handler for forwarding messages
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not access_granted(update):
        await update.message.reply_text("На жаль, ви не маєте доступу до написання госіпів 🥲")
        return

    start_msg = random.choice(gossip_starts)
    text = f"🗣️ <b>{start_msg}</b>\n<blockquote>{update.message.text}</blockquote>"

    # todo catch exceptions
    # todo timeout
    if config.is_forwarding_enable():
        await context.bot.send_message(
            chat_id=config.get_chat_id(),
            text=text,
            parse_mode='HTML')
        await update.message.reply_text("Повідомлення надіслано!")
    else:
        await update.message.reply_text("Бота в групі було вимкнено!")

def main():
    application = ApplicationBuilder().token(config.get_access_token()).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("enable", enable))
    application.add_handler(CommandHandler("disable", disable))

    # tbd /set_public_password

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))

    application.run_polling()

if __name__ == "__main__":
    main()

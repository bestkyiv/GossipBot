from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from settings import Settings

# todo save to storage
user_access = {}
settings = Settings()

# Command handler for '/start'
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if settings.is_access_check_enable() and user_id not in user_access:
        await update.message.reply_text("Welcome! Please enter the password to gain access:")
    else:
        await update.message.reply_text("You already have access. Send a message, and I'll forward it to the chat.")

# Command handler for '/chat_id'
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    name = update.effective_chat.title

    # todo catch exceptions
    await update.message.reply_text(
        f"Chat ID: `{chat_id}`.\nName: `{name}`",
        parse_mode='Markdown')

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not settings.is_access_check_enable():
        return
    # todo
    # user_id = update.effective_user.id
    # if user_id in user_access:
    #     await update.message.reply_text("You already have access. Send a message, and I'll forward it to the chat.")
    #     return  # User already has access

    # if update.message.text == PASSWORD:
    #     user_access[user_id] = True
    #     await update.message.reply_text("Access granted! You can now send messages to be forwarded.")
    # else:
    #     await update.message.reply_text("Incorrect password. Try again.")

# Message handler for forwarding messages
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if settings.is_access_check_enable():
        await check_password(update, context)
        return

    text = f"🗣️ <b>Gossip</b>\n<blockquote>{update.message.text}</blockquote>"

    # todo catch exceptions
    await context.bot.send_message(
        chat_id=settings.get_chat_id(),
        text=text,
        parse_mode='HTML')

    await update.message.reply_text(
        text="The gossip has been sended!",
        parse_mode='Markdown')


def main():
    application = ApplicationBuilder().token(settings.get_access_token()).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("chat_id", get_chat_id))
    # todo handler for chat configuration

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))

    application.run_polling()

if __name__ == "__main__":
    main()

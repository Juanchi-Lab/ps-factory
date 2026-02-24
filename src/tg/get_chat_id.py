import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

load_dotenv("/opt/ps_factory/config/.env")

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    print("\n==============================")
    print(f"CHAT_ID: {chat.id}")
    print(f"CHAT_TITLE: {chat.title}")
    print(f"CHAT_TYPE: {chat.type}")

    if user:
        print(f"FROM_USER: {user.username} ({user.id})")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handler))

    print("Listening... Send a message in the group.")
    app.run_polling()

if __name__ == "__main__":
    main()

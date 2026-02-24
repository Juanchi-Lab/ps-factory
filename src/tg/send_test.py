import os
from dotenv import load_dotenv
import asyncio
from telegram import Bot

load_dotenv("/opt/ps_factory/config/.env")

async def main():
    bot = Bot(token=os.environ["TG_BOT_TOKEN"])
    chat_id = int(os.environ["TG_CHAT_DRAFTS_ID"])
    await bot.send_message(chat_id=chat_id, text="✅ PS Factory: Telegram wired up from VPS.")
    print("sent")

if __name__ == "__main__":
    asyncio.run(main())

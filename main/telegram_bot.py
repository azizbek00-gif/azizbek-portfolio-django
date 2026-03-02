import telegram
import asyncio
import logging
from datetime import datetime

# Telegram bot sozlamalari
BOT_TOKEN = "8497289699:AAHz6RRU3bmQJwHRMgWCncF5Jcv0daPQAKM"
CHAT_ID = None  # Keyin o'zgartiriladi

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        self.bot = telegram.Bot(token=BOT_TOKEN)
    
    async def send_message(self, message):
        """Xabarni Telegram'ga yuborish"""
        global CHAT_ID
        try:
            # Agar CHAT_ID noma'lum bo'lsa, avtomatik olish
            if CHAT_ID is None:
                await self.get_chat_id()
            
            if CHAT_ID:
                await self.bot.send_message(
                    chat_id=CHAT_ID,
                    text=message,
                    parse_mode='HTML'
                )
                return True
            else:
                logger.error("Chat ID topilmadi")
                return False
                
        except Exception as e:
            logger.error(f"Telegram xatolik: {e}")
            return False
    
    async def get_chat_id(self):
        """Telegram Chat ID ni avtomatik olish"""
        global CHAT_ID
        try:
            updates = await self.bot.get_updates()
            if updates:
                # Eng so'nggi xabardan chat_id olish
                last_update = updates[-1]
                if last_update.message:
                    CHAT_ID = last_update.message.chat.id
                    logger.info(f"Chat ID topildi: {CHAT_ID}")
                    return CHAT_ID
            else:
                logger.warning("Hech qanday xabar yo'q. Botga /start yozing.")
                return None
        except Exception as e:
            logger.error(f"Chat ID olishda xatolik: {e}")
            return None
    
    async def send_contact_notification(self, name, email, message_text):
        """Kontakt form xabarnomasi"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        message = f"""
<b>📬 YANGI XABAR KELDI!</b>

<b>👤 Ism:</b> {name}
<b>📧 Email:</b> {email}
<b>💬 Xabar:</b>
<code>{message_text}</code>

<b>🕐 Vaqt:</b> {current_time}
"""
        return await self.send_message(message)

# Asinxron funksiya
async def send_telegram_message(name, email, message_text):
    notifier = TelegramNotifier()
    await notifier.send_contact_notification(name, email, message_text)

# Sinxron funksiya (Django dan chaqirish uchun)
def send_notification(name, email, message_text):
    """Django views dan chaqirish uchun"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_telegram_message(name, email, message_text))
        loop.close()
        return True
    except Exception as e:
        logger.error(f"Xatolik: {e}")
        return False

# Chat ID ni test qilish uchun
def test_bot():
    """Botni test qilish"""
    notifier = TelegramNotifier()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(notifier.get_chat_id())
    loop.close()

if __name__ == "__main__":
    test_bot()

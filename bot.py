import os
import re
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]

PRICES = """Актуальные цены CutStudio:

• YouTube Shorts / TikTok / Instagram до 3 минут — 80 ₽
• YouTube до 10 минут — 150 ₽
• YouTube до 30 минут — 250 ₽
• YouTube до 1 часа — 300 ₽
• Более 1 часа — 450 ₽
• VK Video и другие приложения — скидка 10%."""

ORDER = "Чтобы оформить заказ на CutStudio нужно написать менеджеру в Telegram: @CutStudiorg"

async def reply(update: Update, text: str):
    if update.effective_message:
        await update.effective_message.reply_text(text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message or not update.effective_message.text:
        return

    text = update.effective_message.text.lower().strip()

    if any(w in text for w in ("цен", "стоим", "прайс", "сколько стоит", "сколько")):
        await reply(update, PRICES)
        return

    if any(w in text for w in ("заказ", "заказать", "оформить", "хочу монтаж", "монтаж")):
        await reply(update, ORDER)
        return

    if any(w in text for w in ("срок", "сколько времени", "когда будет", "долго", "готово")):
        await reply(update, "Срок выполнения зависит от длительности и сложности видео. Точный срок вам сообщит менеджер при оформлении заказа.")
        return

    if any(w in text for w in ("оплат", "платить", "деньги", "рубл", "сум", "наличн", "реквизит", "карта")):
        await reply(update, "Оплата производится после выполнения работы. Можно платить в любой валюте, в том числе рублями или сумами. Наличными принимаем только в Самарканде. По способу оплаты и реквизитам напишите менеджеру: @CutStudiorg")
        return

    if any(w in text for w in ("привет", "здравств", "добрый", "доброе", "добрый вечер")):
        await reply(update, "Здравствуйте! Я бот CutStudio. Могу ответить на вопросы о цене, сроках, оплате и оформлении заказа.")
        return

    if any(w in text for w in ("cutstudio", "cut studio")):
        await reply(update, "Я отвечаю на вопросы о CutStudio: цена, срок, оплата и оформление заказа.")
        return

    if any(w in text for w in ("кто ты", "что ты", "помощь", "help")):
        await reply(update, "Я информационный бот CutStudio. Задавайте вопросы о цене, сроках, оплате и заказе.")
        return

    await reply(update, "Пожалуйста уточните вопрос и я отвечу")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

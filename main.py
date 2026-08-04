import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from database.database import add_user

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
        user.id,
        user.username,
        user.first_name,
    )

    if context.args:
        target_id = context.args[0]

        context.user_data["target"] = target_id

        await update.message.reply_text(
            "✍️ Anonim xabaringizni yuboring."
        )
        return

    bot_username = (await context.bot.get_me()).username

    link = f"https://t.me/{bot_username}?start={user.id}"

    await update.message.reply_text(
        f"🔗 Sizning anonim havolangiz:\n\n{link}\n\n"
        "Do'stlaringizga yuboring."
    )


async def anonymous_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "target" not in context.user_data:
        return

    target = int(context.user_data["target"])

    sender = update.effective_user

    text = update.message.text

    sender_username = (
        f"@{sender.username}"
        if sender.username
        else "Yo'q"
    )

    message = f"""
📩 Yangi anonim xabar

{text}

━━━━━━━━━━━━

👤 Kim yubordi

ID: {sender.id}
Username: {sender_username}
Ism: {sender.first_name}
"""

    await context.bot.send_message(
        chat_id=target,
        text=message,
    )

    await update.message.reply_text(
        "✅ Xabaringiz yuborildi."
    )

    context.user_data.clear()


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            anonymous_message,
        )
    )

    print("Bot ishga tushdi...")

    app.run_polling()


if __name__ == "__main__":
    main()

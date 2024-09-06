from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Foydalanuvchilar ID sini saqlash uchun dictionary
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum!   #Edu_Figma Botimizga xush kelibsiz!\n "
                                    "\nQandaydir tushunmovchilik yoki savollar bo'lsa menga murojaat qilsangiz bo'ladi.\n"
                                    "\nEslatma: SAVOL | TUSHUNMOVCHILIK | MUNOZARA | QO'SHIMCHA FIKR + TG NICKNAME.\n"
                                    "\nTo'g'ridan to'g'ri bog'lanish uchun: @ravshanovich11 ")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Foydalanuvchi ID sini va xabarni olamiz
    user_id = update.message.chat_id
    message_text = update.message.text

    # Foydalanuvchidan kelgan xabarni adminstratorga yuborish
    admin_id = '1946323657'  # O'zingizning Telegram ID
    user_data[user_id] = update.message.from_user.username or update.message.from_user.first_name

    # Adminstratorga xabar yuborish
    await context.bot.send_message(
        chat_id=admin_id,
        text=f"Foydalanuvchi {user_data[user_id]} (ID: {user_id}) dan xabar:\n\n{message_text}",
        reply_markup={'force_reply': True}
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Javob matnini va foydalanuvchi ID sini olish
    if update.message.reply_to_message:
        try:
            # Xabarni qayta yo'naltirish uchun foydalanuvchi ID sini olish
            replied_text = update.message.reply_to_message.text
            user_id_start = replied_text.find("ID: ") + 4
            user_id = int(replied_text[user_id_start:].split()[0])
            reply_text = update.message.text

            # Foydalanuvchiga javob yuborish
            await context.bot.send_message(chat_id=user_id, text=reply_text)
            await update.message.reply_text("Javob yuborildi!")

        except Exception as e:
            await update.message.reply_text(f"Xatolik yuz berdi: {e}")
    else:
        await update.message.reply_text("Iltimos, reply orqali javob bering!")


if __name__ == '__main__':
    application = ApplicationBuilder().token('7302921737:AAHsGHdQmqxEXHH4yLP8ryhReKDLx-fIDLg').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.TEXT, reply))

    application.run_polling()

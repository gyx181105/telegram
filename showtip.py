import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# 配置日志记录
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 处理 /start 命令的函数
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("点击查看提示消息", callback_data='show_tip')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="你好，请问有什么问题？", reply_markup=reply_markup)

# 处理用户点击提示按钮的函数
async def show_tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是一个提示消息！")

# 处理用户点击按钮的回调函数
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'show_tip':
        await show_tip(update, context)

if __name__ == '__main__':
    # 创建 Telegram 应用
    application = ApplicationBuilder().token('6562877686:AAGwMJV-0OOzhkluIEmx8ANpvyIbzuredug').build()

    # 添加处理 /start 命令的处理程序
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # 添加处理用户点击按钮的回调函数
    button_handler = CallbackQueryHandler(button)
    application.add_handler(button_handler)

    # 启动应用，开始接收和处理消息
    application.run_polling()



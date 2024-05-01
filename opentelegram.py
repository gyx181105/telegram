import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext

# 配置日志记录
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

# 设置 OpenAI API 密钥
api_key = "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"

# 处理 /start 命令的函数
async def start(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="你好")

# 生成回复的函数
async def generate_response(update: Update, context: CallbackContext) -> None:
    message = update.message.text

    # 使用 OpenAI API 生成回复
    completion_response = OpenAI.ChatCompletion.create(
        engine="davinci-002",
        prompt=message,
        max_tokens=50
    )

    # 从生成的回复中获取文本内容
    bot_response = completion_response.choices[0].text

    # 将生成的回复发送给用户
    await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)



# 处理未知命令的函数
async def unknown(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    # 创建 Telegram 应用
    application = ApplicationBuilder().token("7173521029:AAE45s3RYjfEVczFDzIgTQrXMpk9SQZZ8wM").build()

    # 添加处理 /start 命令的处理程序
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # 添加生成回复的处理程序
    generate_response_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), generate_response)
    application.add_handler(generate_response_handler)

    # 添加处理未知命令的处理程序
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    # 启动应用，开始接收和处理消息
    application.run_polling()

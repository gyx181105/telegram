import logging
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# 配置日志记录
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 配置新闻API的访问
NEWS_API_KEY = 'ec06b729c2854d98be227b565df5539c'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=' + NEWS_API_KEY

# 处理 /start 命令的函数
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="你好，请问有什么问题？")

# 处理 /help 命令的函数
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是帮助信息")

# 处理 /about 命令的函数
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是关于信息")

# 获取最新新闻的函数
async def fetch_news():
    response = requests.get(NEWS_API_URL)
    news_items = response.json().get('articles', [])
    news_list = []
    for item in news_items[:5]:  # 只获取前5条新闻
        title = item['title']
        url = item['url']
        news_list.append(f"{title}: {url}")
    return "\n\n".join(news_list)

# 处理 /menu 命令的函数，显示一个内联菜单
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🖼️新闻", callback_data='news'),
            InlineKeyboardButton("🖼️历史", callback_data='history'),
            InlineKeyboardButton("🖼️经济", callback_data='economy'),
        ],
        [
            InlineKeyboardButton("🖼️技术", callback_data='technology'),
            InlineKeyboardButton("🖼️文化", callback_data='culture'),
            InlineKeyboardButton("🖼️旅游", callback_data='travel'),
        ],
        
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="请选择一个选项：", reply_markup=reply_markup)

# 处理内联键盘选项的函数
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'news':
        # 获取最新新闻链接
        news_text = await fetch_news()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=news_text)
    else:
        await query.edit_message_text(text=f"你选择了: {query.data}")

if __name__ == '__main__':
    # 创建 Telegram 应用
    application = ApplicationBuilder().token('7095332277:AAH-0lLXiOmDcwrxyouoPJOQ4f8PR9tELN8').build()

    # 添加处理 /start, /help, /about, /menu 命令的处理程序
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('about', about))
    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(CallbackQueryHandler(button))  # 添加按钮点击处理

    # 启动应用，开始接收和处理消息
    application.run_polling()

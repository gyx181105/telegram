import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# 设置日志记录级别
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Telegram Bot 的 token
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# DuckDuckGo API 的基础 URL
DUCKDUCKGO_API_BASE_URL = "https://api.duckduckgo.com/"

# 处理 /start 命令的函数
def start(update, context):
    update.message.reply_text("欢迎使用搜索引擎机器人！发送 /search [query] 来执行搜索。")

# 处理 /search 命令的函数
def search(update, context):
    query = " ".join(context.args)
    if query:
        search_results = perform_search(query)
        update.message.reply_text(search_results)
    else:
        update.message.reply_text("请输入要搜索的内容。")

# 执行搜索的函数
def perform_search(query):
    params = {
        "q": query,
        "format": "json"
    }
    response = requests.get(DUCKDUCKGO_API_BASE_URL, params=params)
    data = response.json()
    if data.get("AbstractText"):
        return data["AbstractText"]
    elif data.get("RelatedTopics"):
        return data["RelatedTopics"][0]["Text"]
    else:
        return "没有找到相关结果。"

# 设置 Updater 和 Dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# 添加处理程序
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("search", search))

# 启动机器人
updater.start_polling()
updater.idle()

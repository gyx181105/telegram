import logging
import asyncio
import requests
import asyncpgsa
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler,filters
import openai


# 配置日志记录
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# 配置 OpenAI API 密钥
openai.api_key = "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"


# 配置新闻API的访问
NEWS_API_KEY = 'ec06b729c2854d98be227b565df5539c'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=' + NEWS_API_KEY

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

# 查询数据库的函数
async def query_database(offset=0, limit=2):
    # 假设你的数据库配置如下
    database_config = {
        'user': 'postgres',
        'password': '901205',
        'database': 'test0704',
        'host': 'localhost',
        'port': '5432'
    }
    
    # 连接到数据库
    async with asyncpgsa.create_pool(**database_config) as pool:
        async with pool.acquire() as conn:
            try:
                result = await conn.fetch('SELECT * FROM f_node_stats LIMIT $1 OFFSET $2', limit, offset)
                return result
            except Exception as e:
                # 处理异常情况，例如数据库连接失败、查询失败等
                logging.error(f"Failed to query database: {e}")
                return None
    
    # # 关闭数据库连接
    # await conn.close()
    
    # return result

# 处理 /start 命令的函数
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="你好，请问有什么问题？")

# 处理 /help 命令的函数
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是帮助信息")

# 处理 /about 命令的函数
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是关于信息")

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

# 处理内联按钮点击事件的函数
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'news':
        # 获取最新新闻链接
        news_text = await fetch_news()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=news_text)
    elif query.data == 'history':
        # 获取历史数据
        offset = 0  # 初始偏移量为0
        history_data = await query_database(offset=offset)
        if history_data:
            # 只发送前两行数据
            message = "\n".join([str(row) for row in history_data[:2]])
            # 添加下一页按钮
            keyboard = [[InlineKeyboardButton("下一页", callback_data='next_page|1')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=message, reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="未找到历史数据")
    elif query.data.startswith('next_page|'):
        # 获取当前页数
        page_num = int(query.data.split('|')[1])
        # 计算偏移量
        offset = (page_num - 1) * 2
        # 获取历史数据
        history_data = await query_database(offset=offset)
        if history_data:
            # 只发送前两行数据
            message = "\n".join([str(row) for row in history_data[:2]])
            # 添加上一页和下一页按钮
            keyboard = [
                [InlineKeyboardButton("上一页", callback_data=f'prev_page|{page_num-1}'),
                 InlineKeyboardButton("下一页", callback_data=f'next_page|{page_num+1}')],
            ]
            # 如果是第一页，则不显示上一页按钮
            if page_num == 1:
                keyboard[0].pop(0)
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=message, reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="没有更多数据了")
    elif query.data.startswith('prev_page|'):
        # 获取当前页数
        page_num = int(query.data.split('|')[1])
        # 计算偏移量
        offset = (page_num - 1) * 2
        # 获取历史数据
        history_data = await query_database(offset=offset)
        if history_data:
            # 只发送前两行数据
            message = "\n".join([str(row) for row in history_data[:2]])
            # 添加上一页和下一页按钮
            keyboard = [
                [InlineKeyboardButton("上一页", callback_data=f'prev_page|{page_num-1}'),
                 InlineKeyboardButton("下一页", callback_data=f'next_page|{page_num+1}')],
            ]
            # 如果是第一页，则不显示上一页按钮
            if page_num == 1:
                keyboard[0].pop(0)
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=message, reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="没有更多数据了")
    else:
        await query.edit_message_text(text=f"你选择了: {query.data}")

# 处理普通文本消息的函数
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text is not None and not update.message.text.startswith('/'):
        # 获取用户发送的文本消息
        user_input = update.message.text
        
        # 使用 OpenAI API 生成响应
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
            temperature=0.7,
            max_tokens=150
        )
        
        # 从 OpenAI API 响应中获取生成的回复消息
        reply_message = response.choices[0].message["content"].strip()

        # 发送回复消息给用户
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# # 定时发送 "你好" 消息的函数
# async def send_hello_message(application, chat_id):
#     while True:
#         await asyncio.sleep(60)  # 每3秒发送一次消息
#         await application.bot.send_message(chat_id=chat_id, text="你好")

if __name__ == '__main__':
    # 创建 Telegram 应用
    application = ApplicationBuilder().token('7095332277:AAH-0lLXiOmDcwrxyouoPJOQ4f8PR9tELN8').build()

    # 添加处理 /start, /help, /about, /menu 命令的处理程序
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('about', about))
    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(CallbackQueryHandler(button))  # 添加按钮点击处理
    # 添加处理普通文本消息的处理程序
    application.add_handler(MessageHandler(callback=handle_message, filters=None))


    # # 设置定时器，每3秒钟发送一次 "你好" 消息
    # loop = asyncio.get_event_loop()
    # chat_id = '6732994283'  # 将此处替换为你的聊天 ID
    # loop.create_task(send_hello_message(application, chat_id))

    # 启动应用，开始接收和处理消息
    application.run_polling()

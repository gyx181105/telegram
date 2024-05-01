import requests

# 设置你的 Telegram Bot API Token
TOKEN = '7095332277:AAH-0lLXiOmDcwrxyouoPJOQ4f8PR9tELN8'

# 发送一个请求获取最新消息
response = requests.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates')

# 解析响应并获取最新消息的 chat_id
data = response.json()
latest_message = data['result'][-1]  # 获取最新的一条消息
chat_id = latest_message['message']['chat']['id']
print("Chat ID:", chat_id)

from openai import OpenAI
import os


api_key = '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'  # 用你的实际 API 密钥替换这里的字符串


client = OpenAI(
  api_key=api_key#os.environ['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'],  # this is also the default, it can be omitted
)


completion =  client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])
# 打印生成的文本
print(completion.choices[0].message.content)
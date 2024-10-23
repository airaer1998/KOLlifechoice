import openai

# 设置 API 密钥
openai.api_key = "****"

start_sequence = "\nA:"
restart_sequence = "Q: "

prompt = " "

while len(prompt) != 0:
    # 用户输入问题
    prompt = input(restart_sequence)

    # 调用 GPT-4 API
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # 使用 gpt-4 模型
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},  # 系统消息
            {"role": "user", "content": prompt}  # 用户消息
        ],
        temperature=1,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=0
    )

    # 打印 GPT-4 的回复
    print(start_sequence, response["choices"][0]["message"]["content"].strip())



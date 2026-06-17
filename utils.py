import os
from datetime import datetime


def call_deepseek(client, prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一名专业、务实、适合新手的计算机求职辅导老师。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=False
    )

    return response.choices[0].message.content


def save_history(result):
    history_dir = "history"

    if not os.path.exists(history_dir):
        os.makedirs(history_dir)

    file_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"interview_prepare_{file_time}.txt"
    file_path = os.path.join(history_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(result)

    return file_path
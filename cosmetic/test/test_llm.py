import os
import requests
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def upload_image(file_path):
    url = 'http://127.0.0.1:5000/upload'
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()['url']
    else:
        raise Exception(f"Error uploading image: {response.content}")

image_directory = '/Users/bagchan-yeong/Desktop/cosmetic/graph'
image_files = [os.path.join(image_directory, file) for file in os.listdir(image_directory) if file.endswith(('png', 'jpg', 'jpeg'))]

image_urls = [upload_image(image_file) for image_file in image_files]

print("Uploaded image URLs:", image_urls)

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

if openai.api_key is None:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")


def generate_report(image_urls):
    messages = [
        {
            "role": "system",
            "content": "You are a trend researcher specializing in analyzing market trends from graphical data. Your task is to interpret the given cosmetic market trend graphs and generate a detailed report."
        },
        {
            "role": "user",
            "content": "Analyze the trends shown in these cosmetic market graphs and generate a report in korean"
        }
    ]

    for url in image_urls:
        messages.append({
            "role": "user",
            "content": f"Image URL: {url}"
        })
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1500,
    )

    return response.choices[0].message.content

# 보고서 생성
report = generate_report(image_urls)
print(report)

# 보고서를 파일에 저장
with open('cosmetic_market_trend_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

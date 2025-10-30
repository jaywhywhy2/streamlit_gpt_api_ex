from dotenv import load_dotenv
import os
from openai import OpenAI

# .env 파일 로드, # 기존 환경변수 덮어쓰기
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# openai api인증 및 OpenAI객체생성
client = OpenAI(api_key = OPENAI_API_KEY)

# 챗 컴플리션 실행
completion = client.chat.completions.create(
    model="gpt-5",
    messages=[
        # System 프롬포트 #리스트 안에 2개의 딕셔너리갇 ㅡㄹ어가는 것은 기본
        {
            "role": "system",
            "content": "You are an IT professional who explains things easily enough that even elementary school students can understand."}, #페르소나 설정,
        # User 프롬포트
        {
            "role": "user",
            "content": "클라우드와 플랫폼의 차이점을 설명해줘."}
    ]
)

# 결과 출력
print(completion.choices[0].message.content)
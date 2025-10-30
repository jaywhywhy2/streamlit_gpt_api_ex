####### lib 설치 ##########
# pip install openai
# pip install streamlit
# pip install python-dotenv
###########################
# 실행 : streamlit run 1-2_dalle3_streamlit.py
###########################

import streamlit as st
import io
import base64
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv
import os
import time


# .env 파일 경로 지정 
load_dotenv(override=True)

# Open AI API 키 설정하기
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key = OPENAI_API_KEY)

# 프롬포트 예시
# prompt = 장화신은 고양이가 우주를 걷는 모습
# prompt = "Baby dog walking in the space"

# 이미지 생성 함수 정의
def get_image(prompt) :
        response = client.images.generate(
        model="dall-e-3", # 모델은 DALLE 버전3 (현 최신 버전)
                prompt=prompt, # 사용자의 프롬프트
                size="1024x1024", # 이미지의 크기
                quality="standard", # 이미지 퀄리티는 '표준'
                response_format='b64_json', # 이때 Base64 형태의 이미지를 전달한다.
                n=1,
        )

        response = response.data[0].b64_json # DALLE로부터 Base64 형태의 이미지를 얻음.
        image_data = base64.b64decode(response) # Base64로 쓰여진 데이터를 이미지 형태로 변환
        image = Image.open(io.BytesIO(image_data)) # '파일처럼' 만들어진 이미지 데이터를 컴퓨터에서 볼 수 있도록 Open
        # 이미지 저장하기, 폴더 없으면 생성
        os.makedirs('output_img', exist_ok=True)
        # 현재 시간을 기반으로 고유한 파일 이름 생성
        timestamp = int(time.time())
        image.save(f"output_img/dalle_image_{timestamp}.png")

        return image

prompt = "Baby dog walking in the space"
#함수 호출
image = get_image(prompt)

def main():
        st.title("그림 그리는 AI 화가 서비스 👨‍🎨")
        st.image('https://wikidocs.net/images/page/215361/%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%ED%99%94%EA%B0%80.png')


        st.text("🎨 Tell me the picture you want. I'll draw it for you!")

        input_text = st.text_area("원하는 이미지의 설명을 영어로 적어보세요.", height=200)

        # Painting이라는 버튼을 클릭하면 True
        if st.button("Painting"):
                # 이미지 프롬프트가 작성된 경우 True
                if input_text:
                        try:
                                # 사용자의 입력으로부터 이미지를 전달받는다.
                                dalle_image = get_image(input_text)

                                # st.image()를 통해 이미지를 시각화.
                                st.image(dalle_image)
                        except:
                                st.error("요청 오류가 발생했습니다")
                # 이미지 저장 버튼 추가
                if st.button("Save Image"):
                        try:
                                # 현재 시간 기반 파일명 생성
                                timestamp = int(time.time())
                                filename = f"output_img/dalle_image_{timestamp}.png"
                                dalle_image.save(filename)
                                st.success(f"Image saved as {filename}")
                        except Exception as e:
                                st.error(f"Failed to save image: {str(e)}")
                # 만약 이미지 프롬프트가 작성되지 않았다면
                else:
                        st.warning("텍스트를 입력하세요")

#main 함수 실행
if __name__ == "__main__":
        main()
####### lib 설치 ##########
# pip install openai
# pip install streamlit
# pip install python-dotenv
###########################
# 실행 : streamlit run 2-4_docent_euntaek.py
###########################
import base64
from io import BytesIO
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image

# .env 파일 로드
load_dotenv(override=True)

# Open AI API 키 설정 및 OpenAI 객체 생성
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# 이미지를 Base64로 변환하는 함수
def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")  # PNG 형식으로 변환
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# 이미지 파일을 분석하여 설명을 반환하는 함수
def ai_describe(image_data, is_url=True):
    try:
        if is_url:
            image_content = {"type": "image_url", "image_url": {"url": image_data}}
        else:
            base64_image = encode_image(image_data)  # 이미지를 Base64로 변환
            image_content = {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 미술관 20년이상 경력을 보야한 전문 큐레이터입니다."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 이미지에 대해서 자세하게 설명해 주세요."},
                        image_content,
                    ],
                }
            ],
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {str(e)}"

# 웹 앱 UI 설정
st.title("AI 도슨트: 이미지를 설명해드려요!")

# 선택 탭 추가
tab1, tab2 = st.tabs(["이미지 파일 업로드", "이미지 URL 입력"])

with tab1:
    # 세션 상태 초기화
    if 'uploaded_images' not in st.session_state:
        st.session_state.uploaded_images = []
    
    # 저장된 모든 이미지와 해설 표시
    for idx, item in enumerate(st.session_state.uploaded_images):
        st.image(item['image'], width=300)
        
        # 해설과 복사 버튼
        col1, col2 = st.columns([20, 10])
        with col1:
            st.success(item['description'])
        with col2:
            st.markdown(f"""
                <button onclick="navigator.clipboard.writeText(`{item['description'].replace('`', '').replace("'", "\\'")}`);" 
                        style="padding: 5px 8px; font-size: 12px; cursor: pointer; border: 1px solid #ccc; border-radius: 3px; background: white;">
                    📋
                </button>
                """, unsafe_allow_html=True)
        
        # 추천 서비스 섹션
        if 'recommendations' in item:
            st.markdown("**🔍 유사한 이미지 추천**")
            rec_cols = st.columns(3)
            for rec_idx, rec_img in enumerate(item['recommendations']):
                with rec_cols[rec_idx]:
                    st.image(rec_img, use_container_width=True)
        
        st.markdown("---")
    
    # 새 이미지 업로드 영역 (항상 표시)
    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"], key=f"uploader_{len(st.session_state.uploaded_images)}")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, width=300)
        
        if st.button("해설", key=f"file_button_{len(st.session_state.uploaded_images)}"):
            result = ai_describe(image, is_url=False)
            
            # 유사 이미지 추천 생성 (예시 - 실제로는 AI API나 이미지 검색 API 사용)
            # 여기서는 더미 이미지로 예시를 보여드립니다
            recommendations = [
                image,  # 임시로 같은 이미지 사용 (실제로는 유사 이미지 URL이나 파일)
                image,
                image
            ]
            
            # 이미지, 해설, 추천을 세션에 저장
            st.session_state.uploaded_images.append({
                'image': image,
                'description': result,
                'recommendations': recommendations
            })
            st.rerun()

with tab2:
    input_url = st.text_area("이미지 URL을 입력하세요", height=70)
    if input_url:
        st.image(input_url, width=300)
        if st.button("해설", key="url_button"):
            result = ai_describe(input_url, is_url=True)
            st.success("아래는 AI해석 결과입니다! copy를 원하시면 우측 버튼을 클릭해주세요!")
            st.code(result, language=None)

 
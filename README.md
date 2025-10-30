# streamlit_gpt_api_ex

# git clone
```

```

# 가상환경 만들기 및 활성화
```
conda create -n gpt.env python=3.12
conda activate gpt_env
```
# 가상환경을 주피터 노트북에 등록하기
```
* jupyter 노트북에서 파이썬 코드를 실행할 수 있는 파이썬 
pip install ipykernel
* jupyter lab에 가상환경(gpt_env) 등록하기
python -m ipykernel install --user --name gpt_env
```

# 설치 라이브러리
```
* 환경변수 로딩 라이브러리 설치
pip install python-dotenv

* OPENAI사 라이브러리 설치
pip install openai

* 이미지 처리 시 필요한 라이브러리
pip install Pillow

#웹 구현 라이브러리
pip install steammlit
```

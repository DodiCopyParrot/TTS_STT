# Python 이미지를 사용하여 시작
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 파일 복사
COPY . /app

# 종속성 설치
RUN pip3 install openai flask

RUN pip install openai==1.54.1

RUN pip3 install gtts

RUN pip install requests

RUN pip install flask_cors

ENV OPENAI_API_KEY=YOUR_ACTUAL_API_KEY

# Flask 서버 실행
CMD ["python3", "app.py"]


## docker build --platform linux/amd64 --no-cache -t zxz4641/tts-stt:1.0.3 .
## docker push zxz4641/tts-stt:1.0.3
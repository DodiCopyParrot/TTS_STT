## 초기 설정
```
python3 -m venv venv
source venv/bin/activate

pip3 install openai flask

pip install openai==1.54.1

pip3 install gtts

pip install requests
```


## OpenAI API KEY 발급
1. OpenAI 페이지 이동
    * https://platform.openai.com/login 로 이동
    
2. API Key 발금
    * https://platform.openai.com/account/api-keys 이동
    * Create new secret key 클릭


## 로컬 서버 실행
```
python3 app.py
```

## Docker 빌드 및 실행
```
# Docker 이미지 빌드
docker build -t tts_stt_api .

# 컨테이너 실행
docker run -d -p 5000:5000 tts_stt_api

```

## API List
### `TTS`
```
curl -X POST http://localhost:5001/tts \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, this is a test message."}'

```
### `STT`
```
curl -X POST http://localhost:5001/stt \
     -F "file=@sample_audio.wav"
```

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
from gtts import gTTS
from io import BytesIO
import requests
import openai
import os

app = Flask(__name__)
CORS(app)
openai_api_key = os.getenv('OPENAI_API_KEY')


# 텍스트를 오디오로 변환하는 엔드포인트
@app.route('/tts', methods=['POST'])
def text_to_speech_api():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    # gTTS로 TTS 수행
    tts = gTTS(text=text, lang='en')
    # 메모리 내 파일 객체 생성
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)

    # 생성된 음성 파일 전송
    return send_file(
        audio_file,
        mimetype="audio/mpeg",
        as_attachment=False,
        download_name="output.mp3"
    )

# 오디오 파일을 텍스트로 변환하는 엔드포인트
@app.route('/stt', methods=['POST'])
def speech_to_text_api():
    audio_file = request.files.get('file')
    if not audio_file:
        return jsonify({'error': 'Audio file is required'}), 400

    temp_file_path = 'temp_audio_file.wav'

    try:
        # 오디오 파일 임시 저장
        audio_file.save(temp_file_path)

        # OpenAI STT API 호출 (HTTP 요청 사용)
        with open(temp_file_path, 'rb') as file:
            response = requests.post(
                'https://api.openai.com/v1/audio/transcriptions',
                headers={
                    'Authorization': f'Bearer {openai_api_key}',
                },
                files={
                    'file': file
                },
                data={
                    'model': 'whisper-1',
                    'language': 'en'  # 필요한 경우 언어 설정
                }
            )

        # 응답 상태 코드 확인 및 에러 처리
        if response.status_code != 200:
            print('Response Status Code:', response.status_code)
            print('Response Content:', response.text)
            return jsonify({'error': response.json()}), response.status_code

        transcription = response.json()['text']
        return jsonify({'transcription': transcription})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        # 임시 파일 삭제
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

# Flask와 OpenAI 라이브러리를 임포트합니다.
from flask import Flask, request, render_template
import openai

# Flask 애플리케이션 인스턴스를 생성합니다.
# 여기서 'template_folder' 인자는 템플릿 파일들이 저장된 폴더의 경로입니다.
app = Flask(__name__, template_folder='C:\geoiot\OpenLayers\openapi')

# OpenAI API 키를 설정합니다.
openai.api_key = "본인의 OpenAI API 키 입력"

# 대화 내역을 저장할 전역 리스트를 생성합니다.
conversation_history = []

# '/' 경로에 대한 라우트를 설정합니다. GET과 POST 메서드를 모두 허용합니다.
@app.route('/', methods=['GET', 'POST'])
def ask_question():
    # POST 메서드로 요청이 들어올 경우
    if request.method == 'POST':
        # 사용자의 질문을 폼 데이터에서 추출합니다.
        user_question = request.form['user_question']
        messages = [{"role": "user", "content": user_question}]

        # 기존 대화 내역을 메시지에 추가합니다.
        for entry in conversation_history:
            messages.append({"role": entry['role'], "content": entry['content']})

        # OpenAI의 GPT 모델을 사용하여 대화 완성을 요청합니다.
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=messages
        )

        # GPT의 응답을 추출합니다.
        assistant_answer = completion.choices[0].message["content"].strip()

        # 사용자 질문과 GPT의 응답을 대화 내역에 추가합니다.
        conversation_history.append({"role": "user", "content": user_question})
        conversation_history.append({"role": "assistant", "content": assistant_answer})

    # index.html 템플릿을 렌더링하고 대화 내역을 전달합니다.
    return render_template('index.html', conversation_history=conversation_history)

# 애플리케이션이 직접 실행되는 경우에만 서버를 시작합니다.
if __name__ == '__main__':
    app.run(debug=True)

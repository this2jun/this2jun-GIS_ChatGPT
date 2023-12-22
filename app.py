from flask import Flask, jsonify, render_template, request
import openai

app = Flask(__name__)


openai.api_key = "본인의 API 키 입력."


shelters = [
    {"id": 1, "name": "대피소 A", "latitude": 37.5665, "longitude": 126.9780},  # Seoul City Hall
    {"id": 2, "name": "대피소 B", "latitude": 37.5512, "longitude": 126.9880}  # N Seoul Tower
]


conversation_history = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_question = request.form['user_question']
        messages = [{"role": "user", "content": user_question}]

        for entry in conversation_history:
            
            role = entry['role']
            if role not in ['user', 'assistant']:
                role = 'user'  
            messages.append({"role": role, "content": entry['content']})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        assistant_answer = completion.choices[0].message["content"].strip()

        conversation_history.append({"role": "user", "content": user_question})
        conversation_history.append({"role": "assistant", "content": assistant_answer})

    return render_template('index.html', conversation_history=conversation_history)

@app.route('/get_shelters')
def get_shelters():
    return jsonify(shelters)

if __name__ == '__main__':
    app.run(debug=True)

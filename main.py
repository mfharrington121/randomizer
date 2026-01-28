from flask import Flask, render_template, jsonify
import os, random, requests, json, matplotlib.pyplot as plt

numbers = []

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/get-number')
def get_number():
    # number = random.randint(1,100)
    YOUR_OPENROUTER_API_KEY = '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'
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {YOUR_OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1", # Optional
        "messages": [
        {
            "role": "user",
            "content": "What is a random number between 1 and 100? only respond with the number."
        }
        ]
    })
    )
    number = int(response.json()['choices'][0]['message']['content'])
    numbers.append(number)
    create_histogram()
    return jsonify({'numbers': numbers})

def create_histogram():
    plt.hist([int(number) for number in numbers], bins=range(1, 100), edgecolor='black')
    plt.title('Histogram of "Random" Numbers')
    plt.xlabel('Number')
    plt.ylabel('Frequency')
    plt.savefig('static/histogram.png')
    plt.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
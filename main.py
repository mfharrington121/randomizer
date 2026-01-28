from flask import Flask, render_template, jsonify
import os, random, requests, json, matplotlib, plotly
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go


numbers = []

app = Flask(__name__, static_folder='static')

@app.route('/')
def hello():
    return render_template('index.html')

#@app.route('/histogram')
#def histogram():
    fig = go.Figure(data=[go.Histogram(x=numbers, nbinsx=20)])
    fig.update_layout(
        title='Random Numbers Distribution',
        xaxis_title='Number',
        yaxis_title='Frequency',
        template='plotly_white',
        height=500,
        width=700
    )
    return fig.to_html(include_plotlyjs='cdn')

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
            "content": "What is a random number between 1 and 100? Respond ONLY with the number, no other text or thinking."
        }
        ]
    })
    )

    content = response.json()['choices'][0]['message']['content']
    number = int(''.join(filter(str.isdigit, content)))
    numbers.append(number)

    create_histogram()
    return jsonify({'numbers': numbers})

def create_histogram():
    print(f"Creating histogram with numbers: {numbers}")
    try:
        fig = go.Figure(data=[go.Histogram(x=numbers, nbinsx=20)])
        fig.update_layout(
            title='Random Numbers Distribution',
            xaxis_title='Number',
            yaxis_title='Frequency',
            template='plotly_white',
            height=500,
            xaxis=dict(range=[0, 100])
        )
        fig.write_html('static/histogram.html')
        print("Histogram created successfully")
    except Exception as e:
        print(f"Error creating histogram: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
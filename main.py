from flask import Flask, render_template, jsonify
import random
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/get-number')
def get_number():
    number = random.randint(1,100)
    return jsonify({'number': number})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
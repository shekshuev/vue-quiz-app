from flask import Flask,request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
from datetime import datetime
import json
import random
import sys


load_dotenv()

webapp = Flask(__name__)
CORS(webapp)

answered = dict()

count = 0
count_variants = 0
questions = []

# with open(os.path.join(webapp.root_path, 'static', 'questions.json')) as f:
with open(os.path.join(os.path.dirname(sys.executable), 'static', 'questions.json')) as f:
    data = json.load(f)
    count = int(data["count"])
    questions = data["questions"]
    random.shuffle(questions)
    count_variants = int(len(questions) / count)

@webapp.route('/', defaults={'path': ''})
@webapp.route('/<path:path>')
def catch_all(path):
    return webapp.send_static_file("index.html")

@webapp.get('/categories')
@cross_origin()
def get_category():
    ip = request.remote_addr
    last_ip_number = int(ip.split('.')[3])
    if answered.get(last_ip_number):
        return jsonify({'message':'Вы уже прошли тестирование'}), 400
    else:
        return webapp.send_static_file("categories.json")

@webapp.get('/questions')
@cross_origin()
def get_questions():
    ip = request.remote_addr
    last_ip_number = int(ip.split('.')[3])
    if not data:
        return jsonify({'message':'Файл с вопросами не найден'}), 400
    else:
        variant = last_ip_number % count_variants
        if answered.get(last_ip_number):
            return jsonify({'message':'Вы уже прошли тестирование'}), 400
        else:
            return questions[variant:count + 1], 200

@webapp.route('/finish', methods=['POST'])
def add_message():
    ip = request.remote_addr
    last_ip_number = int(ip.split('.')[3])
    content = request.json
    print(content['count'])
    answered[last_ip_number] = content['count']
    variant = last_ip_number % count_variants
    with open("results.csv", "a") as myfile:
        myfile.write(f"{datetime.now()}, {ip}, {variant}, {content['count']}\n")
    return ('', 204)

if __name__ == "__main__":
    webapp.run(host="0.0.0.0", port=os.getenv("FLASK_PORT") or 8088)

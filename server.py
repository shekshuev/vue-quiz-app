from flask import Flask,request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os

load_dotenv()

webapp = Flask(__name__)
CORS(webapp)

answered = dict()

@webapp.route('/', defaults={'path': ''})
@webapp.route('/<path:path>')
def catch_all():
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
    question_files = list(filter(lambda name: name.endswith('.json'), os.listdir(os.path.join(webapp.root_path, 'static', 'questions'))))
    variant = last_ip_number % len(question_files)
    if answered.get(last_ip_number):
        return jsonify({'message':'Вы уже прошли тестирование'}), 400
    else:
        return webapp.send_static_file(f"questions/{question_files[variant]}")

@webapp.route('/finish', methods=['POST'])
def add_message():
    ip = request.remote_addr
    last_ip_number = int(ip.split('.')[3])
    content = request.json
    print(content['count'])
    answered[last_ip_number] = content['count']
    return ('', 204)

if __name__ == "__main__":
    webapp.run(port=os.getenv("FLASK_PORT") or 8080)
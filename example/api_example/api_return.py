from flask import Flask, request
from flask_cors import CORS
from api_db import APIdb
from urllib.parse import parse_qs
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['MAX_CONTENT_LENGTH'] = 16777216

@app.route('/get_quant_messages', methods=['GET'])
def get_quant_messages():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return str(APIdb().getQuantMessages(data['campanha_item_id']))
    except Exception as e:
        return str(e)

@app.route('/return_messages', methods=['POST'])
def return_messages():
    try:
        data = parse_qs(request.get_data().decode("utf-8"))
        data_dict = {}
        for i in data:
            data_dict[i] = data[i][0]
        APIdb().insertReturnMessages(
            data_dict['device_id'],
            data_dict['contact_phone_number'],
            data_dict['custom_id'],
            data_dict['order'],
            data_dict['message_time'],
            data_dict['readed_at'],
            data_dict['returned'],
            datetime.now()
        )
        return 'OK'
    except Exception as e:
        return str(e)

def create_app():
    return app
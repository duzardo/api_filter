# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, request
from flask_cors import CORS
from api_db import APIdb

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['MAX_CONTENT_LENGTH'] = 16777216

### ------------------------ DEVICE COMMUNICATIONS ------------------------ ###
@app.route('/envia_corpo_saudacao', methods=['GET'])
def envia_corpo_saudacao():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().enviaCorpoSaudacao(data['message_id'])
    except Exception as e:
        return str(e)

@app.route('/get_only_reader_bot', methods=['GET'])
def get_only_reader_bot():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        send_type = APIdb().getOnlyReaderBot(data['device_id'])
        if send_type == '3':
            return 'True'
        else:
            return 'False'
    except Exception as e:
        return str(e)

@app.route('/update_greeting_time', methods=['POST'])
def update_greeting_time():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().updateGreetingTime(data['device_id'], datetime.now())
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/get_last_greeting_time', methods=['GET'])
def get_last_greeting_time():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return str(APIdb().getLastGreetingTime(data['device_id']))
    except Exception as e:
        return str(e)

@app.route('/get_server_active', methods=['GET'])
def get_server_active():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getServerActive(data['device_id'])
    except Exception as e:
        return str(e)

@app.route('/get_active_greeting_messages', methods=['GET'])
def get_active_greeting_messages():
    try:
        return APIdb().getActiveGreetingMessages()
    except Exception as e:
        return str(e)

@app.route('/get_all_phones', methods=['GET'])
def get_all_phones():
    try:
        return APIdb().getAllPhones()
    except Exception as e:
        return str(e)

@app.route('/get_send_messages_not_greetings', methods=['GET'])
def get_send_messages_not_greetings():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getSendMessagesNotGreetings(data['device_id'])
    except Exception as e:
        return str(e)

@app.route('/get_greeting_messages', methods=['GET'])
def get_greeting_messages():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getGreetingMessages(data['device_id'])
    except Exception as e:
        return str(e)

@app.route('/get_greeting_number', methods=['GET'])
def get_greeting_number():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        greeting_number = APIdb().getGreetingNumber(data['device_id'])
        if greeting_number:
            return greeting_number
        else:
            return 'None'
    except Exception as e:
        return str(e)

@app.route('/get_random_greeting_num', methods=['GET'])
def get_random_greeting_num():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        greeting_number = APIdb().getRandomGreetingNum(data['device_id'])
        if greeting_number:
            return greeting_number
        else:
            return 'None'
    except Exception as e:
        return str(e)

@app.route('/set_greeting_number', methods=['POST'])
def set_greeting_number():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().setGreetingNumber(data['device_id'], data['greeting_number'])
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/get_greeting_number_two', methods=['GET'])
def get_greeting_number_two():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        greeting_numbers = APIdb().getGreetingNumberTwo(data['device_id'], data['vgroup_id'])
        if greeting_numbers:
            return greeting_numbers
        else:
            return 'None'
    except Exception as e:
        return str(e)

@app.route('/get_greeting_number_one', methods=['GET'])
def get_greeting_number_one():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        greeting_numbers = APIdb().getGreetingNumberOne(data['device_id'], data['group_id'])
        if greeting_numbers:
            return greeting_numbers
        else:
            return 'None'
    except Exception as e:
        return str(e)

@app.route('/get_greeting_configs', methods=['GET'])
def get_greeting_configs():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getGreetingConfigs(data['device_id'])
    except Exception as e:
        return str(e)

@app.route('/set_qrcode_true', methods=['POST'])
def set_qrcode_true():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().setQRCode(data['device_id'], True)
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/set_qrcode_false', methods=['POST'])
def set_qrcode_false():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().setQRCode(data['device_id'], False)
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/insert_monitor', methods=['POST'])
def insert_monitor():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().insertMonitor(data['contact_phone_number'], data['photo'], data['status'], data['tick'])
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/get_greeting', methods=['GET'])
def get_greeting():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        greeting = APIdb().getGreeting(data['device_id'], data['contact_phone_number'], datetime.now().strftime('%Y-%m-%d'))
        if greeting:
            return 'OK'
        else:
            return 'NOK'
    except Exception as e:
        return str(e)

@app.route('/insert_greeting', methods=['POST'])
def insert_greeting():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().insertGreeting(data['device_id'], data['contact_phone_number'])
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/get_config', methods=['GET'])
def get_config():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return str(APIdb().getConfig(data['config_id']))
    except Exception as e:
        return str(e)

@app.route('/get_phones2prank', methods=['GET'])
def get_phones2prank():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getPhones2Prank(data['group_id'], data['device_id'])
    except Exception as e:
        return str(e)

@app.route('/get_group_bydevice', methods=['GET'])
def get_group_bydevice():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return str(APIdb().getGroupByDevice(data['device_id']))
    except Exception as e:
        return str(e)

@app.route('/set_device_freshing', methods=['POST'])
def set_device_freshing():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().setDeviceFreshing(data['device_id'])
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/is_fresh_device', methods=['GET'])
def is_fresh_device():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().isFreshDevice(data['device_id'])
    except Exception as e:
        return str(e)

@app.route('/get_emoji_code', methods=['POST'])
def get_emoji_code():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        em_code = APIdb().getEmojiCode(data['emoji_image'])
        if em_code:
            return em_code
        else:
            return 'None'
    except Exception as e:
        return str(e)

@app.route('/invalid_contact_phone', methods=['POST'])
def invalid_contact_phone():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().updateContactPhoneNumber(data['number'], datetime.now(), False)
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/valid_contact_phone', methods=['POST'])
def valid_contact_phone():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().updateContactPhoneNumber(data['number'], datetime.now(), True)
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/update_return_message', methods=['POST'])
def update_return_message():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().updateReturnMessage(data['c_id'], datetime.now())
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/post_emojis', methods=['POST'])
def post_emojis():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().postEmojis(data['emoji_code'], data['emoji_image'])
        return 'OK'
    except Exception as e:
        return str(e)

@app.route('/get_send_messages', methods=['GET'])
def get_send_messages():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getSendMessages(data['device_id'])
    except Exception as e:
        return str(e)

@app.route('/get_prank_messages', methods=['GET'])
def get_prank_messages():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getPrankMessages(data['device_id'])
    except Exception as e:
        return str(e)

@app.route('/get_messages_out', methods=['GET'])
def get_messages_out():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getMessagesOut(data['device_id'], data['device'])
    except Exception as e:
        return str(e)

@app.route('/get_return_messages_id', methods=['GET'])
def get_return_messages_id():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getReturnMessagesID(data['device_id'], data['contact_phone_number'])
    except Exception as e:
        return str(e)

@app.route('/get_last_id', methods=['GET'])
def get_last_id():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return str(APIdb().getLastMessageID(data['device_id'], data['contact_phone_number'], data['order']))
    except Exception as e:
        return str(e)

@app.route('/get_last_message_order', methods=['GET'])
def get_last_message_order():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return str(APIdb().getLastMessageOrder(data['device_id'], data['contact_phone_number']))
    except Exception as e:
        return str(e)

@app.route('/get_last_job', methods=['GET'])
def get_last_job():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getLastJob(data['device_id'])
    except Exception as e:
        return str(e)

@app.route('/get_phone_number', methods=['GET'])
def get_phone_number():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getPhoneNumber(data['device_id'])
    except Exception as e:
        return str(e)

@app.route('/update_job', methods=['GET'])
def update_job():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().updateJob(data['device_id'], data['last_job'])
        return "OK"
    except Exception as e:
        return str(e)

@app.route('/update_send_message', methods=['GET'])
def update_send_message():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().updateSendMessage(data['id'], data['sended_at'])
        return "OK"
    except Exception as e:
        return str(e)

def create_app():
    return app

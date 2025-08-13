# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, request
from flask_cors import CORS
from configparser import ConfigParser
from api_db import APIdb

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["MAX_CONTENT_LENGTH"] = 16777216


### -------------------------- APP COMMUNICATIONS ------------------------- ###
@app.route("/check_if_device_is_capable", methods=["GET"])
def check_if_device_is_capable():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().checkIfDeviceIsCapable(data["device_id"])
    except Exception as e:
        return str(e)


@app.route("/get_chrome_devices_active", methods=["GET"])
def get_chrome_devices_active():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getChromeDevicesActive(
            data["server"], data["slots"], data["not_in_str"]
        )
    except Exception as e:
        return str(e)


@app.route("/open_inactive_devices", methods=["GET"])
def open_inactive_devices():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().openInactiveDevices()
    except Exception as e:
        return str(e)


@app.route("/get_server_active", methods=["GET"])
def get_server_active():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getServerActiveByServer(data["server_nick"])
    except Exception as e:
        return str(e)


@app.route("/get_devices_by_vmname", methods=["GET"])
def get_devices_by_vmname():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getDevicesByVMName(data["nick"])
    except Exception as e:
        return str(e)


@app.route("/get_device_server", methods=["GET"])
def get_device_server():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        server = APIdb().getDeviceServer(data["device_id"])
        if server:
            return server
        else:
            return ""
    except Exception as e:
        return str(e)


@app.route("/set_device_ip", methods=["POST"])
def set_device_ip():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().setDeviceIP(data["device_id"], data["device_ip"])
        return "OK"
    except Exception as e:
        return str(e)


@app.route("/get_device_ip", methods=["GET"])
def get_device_ip():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        device_ip = APIdb().getDeviceIP(data["device_id"])
        if device_ip:
            return device_ip
        else:
            return ""
    except Exception as e:
        return str(e)


@app.route("/release_v8", methods=["GET"])
def release_v8():
    try:
        cp = ConfigParser()
        cp.read(r"/usr/api_v8/release.ini")
        return f"Release version V8: {cp['release']['version_v8']}"
    except Exception as e:
        return f"Erro: {str(e)}"


@app.route("/update_app_v8", methods=["GET"])
def update_app_v8():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        cp = ConfigParser()
        cp.read(r"/usr/api_v8/release.ini")
        if data["client_version"] != cp["release"]["version_v8"]:
            return cp["release"]["url_files_v8"] + cp["release"]["version_v8"] + ".zip"
        else:
            return ""
    except Exception as e:
        return str(e)


@app.route("/set_version_v8", methods=["GET"])
def set_version_v8():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        cp = ConfigParser()
        cp.read(r"/usr/api_v8/release.ini")
        cp["release"]["version_v8"] = data["version"]
        with open(r"/usr/api_v8/release.ini", "w") as configfile:
            cp.write(configfile)
        return f"Versão atualizada para: {data['version']}<br>Necessário garantir o arquivo /var/www/api_store/cob_update_v8/{data['version']}.zip"
    except Exception as e:
        return f"Erro: {str(e)}"


@app.route("/release", methods=["GET"])
def release():
    try:
        cp = ConfigParser()
        cp.read(r"/usr/api_v8/release.ini")
        return f"Release version: {cp['release']['version']}"
    except Exception as e:
        return f"Erro: {str(e)}"


@app.route("/update_app", methods=["GET"])
def update_app():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        cp = ConfigParser()
        cp.read(r"/usr/api_v8/release.ini")
        if data["client_version"] != cp["release"]["version"]:
            return cp["release"]["url_files"] + cp["release"]["version"] + ".zip"
        else:
            return ""
    except Exception as e:
        return str(e)


@app.route("/set_version", methods=["GET"])
def set_version():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        cp = ConfigParser()
        cp.read(r"/usr/api_v8/release.ini")
        cp["release"]["version"] = data["version"]
        with open(r"/usr/api_v8/release.ini", "w") as configfile:
            cp.write(configfile)
        return f"Versão atualizada para: {data['version']}<br>Necessário garantir o arquivo /var/www/api_store/cob_update_v8/{data['version']}.zip"
    except Exception as e:
        return f"Erro: {str(e)}"


@app.route("/get_devices_to_clean", methods=["GET"])
def get_devices_to_clean():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getDevicesToClean(data["server"])
    except Exception as e:
        return str(e)


@app.route("/get_chrome_devices", methods=["GET"])
def get_chrome_devices():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getChromeDevices(
            data["server"], data["slots"], data["not_in_str"]
        )
    except Exception as e:
        return str(e)


@app.route("/get_bot_devices", methods=["GET"])
def get_bot_devices():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getBotDevices(data["server"])
    except Exception as e:
        return str(e)


@app.route("/unregister_server", methods=["POST"])
def unregister_server():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().unregisterServer(data["nick"], datetime.now())
        return "OK"
    except Exception as e:
        return str(e)


@app.route("/deactive_server", methods=["POST"])
def deactive_server():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().changeStatusServer(data["nick"], datetime.now(), False)
        return "OK"
    except Exception as e:
        return str(e)


@app.route("/active_server", methods=["POST"])
def active_server():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().changeStatusServer(data["nick"], datetime.now(), True)
        return "OK"
    except Exception as e:
        return str(e)


@app.route("/post_new_server", methods=["POST"])
def post_new_server():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        APIdb().postNewServer(data["ip"], data["nick"], datetime.now())
        return "OK"
    except Exception as e:
        return str(e)


@app.route("/get_devices_ngroups", methods=["GET"])
def get_devices_ngroups():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getDevicesNGroups(data["nick"])
    except Exception as e:
        return str(e)


@app.route("/get_devices", methods=["GET"])
def get_devices():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getDevices(data["nick"])
    except Exception as e:
        return str(e)


@app.route("/get_server", methods=["GET"])
def get_server():
    try:
        req = request.args
        data = {}
        for i in req:
            data[i] = req.get(i)
        return APIdb().getServer(data["nick"])
    except Exception as e:
        return str(e)


@app.route("/get_servers", methods=["GET"])
def get_servers():
    try:
        return APIdb().getServers()
    except Exception as e:
        return str(e)


def create_app():
    return app

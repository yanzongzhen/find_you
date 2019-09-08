# -*- coding: utf-8 -*-
# @Time    : 2019/8/30 20:18
# @Author  : Yanzongzhen
# @Email   : yanzongzhen127@outlook.com
# @File    : server.py
# @Software: PyCharm
from flask import Flask, request
import configparser
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from gevent import monkey
import json
import os
import datetime
monkey.patch_all()
from spider.main import Location
from werkzeug.utils import secure_filename


conf = configparser.ConfigParser()
conf.read('config.ini')
host = conf['server']['host']
port = int(conf['server']['port'])
debug = conf['system']['debug']
server = conf['system']['host']

app = Flask(__name__)
CORS(app, supports_credentials=True)
if debug == 'True' or debug == 'true':
    app.debug = True


@app.route('/api')
def index():
    res = {
        "status": 0,
        "msg": "获取正常"
    }
    return json.dumps(res)


@app.route('/api/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(
            basepath, 'static/images', secure_filename(f.filename))
        if os.path.isfile(upload_path):
            os.remove(upload_path)
            f.save(upload_path)
        else:
            f.save(upload_path)
        res = {
            "code": 0,
            "msg": "上传成功",
            "name": f.filename,
            "url": f"http://{server}/static/images/{f.filename}"
        }
        return json.dumps(res)


@app.route('/api/finder', methods=['POST'])
def finder():
    if request.method == 'POST':
        f = request.form.get('filename')
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'static/images', secure_filename(f))
        if os.path.isfile(file_path):
            location = Location(file_path)
            address, take_time = location.run()
            if take_time:
                ok = True
                shut_time = str(take_time).split(" ")[0].replace(":", "-")
                toady = location.judge_time_met(take_time)
            else:
                ok = False
                shut_time = str(datetime.date.today())
                toady = False
            res = {
                "code": 0,
                "data": {
                    "ok": ok,
                    "address": address,
                    "shut_time": shut_time,
                    "is_today": toady,
                    "picture": f"http://{server}/static/images/{f}"
                }
            }
        else:
            res = {
                "code": 1,
                "msg": "请先上传高清大图"
            }
        return json.dumps(res)


@app.route('/api/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        f = request.form.get('filename')
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'static/images', secure_filename(f))
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                res = {
                    "code": 0,
                    "msg": '删除成功'
                }
            except Exception as e:
                res = {
                    "code": 1,
                    "msg": e
                }
        else:
            res = {
                "code": 1,
                "msg": "未找到相关图片"
            }
        return json.dumps(res)


if __name__ == '__main__':
    print(f'start server at http://{host}:{port}')
    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()

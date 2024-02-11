# Router & Template_Render
from flask import Blueprint, render_template, jsonify
# 「.env」で設定した環境変数を使用する
import settings
# ログ出力のために、loggerをimportする
from logoutput import logger
import traceback
# Post受信をするためにFlask_requestをimportする
from flask import request, jsonify

# import requests
import pprint

import pandas as pd

import modules

# PythonからPythonScriptを呼び出すためのモジュール！ => プログラム内でコマンド実行！
# import subprocess

# Generate Router Instance => Base_URLの設定はここ！
router = Blueprint('router', __name__)


# ルート, Method: GET
@router.route('/', methods=['GET'])
def index():
    try:
        logger.debug('Flask-API-ルート起動！')
        return render_template('index.html')
    except Exception as error:
        error_msg: str = traceback.format_exc()
        logger.error(f"APIルート: Error:  {error_msg}")

# Robotama_エンドポイント, Method: GET


@router.route('/robotama', methods=['GET'])
def robotama():
    return 'Robotamaなのだ！！'

# FrontAppの情報を確認するためのエンドポイント, Method: GET


@router.route('/front-info', methods=['GET'])
def front_info():
    logger.debug('FrontApp-Info-アクセス！')
    front_end_url = settings.FRONT_APP_URL
    msg = f"FrontAppのURLは: {front_end_url}"
    return msg

# Userの現在の位置情報 & お気に入りの場所の Type List から 近場のおすすめ Spot を提案する処理のエンドポイント, Method: POST


@router.route('/recommend-spots', methods=['POST'])
def create_recommend_spots():
    logger.debug('create_recommend_spots Start')
    print('create_recommend_spots Start')

    # JSONデータを受け取る
    data = request.json
    logger.debug(data)
    # Sample: {'favoriteList': ['遊園地・テーマパーク', '動物園', '水族館'], 'userCurrentPosition': {'address': '日本、〒136-0072 東京都江東区大島７丁目３６−８', 'latitude': 0, 'longitude': 0}}
    print(data)

    # おすすめのスポットを提案する処理を実行する
    results = modules.recommendedSpots.recommendedSpots(data)
    return jsonify(results)


# @router.before_request
# def before_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response


# Requestの後処理
@router.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

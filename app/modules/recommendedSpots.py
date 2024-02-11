### 指定した住所から、近い遊び場・観光スポットの提案リストを作成する Python Module 処理フロー Summary ###

# 1. FrontEnd から JSONデータ を受け取る

# - JSONデータの形式

# 2. ChatGPT に渡すための Messageを作成する

# 3. ChatGPT に Messageを渡して、返答を受け取る

# 4. ChatGPTの返答を、JSONデータに変換する

# 5. JSONデータを、FrontEnd に返す

################################################################################################

## Import Block ##
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,  # システムメッセージ
    HumanMessage,  # 人間の質問
    AIMessage,  # ChatGPTの返答
)

import openai
import json
import pprint
import dotenv
import os
import traceback
import pandas as pd
import base64


## 環境変数 ##
dotenv.load_dotenv('.env')

print('お気に入り Module Call')
print('Debug ロボたま')
print('Debug ロボたま 2')

# 1. Project・Root Path
project_root = os.path.abspath("../")
print('project_root', project_root)

# 2. OPENAI_KEY を取得する
OPENAI_KEY = dotenv.get_key('.env', 'OPENAI_KEY')
print('OPENAI_KEY: ', OPENAI_KEY)
print('------------------------------------------------------------')


#
def recommendedSpots(json_params):

    print('------------------------------------------------------------')
    print('おすすめ・スポットを提案する Python Script Start！')

    # 1. User の現在の位置情報
    user_address = json_params['userCurrentPosition']['address']
    print('user_address: ', user_address)

    # 2. User の好きな場所 カテゴリー・リスト
    favorite_list = json_params['favoriteList']
    print('favorite_list: ', favorite_list)

    # リストをカンマ区切りの文字列に変換
    favorite_list_str = ', '.join(favorite_list)
    print('favorite_list_str: ', favorite_list_str)

    # 3. ChatGPTの設定(人格・Persona)プロンプト
    persona_prompt = f'''
    あなたは、地理情報や、観光スポット、遊ぶ場所などに詳しいプロのChatbotです。
    あなたは、地理情報や、観光スポット、遊ぶ場所などに詳しいプロのChatbotとして、質問に対して、必ず回答フォーマット(Sample)と同じ構造のJSONで回答をします。
    また、あなたは、以下の制約条件と回答条件を厳密に守る必要があります。

    制約条件:
    * あなたは、お客さんのために、{user_address}に近い、おすすめの観光スポット・遊ぶ場所を5つ提案する必要があります。
    * 地理情報や、観光スポット、遊ぶ場所などに詳しいプロのChatbotとして、質問に対して、必ず回答フォーマット(Sample)のようなJSONで回答をします。
    * お客さんのデータを参考に、おすすめの観光スポット・遊ぶ場所を、回答フォーマット(Sample)のようなJSONで、5つ提案してください。
    * 必ず5つの回答・JSONデータは、リスト(配列)に入れて回答してください。

    お客さんのデータ:
    * 住所のデータ: {user_address}
    * 好きな観光スポット・遊ぶ場所の傾向のリスト・データ: {favorite_list_str}
    '''

    # 4. 回答フォーマット: JSONフォーマット
    answer_format = '''
    回答フォーマット(Sample):
    [
        {
        "name": "東京スカイツリー",
        "description": "東京スカイツリーは、東京都墨田区押上にある電波塔です。",
        "address": "東京都墨田区押上1-1-2",
        "recommended_points": "展望台からの眺めが最高で、東京の景色を一望できます。あなたは、その景色を見たら、感動すること間違いなしです。",
        "latitude": 35.710063,
        "longitude": 139.8107
        }
    ]
    '''

    # 5. 回答フォーマットをプロンプトに追加: JSON文字列の {} を f文字列に含めないために 後から追加する
    persona_prompt = f'{persona_prompt}\n{answer_format}'
    print('GPTの人格(Persona)プロンプト: ', persona_prompt)

    # 6. 質問文
    question = f'''
    質問：
    * お客さんのために、{user_address}に近い、おすすめの観光スポット・遊ぶ場所を、回答フォーマット(Sample)のようなJSONで、5つ回答してください。
    * 必ず5つの回答・JSONデータは、リスト(配列)に入れて回答してください。

    お客さんのデータ:
    * 住所のデータ: {user_address}
    * 好きな観光スポット・遊ぶ場所の傾向のリスト・データ: {favorite_list_str}
    '''

    # 7. 質問文に対する回答事例のフォーマット
    question_support_format = '''
    回答フォーマット(Sample):
    [
        {
        "name": "東京スカイツリー",
        "description": "東京スカイツリーは、東京都墨田区押上にある電波塔です。",
        "address": "東京都墨田区押上1-1-2",
        "recommended_points": "展望台からの眺めが最高で、東京の景色を一望できます。あなたは、その景色を見たら、感動すること間違いなしです。",
        "latitude": 35.710063,
        "longitude": 139.8107
        }
    ]
    '''
    # 8. 回答フォーマットをプロンプトに追加: JSON文字列の {} を f文字列に含めないために 後から追加する
    question = f'{question}\n{question_support_format}'
    print('質問文 プロンプト: ', question)

    json_data = []

    try:

        # 5. ChatGPT・Instance
        llm = ChatOpenAI(
            openai_api_key=OPENAI_KEY,
            # model="gpt-3.5-turbo",
            model="gpt-4",
            temperature=0,  # 精度をできるだけ高くする
        )

        # 6. LLM に渡すための Messageを作成する
        messages = [
            SystemMessage(content=persona_prompt),  # System Message = AIの「キャラ設定」のようなもの
            HumanMessage(content=question)  # 提案する内容
        ]
        response = llm(messages)
        print('ChatGPTの返答: ', response)
        json_string = response.content
        print('ChatGPTの返答(JSON): ', json_string)

        print('Debug ぴゅぴゅ丸')

        print('Debug ぴゅぴゅ丸 Ver.2')

        print('Debug ぴゅぴゅ丸 Ver.3')

        # Pythonで、文字列として、渡された JSONデータの形をJSONデータにする
        json_data = json.loads(json_string)
        print('文字列 JSON を JSONに変換: ', json_data)

    except Exception as error:
        # traceback.format_exc() で例外の詳細情報を取得する
        error_msg: str = traceback.format_exc()
        print(error_msg)
        return {
            "status": 500,
            "error_msg": error_msg
        }
        # 例外を無視したい場合は、pass を使用する
        pass

    # finally-ブロック => 必ず最後に実行される処理
    finally:
        # json_encode = json.dumps(target_row, ensure_ascii=False, indent=2)
        print('json_encode')
        # print(json_encode)

        response = {
            "status": 200,
            "data": json_data
        }
        print('response', response)
        print('必ず最後に実行したり処理を実行するブロック')
        print('----------------------------------------------------')
        return response

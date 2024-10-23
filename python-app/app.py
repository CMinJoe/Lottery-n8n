from flask import Flask, jsonify,request
from TaiwanLottery import TaiwanLotteryCrawler
# 載入 json 標準函式庫，處理回傳的資料格式
import json
import logging
import os


# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)  # 設定日誌級別為 INFO
logger = logging.getLogger(__name__)

@app.route('/lottery', methods=['GET'])
def get_data_lottery():
    lottery = TaiwanLotteryCrawler()
    lotteryResult = lottery.lotto649()[0]
    print(lotteryResult)
    return lotteryResult

@app.route('/lottery539', methods=['GET'])
def get_data_lottery539():
    lottery = TaiwanLotteryCrawler()
    result539 = lottery.daily_cash()[0]
    print(result539)
    return result539

@app.route("/linebot", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)   
        logging.info("linebot text = %s",json.dumps(json_data))                      # json 格式化訊息內容
        access_token = os.getenv('LINE_ACCESS_TOKEN')
        secret = os.getenv('LINE_SECRET')
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            print(msg)                                       # 印出內容
            reply = msg
        else:
            reply = '你傳的不是文字呦～'
        print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'           

@app.route("/sendMsg", methods=['POST'])
def linebotSendMsg():
    body = request.get_data(as_text=True) 
    print("Request = %s",json.dumps(body));
    req = json.loads(body);
    logging.info("Request Json = %s",json.dumps(req))                      # json 格式化訊息內容
    access_token = os.getenv('LINE_ACCESS_TOKEN');
    secret = os.getenv('LINE_SECRET');
    line_bot_api = LineBotApi(access_token)
    try:
        # 網址被執行時，等同使用 GET 方法發送 request，觸發 LINE Message API 的 push_message 方法
        line_bot_api.push_message(secret, TextSendMessage(text=req['sendMsg']))
        return 'OK'
    except:
        print('error')

@app.route('/health')
def health_check():
    return jsonify(status="healthy"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

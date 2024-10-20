from flask import Flask, jsonify
from TaiwanLottery import TaiwanLotteryCrawler

app = Flask(__name__)

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

@app.route('/health')
def health_check():
    return jsonify(status="healthy"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

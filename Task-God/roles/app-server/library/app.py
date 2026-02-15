from  flask import Flask

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return {'status': 'ok', 'message': 'pong'}, 200

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(debug=True)

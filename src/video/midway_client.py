from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def midway():
    request = requests.get('')
    return request.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
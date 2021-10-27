from google.cloud import datastore
from flask import Flask, request
import json
import constants
import loads
import boats

app = Flask(__name__)
app.register_blueprint(loads.bp)
app.register_blueprint(boats.bp)

@app.route('/')
def index():
    return "Please navigate to /boats to use this API"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

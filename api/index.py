# api/index.py
# Flask API

from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/api/hello')
def hello():
  return 'Hello from Python!' 

if __name__ == '__main__':
  app.run(port=5328)
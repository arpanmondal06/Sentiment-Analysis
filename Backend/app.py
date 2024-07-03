from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from routes import init_routes

init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)

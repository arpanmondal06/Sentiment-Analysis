from flask import request, jsonify
from controller import analyze_comments

def init_routes(app):
    @app.route('/analyze', methods=['POST'])
    def analyze():
        return analyze_comments(request.json)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_file(f'static/{path}')

from flask import jsonify
from utils import fetch_comments, analyze_text, sentiment_analysis, create_emotion_graph

def analyze_comments(data):
    video_id = data['videoId']
    comments = fetch_comments(video_id)
    full_text = " ".join(comments)
    emotions = analyze_text(full_text)
    sentiment = sentiment_analysis(full_text)
    graph_path = create_emotion_graph(emotions)

    return jsonify({
        'emotions': dict(emotions),
        'sentiment': sentiment,
        'graph_path': graph_path
    })

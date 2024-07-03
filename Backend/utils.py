import string
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import googleapiclient.discovery
import os
from dotenv import load_dotenv, dotenv_values
import matplotlib.pyplot as plt
import matplotlib

# Load environment variables from the .env file
load_dotenv()

# Use a non-interactive backend for matplotlib
matplotlib.use('Agg')

def fetch_comments(video_id):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv('KEY')

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        maxResults=500,
        videoId=video_id
    )
    response = request.execute()

    comments = []
    for item in response['items']:
        comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])

    return comments

def analyze_text(text):
    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    tokenized_words = word_tokenize(cleaned_text, "english")
    final_words = [word for word in tokenized_words if word not in stopwords.words('english')]

    emotion_list = []
    with open('emotion.txt', 'r') as file:
        for line in file:
            clear_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
            word, emotion = clear_line.split(':')
            if word in final_words:
                emotion_list.append(emotion)

    return Counter(emotion_list)

def sentiment_analysis(text):
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    if score['neg'] > score['pos']:
        return 'Negative'
    elif score['pos'] > score['neg']:
        return 'Positive'
    else:
        return 'Neutral'

def create_emotion_graph(emotions):
    plt.figure(figsize=(10, 5))
    plt.bar(emotions.keys(), emotions.values())
    plt.xlabel('Emotions')
    plt.ylabel('Counts')
    plt.title('Emotion Analysis of YouTube Comments')
    plt.xticks(rotation=45)
    plt.tight_layout()
    graph_path = 'static/emotions.png'
    plt.savefig(graph_path)
    plt.close()
    return graph_path

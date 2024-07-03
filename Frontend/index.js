async function analyzeComments() {
    const videoId = document.getElementById('videoId').value;
    const response = await fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ videoId: videoId })
    });
    const data = await response.json();

    document.getElementById('sentiment').innerText = 'Sentiment: ' + data.sentiment;

    const emotionsDiv = document.getElementById('emotions');
    emotionsDiv.innerHTML = '';
    for (const [emotion, count] of Object.entries(data.emotions)) {
        const emotionElement = document.createElement('p');
        emotionElement.innerText = `${emotion}: ${count}`;
        emotionsDiv.appendChild(emotionElement);
    }

    const graphImage = document.getElementById('graph');
    graphImage.src = 'http://127.0.0.1:5000/' + data.graph_path + '?t=' + new Date().getTime();
}

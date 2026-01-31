import requests

API_KEY = 'AIzaSyBGejD52umVgnTYhtadb72LSgUdwZxYqFM'
VIDEO_ID = 'dQw4w9WgXcQ'   # ganti sesuai video kamu

def get_comments(limit=200):
    comments = []
    next_page_token = None

    while True:
        url = 'https://www.googleapis.com/youtube/v3/commentThreads'
        params = {
            'part': 'snippet',
            'videoId': VIDEO_ID,
            'key': API_KEY,
            'textFormat': 'plainText',
            'maxResults': 100,
            'pageToken': next_page_token
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            break

        data = response.json()

        for item in data.get('items', []):
            comments.append(
                item['snippet']['topLevelComment']['snippet']['textDisplay']
            )
            if len(comments) >= limit:
                return comments

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return comments

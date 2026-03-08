import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyC05pt4JqXZg11dA9TmswMGrepGdVTYmz4"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

request = youtube.commentThreads().list(
    part="snippet",
    videoId="G6FuWd4wNd8",
    maxResults=100
)
response = request.execute()
comments = []

for item in response['items']:
    comment = item['snippet']['topLevelComment']['snippet']
    comments.append([
        comment['authorDisplayName'].replace("&#39;", "'").replace("</b>", " ").replace("<b>", " ").replace("<br>", " "),
        comment['publishedAt'].replace("&#39;", "'").replace("</b>", " ").replace("<b>", " ").replace("<br>", " "),
        comment['updatedAt'].replace("&#39;", "'").replace("</b>", " ").replace("<b>", " ").replace("<br>", " "),
        comment['likeCount'],
        comment['textDisplay'].replace("&#39;", "").replace("</b>", "").replace("<b>", " ").replace("<br>", " ")
    ])

df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])
df.head(100).to_csv('youtube_comments.txt', index=False, sep='\t', quoting=1, escapechar="'")  # Using tab as the separator

print("Output written to youtube_comments.txt")
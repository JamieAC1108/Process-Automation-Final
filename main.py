import googleapiclient.discovery
import string
import re
from dotenv import load_dotenv
import os
import json
import requests
import syllables
import random

load_dotenv()
DEVELOPER_KEY = os.getenv("devkey")
VIDEO_ID = "zdo-QYvR8Uk"
WEBHOOK_URL = os.getenv("webhook")

##### GET COMMENTS #####

def get_comments(video_id):
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=DEVELOPER_KEY
    )

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=1000
    )

    response = request.execute()
    comments = []

    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        cleaned = (
            comment.replace("&#39;", "'")
            .replace("</b>", "")
            .replace("<b>", "")
            .replace("<br>", " ")
        )
        comments.append(cleaned)

    return comments

##### COUNT SYLLABLES #####

def count_syllables(comment):
    words = comment.split()
    word_counts = []

    for word in words:
        cleaned = word.translate(str.maketrans("", "", string.punctuation)).lower()
        count = syllables.estimate(cleaned)
        word_counts.append((word, count))

    return word_counts

##### BUILD HAIKU #####

def build_haiku(word_counts):
    first, second, third = [], [], []
    s1 = s2 = s3 = 0
    stage = 1

    for word, syllables in word_counts:
        if stage == 1:
            if s1 + syllables > 5:
                return None
            first.append(word)
            s1 += syllables
            if s1 == 5:
                stage = 2
        elif stage == 2:
            if s2 + syllables > 7:
                return None
            second.append(word)
            s2 += syllables
            if s2 == 7:
                stage = 3
        elif stage == 3:
            if s3 + syllables > 5:
                return None
            third.append(word)
            s3 += syllables

    if s1 == 5 and s2 == 7 and s3 == 5:
        return "\n".join([
            " ".join(first),
            " ".join(second),
            " ".join(third)
        ])
    return None

##### MAIN #####

def main():

    comments = get_comments(VIDEO_ID)

    haikus = []

    
    for comment in comments:
        word_counts = count_syllables(comment)
        haiku = build_haiku(word_counts)
        if haiku:
            haikus.append(haiku)
    
    random_haiku = random.choice(haikus)

    payload = {"content": random_haiku}

    requests.post(WEBHOOK_URL, json=payload)


if __name__ == "__main__":
    main()
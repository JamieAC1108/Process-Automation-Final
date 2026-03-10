import googleapiclient.discovery
import string
import re

DEVELOPER_KEY = "AIzaSyC05pt4JqXZg11dA9TmswMGrepGdVTYmz4"
VIDEO_ID = "zdo-QYvR8Uk"

##### LOADING THE SYLLABLE DICTIONARY #####

def load_syllables(file_path):
    syllables = {}
    digits = tuple(string.digits)
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line and line[0] != ";"]

    for line in lines:
        tokens = line.split()
        count = len([token for token in tokens[1:] if token.endswith(digits)])
        syllables[tokens[0].lower()] = count

    return syllables

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

def estimate_syllables(word):
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for c in word:
        if c in vowels:
            if not prev_vowel:
                count += 1
            prev_vowel = True
        else:
            prev_vowel = False
    return max(1, count)

def count_syllables(comment, syllable_data):
    words = comment.split()
    word_counts = []

    for word in words:
        cleaned = word.translate(str.maketrans("", "", string.punctuation)).lower()
        count = syllable_data.get(cleaned, estimate_syllables(cleaned))
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
    syllable_data = load_syllables("Words.txt")
    comments = get_comments(VIDEO_ID)

    print("\n-- Generated Haikus --\n")
    for i, comment in enumerate(comments):
        word_counts = count_syllables(comment, syllable_data)
        haiku = build_haiku(word_counts)
        if haiku:
            print(f"Haiku from comment {i + 1}:")
            print(haiku)
            print()

if __name__ == "__main__":
    main()
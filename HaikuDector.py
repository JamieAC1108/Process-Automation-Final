
# this is the actual bot
import string
import re

syllable_data = {}

# Load syllable data from the file
with open('syllables.txt', 'r', encoding='utf-8') as syllable_file:
    for line in syllable_file:
        line = line.strip().lower().replace(',', '').replace('"', '').replace('\n', ' ')
        if line:  
            parts = re.split(r'\s*:\s*', line)
            if len(parts) == 2:  
                word = parts[0].strip().lower()
                syllable_count = int(parts[1].replace(',', '').replace('"', '').strip())
                syllable_data[word] = syllable_count

comment_syllable_counts = {}

# Process YouTube comments
with open('youtube_comments.txt', 'r', encoding='utf-8') as comment_file:
    youtube_comments = comment_file.readlines()

# Check each comment for syllable count
for idx, line in enumerate(youtube_comments):
    columns = line.strip().split('\t')  
    if len(columns) >= 5:  
        comment = columns[4]  
        words = comment.strip().split()  
        total_syllables = 0
        syllable_breakdown = []

        for word in words:
            word_cleaned = word.translate(str.maketrans('', '', string.punctuation)).lower()
            syllable_count = syllable_data.get(word_cleaned, 0)
            total_syllables += syllable_count
            syllable_breakdown.append(syllable_count)

        # Check if the comment has exactly 17 syllables
        if total_syllables == 17:
            # Split words into 5-7-5 structure
            first_line, second_line, third_line = [], [], []
            syllable_count_first = 0
            syllable_count_second = 0
            
            for word in words:
                word_cleaned = word.translate(str.maketrans('', '', string.punctuation)).lower()
                syllable_count = syllable_data.get(word_cleaned, 0)

                # Fill the first line
                if syllable_count_first < 5:
                    first_line.append(word)
                    syllable_count_first += syllable_count
                # Fill the second line
                elif syllable_count_second < 7:
                    second_line.append(word)
                    syllable_count_second += syllable_count
                # Fill the third line
                else:
                    third_line.append(word)

            # Write the haiku to haiku.txt
            with open('haiku.txt', 'a', encoding='utf-8') as haiku_file:
                haiku_file.write(' '.join(first_line) + '\n')
                haiku_file.write(' '.join(second_line) + '\n')
                haiku_file.write(' '.join(third_line) + '\n\n')  # Add a newline between haikus

                print(f'Haiku from comment {idx + 1} written to haiku.txt!')

        # Store the syllable count for this comment
        comment_syllable_counts[idx + 1] = total_syllables


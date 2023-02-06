from youtube_transcript_api import YouTubeTranscriptApi as yt
import re

# Insert YouTube URL video ID
url = input("Enter YouTube Video URL: ")  # https://www.youtube.com/watch?v=7g1pmHSWHe0
vid_id = url.split("=")[-1]
data = yt.get_transcript(vid_id, languages=['en'])  # If en didn't work, try "en-US"

transcript = ""
transcript_list = []
for dct in data:
    seconds = dct["start"] % (24 * 3600)
    minutes = seconds // 60
    seconds %= 60
    transcript = transcript + "%02d:%02d" % (minutes, seconds) + "\n" + str(dct["text"]) + "\n"

    timestamp = "%02d:%02d - " % (minutes, seconds) + str(dct["text"])
    transcript_list.append(timestamp)

# print(transcript)
# print(*transcript_list, sep='\n')

timestamps = r'\d{2}:\d{2}'
operation = False

prompt1 = input("Would you like to extract custom or whole script?\n"
                "Type 'w' for whole script.\n"
                "Type 'c' for custom script.\n"
                "Type 'f' to find word.\n")

if prompt1.lower() == "w" or prompt1.lower() == "whole":
    transcript = re.sub(timestamps, '', transcript).replace('\n', ' ').replace('  ', ' ')
    operation = True

elif prompt1.lower() == 'c' or prompt1.lower() == "custom":

    prompt2 = input('Choose start time in the following format "XX:XX":\n'
                    'Or type "0" to start from beginning.\n')

    prompt3 = input('Choose end time in the following format "XX:XX":\n'
                    'Or type "1" to finish at end.\n')

    if prompt2 in transcript or prompt2 == "0" and prompt3 in transcript or prompt3 == "1":
        if prompt2 != "0":
            transcript = transcript.split(prompt2)[1]
        if prompt3 != "1":
            transcript = transcript.split(prompt3)[0]

        transcript = re.sub(timestamps, '', transcript).replace('\n', ' ').replace('  ', ' ')
        operation = True

    else:
        print("Time frame was not found in the given transcript file.")

elif prompt1.lower() == 'f' or prompt1.lower() == "find":
    occurrences = []
    find = input("What word are you looking for: ")
    for line in transcript_list:
        if find.lower() in line.lower():
            # "\033[4m" = Underline  # "\033[1m" = Bold  # '\33[32m' = Green (More operations below)
            # '\33[32m' + '\33[3m' + find + '\033[0m'    # For Multiple Operations
            occurrences.append(line.replace(find.lower(), '\33[32m' + find.lower() + '\033[0m')
                               .replace(find.title(), '\33[32m' + find.title() + '\033[0m'))
    print(*occurrences, sep='\n')

if operation:
    file_name = input("What would you like to name your txt file? ")
    if file_name == "":
        file_name = "untitled"
    with open(fr"C:\Users\ahmad\Desktop\{file_name}.txt", "w", encoding="utf8") as file:
        file.write(transcript)



"""Helper Functions for song parser script
"""
import re
import os
import noiseWords

#use regex to add/match all song titles to one of 2 lists
#ready_to_parse -> in the correct format <artist> - <song title>
#not_ready_to_parse -> all others
def filter_song_titles(directory: str) -> tuple[list,list]:
    song_files = os.listdir(directory)
    ready_to_parse, not_ready_to_parse = [],[]
    
    for song in song_files:
        # print(f"testing song: {song}")
        if re.match(r".+[-_].+",song):
            # print("Correct format!")
            ready_to_parse.append(song)
        else:
            not_ready_to_parse.append(song)
    return (ready_to_parse,not_ready_to_parse)

#clean video titles in order to have cleaner data to be added to mp3 metadata
def clean_title(initial_title: str, remove_brackets_flag: bool) -> tuple[str | None, str]:
    cleaned_title = initial_title
    
    # remove bracketed content
    if remove_brackets_flag:
        cleaned_title = re.sub(r"[\(\[\{].*?[\)\]\{]", "", cleaned_title)
    
    # remove noise words
    for word in noiseWords.NOISE_WORDS:
        cleaned_title = cleaned_title.replace(word, "")

    #remove leading, trailing, and extra whitespace
    cleaned_title = cleaned_title.strip()
    re.sub(r"\s+"," ",cleaned_title) # \s+ -> "match 1 or more whitespace characters"
    
    try:
        artist, song_title = cleaned_title.split("-")
        return artist.strip(), song_title.strip()
    except ValueError:
        print(f"Something went wrong with song title: {initial_title}")
        return None, cleaned_title


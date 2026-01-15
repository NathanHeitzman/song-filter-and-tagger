import os
import filterTitleFormats
from mutagen.mp3 import MP3
from mutagen.easyid3 import ID3, EasyID3

# audio_metadata = MP3("./songs/Zyzz - You Are My Angel (HD) [Mm24HMrK6Js].mp3", ID3=EasyID3)
ready_to_parse_songs, not_ready_to_parse_songs = filterTitleFormats.filter_song_titles("./songs")

for song_title in ready_to_parse_songs:
    audio_metadata = MP3(f"./songs/{song_title}", ID3=EasyID3)
    artist, title = filterTitleFormats.clean_title(song_title,True)
    
    #Update the songs metadata
    if artist:
        audio_metadata["title"] = title
        audio_metadata["artist"] = artist
        audio_metadata.save()

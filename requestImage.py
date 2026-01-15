import requests
import json
import os
from dotenv import load_dotenv

#load personal email address to be sent to musicbrainz for communication
load_dotenv()
email_address = os.getenv("EMAIL_ADDRESS")
HEADERS = {
    "User-Agent": f"Tagger/1.0 ({email_address})",
    "From": email_address
}

def request_image(artist: str, song_title: str, write_to_file: bool) -> str | bool:
    url = f"https://musicbrainz.org/ws/2/recording/"
    query = f'recording:"{song_title}" AND artist:"{artist}"'
    response = requests.get(url,headers=HEADERS, params={"query":query, "fmt":"json"})

    if response.status_code != 200:
        print(f"Failed to find song: {song_title} by {artist}")
        return False
    
    data = response.json()
    recording = data["recordings"][0]
    
    if write_to_file:
        json_string = json.dumps(recording,indent=4)
        with open("jsonResponse.json", "w") as json_file:
            json_file.write(json_string)
    return recording

#request_image("Radiohead","Creep", True)
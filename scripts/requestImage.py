"""
MusicBrainz API Connector

This module handles communication with the MusicBrainz Web Service (XML/JSON). 
It uses a Lucene-based search query to locate recordings and retrieve 
metadata, which can then be used to fetch album art or update ID3 tags.

Note:
    MusicBrainz requires a descriptive 'User-Agent' header, including a 
    contact email, to identify your application. This script expects a .env 
    file containing an EMAIL_ADDRESS variable, though it can be hardcoded 
    directly into the script if preferred.
"""

import requests
import json
import os
import re
from dotenv import load_dotenv
from datetime import datetime

#load personal email address to be sent to musicbrainz for communication
load_dotenv()
email_address = os.getenv("EMAIL_ADDRESS")
HEADERS = {
    "User-Agent": f"Tagger/1.0 ({email_address})",
    "From": email_address
}

#request an album cover from the MusicBrainz API
def request_image(artist: str, song_title: str, write_to_file: bool) -> str | bool:
    url = f"https://musicbrainz.org/ws/2/recording/"
    query = f'recording:"{song_title}" AND artist:"{artist}"'
    response = requests.get(url,headers=HEADERS, params={"query":query, "fmt":"json"})

    if response.status_code != 200:
        print(f"Failed to find song: {song_title} by {artist}")
        return False
    
    data = response.json()
    recording = data["recordings"]
    
    if write_to_file:
        json_string = json.dumps(data,indent=4)
        with open("jsonResponse.json", "w") as json_file:
            json_file.write(json_string)
    
    return recording
#request_image("Radiohead","Creep", True)

#Look through every recording in JSON and return all releases with
#a primary type of album 
def filter_recordings(json: dict) -> list[dict]:
    valid_releases = []
    for recording in json.get("recordings", []):
        for release in recording.get("releases", []):
            release_group = release.get("release-group", {}) 
            if release_group.get("primary-type", "") == "Album":
                valid_releases.append(release)
    
    #Throw out releases that do not have a status of official
    official_releases = [release for release in valid_releases if release.get("status") == "Official"]
    
    #Sort the datetime objects
    dates = []
    for release in official_releases:
        current_date = (release.get("date", "9999-99-99"))
        dates.append(parse_date(current_date))
    sorted_dates = dates.sort(reverse=True) 
    
    return sorted_dates

#takes a filepath and filters out garbadge releases for a selected song
def filter_file_recordings(filePath: str) -> list[dict] | bool:
    try:
        with open(filePath, "r") as json_file, open("filtered.json", "w") as filtered_json:
            json_data = json.load(json_file)
            valid_releases = filter_recordings(json_data)
            json_string = json.dumps(valid_releases, indent=4)
            filtered_json.write(json_string)
        return valid_releases
    
    except FileNotFoundError:
        print("One or more files not found")
        return False

# parse a given date string to a datetime object
# example date: "2009-03-24"
def parse_date(date: str) -> datetime:
    print(f"parsing: {date}")
    if re.match(r"\d{4}-\d{2}-\d{2}", date):
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
        return datetime(year,month,day)
    else:
        return datetime(9999,12,30)
    
filter_file_recordings("./jsonResponse.json")

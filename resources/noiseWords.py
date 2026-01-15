"""
Noise Word Configuration

This module defines a list of 'noise' strings commonly found in media 
filenames, particularly those sourced from video platforms or web streams. 
These strings are targeted for removal to ensure that MusicBrainz API 
queries and ID3 tags remain clean and professional.

Maintenance:
    Add new common suffixes or quality descriptors here to improve 
    the parsing accuracy of the 'clean_title' function.
"""

NOISE_WORDS = [
    "official video",
    "official audio",
    "lyrics",
    "hd",
    "hq",
    "4k",
    "8k",
    "1080p",
    "720p",
    "60fps",
    ".mp3",
    ".mp4"
]
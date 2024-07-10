import re

def extract_timestamps(transcription: str) -> list:
    words = re.findall(r'\b\w+\b', transcription)

    timestamps = []
    start_time = 0
    for word in words:
        end_time = start_time + len(word)
        timestamps.append({
            "word": word,
            "start_time": start_time,
            "end_time": end_time
        })
        start_time = end_time + 1

    return timestamps

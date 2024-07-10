import os
import json

def save_files(transcription, summary, timestamps, transcription_filename, summary_filename, timestamps_filename):
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    # Save transcription
    transcription_path = os.path.join(results_dir, transcription_filename)
    with open(transcription_path, "w") as f:
        f.write(transcription)

    # Save summary
    summary_path = os.path.join(results_dir, summary_filename)
    with open(summary_path, "w") as f:
        f.write(summary)

    # Save timestamps
    timestamps_path = os.path.join(results_dir, timestamps_filename)
    with open(timestamps_path, "w") as f:
        json.dump(timestamps, f, indent=4)

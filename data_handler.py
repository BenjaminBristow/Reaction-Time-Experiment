import csv
import os

class DataHandler:
    def __init__(self, filename="experiment_results.csv"):
        self.filename = filename
        self.fieldnames = [
            "participant_id",
            "block_name",
            "is_practice",
            "trial_number",
            "target_color",
            "pressed_key",
            "is_correct",
            "reaction_time_ms"
        ]

    def append_trial(self, trial_data):
        """Appends a single trial dictionary row into the CSV file."""
        file_exists = os.path.exists(self.filename)
        with open(self.filename, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(trial_data)
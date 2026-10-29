import csv
import os

class DataHandler:
    def __init__(self, participant_id, folder_name="csv_data"):
        self.folder_name = folder_name
        self.participant_id = participant_id
        
        # Automatically create csv_data folder if it doesn't exist
        os.makedirs(self.folder_name, exist_ok=True)
        
        self.filename = os.path.join(self.folder_name, f"RT_Experiment_{self.participant_id}.csv")
        self.fieldnames = [
            "participant_id",
            "condition",
            "is_practice",
            "trial_number",
            "target_color",
            "pressed_key",
            "is_correct",
            "reaction_time_ms"
        ]

    def append_trial(self, trial_data):
        """Appends a single trial row into the participant's CSV file inside csv_data/."""
        file_exists = os.path.exists(self.filename)
        with open(self.filename, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(trial_data)
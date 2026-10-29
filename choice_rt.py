import random

class ChoiceRTBlock:
    def __init__(self, trial_count=20, is_practice=False):
        self.trial_count = trial_count
        self.is_practice = is_practice
        self.name = "Choice Practice" if is_practice else "Choice Main"
        self.title = f"Choice Reaction Time ({'Practice' if is_practice else 'Main Test'})"
        self.guide_text = "RED = Press 'F'  |  BLUE = Press 'J'"
        self.instruction_text = (
            "Two different colors will appear:\n\n"
            "• Press 'F' for RED circle (Left Hand)\n"
            "• Press 'J' for BLUE circle (Right Hand)\n\n"
            "Press SPACEBAR when ready to begin."
        )

    def generate_trials(self):
        """Returns randomized 50/50 mix of red and blue stimulus trials."""
        trials = ["red" if i % 2 == 0 else "blue" for i in range(self.trial_count)]
        random.shuffle(trials)
        return trials

    def check_response(self, target_color, key_pressed):
        """Validates keypress against target stimulus color."""
        if target_color == "red" and key_pressed == "f":
            return True
        if target_color == "blue" and key_pressed == "j":
            return True
        return False
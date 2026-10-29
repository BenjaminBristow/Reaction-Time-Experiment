class SimpleRTBlock:
    def __init__(self, trial_count=20, is_practice=False):
        self.trial_count = trial_count
        self.is_practice = is_practice
        self.name = "Simple Practice" if is_practice else "Simple Main"
        self.title = f"Simple Reaction Time ({'Practice' if is_practice else 'Main Test'})"
        self.guide_text = "Press SPACEBAR when RED circle appears"
        self.instruction_text = (
            "Focus on the center cross.\n\n"
            "Whenever a RED circle appears, press SPACEBAR as fast as you can.\n\n"
            "Press SPACEBAR when ready to begin."
        )

    def generate_trials(self):
        """Returns list of stimulus colors for simple RT."""
        return ["red"] * self.trial_count

    def check_response(self, target_color, key_pressed):
        """Validates if keypress is correct for simple RT."""
        return key_pressed == "space"
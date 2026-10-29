import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

from simple_rt import SimpleRTBlock
from choice_rt import ChoiceRTBlock
from data_handler import DataHandler

class ReactionTimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reaction Time Experiment")
        self.root.geometry("700x550")
        self.root.configure(bg="#121212")

        self.participant_id = ""
        self.experiment_data = []
        self.current_block_index = 0
        self.current_trial_index = 0
        self.trial_list = []
        self.accepting_input = False
        self.stimulus_start_time = 0.0
        self.current_state = "WELCOME"

        # Instantiate block pipeline
        self.blocks = [
            SimpleRTBlock(trial_count=6, is_practice=True),
            SimpleRTBlock(trial_count=20, is_practice=False),
            ChoiceRTBlock(trial_count=6, is_practice=True),
            ChoiceRTBlock(trial_count=20, is_practice=False)
        ]

        self.main_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=620, height=480)

        self.root.bind("<Key>", self.handle_keypress)
        self.show_welcome_screen()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.current_state = "WELCOME"
        self.clear_frame()

        tk.Label(self.main_frame, text="Reaction Time Study", font=("Segoe UI", 20, "bold"), fg="#ffffff", bg="#1e1e1e").pack(pady=(40, 10))
        tk.Label(self.main_frame, text="Please enter Participant ID to start:", font=("Segoe UI", 11), fg="#b0b0b0", bg="#1e1e1e").pack(pady=10)

        self.entry_id = tk.Entry(self.main_frame, font=("Segoe UI", 12), justify="center", bg="#2a2a2a", fg="#ffffff", insertbackground="white")
        self.entry_id.pack(pady=15, ipady=5, ipadx=10)
        self.entry_id.focus()

        ttk.Button(self.main_frame, text="Start Experiment", command=self.validate_and_start).pack(pady=20)

    def validate_and_start(self):
        val = self.entry_id.get().strip()
        if not val:
            messagebox.showwarning("Input Required", "Please enter a Participant ID.")
            return
        self.participant_id = val
        self.csv_handler = DataHandler(f"RT_Experiment_{self.participant_id}.csv")
        self.show_instructions_screen()

    def show_instructions_screen(self):
        self.current_state = "INSTRUCTIONS"
        self.clear_frame()
        block = self.blocks[self.current_block_index]

        tk.Label(self.main_frame, text=block.title, font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#1e1e1e").pack(pady=(40, 20))
        tk.Label(self.main_frame, text=block.instruction_text, font=("Segoe UI", 11), fg="#b0b0b0", bg="#1e1e1e", justify="center").pack(pady=20)

    def show_task_screen(self):
        self.current_state = "TASK"
        self.clear_frame()
        block = self.blocks[self.current_block_index]

        self.lbl_guide = tk.Label(self.main_frame, text=block.guide_text, font=("Segoe UI", 12, "bold"), fg="#4da6ff", bg="#1e1e1e")
        self.lbl_guide.pack(pady=(15, 5))

        self.canvas = tk.Canvas(self.main_frame, width=540, height=260, bg="#0d0d0d", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.lbl_feedback = tk.Label(self.main_frame, text="", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#1e1e1e")
        self.lbl_feedback.pack(pady=5)

        self.current_trial_index = 0
        self.trial_list = block.generate_trials()
        self.run_trial()

    def run_trial(self):
        self.accepting_input = False
        self.canvas.delete("all")
        self.lbl_feedback.config(text="")
        self.canvas.create_text(270, 130, text="+", fill="#666666", font=("Segoe UI", 36, "bold"))

        iti = random.randint(1000, 2000)
        self.root.after(iti, self.present_stimulus)

    def present_stimulus(self):
        self.canvas.delete("all")
        target_color = self.trial_list[self.current_trial_index]
        fill_color = "#ff4d4d" if target_color == "red" else "#3385ff"

        self.canvas.create_oval(220, 80, 320, 180, fill=fill_color, outline="")
        self.stimulus_start_time = time.perf_counter()
        self.accepting_input = True

    def handle_keypress(self, event):
        key = event.keysym.lower()

        if self.current_state == "INSTRUCTIONS" and key == "space":
            self.show_task_screen()
            return

        if self.current_state == "TASK" and self.accepting_input:
            response_time = time.perf_counter()
            self.accepting_input = False

            rt_ms = int(round((response_time - self.stimulus_start_time) * 1000))
            current_block = self.blocks[self.current_block_index]
            target_color = self.trial_list[self.current_trial_index]

            is_correct = current_block.check_response(target_color, key)

            trial_record = {
                "participant_id": self.participant_id,
                "block_name": current_block.name,
                "is_practice": 1 if current_block.is_practice else 0,
                "trial_number": self.current_trial_index + 1,
                "target_color": target_color,
                "pressed_key": "space" if key == "space" else key,
                "is_correct": 1 if is_correct else 0,
                "reaction_time_ms": rt_ms
            }

            self.experiment_data.append(trial_record)
            self.csv_handler.append_trial(trial_record)

            if current_block.is_practice:
                if is_correct:
                    self.lbl_feedback.config(text=f"Correct! ({rt_ms} ms)", fg="#4caf50")
                else:
                    self.lbl_feedback.config(text="Incorrect key!", fg="#f44336")

            self.current_trial_index += 1
            delay = 1000 if current_block.is_practice else 600

            if self.current_trial_index < len(self.trial_list):
                self.root.after(delay, self.run_trial)
            else:
                self.current_block_index += 1
                if self.current_block_index < len(self.blocks):
                    self.root.after(800, self.show_instructions_screen)
                else:
                    self.root.after(800, self.show_finish_screen)

    def show_finish_screen(self):
        self.current_state = "FINISH"
        self.clear_frame()

        tk.Label(self.main_frame, text="Experiment Complete!", font=("Segoe UI", 18, "bold"), fg="#ffffff", bg="#1e1e1e").pack(pady=(30, 10))
        tk.Label(self.main_frame, text=f"Data recorded live to:\nRT_Experiment_{self.participant_id}.csv", font=("Segoe UI", 11), fg="#4caf50", bg="#1e1e1e").pack(pady=20)
        ttk.Button(self.main_frame, text="Exit", command=self.root.quit).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReactionTimeApp(root)
    root.mainloop()
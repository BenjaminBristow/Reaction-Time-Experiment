# Reaction Time Experiment: Simple vs. Choice RT

A modular, Python-based psychology lab experiment built with `tkinter` to compare human response speeds across two cognitive conditions: **Simple Reaction Time (Simple RT)** and **Choice Reaction Time (Choice RT)**.

All participant data files are automatically organized into a `csv_data/` subfolder, and an included standard-library script merges them into a single `master_experiment_data.csv` file in the root directory for statistical analysis in **Jamovi**, **R**, **SPSS**, or **Excel**.

---

## 📁 Repository Structure

```text
rt_experiment/
├── csv_data/                  # Subfolder storing individual participant CSV outputs
│   └── RT_Experiment_P01.csv  # Example participant output
├── main.py                    # Main GUI application & experiment manager
├── simple_rt.py               # Logic & trial generator for Simple RT blocks
├── choice_rt.py               # Logic & trial generator for Choice RT blocks
├── data_handler.py            # Automatically saves participant data to csv_data/
├── merge_data.py              # Merges all CSVs in csv_data/ into master_experiment_data.csv
├── .gitignore                 # Excludes cache files
└── README.md                  # Project documentation
```

---

## ⚙️ Experimental Design

| Feature | Simple RT Condition | Choice RT Condition |
| :--- | :--- | :--- |
| **Independent Variable** | Single Target $\rightarrow$ Single Key | Dual Target Colors $\rightarrow$ Distinct Keys |
| **Stimulus** | Red Circle | Red Circle or Blue Circle (50/50 randomized) |
| **Response Key** | `SPACEBAR` | `F` (for Red) or `J` (for Blue) |
| **Target Cognitive Factor** | Baseline sensory-motor latency | Visual discrimination + choice selection overhead |
| **Delay Interval** | Randomized 1,000 ms – 2,000 ms Inter-Trial Interval (ITI) | Randomized 1,000 ms – 2,000 ms Inter-Trial Interval (ITI) |

---

## 🚀 Quick Start

### Prerequisites
* **Python 3.8+** (Uses standard libraries `tkinter`, `time`, `random`, `csv`, `os`, and `glob`—no `pip install` required).

### Running the Experiment

1. Launch the application:
   ```bash
   python3 main.py
   ```
2. Enter a unique **Participant ID** (e.g., `P01`, `P02`) when prompted.
3. Complete the 4 experiment blocks (Simple Practice, Simple Main, Choice Practice, Choice Main).
4. Results automatically save to:
   ```text
   csv_data/RT_Experiment_<Participant_ID>.csv
   ```

---

## 📊 Merging Data & Analyzing in Jamovi

When multiple participants have completed the test across different sessions or computers:

1. Ensure all individual participant `.csv` files are saved inside the `csv_data/` folder.
2. Run the merge script from your terminal:
   ```bash
   python3 merge_data.py
   ```
3. A combined dataset named `master_experiment_data.csv` will be created in your root project directory.

### Jamovi Analysis Steps

1. Open **Jamovi** and import `master_experiment_data.csv`.
2. Apply a filter (**Data** $\rightarrow$ **Filters**) to exclude practice runs and wrong keypresses:
   ```text
   is_practice == 0  and  is_correct == 1
   ```
3. Perform analysis:
   * **Descriptive Statistics:** Calculate mean `reaction_time_ms` split by `condition` (`simple` vs. `choice`).
   * **Paired Samples t-test:** Compare participant mean reaction times between `simple` and `choice` conditions.

---

## 📝 Data Dictionary

| Column Header | Type | Description |
| :--- | :--- | :--- |
| `participant_id` | Nominal | Unique participant identifier |
| `condition` | Nominal | Task condition (`simple` or `choice`) |
| `is_practice` | Nominal (0/1) | `1` = Practice trial, `0` = Main test block |
| `trial_number` | Integer | Trial sequence number within block |
| `target_color` | Nominal | Visual stimulus color (`red` or `blue`) |
| `pressed_key` | Nominal | Key pressed by participant (`space`, `f`, or `j`) |
| `is_correct` | Nominal (0/1) | `1` = Correct response, `0` = Incorrect keypress |
| `reaction_time_ms` | Continuous | Measured response time in milliseconds |

import glob
import csv

# Find all participant CSV files in the current directory
csv_files = glob.glob("RT_Experiment_*.csv")

if not csv_files:
    print("No participant CSV files found matching 'RT_Experiment_*.csv'")
else:
    master_rows = []
    header = None

    for file_path in csv_files:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            if not reader:
                continue
            
            # Save the header row from the first valid file
            if header is None:
                header = reader[0]
            
            # Append all data rows (excluding the header)
            master_rows.extend(reader[1:])

    if header:
        with open("master_experiment_data.csv", mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(master_rows)
        
        print(f"Successfully merged {len(csv_files)} files into 'master_experiment_data.csv'!")
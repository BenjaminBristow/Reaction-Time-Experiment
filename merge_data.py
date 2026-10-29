import glob
import csv
import os

def merge_all_csvs():
    search_path = os.path.join("csv_data", "*.csv")
    csv_files = glob.glob(search_path)

    if not csv_files:
        print("No participant CSV files found inside 'csv_data/' folder!")
        return

    master_rows = []
    header = None

    for file_path in csv_files:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            if not reader:
                continue
            
            # Use header from first file
            if header is None:
                header = reader[0]
            
            # Append rows excluding header
            master_rows.extend(reader[1:])

    if header:
        output_path = "master_experiment_data.csv"
        with open(output_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(master_rows)
        
        print(f"Successfully merged {len(csv_files)} files into '{output_path}' in the main directory!")

if __name__ == "__main__":
    merge_all_csvs()
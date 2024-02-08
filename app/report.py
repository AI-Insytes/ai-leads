import json
import csv
import os
from app.file_utils import save_to_file, create_directory
from pathlib import Path

def main_report(lead_category):

    base_dir = Path(__file__).resolve().parent.parent / "pseudobase" / "leads_data"
    json_file_name = f"{lead_category}_leads.json"
    json_file_path = base_dir / json_file_name

    csv_file_path = Path(__file__).resolve().parent.parent / "leads_and_messages" / "leads_report.csv"

    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Ensure the leads_and_messages directory exists
        csv_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            # No predefined headers; keys are written dynamically
            for item in data:
                # Write each key-value pair on separate rows
                for key, value in item.items():
                    writer.writerow([key, value])
                
                # Optionally, add a blank row after each item for readability
                writer.writerow([])

    except Exception as e:
        print(f"Failed to write to the report. Error: {e}")

if __name__ == "__main__":
    base_directory = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    main_report()
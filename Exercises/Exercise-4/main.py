import os
import json
import csv
import glob
from typing import Dict, Any

def flatten_json(data: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
    """
    Flatten a nested dictionary structure.
    Handles nested dictionaries by concatenating keys with underscores.
    """
    flattened = {}
    for key, value in data.items():
        new_key = f"{prefix}{key}"
        if isinstance(value, dict):
            flattened.update(flatten_json(value, f"{new_key}_"))
        else:
            flattened[new_key] = value
    return flattened

def convert_json_to_csv(json_path: str, output_dir: str = "output") -> None:
    """
    Convert a single JSON file to CSV with flattened structure.
    Creates output directory if it doesn't exist.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read JSON file
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    
    # Flatten the JSON structure
    flattened_data = flatten_json(data)
    
    # Determine output CSV path
    base_name = os.path.basename(json_path)
    csv_name = os.path.splitext(base_name)[0] + '.csv'
    csv_path = os.path.join(output_dir, csv_name)
    
    # Write to CSV
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=flattened_data.keys())
        writer.writeheader()
        writer.writerow(flattened_data)
    
    print(f"Converted {json_path} to {csv_path}")

def find_and_convert_json_files(root_dir: str = "data") -> None:
    """
    Recursively find all JSON files in directory and convert them to CSV.
    """
    # Search for all JSON files recursively
    json_files = glob.glob(os.path.join(root_dir, '**/*.json'), recursive=True)
    
    if not json_files:
        print(f"No JSON files found in {root_dir}")
        return
    
    print(f"Found {len(json_files)} JSON files to convert")
    
    for json_file in json_files:
        try:
            convert_json_to_csv(json_file)
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")

def main():
    print("Starting JSON to CSV conversion...")
    find_and_convert_json_files()
    print("Conversion complete!")

if __name__ == "__main__":
    main()

import json
import csv
from pathlib import Path

def find_json_files(base_dir):
    return list(base_dir.rglob("*.json"))

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], f'{name}{a}_')
        elif isinstance(x, list):
            out[name[:-1]] = ','.join(map(str, x))
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def convert_json_to_csv(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]  # chuyển thành list nếu là 1 dict

    flat_data = [flatten_json(item) for item in data]

    csv_file = json_file.with_suffix('.csv')
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=flat_data[0].keys())
        writer.writeheader()
        writer.writerows(flat_data)
def main_1():
    base_dir = Path("/app/data")  # Thư mục dữ liệu nằm trong container tại /app/data
    json_files = find_json_files(base_dir)
    for file in json_files:
        convert_json_to_csv(file)
        print(f"✅ Đã chuyển {file.name} → {file.with_suffix('.csv').name}")

if __name__ == "__main__":
    main_1()

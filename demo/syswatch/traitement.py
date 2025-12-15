import csv
import json

def export_csv(data, filePath):
    with open(filePath, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(data)
    return

def export_json(data, filePath):
    with open(filePath, 'a') as file:
        for entry in data:
            json.dump(entry, file, indent=2)
    return
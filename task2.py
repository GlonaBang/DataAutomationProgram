import os
import re
import random
from datetime import datetime

def create_dev_set(full_data_dir, dev_data_dir, ratio=10):
    os.makedirs(dev_data_dir, exist_ok=True)
    for file_name in sorted(os.listdir(full_data_dir)):
        with open(f'{full_data_dir}/{file_name}') as file_full,\
                open(f'{dev_data_dir}/{file_name}', 'w') as file_dev:
            for line in file_full:
                rand_num = random.randint(0, 100)
                if rand_num < ratio:
                    file_dev.write(line)

def load_phone_calls_dict(data_dir):
    phone_calls_dict = {}
    for file in os.listdir(data_dir):
        if re.match(".*([2][0-9]{3})", file) is None:
            continue
        with open(f"{data_dir}/{file}", mode="r") as f:
            for line in f:
                timestamp, phone_number = line.split(": ")
                phone_number = phone_number.strip()
                date_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                area_code = phone_number[3:6]
                if 0 <= date_time.hour < 6:
                    if area_code in phone_calls_dict:
                        if phone_number in phone_calls_dict[area_code]:
                            phone_calls_dict[area_code][phone_number].append(date_time)
                        else:
                            phone_calls_dict[area_code][phone_number] = [date_time]
                    else:
                        phone_calls_dict[area_code] = {
                            phone_number: [date_time]}
    return phone_calls_dict

def generate_phone_call_counts(phone_calls_dict):
    num_dict = {}
    for d in phone_calls_dict.values():
        for num, timestamps in d.items():
            num_dict[num] = len(timestamps)
    return num_dict

def most_frequently_called(phone_call_counts, top_n):
    n = 0
    most = []
    for k, v in phone_call_counts.items():
        if n < top_n:
            most.append((k, v))
        n += 1
    most = sorted(most, key=lambda x: x[1], reverse=True)
    return most

def export_phone_call_counts(most_frequent_list, out_file_path):
    with open(out_file_path, mode = "w") as f:
        for t in most_frequent_list:
            f.write(f"{t[0]}: {t[1]}\n")

def export_redials_report(phone_calls_dict, report_dir):
    for area_code, ac_data in phone_calls_dict.items():
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        with open(f"{report_dir}/{area_code}.txt", mode = "w") as f:
            for phone_number, call_data in ac_data.items():
                call_data = sorted(call_data)
                prev = None
                delta = None
                for call in call_data:
                    if not prev:
                        prev = call
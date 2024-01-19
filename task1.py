from datetime import datetime

def filter_phone_calls(area_code, start_hour, end_hour, input_path, output_path):
    area_code = str(area_code)
    with open(input_path, mode = "r") as f, open(output_path, mode = "w") as f2:
        for line in f:
            timestamp, phone_number = line.split(": ")
            date_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            if phone_number[3:6] == area_code and (start_hour <= date_time.hour < end_hour):
                f2.write(f"{timestamp} {phone_number}")

if __name__ == "__main__":
    filter_phone_calls(
        area_code=412,
        start_hour=0,
        end_hour=6,
        input_path='data/phone_calls.txt',
        output_path='data/phone_calls_filtered.txt'
)
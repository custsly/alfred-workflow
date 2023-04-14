import argparse
import csv
import json

parser = argparse.ArgumentParser(description='Convert JSON to CSV')

parser.add_argument('-i', '--input', help='Input JSON file', type=str, required=True)
parser.add_argument('-o', '--output', help='Output CSV file', type=str, required=True)

def get_json_arr(json_data):
    """
    从 json 中取 json 数组
    """
    if isinstance(json_data, list):
        return json_data

    for key in json_data:
        val = json_data[key]
        if isinstance(val, list):
            return val

    return None

def convert_json_to_csv(input_json_path, output_csv_path):
    with open(input_json_path) as json_file:
        json_data = json.load(json_file)

    json_arr = get_json_arr(json_data)
    if not json_arr:
        raise Exception("Not JsonArr And Not Contains JsonArr")

    with open(output_csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        for index, data in enumerate(json_arr):
            # 写入标题
            if index == 0:
                header = data.keys()
                csv_writer.writerow(header)

            csv_writer.writerow(data.values())


if __name__ == '__main__':
    try:
        args = parser.parse_args()
        convert_json_to_csv(args.input, args.output)
    except Exception as e:
        print(str(e), end='')

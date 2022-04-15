import argparse
import csv
import json

parser = argparse.ArgumentParser(description='Convert JSON to CSV')

parser.add_argument('-i', '--input', help='Input JSON file', type=str, required=True)
parser.add_argument('-o', '--output', help='Output CSV file', type=str, required=True)


def convert_json_to_csv(input_json_path, output_csv_path):
    with open(input_json_path) as json_file:
        json_data = json.load(json_file)

    with open(output_csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        for index, data in enumerate(json_data):
            # 写入标题
            if index == 0:
                header = data.keys()
                csv_writer.writerow(header)
            
            csv_writer.writerow(data.values())


if __name__ == '__main__':
    args = parser.parse_args()
    convert_json_to_csv(args.input, args.output)

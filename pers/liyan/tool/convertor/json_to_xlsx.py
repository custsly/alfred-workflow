import argparse
import json

import pandas as pd

parser = argparse.ArgumentParser(description='Convert JSON to XLSX')

parser.add_argument('-i', '--input', help='Input JSON file', type=str, required=True)
parser.add_argument('-o', '--output', help='Output XLSX file', type=str, required=True)


def convert_json_to_xlsx(input_json_path, output_xlsx_path):
    with open(input_json_path) as json_file:
        json_data = json.load(json_file)

    all_rows = []
    column_list = None

    for index, data in enumerate(json_data):
        if index == 0:
            column_list = data.keys()
        all_rows.append(data.values())

    df = pd.DataFrame(all_rows, columns=column_list)
    df.to_excel(output_xlsx_path, index=False, engine='xlsxwriter')


if __name__ == '__main__':
    args = parser.parse_args()
    convert_json_to_xlsx(args.input, args.output)

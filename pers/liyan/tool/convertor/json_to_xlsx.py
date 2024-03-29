import argparse
import json

import pandas as pd

parser = argparse.ArgumentParser(description='Convert JSON to XLSX')

parser.add_argument('-i', '--input', help='Input JSON file', type=str, required=True)
parser.add_argument('-o', '--output', help='Output XLSX file', type=str, required=True)


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


def convert_json_to_xlsx(input_json_path, output_xlsx_path):
    with open(input_json_path) as json_file:
        json_data = json.load(json_file)

    json_arr = get_json_arr(json_data)
    if not json_arr:
        raise Exception("Not JsonArr And Not Contains JsonArr")

    all_rows = []
    column_list = None

    for index, data in enumerate(json_arr):
        if index == 0:
            column_list = data.keys()
        all_rows.append(data.values())

    df = pd.DataFrame(all_rows, columns=column_list)
    df.to_excel(output_xlsx_path, index=False, engine='xlsxwriter')


if __name__ == '__main__':
    try:
        args = parser.parse_args()
        convert_json_to_xlsx(args.input, args.output)
        print('ok', end='')
    except Exception as e:
        print(str(e), end='')

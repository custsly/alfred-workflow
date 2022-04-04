import pandas as pd

import color.color_util as color_util

color_dict = {}
column_name = None


def coloring_cell_by_val(ser):
    color = color_dict.get(ser[column_name])
    return [f'background-color:{color}'] * ser.size


def generate_value_color_map(column_values):
    unique_vals = column_values.unique()
    color_generator = color_util.random_hex_color_generator(0.414, 0.818, unique_vals.size)

    return {val: next(color_generator) for val in unique_vals}


def coloring_by_unique_value(input_file_path, output_file_path, col_name):
    df = pd.read_excel(input_file_path)
    global color_dict, column_name
    color_dict = generate_value_color_map(df[col_name])
    column_name = col_name
    df = df.style.apply(coloring_cell_by_val, axis=1)
    df.to_excel(output_file_path, index=False, engine='openpyxl')


if __name__ == '__main__':
    coloring_by_unique_value('/Users/shiliyan/Desktop/工号用户名问题_20220310的副本.xlsx',
                             '/Users/shiliyan/Desktop/工号用户名问题_20220310的副本.xlsx', 'user_id')

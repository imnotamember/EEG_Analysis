import pandas as pd

from file_utilities import name


def empty_header_labeler(header):
    meta_mapper = {0: 'meta_label_{0}', 1: 'meta_data_{0}'}
    new_pair_index = 0
    for index, label in enumerate(header):
        if label is None:
            header[index] = meta_mapper[new_pair_index % 2].format(int(new_pair_index / 2))
            new_pair_index += 1
    return header


def egi_events_to_df(file_path):
    df = pd.read_csv(file_path, skiprows=2, header=None, sep='\n')
    df = df[0].str.split('\t', expand=True)
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)
    df.columns = empty_header_labeler(df.columns.tolist())
    return df


def update_egi_events_csv(file_path):
    df = egi_events_to_df(file_path)
    csv_file_path = name.update_filename(file_path, new_folder='csv', new_extension='csv')
    df.to_csv(csv_file_path, index=False)
    return csv_file_path

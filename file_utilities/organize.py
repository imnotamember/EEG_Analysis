import os
from os.path import join, splitext


def collect_files(folder_path, file_name_delimiter='_', file_extension='evt'):
    return_file_paths = []
    return_file_sub_names = []
    for file_name in os.listdir(folder_path):
        current_file_name, current_file_extension = splitext(file_name)
        if current_file_extension[1:] == file_extension:
            return_file_sub_names.append(current_file_name.split(file_name_delimiter))
            return_file_paths.append(join(folder_path, file_name))
    return return_file_paths, return_file_sub_names

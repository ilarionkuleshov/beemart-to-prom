import os
from datetime import datetime


def get_configured_paths(data_directory, products_file, logs_file):
    if not os.path.isdir(data_directory):
        os.mkdir(data_directory)

    date_dir = f"{data_directory}/{datetime.now().strftime('%d.%m.%Y')}"
    if not os.path.isdir(date_dir):
        os.mkdir(date_dir)

    files_counter = 0
    for file in os.listdir(date_dir):
        if file.startswith(logs_file.split(".")[0]):
            files_counter += 1

    if files_counter:
        products_file_path = f"{date_dir}/{products_file.split('.')[0]}_{files_counter}.{products_file.split('.')[1]}"
        logs_file_path = f"{date_dir}/{logs_file.split('.')[0]}_{files_counter}.{logs_file.split('.')[1]}"
    else:
        products_file_path = f"{date_dir}/{products_file}"
        logs_file_path = f"{date_dir}/{logs_file}"

    return products_file_path, logs_file_path

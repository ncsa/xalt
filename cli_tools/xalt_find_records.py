import os
import json
from datetime import datetime

# root_directory = '/sw/workload/delta/json'
root_directory = '/home/prakhar/code/work/ncsa'



# Function to process JSON files and collect data
def step1(username, root_dir=root_directory):
    file_list = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file.startswith('run.') and file.endswith('.json') and username in file and ".aaa." in file:
                with open(file_path, 'r') as f:
                        file_list.append(file)
                       
    return file_list

# Function to process JSON data and the file paths to incorprate datetime filters
def step2(start_record_paths, start_date, end_date):
    filtered_paths = []
    if start_date != '':
        start_date = datetime.strptime(start_date, "%m/%d/%Y")
    else:
        start_date = None

    if end_date !='':
        end_date= datetime.strptime(end_date, "%m/%d/%Y")
    else:
        end_date = None
    

    for rec_pth in start_record_paths:
        path_components = rec_pth.split('.')
        record_date = path_components[2][:10]
        record_date = (datetime.strptime(record_date, "%Y_%m_%d"))

        if start_date is None and end_date is None:
            filtered_paths.append(rec_pth)
        elif start_date is None:
            if record_date <= end_date:
                filtered_paths.append(rec_pth)
        elif end_date is None:
            if start_date <= record_date:
                filtered_paths.append(rec_pth)
        else:
            if start_date <= record_date <= end_date:
                filtered_paths.append(rec_pth)

    return filtered_paths

def process_files(root_dir):
    pkg_data_list = []
    run_start_data_list = []
    run_end_data_list = []

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file.startswith('pkg.') and file.endswith('.json'):
                with open(file_path, 'r') as f:
                    try:
                        data = json.load(f)
                        pkg_data_list.append(data)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON for file {file_path}: {e}")
            
            elif file.startswith('run.') and file.endswith('.json'):
                if '.aaa.' in file:
                    with open(file_path, 'r') as f:
                        try:
                            data = json.load(f)
                            run_start_data_list.append(data)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON for file {file_path}: {e}")
                elif '.zzz.' in file:
                    with open(file_path, 'r') as f:
                        try:
                            data = json.load(f)
                            run_end_data_list.append(data)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON for file {file_path}: {e}")
    
    return pkg_data_list, run_start_data_list, run_end_data_list


# Main function
if __name__ == '__main__':
    
    print("Enter your search parameters")

    username = None
    while username is None:
        username = input("Enter username: ")
        start_date = input("Start date (inclusive - MM/DD/YYYY format): ")
        end_date = input("End date (inclusive - MM/DD/YYYY format): ")
        slurm_jid = input("Enter slurm Job ID: ")
        xalt_run_uuid = input("Enter XALT RUN UUID: ")

    
    # Step 1, find matching xalt_run_uuids for username start_records
    start_record_paths = step1(username)
    
    # Step 2: Filter records between start and end date
    record_paths = step2(start_record_paths, start_date, end_date)
    print(record_paths)

    # pkg_data_list, run_start_data_list, run_end_data_list  = process_files(root_directory)



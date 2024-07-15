import os
import json
from datetime import datetime
from datetime import timedelta 
# root_directory = '/sw/workload/delta/json'
root_directory = '/home/prakhar/code/work/ncsa'



# Function to process JSON files and collect data
def step1(username, root_dir=root_directory):
    file_list = []
    file_paths = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file.startswith('run.') and file.endswith('.json') and username in file and ".aaa." in file:
                file_list.append(file_path)
    return file_list

# Function to process JSON data and the file paths to incorprate datetime filters
def step2(start_record_paths, start_date, end_date):
    filtered_paths = []
    if start_date != '':
        start_date = datetime.strptime(start_date, "%m/%d/%Y") - timedelta(days=1)
    else:
        start_date = None

    if end_date !='':
        end_date= datetime.strptime(end_date, "%m/%d/%Y") + timedelta(days=1)
    else:
        end_date = None
    

    for rec_pth in start_record_paths:
        rec_name = rec_pth.split('/')[-1]
        name_compnents= rec_name.split('.')
        record_date = name_compnents[2][:10]
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

def step3(record_paths, xalt_run_uuid):
    filtered_paths = []
    for rec_pth in record_paths:
        record_name = rec_pth.split('/')[-1]
        rec_run_uuid = record_name.split('.')[-2]
        if xalt_run_uuid in rec_run_uuid:
            filtered_paths.append(rec_pth)
    return filtered_paths

def step4(record_data, record_paths, slurm_jid):
    filtered_data = []
    filtered_paths  = []
    if slurm_jid !='' and slurm_jid is not None:
        include =  False
    else:
        include = True
    for i,record in enumerate(record_data):
        
        if record_data is None:
            continue

        if include is True:
            filtered_paths.append(record_paths[i])
            filtered_data.append(record_data[i])
            continue
        
        userT_jid =  record['userT']['job_id']
        envT_jid = record['envT']['SLURM_JOB_ID']
        
        if slurm_jid in userT_jid or slurm_jid in envT_jid:
            filtered_paths.append(record_paths[i])
            filtered_data.append(record_data[i])
            
    return filtered_data, filtered_paths

def process_files(record_paths):
    pkg_data_list = []
    
    for path in record_paths:
        with (open(path, 'r') as f):
            try:
                data = json.load(f)
                pkg_data_list.append(data)
            except json.JSONDecodeError as e:
                pkg_data_list.append(None)
                print(f"Failed to open {path}: {e}")
   
    return pkg_data_list 

def display_summary(filtered_data, filtered_paths):
    for path in filtered_paths:
        print(path)
        for datum in filtered_data:
            print(datum)

        break


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

    # Step 3: Filter with xalt_run_uuid
    if xalt_run_uuid !='' and xalt_run_uuid is not None:
        record_paths = step3(record_paths, xalt_run_uuid)
   
    print("Records filtered. Extracting JSON now...")
    record_data = process_files(record_paths)


    # Step 4: Filter with Slurm Job ID 
    filtered_data, filtered_paths = step4(record_data, record_paths, slurm_jid)

    user_conf = input(f"There are {len(filtered_data)} records matching your parameters. Do you want to proceed with displaying these records? (yes/no)")
    if user_conf != 'yes':
        exit()

    display_summary(filtered_data, filtered_paths)


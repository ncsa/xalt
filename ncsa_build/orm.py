import sys
import os
import re
from pathlib import Path
import mariadb
import json
from ClassHelper import PkgObj, LinkObj, RunObj

def connectDB(username, password, hostname, dbname):
    """
    Connect to the MariaDB database using provided credentials.
    """
    try:
        conn = mariadb.connect(
            user=username,
            password=password,
            host=hostname,
            port=3306,  # Use integer here
            database=dbname
        )
        print("MariaDB connection established.")
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)

def createLogList():
    """
    Create a list of log files based on the XALT_FILE_PREFIX environment variable.
    """
    xalt_log_dir = os.getenv("XALT_FILE_PREFIX")
    if xalt_log_dir is None:
        print("Error: XALT_FILE_PREFIX environment variable not set.")
        sys.exit(1)
    xalt_logs = list(Path(xalt_log_dir).rglob('*delta*.json'))
    return xalt_logs

def splitLogs(file_paths):
    run_files = []
    link_files = []
    pkg_files = []

    # Updated patterns
    run_pattern = re.compile(r"^run\.delta")
    link_pattern = re.compile(r"^link\.delta")
    pkg_pattern = re.compile(r"^pkg\.delta")

    for file_path in file_paths:
        file_name = Path(file_path).name

        if run_pattern.match(file_name):
            run_files.append(file_path)
        elif link_pattern.match(file_name):
            link_files.append(file_path)
        elif pkg_pattern.match(file_name):
            pkg_files.append(file_path)
        else:
            print(f"No match: {file_name}")

    return run_files, link_files, pkg_files



def ingestPkgRecords(pkg_paths):
    pkg_dict = {}

    for pkg in pkg_paths:
        with open(pkg, 'r') as file:
            data = json.load(file)
            obj = PkgObj(data)

            if obj.xalt_run_uuid in pkg_dict:
                pkg_dict[obj.xalt_run_uuid].append(obj)
            else:
                pkg_dict[obj.xalt_run_uuid] = [obj]  # Initialize as an array to bundle pkgs for the same run record

    return pkg_dict


def ingestLinkRecords(link_paths):
    link_dict = {}
    for link in link_paths:
        print(link)
        with open(link, 'r') as file:
            data = json.load(file)
            obj = LinkObj(data)

            if obj.xalt_run_uuid in link_dict:
                link_dict[obj.xalt_run_uuid].append(obj)
            else:
                link_dict[obj.xalt_run_uuid] = [obj]  # Initialize as an array to bundle links for the same run record

    return link_dict

def ingestRunRecords(run_paths):
    run_dict = {}

    for run in run_paths:
        with open(run, 'r') as file:
            data = json.load(file)
            obj = RunObj(data)

            if obj.xalt_run_uuid in run_dict:
                run_dict[obj.xalt_run_uuid].append(obj)
            else:
                run_dict[obj.xalt_run_uuid] = [obj]  # Initialize as an array to bundle runs for the same run record

    return run_dict


def main():
    # Validate command-line arguments
    if len(sys.argv) < 5:
        print("Usage: script.py <username> <password> <hostname> <dbname>")
        sys.exit(1)

    # Parse command-line arguments
    username, password, hostname, dbname = sys.argv[1:5]

    # Fetch log files
    logfiles = createLogList()
    print(f"Found {len(logfiles)} log files to process.")
    # Perform operations with `conn` and `logfiles` as needed.

    run, link, pkg = splitLogs(logfiles)
    # Establish database connection
    # conn = connectDB(username, password, hostname, dbname)

    link_dict = ingestLinkRecords(link)
    pkg_dict = ingestPkgRecords(pkg)
    run_dict = ingestRunRecords(run)


    
    """
    Now we can index into records using the RUN UUID. 
    The general ingestion workflow can go like this
    """

if __name__ == "__main__":
    main()

import sys
import os
import re
from pathlib import Path
try:
  import configparser
except:
  import ConfigParser as configparser
#import mariadb
import json
<<<<<<< Updated upstream:ncsa_build/orm.py
from ClassHelper import PkgObj, LinkObj, RunObj
=======
from DeltaUploadClasses import PkgObj, LinkObj, RunObj
import mysql.connector
from mysql.connector import Error
>>>>>>> Stashed changes:ncsa_build/delta_upload_xalt_records.py


def connectDB(my_config):
    """
    Connect to the MariaDB database using provided credentials.
    """
    try:
#        conn = mariadb.connect(
#            user=username,
#            password=password,
#            host=hostname,
#            port=3306,  # Use integer here
#            database=dbname
#        )
#      my_config.print()
      my_database=my_config.get("MYSQL","DB")
      my_host=my_config.get("MYSQL","HOST")
      my_user=my_config.get("MYSQL","USER")
      my_password=my_config.get("MYSQL","PASSWD")
      print(f'parsed config host=>>{my_host}<<')
      print(f'parsed config user=>>{my_user}<<')
      print(f'parsed config pwd=>>{my_password}<<')
      print(f'parsed config db=>>{my_database}<<')


      print('about to try DB connection.')
      
#      conn = mysql.connector.connect(
#        my_host=my_config.get("MYSQL","HOST"),
#        user=my_config.get("MYSQL","USER"),
#        password=my_config.get("MYSQL","PASSWD"),
#        database=my_config.get("MYSQL","DB")
#      )
      conn = mysql.connector.connect(
        host=my_host,
        user=my_user,
        password=my_password,
        database=my_database,
        use_pure=True
      )
      print('back from connect call.')
      print(conn)

      print("DB connection established.")
      return conn
    except mysql.Error as e:
#    finally:

      #print(f"Error connecting to database: {e}")
      print(f"Error connecting to database:")
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

#    log_root_directory = os.environ.get("XALT_LOG_FILE_DIR")
#    if not log_root_directory :
#        print()
#        print("WARNING: XALT_LOG_FILE_DIR unset!  Nowhere to read files from.")
#        print("aborting")
#        print()
#        exit()

    XALT_ETC_DIR = os.environ.get("XALT_ETC_DIR")
    if not XALT_ETC_DIR :
      print()
      print("WARNING: XALT_ETC_DIR unset!  Without that we have no configuration.")
      print("aborting")
      print()
      exit()

    Configfilename = os.path.join(XALT_ETC_DIR,"xalt_db.conf")
  
    print("config filename:")
    print(Configfilename)
    print("filename done")
  
    print("about to read config file")
    config = configparser.ConfigParser()     
    config.read(Configfilename)
    print("configuration read; printing sections: ")
    config_sections_list=config.sections()
    n_sections=len(config_sections_list)
    print(f"The config file contained {n_sections} non-default sections.")
    


        
#    # Validate command-line arguments
#    if len(sys.argv) < 5:
#        print("Usage: script.py <username> <password> <hostname> <dbname>")
#        sys.exit(1)

    # Parse command-line arguments
#    username, password, hostname, dbname = sys.argv[1:5]

#    # Fetch log files
    logfiles = createLogList()
    print(f"Found {len(logfiles)} log files to process.")
#    print("here is the log file list:")
#    print(logfiles)
#    print("finished log file list")

    #    # Perform operations with `conn` and `logfiles` as needed.

    run, link, pkg = splitLogs(logfiles)
    # Establish database connection
    conn = connectDB(config)

    if conn.is_connected():
      print("we're connected to database!")
    else:
      print("we are NOT connected.  :-(")
      
#    print("regardless, exit to test.")
#    sys.exit(1)

    
    link_dict = ingestLinkRecords(link)
    pkg_dict = ingestPkgRecords(pkg)
    run_dict = ingestRunRecords(run)


    
    """
    Now we can index into records using the RUN UUID. 
    The general ingestion workflow can go like this
    """

    
    
    print('about to run dictionary upload of Run objects')
    for run_key,run_obj in run_dict.items():
      print(f"******* RUN using key {run_key}")
      #print(run_obj)
      print('run object is of type')
      print(type(run_obj))
      print('finish type')
      for run_subobject in run_obj:
        print('run subobject is of type')
        print(type(run_subobject))
        print('finish subobject; now print')
        print(run_subobject)
        print('done printing subobject')

#      serialized_run_obj=json.loads(run_obj)
#      print(json.dumps(serialized_run_obj,indent=5))
      print("about to write to DB")
      run_obj[0].writeToDB(conn)
      
      

    print('done uploading RUN dictionary')

    print('finished test run on RUN dictionary')


    print('about to run dictionary upload of Pkg objects')
    for pkg_key,pkg_obj in pkg_dict.items():
      print(f"******* PKG using key {run_key}")
      #print(run_obj)
      print('pkg object is of type')
      print(type(pkg_obj))
      print('finish type')
      for pkg_subobject in pkg_obj:
        print('run subobject is of type')
        print(type(pkg_subobject))
        print('finish subobject; now print')
        print(pkg_subobject)
        print('done printing subobject')

#      serialized_run_obj=json.loads(run_obj)
#      print(json.dumps(serialized_run_obj,indent=5))
      print("about to write to DB")
      pkg_obj[0].writeToDB(conn)
      
      

    print('done uploading PKG dictionary')

    print('finished test run on PKG dictionary')


#    print('about to run dictionary upload of Package objects')
#    for pkg_key,pkg_obj in pkg_dict.items():
#      print(f"using key {pkg_key}")
#      print(pkg_obj)
#      print("about to write to DB")
#      pkg_obj[0].writeToDB(conn)
#    print('done uploading PKG dictionary')  
#    print('about to run dictionary upload of Link objects')
#    for link_key,link_obj in link_dict.items():
#      print(f"using key {link_key}")
#      print(link_obj)
#      print("about to write to DB")
#      link_obj[0].writeToDB(conn)
#    print ('done uploading LINK objects')
    
if __name__ == "__main__":
    main()
